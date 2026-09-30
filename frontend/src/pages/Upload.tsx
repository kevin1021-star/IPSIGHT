import { useState, useRef, useCallback, type DragEvent, type ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Upload as UploadIcon,
  FileCode2,
  Network,
  ChevronDown,
  X,
  Loader2,
  CheckCircle2,
  AlertCircle,
  FileText,
} from 'lucide-react';
import { clsx } from 'clsx';
import { assessmentsApi, type VendorType } from '../lib/api';

type TabType = 'pcap' | 'config';

const VENDORS: { value: VendorType; label: string }[] = [
  { value: 'strongswan',  label: 'strongSwan'       },
  { value: 'cisco_ios',   label: 'Cisco IOS'        },
  { value: 'cisco_asa',   label: 'Cisco ASA'        },
  { value: 'fortinet',    label: 'Fortinet FortiGate'},
  { value: 'juniper',     label: 'Juniper SRX'      },
  { value: 'palo_alto',   label: 'Palo Alto Networks'},
];

const ACCEPT: Record<TabType, string> = {
  pcap:   '.pcap,.pcapng',
  config: '.conf,.cfg,.txt',
};

export default function Upload() {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [tab, setTab] = useState<TabType>('pcap');
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [vendor, setVendor] = useState<VendorType>('strongswan');
  const [name, setName] = useState('');
  const [progress, setProgress] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const resetFile = () => {
    setFile(null);
    setError(null);
    setProgress(0);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleDrop = useCallback(
    (e: DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      setDragging(false);
      const dropped = e.dataTransfer.files[0];
      if (!dropped) return;
      setFile(dropped);
      if (!name) setName(dropped.name.replace(/\.[^.]+$/, ''));
    },
    [name],
  );

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const picked = e.target.files?.[0];
    if (!picked) return;
    setFile(picked);
    if (!name) setName(picked.name.replace(/\.[^.]+$/, ''));
  };

  const handleSubmit = async () => {
    if (!file) { setError('Please select a file to upload.'); return; }
    if (!name.trim()) { setError('Please provide an assessment name.'); return; }

    setUploading(true);
    setError(null);
    setProgress(0);

    try {
      let assessment;
      if (tab === 'pcap') {
        assessment = await assessmentsApi.uploadPcap(file, name.trim(), setProgress);
      } else {
        assessment = await assessmentsApi.uploadConfig(file, vendor, name.trim(), setProgress);
      }
      setSuccess(true);
      setTimeout(() => navigate(`/assessment/${assessment.id}`), 800);
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : 'Upload failed. Check the API server.',
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto animate-slide-up">
      {/* Page header */}
      <div className="mb-6">
        <h1 className="text-xl font-bold text-slate-100">New Assessment</h1>
        <p className="text-sm text-slate-500 mt-0.5">
          Upload a packet capture or vendor config file for automated IPsec security analysis
        </p>
      </div>

      <div className="glass-card p-6 space-y-6">
        {/* Tab Switcher */}
        <div className="flex gap-2 p-1 bg-slate-900/60 rounded-lg border border-slate-700/40">
          <button
            onClick={() => { setTab('pcap'); resetFile(); }}
            className={clsx(
              'flex-1 flex items-center justify-center gap-2 py-2 rounded-md text-sm font-medium transition-all duration-200',
              tab === 'pcap'
                ? 'bg-cyber-600/20 text-cyber-400 border border-cyber-500/30 shadow-sm'
                : 'text-slate-400 hover:text-slate-200',
            )}
          >
            <Network size={15} />
            PCAP File
          </button>
          <button
            onClick={() => { setTab('config'); resetFile(); }}
            className={clsx(
              'flex-1 flex items-center justify-center gap-2 py-2 rounded-md text-sm font-medium transition-all duration-200',
              tab === 'config'
                ? 'bg-cyber-600/20 text-cyber-400 border border-cyber-500/30 shadow-sm'
                : 'text-slate-400 hover:text-slate-200',
            )}
          >
            <FileCode2 size={15} />
            Config File
          </button>
        </div>

        {/* Vendor selector (config tab only) */}
        {tab === 'config' && (
          <div className="animate-fade-in">
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
              Vendor / Platform
            </label>
            <div className="relative">
              <select
                value={vendor}
                onChange={(e) => setVendor(e.target.value as VendorType)}
                className="input-field appearance-none pr-10"
              >
                {VENDORS.map((v) => (
                  <option key={v.value} value={v.value}>{v.label}</option>
                ))}
              </select>
              <ChevronDown size={15} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" />
            </div>
          </div>
        )}

        {/* Assessment name */}
        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
            Assessment Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder={tab === 'pcap' ? 'e.g. Site-A to Site-B Tunnel' : 'e.g. HQ Firewall Config'}
            className="input-field"
          />
        </div>

        {/* Drop zone */}
        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
            {tab === 'pcap' ? 'Packet Capture (.pcap, .pcapng)' : 'Configuration File (.conf, .cfg, .txt)'}
          </label>
          <div
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
            onClick={() => !uploading && fileInputRef.current?.click()}
            className={clsx(
              'relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200',
              dragging
                ? 'border-cyber-400 bg-cyber-500/10'
                : file
                ? 'border-success-500/50 bg-success-500/5'
                : 'border-slate-600/60 bg-slate-800/30 hover:border-cyber-600/60 hover:bg-cyber-500/5',
              uploading && 'pointer-events-none opacity-70',
            )}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept={ACCEPT[tab]}
              onChange={handleFileChange}
              className="hidden"
            />

            {file ? (
              <div className="flex flex-col items-center gap-2 animate-fade-in">
                <div className="w-12 h-12 rounded-xl bg-success-500/15 border border-success-500/30 flex items-center justify-center">
                  <FileText size={22} className="text-success-400" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-200">{file.name}</p>
                  <p className="text-xs text-slate-500 mt-0.5">
                    {(file.size / 1024).toFixed(1)} KB · Ready to upload
                  </p>
                </div>
                <button
                  type="button"
                  onClick={(e) => { e.stopPropagation(); resetFile(); }}
                  className="text-xs text-slate-500 hover:text-danger-400 transition-colors flex items-center gap-1 mt-1"
                >
                  <X size={12} /> Remove file
                </button>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-3">
                <div className={clsx(
                  'w-14 h-14 rounded-xl flex items-center justify-center border transition-colors',
                  dragging
                    ? 'bg-cyber-500/20 border-cyber-500/50'
                    : 'bg-slate-800/60 border-slate-700/50',
                )}>
                  <UploadIcon size={24} className={dragging ? 'text-cyber-400' : 'text-slate-500'} />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-300">
                    {dragging ? 'Drop it!' : 'Drag & drop or click to browse'}
                  </p>
                  <p className="text-xs text-slate-600 mt-0.5">
                    Accepted: {ACCEPT[tab]}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Progress bar */}
        {uploading && (
          <div className="animate-fade-in">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
              <span>Uploading & analyzing…</span>
              <span>{progress}%</span>
            </div>
            <div className="h-1.5 bg-slate-700/60 rounded-full overflow-hidden">
              <div
                className="h-full bg-cyber-500 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="flex items-start gap-2.5 px-4 py-3 rounded-lg bg-danger-500/10 border border-danger-500/30 text-danger-400 text-sm animate-fade-in">
            <AlertCircle size={16} className="flex-shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Success */}
        {success && (
          <div className="flex items-center gap-2.5 px-4 py-3 rounded-lg bg-success-500/10 border border-success-500/30 text-success-400 text-sm animate-fade-in">
            <CheckCircle2 size={16} />
            <span>Analysis complete! Redirecting to results…</span>
          </div>
        )}

        {/* Submit */}
        <button
          onClick={handleSubmit}
          disabled={uploading || success || !file}
          className="btn-primary w-full h-11"
        >
          {uploading ? (
            <><Loader2 size={16} className="animate-spin" /> Analyzing…</>
          ) : success ? (
            <><CheckCircle2 size={16} /> Done!</>
          ) : (
            <><UploadIcon size={16} /> Run Security Analysis</>
          )}
        </button>
      </div>

      {/* Info box */}
      <div className="mt-4 glass-card p-4 border-cyber-500/20 bg-cyber-500/5">
        <p className="text-xs text-cyber-400/80 font-medium mb-1">What happens next?</p>
        <p className="text-xs text-slate-500 leading-relaxed">
          {tab === 'pcap'
            ? 'The engine dissects IKE/ESP packets, infers cipher suites, evaluates quantum exposure (QTEI), and cross-checks NIST/NSA/BSI/ANSSI policy compliance.'
            : 'The engine parses your vendor config, extracts IKE phase 1/2 parameters, and audits against hardened cryptographic policy baselines.'}
        </p>
      </div>
    </div>
  );
}

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Shield, Download, FileJson, Anchor, ChevronLeft,
  AlertTriangle, Zap, Cpu, Copy, Check, X, Loader2,
} from 'lucide-react';
import { assessmentsApi, reportsApi } from '../lib/api';
import type { Assessment } from '../lib/api';
import RiskGauge from '../components/RiskGauge';
import FindingsTable from '../components/FindingsTable';

type Tab = 'findings' | 'pq' | 'esp';

export default function AssessmentDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('findings');
  const [showRemediation, setShowRemediation] = useState(false);
  const [remediation, setRemediation] = useState<Record<string, string> | null>(null);
  const [remediating, setRemediating] = useState(false);
  const [anchoring, setAnchoring] = useState(false);
  const [anchorHash, setAnchorHash] = useState<string | null>(null);
  const [copied, setCopied] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    assessmentsApi.get(id)
      .then(data => setAssessment(data))
      .catch(e => setError(e.response?.data?.detail ?? 'Failed to load assessment'))
      .finally(() => setLoading(false));
  }, [id]);

  const handleDownloadPdf = async () => {
    if (!id) return;
    const blob = await reportsApi.downloadPdf(id);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `cipher-sentinel-${id}.pdf`; a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadJson = async () => {
    if (!id) return;
    const blob = await reportsApi.getJsonReport(id) as unknown as Blob;
    // Try blob or JSON
    const url = URL.createObjectURL(new Blob([JSON.stringify(blob, null, 2)], { type: 'application/json' }));
    const a = document.createElement('a');
    a.href = url; a.download = `cipher-sentinel-${id}.json`; a.click();
    URL.revokeObjectURL(url);
  };

  const handleRemediate = async () => {
    if (!id) return;
    setRemediating(true);
    try {
      const result = await assessmentsApi.getRemediation(id);
      // result.configs has vendor → config strings
      const configs = (result as any).configs ?? result;
      setRemediation(configs);
      setShowRemediation(true);
    } catch (e: any) {
      alert(e.response?.data?.detail ?? 'Remediation failed');
    } finally {
      setRemediating(false);
    }
  };

  const handleAnchor = async () => {
    if (!id) return;
    setAnchoring(true);
    try {
      const result = await reportsApi.anchorReport(id);
      setAnchorHash((result as any).sha256_hash ?? result.hash);
    } catch (e: any) {
      alert(e.response?.data?.detail ?? 'Anchoring failed');
    } finally {
      setAnchoring(false);
    }
  };

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopied(key);
    setTimeout(() => setCopied(null), 2000);
  };

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <Loader2 className="animate-spin w-8 h-8 text-cyan-400" />
    </div>
  );

  if (error || !assessment) return (
    <div className="p-8 text-center text-red-400">
      <AlertTriangle className="mx-auto mb-4 w-12 h-12" />
      <p>{error ?? 'Assessment not found'}</p>
    </div>
  );

  const pq = assessment.pq_result as any;
  const esp = assessment.esp_result as any;

  const tabs = [
    { key: 'findings' as Tab, label: `Findings (${assessment.findings?.length ?? 0})`, icon: Shield },
    { key: 'pq' as Tab, label: 'Post-Quantum Risk', icon: Zap },
    { key: 'esp' as Tab, label: 'ESP Analysis', icon: Cpu },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button onClick={() => navigate('/')} className="text-slate-400 hover:text-cyan-400 transition-colors">
          <ChevronLeft className="w-6 h-6" />
        </button>
        <div className="flex-1">
          <h1 className="text-xl font-bold text-white font-mono truncate">{assessment.name}</h1>
          <div className="flex items-center gap-3 mt-1">
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
              String(assessment.status) === 'complete' ? 'bg-emerald-500/20 text-emerald-400' :
              String(assessment.status) === 'failed' ? 'bg-red-500/20 text-red-400' :
              'bg-amber-500/20 text-amber-400'
            }`}>
              {assessment.status?.toUpperCase()}
            </span>
            {assessment.ike_version && (
              <span className="text-xs text-cyan-400 font-mono">{assessment.ike_version}</span>
            )}
            {assessment.vendor && (
              <span className="text-xs text-slate-400">{assessment.vendor}</span>
            )}
            <span className="text-xs text-slate-500">
              {new Date(assessment.created_at).toLocaleString()}
            </span>
          </div>
        </div>
        {/* Action buttons */}
        <div className="flex items-center gap-2">
          <button onClick={handleDownloadPdf}
            className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg text-sm transition-colors">
            <Download className="w-4 h-4" /> PDF
          </button>
          <button onClick={handleDownloadJson}
            className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg text-sm transition-colors">
            <FileJson className="w-4 h-4" /> JSON
          </button>
          <button onClick={handleRemediate} disabled={remediating}
            className="flex items-center gap-2 px-3 py-2 bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white rounded-lg text-sm transition-colors">
            {remediating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Shield className="w-4 h-4" />}
            Remediate
          </button>
          <button onClick={handleAnchor} disabled={anchoring || !!anchorHash || !!(assessment as any).report_hash}
            className="flex items-center gap-2 px-3 py-2 bg-purple-700 hover:bg-purple-600 disabled:opacity-40 text-white rounded-lg text-sm transition-colors">
            {anchoring ? <Loader2 className="w-4 h-4 animate-spin" /> : <Anchor className="w-4 h-4" />}
            Anchor
          </button>
        </div>
      </div>

      {/* Anchor hash banner */}
      {(anchorHash || (assessment as any).report_hash?.sha256_hash) && (
        <div className="bg-purple-900/30 border border-purple-500/40 rounded-xl p-4 flex items-center gap-3">
          <Anchor className="w-5 h-5 text-purple-400 shrink-0" />
          <div>
            <p className="text-sm text-purple-300 font-medium">Report Anchored (Tamper-Evident Audit Trail)</p>
            <p className="text-xs font-mono text-purple-400 mt-0.5 break-all">
              SHA-256: {anchorHash ?? (assessment as any).report_hash?.sha256_hash}
            </p>
          </div>
        </div>
      )}

      {/* Top summary row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Gauge */}
        <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 flex flex-col items-center">
          <RiskGauge score={assessment.risk_score} />
        </div>

        {/* Violation summary cards */}
        <div className="lg:col-span-2 grid grid-cols-2 sm:grid-cols-3 gap-4">
          {[
            { label: 'Critical', count: assessment.critical_violations ?? assessment.critical_count ?? 0, color: 'red' },
            { label: 'High',     count: assessment.high_violations     ?? assessment.high_count     ?? 0, color: 'orange' },
            { label: 'Medium',   count: assessment.medium_violations   ?? assessment.medium_count   ?? 0, color: 'amber' },
          ].map(({ label, count, color }) => (
            <div key={label} className="bg-slate-800 border border-slate-700 rounded-xl p-4">
              <p className={`text-3xl font-bold font-mono ${
                color === 'red' ? 'text-red-400' : color === 'orange' ? 'text-orange-400' : 'text-amber-400'
              }`}>{count}</p>
              <p className="text-sm text-slate-400 mt-1">{label} Violations</p>
            </div>
          ))}
          {assessment.exchange_type && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 col-span-2 sm:col-span-1">
              <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">Exchange</p>
              <p className="text-sm text-cyan-400 font-mono leading-tight">{assessment.exchange_type}</p>
            </div>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden">
        <div className="flex border-b border-slate-700">
          {tabs.map(({ key, label, icon: Icon }) => (
            <button key={key} onClick={() => setActiveTab(key)}
              className={`flex items-center gap-2 px-6 py-4 text-sm font-medium transition-colors border-b-2 ${
                activeTab === key
                  ? 'border-cyan-400 text-cyan-400 bg-cyan-400/5'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}>
              <Icon className="w-4 h-4" />
              {label}
            </button>
          ))}
        </div>

        <div className="p-6">
          {/* Findings tab */}
          {activeTab === 'findings' && (
            <FindingsTable findings={assessment.findings ?? []} />
          )}

          {/* PQ Risk tab */}
          {activeTab === 'pq' && (
            pq ? (
              <div className="space-y-4">
                {/* QTEI Score */}
                <div className="bg-slate-800 rounded-xl p-5">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-sm font-semibold text-slate-300">Quantum Threat Exposure Index (QTEI)</h3>
                    <span className={`text-2xl font-bold font-mono ${
                      pq.qtei_score > 0.7 ? 'text-red-400' : pq.qtei_score > 0.3 ? 'text-amber-400' : 'text-emerald-400'
                    }`}>{((pq.qtei_score ?? 0) * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-3">
                    <div className={`h-3 rounded-full transition-all ${
                      pq.qtei_score > 0.7 ? 'bg-red-500' : pq.qtei_score > 0.3 ? 'bg-amber-500' : 'bg-emerald-500'
                    }`} style={{ width: `${(pq.qtei_score ?? 0) * 100}%` }} />
                  </div>
                  <p className="text-xs text-slate-400 mt-2">{pq.threat_classification?.replace(/_/g, ' ')}</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Shor's */}
                  <div className="bg-slate-800 border border-red-500/20 rounded-xl p-5">
                    <h4 className="text-sm font-semibold text-red-400 mb-3">⚛ Shor's Algorithm Exposure</h4>
                    <dl className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <dt className="text-slate-400">Vulnerable</dt>
                        <dd className={pq.shor_vulnerable ? 'text-red-400' : 'text-emerald-400'}>
                          {pq.shor_vulnerable ? 'YES' : 'NO'}
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-slate-400">HNDL Window</dt>
                        <dd className="text-amber-400 text-xs text-right max-w-[60%]">{pq.hndl_risk_window}</dd>
                      </div>
                    </dl>
                  </div>

                  {/* Grover's */}
                  <div className="bg-slate-800 border border-amber-500/20 rounded-xl p-5">
                    <h4 className="text-sm font-semibold text-amber-400 mb-3">🔍 Grover's Algorithm Exposure</h4>
                    <p className="text-xs text-slate-300 leading-relaxed">{pq.grover_assessment}</p>
                  </div>
                </div>

                {/* Defense action */}
                <div className="bg-emerald-900/20 border border-emerald-500/30 rounded-xl p-5">
                  <h4 className="text-sm font-semibold text-emerald-400 mb-2">🛡 Recommended Defense Action</h4>
                  <p className="text-sm text-slate-300">{pq.defense_action}</p>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-slate-500">
                <Zap className="mx-auto w-10 h-10 mb-3 opacity-30" />
                <p>No post-quantum data — requires PCAP with IKE proposals</p>
              </div>
            )
          )}

          {/* ESP tab */}
          {activeTab === 'esp' && (
            esp ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { label: 'Inferred Cipher', value: esp.inferred_cipher },
                  { label: 'Operational Mode', value: esp.operational_mode },
                  { label: 'Confidence', value: `${((esp.confidence_score ?? 0) * 100).toFixed(1)}%` },
                  { label: 'Shannon Entropy', value: `${esp.entropy?.toFixed(4)} bits/byte` },
                  { label: 'ICV Tag Size', value: `~${esp.icv_bits} bits` },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-slate-800 rounded-xl p-5">
                    <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">{label}</p>
                    <p className="text-lg font-mono text-cyan-300">{value ?? '—'}</p>
                  </div>
                ))}
                <div className="bg-slate-800 rounded-xl p-5 md:col-span-2">
                  <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">PECF Analysis Note</p>
                  <p className="text-sm text-slate-300">
                    Cipher family and VPN mode inferred passively from ESP payload length distribution and 
                    Shannon entropy — <span className="text-cyan-400">no decryption keys required</span> (Patent Claim 1).
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-slate-500">
                <Cpu className="mx-auto w-10 h-10 mb-3 opacity-30" />
                <p>No ESP data — upload a PCAP containing Protocol 50 traffic</p>
              </div>
            )
          )}
        </div>
      </div>

      {/* Remediation Modal */}
      {showRemediation && remediation && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-700">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Shield className="w-5 h-5 text-cyan-400" />
                Autonomous Hardened Configurations
              </h2>
              <button onClick={() => setShowRemediation(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="overflow-y-auto p-6 space-y-4">
              {Object.entries(remediation).map(([vendor, config]) => (
                <div key={vendor} className="border border-slate-700 rounded-xl overflow-hidden">
                  <div className="flex items-center justify-between bg-slate-800 px-4 py-2">
                    <span className="text-sm font-semibold text-cyan-400 font-mono">{vendor}</span>
                    <button onClick={() => copyToClipboard(config, vendor)}
                      className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition-colors">
                      {copied === vendor ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      {copied === vendor ? 'Copied!' : 'Copy'}
                    </button>
                  </div>
                  <pre className="text-xs text-slate-300 bg-slate-950 p-4 overflow-x-auto leading-relaxed">
                    {config}
                  </pre>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

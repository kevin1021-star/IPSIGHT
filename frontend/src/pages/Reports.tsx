import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  FileText, Download, FileJson, Anchor, Search,
  Filter, ChevronRight, Loader2, AlertTriangle,
} from 'lucide-react';
import { assessmentsApi, reportsApi } from '../lib/api';
import type { Assessment } from '../lib/api';
import SeverityBadge from '../components/SeverityBadge';

export default function Reports() {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [filterSeverity, setFilterSeverity] = useState('all');
  const [anchoring, setAnchoring] = useState<string | null>(null);
  const [anchoredHashes, setAnchoredHashes] = useState<Record<string, string>>({});

  useEffect(() => {
    assessmentsApi.list()
      .then(setAssessments)
      .catch(e => setError(e.response?.data?.detail ?? 'Failed to load reports'))
      .finally(() => setLoading(false));
  }, []);

  const handleDownloadPdf = async (id: string, name: string) => {
    const blob = await reportsApi.downloadPdf(id);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${name}-report.pdf`; a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadJson = async (id: string, name: string) => {
    const data = await reportsApi.getJsonReport(id);
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${name}-report.json`; a.click();
    URL.revokeObjectURL(url);
  };

  const handleAnchor = async (id: string) => {
    setAnchoring(id);
    try {
      const result = await reportsApi.anchorReport(id);
      const hash = (result as any).sha256_hash ?? result.hash;
      setAnchoredHashes(prev => ({ ...prev, [id]: hash }));
    } catch (e: any) {
      alert(e.response?.data?.detail ?? 'Anchoring failed');
    } finally {
      setAnchoring(null);
    }
  };

  const filtered = assessments.filter(a => {
    const matchSearch = a.name.toLowerCase().includes(search.toLowerCase()) ||
      (a.vendor ?? '').toLowerCase().includes(search.toLowerCase());
    const matchSev = filterSeverity === 'all' ||
      a.risk_classification?.toLowerCase() === filterSeverity;
    return matchSearch && matchSev;
  });

  const scoreColor = (score: number) =>
    score >= 80 ? 'text-emerald-400' : score >= 50 ? 'text-amber-400' : 'text-red-400';

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <Loader2 className="animate-spin w-8 h-8 text-cyan-400" />
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <FileText className="w-7 h-7 text-cyan-400" /> Reports
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Download PDF/JSON reports and anchor hashes for tamper-evident audit trails
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            value={search} onChange={e => setSearch(e.target.value)}
            placeholder="Search by name or vendor..."
            className="w-full pl-10 pr-4 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-500" />
          <select value={filterSeverity} onChange={e => setFilterSeverity(e.target.value)}
            className="bg-slate-800 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500">
            <option value="all">All Classifications</option>
            <option value="defense_grade">Defense Grade</option>
            <option value="acceptable">Acceptable</option>
            <option value="vulnerable">Vulnerable</option>
            <option value="compromised">Compromised</option>
          </select>
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="bg-red-900/20 border border-red-500/40 rounded-xl p-4 flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 text-red-400 shrink-0" />
          <p className="text-sm text-red-300">{error}</p>
        </div>
      )}

      {/* Reports table */}
      <div className="bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden">
        {filtered.length === 0 ? (
          <div className="text-center py-16 text-slate-500">
            <FileText className="mx-auto w-12 h-12 mb-4 opacity-20" />
            <p>No reports found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700 text-left text-xs text-slate-500 uppercase tracking-wider">
                  <th className="px-5 py-4">Assessment</th>
                  <th className="px-5 py-4">Score</th>
                  <th className="px-5 py-4">Classification</th>
                  <th className="px-5 py-4">Date</th>
                  <th className="px-5 py-4">Anchor Hash</th>
                  <th className="px-5 py-4">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {filtered.map(a => {
                  const hash = anchoredHashes[a.id] ?? (a as any).report_hash?.sha256_hash;
                  return (
                    <tr key={a.id} className="hover:bg-slate-800/50 transition-colors">
                      {/* Name */}
                      <td className="px-5 py-4">
                        <Link to={`/assessment/${a.id}`}
                          className="flex items-center gap-2 text-white hover:text-cyan-400 transition-colors group">
                          <span className="font-mono text-xs truncate max-w-[220px]">{a.name}</span>
                          <ChevronRight className="w-3.5 h-3.5 text-slate-600 group-hover:text-cyan-400 shrink-0" />
                        </Link>
                        {a.vendor && <p className="text-xs text-slate-500 mt-0.5">{a.vendor}</p>}
                      </td>

                      {/* Score */}
                      <td className="px-5 py-4">
                        <span className={`text-lg font-bold font-mono ${scoreColor(a.risk_score)}`}>
                          {a.risk_score}
                        </span>
                        <span className="text-slate-500 text-xs">/100</span>
                      </td>

                      {/* Classification */}
                      <td className="px-5 py-4">
                        <SeverityBadge severity={a.risk_classification as any} />
                      </td>

                      {/* Date */}
                      <td className="px-5 py-4 text-slate-400 text-xs">
                        {new Date(a.created_at).toLocaleDateString()}
                      </td>

                      {/* Anchor hash */}
                      <td className="px-5 py-4">
                        {hash ? (
                          <div className="flex items-center gap-1.5">
                            <Anchor className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                            <span className="text-xs font-mono text-purple-300 truncate max-w-[120px]">
                              {hash.substring(0, 16)}…
                            </span>
                          </div>
                        ) : (
                          <span className="text-xs text-slate-600">Not anchored</span>
                        )}
                      </td>

                      {/* Actions */}
                      <td className="px-5 py-4">
                        <div className="flex items-center gap-2">
                          <button onClick={() => handleDownloadPdf(a.id, a.name)}
                            title="Download PDF"
                            className="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-300 hover:text-white transition-colors">
                            <Download className="w-4 h-4" />
                          </button>
                          <button onClick={() => handleDownloadJson(a.id, a.name)}
                            title="Download JSON"
                            className="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-300 hover:text-white transition-colors">
                            <FileJson className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleAnchor(a.id)}
                            disabled={anchoring === a.id || !!hash}
                            title={hash ? 'Already anchored' : 'Anchor report hash'}
                            className="p-2 rounded-lg bg-purple-800/60 hover:bg-purple-700/60 disabled:opacity-40 text-purple-300 hover:text-white transition-colors">
                            {anchoring === a.id
                              ? <Loader2 className="w-4 h-4 animate-spin" />
                              : <Anchor className="w-4 h-4" />
                            }
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Legend */}
      <div className="flex items-center gap-6 text-xs text-slate-500">
        <div className="flex items-center gap-2">
          <Anchor className="w-3.5 h-3.5 text-purple-400" />
          <span>SHA-256 anchored — tamper-evident audit trail</span>
        </div>
        <span>Total: {assessments.length} assessments</span>
      </div>
    </div>
  );
}

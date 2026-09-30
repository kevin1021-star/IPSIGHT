import { useState, useMemo } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';
import SeverityBadge from './SeverityBadge';
import type { Finding, SeverityLevel } from '../lib/api';

interface FindingsTableProps {
  findings: Finding[];
}

const SEVERITY_ORDER: Record<SeverityLevel, number> = {
  CRITICAL: 0,
  HIGH: 1,
  MEDIUM: 2,
  LOW: 3,
  COMPLIANT: 4,
};

type SortDir = 'asc' | 'desc';

export default function FindingsTable({ findings }: FindingsTableProps) {
  const [sortDir, setSortDir] = useState<SortDir>('asc');
  const [expandedRow, setExpandedRow] = useState<string | null>(null);

  const sorted = useMemo(
    () =>
      [...findings].sort((a, b) => {
        const diff = SEVERITY_ORDER[a.severity] - SEVERITY_ORDER[b.severity];
        return sortDir === 'asc' ? diff : -diff;
      }),
    [findings, sortDir],
  );

  const toggleSort = () => setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));

  if (findings.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-slate-500">
        <p className="text-lg font-medium">No findings recorded</p>
        <p className="text-sm mt-1">This assessment has no policy violations.</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-700/50">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-700/50 bg-slate-900/60">
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider w-32">
              Rule ID
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
              <button
                onClick={toggleSort}
                className="inline-flex items-center gap-1.5 hover:text-slate-200 transition-colors"
              >
                Severity
                {sortDir === 'asc' ? (
                  <ArrowUp size={12} />
                ) : sortDir === 'desc' ? (
                  <ArrowDown size={12} />
                ) : (
                  <ArrowUpDown size={12} />
                )}
              </button>
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Standard
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Violation
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider hidden lg:table-cell">
              Impact
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider hidden xl:table-cell">
              Remediation Goal
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/60">
          {sorted.map((f, idx) => (
            <>
              <tr
                key={`${f.rule_id}-${idx}`}
                className="table-row-hover cursor-pointer"
                onClick={() =>
                  setExpandedRow(expandedRow === f.rule_id ? null : f.rule_id)
                }
              >
                <td className="px-4 py-3">
                  <code className="text-xs font-mono text-cyber-400 bg-cyber-500/10 px-1.5 py-0.5 rounded">
                    {f.rule_id}
                  </code>
                </td>
                <td className="px-4 py-3">
                  <SeverityBadge severity={f.severity} />
                </td>
                <td className="px-4 py-3 text-slate-300 text-xs">{f.standard}</td>
                <td className="px-4 py-3 text-slate-300 max-w-xs truncate">{f.violation}</td>
                <td className="px-4 py-3 text-slate-400 max-w-xs truncate hidden lg:table-cell text-xs">
                  {f.impact}
                </td>
                <td className="px-4 py-3 text-slate-400 max-w-xs truncate hidden xl:table-cell text-xs">
                  {f.remediation_goal}
                </td>
              </tr>
              {expandedRow === f.rule_id && (
                <tr key={`${f.rule_id}-${idx}-expanded`} className="bg-slate-900/80">
                  <td colSpan={6} className="px-6 py-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                          Violation
                        </p>
                        <p className="text-slate-300">{f.violation}</p>
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                          Impact
                        </p>
                        <p className="text-slate-300">{f.impact}</p>
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                          Remediation Goal
                        </p>
                        <p className="text-slate-300">{f.remediation_goal}</p>
                      </div>
                      {f.observed_value && (
                        <div>
                          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                            Observed Value
                          </p>
                          <code className="text-xs font-mono text-warning-400 bg-warning-500/10 px-2 py-1 rounded">
                            {f.observed_value}
                          </code>
                        </div>
                      )}
                    </div>
                  </td>
                </tr>
              )}
            </>
          ))}
        </tbody>
      </table>
    </div>
  );
}

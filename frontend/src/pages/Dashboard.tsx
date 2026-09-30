import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import {
  ShieldAlert,
  Activity,
  TrendingUp,
  Wifi,
  Loader2,
  AlertTriangle,
  RefreshCw,
  ChevronRight,
  Clock,
} from 'lucide-react';
import StatCard from '../components/StatCard';
import SeverityBadge from '../components/SeverityBadge';
import { dashboardApi, type DashboardStats, type TrendPoint, type SeverityLevel } from '../lib/api';

const SEVERITY_COLORS: Record<SeverityLevel, string> = {
  CRITICAL: '#f43f5e',
  HIGH:     '#f97316',
  MEDIUM:   '#f59e0b',
  LOW:      '#3b82f6',
  COMPLIANT:'#10b981',
};

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  });
}

function riskColor(score: number) {
  if (score >= 80) return 'text-success-400';
  if (score >= 50) return 'text-warning-400';
  return 'text-danger-400';
}

const CustomTooltip = ({ active, payload, label }: {
  active?: boolean;
  payload?: { value: number; name: string }[];
  label?: string;
}) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card border border-slate-600/60 px-3 py-2 text-xs shadow-xl">
      <p className="text-slate-400 mb-1">{label}</p>
      {payload.map((p, i) => (
        <p key={i} className="text-slate-200 font-semibold">{p.name}: {p.value}</p>
      ))}
    </div>
  );
};

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [trends, setTrends] = useState<TrendPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [s, t] = await Promise.all([
        dashboardApi.getStats(),
        dashboardApi.getTrends(),
      ]);
      setStats(s);
      setTrends(t);
    } catch {
      setError('Failed to load dashboard data. Is the API server running?');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void fetchData(); }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full min-h-[60vh]">
        <div className="flex flex-col items-center gap-3 text-slate-400">
          <Loader2 size={32} className="animate-spin text-cyber-500" />
          <p className="text-sm">Loading dashboard…</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full min-h-[60vh]">
        <div className="flex flex-col items-center gap-4 text-slate-400 max-w-sm text-center">
          <AlertTriangle size={40} className="text-warning-500" />
          <p className="text-slate-300 font-medium">{error}</p>
          <button onClick={fetchData} className="btn-secondary gap-2">
            <RefreshCw size={14} /> Retry
          </button>
        </div>
      </div>
    );
  }

  // Build bar chart data from severity_distribution
  const severityChartData = stats
    ? (Object.entries(stats.severity_distribution) as [SeverityLevel, number][]).map(
        ([name, count]) => ({ name, count }),
      )
    : [];

  // Format trend data for LineChart
  const trendChartData = trends.map((t) => ({
    date: new Date(t.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    score: t.avg_risk_score,
    assessments: t.assessment_count,
  }));

  return (
    <div className="p-6 space-y-6 animate-slide-up">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-slate-100">Security Dashboard</h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Real-time IPsec VPN security posture overview
          </p>
        </div>
        <button onClick={fetchData} className="btn-secondary text-xs gap-1.5">
          <RefreshCw size={13} />
          Refresh
        </button>
      </div>

      {/* ── Stat Cards ─────────────────────────────────────────────────── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Total Assessments"
          value={stats?.total_assessments ?? 0}
          icon={<Activity size={18} />}
          iconBg="bg-cyber-500/10"
          iconColor="text-cyber-400"
          highlight
        />
        <StatCard
          label="Critical Findings"
          value={stats?.critical_findings ?? 0}
          icon={<ShieldAlert size={18} />}
          iconBg="bg-danger-500/10"
          iconColor="text-danger-400"
        />
        <StatCard
          label="Avg Risk Score"
          value={stats?.avg_risk_score != null ? stats.avg_risk_score.toFixed(1) : '—'}
          icon={<TrendingUp size={18} />}
          iconBg="bg-warning-500/10"
          iconColor="text-warning-400"
          suffix="/ 100"
        />
        <StatCard
          label="High-Risk Tunnels"
          value={stats?.high_risk_tunnels ?? 0}
          icon={<Wifi size={18} />}
          iconBg="bg-orange-500/10"
          iconColor="text-orange-400"
        />
      </div>

      {/* ── Charts Row ─────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Severity Distribution Bar Chart */}
        <div className="glass-card p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
            <ShieldAlert size={15} className="text-danger-400" />
            Severity Distribution
          </h2>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={severityChartData} barCategoryGap="30%">
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(51,65,85,0.5)" vertical={false} />
              <XAxis
                dataKey="name"
                tick={{ fill: '#64748b', fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: '#64748b', fontSize: 11 }}
                axisLine={false}
                tickLine={false}
                allowDecimals={false}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
              <Bar dataKey="count" name="Findings" radius={[4, 4, 0, 0]}>
                {severityChartData.map((entry) => (
                  <Cell
                    key={entry.name}
                    fill={SEVERITY_COLORS[entry.name as SeverityLevel]}
                    fillOpacity={0.85}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Score Trend Line Chart */}
        <div className="glass-card p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
            <TrendingUp size={15} className="text-cyber-400" />
            Risk Score Trend · Last 30 Days
          </h2>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={trendChartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(51,65,85,0.5)" vertical={false} />
              <XAxis
                dataKey="date"
                tick={{ fill: '#64748b', fontSize: 10 }}
                axisLine={false}
                tickLine={false}
                interval="preserveStartEnd"
              />
              <YAxis
                domain={[0, 100]}
                tick={{ fill: '#64748b', fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line
                type="monotone"
                dataKey="score"
                name="Avg Risk Score"
                stroke="#22d3ee"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, fill: '#22d3ee', strokeWidth: 0 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ── Recent Assessments Table ───────────────────────────────────── */}
      <div className="glass-card">
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-800/60">
          <h2 className="text-sm font-semibold text-slate-300 flex items-center gap-2">
            <Clock size={15} className="text-slate-500" />
            Recent Assessments
          </h2>
          <Link to="/reports" className="text-xs text-cyber-400 hover:text-cyber-300 flex items-center gap-1 transition-colors">
            View all <ChevronRight size={12} />
          </Link>
        </div>

        {stats?.recent_assessments?.length === 0 ? (
          <div className="px-5 py-12 text-center text-slate-600 text-sm">
            No assessments yet. <Link to="/upload" className="text-cyber-400 hover:underline">Upload your first file →</Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-slate-900/40">
                  <th className="px-5 py-2.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Name</th>
                  <th className="px-5 py-2.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Risk Score</th>
                  <th className="px-5 py-2.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Classification</th>
                  <th className="px-5 py-2.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                  <th className="px-5 py-2.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Date</th>
                  <th className="px-5 py-2.5" />
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40">
                {stats?.recent_assessments.map((a) => (
                  <tr key={a.id} className="table-row-hover">
                    <td className="px-5 py-3 text-slate-200 font-medium">{a.name}</td>
                    <td className="px-5 py-3">
                      <span className={`font-bold tabular-nums text-base ${riskColor(a.risk_score)}`}>
                        {a.risk_score}
                      </span>
                    </td>
                    <td className="px-5 py-3">
                      <SeverityBadge severity={a.risk_classification as any} />
                    </td>
                    <td className="px-5 py-3">
                      <span className={`text-xs font-medium capitalize ${
                        a.status === 'completed' ? 'text-success-400' :
                        a.status === 'failed' ? 'text-danger-400' :
                        'text-warning-400'
                      }`}>
                        {a.status}
                      </span>
                    </td>
                    <td className="px-5 py-3 text-slate-500 text-xs">{formatDate(a.created_at)}</td>
                    <td className="px-5 py-3">
                      <Link
                        to={`/assessment/${a.id}`}
                        className="text-xs text-cyber-400 hover:text-cyber-300 flex items-center gap-1 justify-end transition-colors"
                      >
                        View <ChevronRight size={12} />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

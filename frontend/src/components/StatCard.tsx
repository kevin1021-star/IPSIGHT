import { clsx } from 'clsx';
import type { ReactNode } from 'react';

interface StatCardProps {
  label: string;
  value: string | number;
  icon: ReactNode;
  iconBg?: string;
  iconColor?: string;
  trend?: {
    value: number;
    label: string;
    positive?: boolean; // true = up is good, false = up is bad
  };
  highlight?: boolean;
  suffix?: string;
}

export default function StatCard({
  label,
  value,
  icon,
  iconBg = 'bg-slate-800',
  iconColor = 'text-slate-400',
  trend,
  highlight = false,
  suffix,
}: StatCardProps) {
  const trendUp = trend && trend.value > 0;
  const trendGood = trend
    ? trend.positive
      ? trendUp
      : !trendUp
    : false;

  return (
    <div
      className={clsx(
        'glass-card p-5 flex flex-col gap-4 relative overflow-hidden transition-all duration-200 hover:border-slate-600/60',
        highlight && 'cyber-border',
      )}
    >
      {/* Background accent */}
      {highlight && (
        <div className="absolute inset-0 bg-gradient-to-br from-cyber-500/5 to-transparent pointer-events-none" />
      )}

      <div className="flex items-start justify-between relative z-10">
        {/* Icon */}
        <div
          className={clsx(
            'w-10 h-10 rounded-lg flex items-center justify-center border',
            iconBg,
            iconColor,
            highlight ? 'border-cyber-500/30' : 'border-slate-700/50',
          )}
        >
          {icon}
        </div>

        {/* Trend badge */}
        {trend && (
          <div
            className={clsx(
              'flex items-center gap-1 text-xs font-semibold px-2 py-0.5 rounded-full border',
              trendGood
                ? 'text-success-400 bg-success-500/10 border-success-500/30'
                : 'text-danger-400 bg-danger-500/10 border-danger-500/30',
            )}
          >
            <span>{trendUp ? '↑' : '↓'}</span>
            <span>{Math.abs(trend.value)}%</span>
          </div>
        )}
      </div>

      {/* Value */}
      <div className="relative z-10">
        <div className="flex items-baseline gap-1">
          <span
            className={clsx(
              'text-3xl font-bold tabular-nums tracking-tight',
              highlight ? 'text-cyber-300' : 'text-slate-100',
            )}
          >
            {value}
          </span>
          {suffix && (
            <span className="text-sm text-slate-500 font-medium">{suffix}</span>
          )}
        </div>
        <p className="text-sm text-slate-400 mt-0.5">{label}</p>
        {trend && (
          <p className="text-xs text-slate-600 mt-0.5">{trend.label}</p>
        )}
      </div>
    </div>
  );
}

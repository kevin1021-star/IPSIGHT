import { clsx } from 'clsx';
import type { SeverityLevel } from '../lib/api';

interface SeverityBadgeProps {
  severity: SeverityLevel;
  size?: 'sm' | 'md';
}

const SEVERITY_STYLES: Record<SeverityLevel, string> = {
  CRITICAL: 'bg-danger-500/15 text-danger-400 border-danger-500/40 ring-danger-500/20',
  HIGH:     'bg-orange-500/15 text-orange-400 border-orange-500/40 ring-orange-500/20',
  MEDIUM:   'bg-warning-500/15 text-warning-400 border-warning-500/40 ring-warning-500/20',
  LOW:      'bg-blue-500/15 text-blue-400 border-blue-500/40 ring-blue-500/20',
  COMPLIANT:'bg-success-500/15 text-success-400 border-success-500/40 ring-success-500/20',
};

const SEVERITY_DOTS: Record<SeverityLevel, string> = {
  CRITICAL: 'bg-danger-400',
  HIGH:     'bg-orange-400',
  MEDIUM:   'bg-warning-400',
  LOW:      'bg-blue-400',
  COMPLIANT:'bg-success-400',
};

export default function SeverityBadge({ severity, size = 'sm' }: SeverityBadgeProps) {
  return (
    <span
      className={clsx(
        'inline-flex items-center gap-1.5 font-semibold uppercase tracking-wider border rounded-md ring-1',
        SEVERITY_STYLES[severity],
        size === 'sm' ? 'px-2 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs',
      )}
    >
      <span className={clsx('w-1.5 h-1.5 rounded-full flex-shrink-0', SEVERITY_DOTS[severity])} />
      {severity}
    </span>
  );
}

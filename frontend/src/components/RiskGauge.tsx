import { useMemo } from 'react';

interface RiskGaugeProps {
  score: number; // 0–100
  size?: number;
}

function getRiskColor(score: number): {
  stroke: string;
  textColor: string;
  label: string;
  bgGlow: string;
} {
  if (score >= 80) {
    return {
      stroke: '#10b981',
      textColor: 'text-success-400',
      label: 'LOW RISK',
      bgGlow: 'rgba(16, 185, 129, 0.15)',
    };
  }
  if (score >= 50) {
    return {
      stroke: '#f59e0b',
      textColor: 'text-warning-400',
      label: 'MEDIUM RISK',
      bgGlow: 'rgba(245, 158, 11, 0.15)',
    };
  }
  return {
    stroke: '#f43f5e',
    textColor: 'text-danger-400',
    label: 'HIGH RISK',
    bgGlow: 'rgba(244, 63, 94, 0.15)',
  };
}

export default function RiskGauge({ score, size = 200 }: RiskGaugeProps) {
  const { stroke, textColor, label, bgGlow } = useMemo(() => getRiskColor(score), [score]);

  const cx = size / 2;
  const cy = size / 2;
  const radius = (size / 2) * 0.72;
  const strokeWidth = size * 0.055;

  // Arc spans 220 degrees (from -200deg to +20deg, i.e. bottom-left to bottom-right)
  const totalArcDeg = 220;
  const progressDeg = (score / 100) * totalArcDeg;

  const toRad = (deg: number) => (deg * Math.PI) / 180;

  const describeArc = (startDeg: number, endDeg: number) => {
    const start = {
      x: cx + radius * Math.cos(toRad(startDeg)),
      y: cy + radius * Math.sin(toRad(startDeg)),
    };
    const end = {
      x: cx + radius * Math.cos(toRad(endDeg)),
      y: cy + radius * Math.sin(toRad(endDeg)),
    };
    const largeArc = endDeg - startDeg > 180 ? 1 : 0;
    return `M ${start.x} ${start.y} A ${radius} ${radius} 0 ${largeArc} 1 ${end.x} ${end.y}`;
  };

  // Convert to SVG angles (SVG 0° = right, clockwise)
  const svgStart = -200; // bottom-left
  const svgEnd = svgStart + progressDeg;
  const trackEnd = svgStart + totalArcDeg;

  return (
    <div
      className="relative inline-flex flex-col items-center justify-center"
      style={{ width: size, height: size }}
    >
      {/* Glow background */}
      <div
        className="absolute inset-0 rounded-full blur-2xl opacity-40"
        style={{ background: bgGlow }}
      />

      <svg width={size} height={size} className="relative z-10 -rotate-[10deg]">
        {/* Background track */}
        <path
          d={describeArc(svgStart, trackEnd)}
          fill="none"
          stroke="rgba(30,41,59,0.8)"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
        />

        {/* Progress arc */}
        {score > 0 && (
          <path
            d={describeArc(svgStart, svgEnd)}
            fill="none"
            stroke={stroke}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            style={{
              filter: `drop-shadow(0 0 6px ${stroke})`,
              transition: 'stroke-dashoffset 0.8s ease-out',
            }}
          />
        )}

        {/* Tick marks */}
        {[0, 25, 50, 75, 100].map((tick) => {
          const angle = svgStart + (tick / 100) * totalArcDeg;
          const inner = radius - strokeWidth / 2 - 4;
          const outer = radius + strokeWidth / 2 + 4;
          const cos = Math.cos(toRad(angle));
          const sin = Math.sin(toRad(angle));
          return (
            <line
              key={tick}
              x1={cx + inner * cos}
              y1={cy + inner * sin}
              x2={cx + outer * cos}
              y2={cy + outer * sin}
              stroke="rgba(148,163,184,0.3)"
              strokeWidth={1.5}
            />
          );
        })}
      </svg>

      {/* Center text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center z-20 rotate-0">
        <span
          className={`font-bold leading-none tabular-nums ${textColor}`}
          style={{ fontSize: size * 0.22 }}
        >
          {score}
        </span>
        <span className="text-slate-500 font-medium mt-1" style={{ fontSize: size * 0.065 }}>
          / 100
        </span>
        <span
          className={`font-bold tracking-widest mt-2 uppercase ${textColor}`}
          style={{ fontSize: size * 0.055 }}
        >
          {label}
        </span>
      </div>
    </div>
  );
}

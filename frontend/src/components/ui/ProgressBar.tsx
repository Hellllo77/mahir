interface Props {
  value: number;
  max: number;
  label?: string;
  showFraction?: boolean;
  color?: string;
}

export function ProgressBar({ value, max, label, showFraction, color }: Props) {
  const pct = max > 0 ? Math.min((value / max) * 100, 100) : 0;
  const met = value >= max;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-1)" }}>
      {(label || showFraction) && (
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          {label && <span className="text-xs text-muted">{label}</span>}
          {showFraction && (
            <span
              className="text-xs"
              style={{ color: met ? "var(--color-success)" : "var(--color-text-secondary)" }}
            >
              {value} / {max}
            </span>
          )}
        </div>
      )}
      <div className="progress-bar-track">
        <div
          className="progress-bar-fill"
          style={{
            width: `${pct}%`,
            background: color ?? (met ? "var(--color-success)" : "var(--color-brand-primary)"),
          }}
          role="progressbar"
          aria-valuenow={value}
          aria-valuemin={0}
          aria-valuemax={max}
        />
      </div>
    </div>
  );
}

"use client";

import type { ExerciseProgress, PfGateConfig } from "@/lib/api-types";
import { ProgressBar } from "@/components/ui/ProgressBar";

interface Props {
  progress?: ExerciseProgress | null;
  gateConfig?: PfGateConfig;
  pendingSubmission?: boolean;
}

function fmtSeconds(sec: number): string {
  if (sec < 60) return `${sec}s`;
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return s > 0 ? `${m}m ${s}s` : `${m}m`;
}

export function PFGateProgress({ progress, gateConfig, pendingSubmission }: Props) {
  const gate = progress?.gate ?? gateConfig;
  if (!gate) return null;

  const attempts = progress?.attempts_genuine ?? 0;
  const approaches = progress?.distinct_approaches ?? 0;
  const seconds = progress?.exploration_seconds ?? 0;

  return (
    <div className="card" style={{ gap: "var(--space-4)", display: "flex", flexDirection: "column" }}>
      <div>
        <h4 style={{ marginBottom: "var(--space-1)" }}>Exploration progress</h4>
        <p className="text-sm text-muted">
          All three conditions must be met to unlock the canonical solution.
        </p>
      </div>

      <div className="stack" style={{ gap: "var(--space-3)" }}>
        {/* Genuine attempts */}
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-1)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span className="text-xs text-muted">Genuine attempts</span>
            <span className="text-xs" style={{ color: attempts >= gate.min_attempts ? "var(--color-success)" : "var(--color-text-secondary)" }}>
              <strong>{attempts}</strong>
              {pendingSubmission && attempts < gate.min_attempts && (
                <span style={{ color: "var(--color-warning, #92400e)", marginLeft: "4px" }}>+1 pending</span>
              )}
              {" "}/ {gate.min_attempts}
            </span>
          </div>
          <ProgressBar value={attempts} max={gate.min_attempts} />
        </div>

        {/* Distinct approaches */}
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-1)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span className="text-xs text-muted">Distinct approaches tried</span>
            <span className="text-xs" style={{ color: approaches >= gate.min_distinct_approaches ? "var(--color-success)" : "var(--color-text-secondary)" }}>
              <strong>{approaches}</strong> / {gate.min_distinct_approaches}
            </span>
          </div>
          <ProgressBar value={approaches} max={gate.min_distinct_approaches} />
        </div>

        {/* Exploration time */}
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-1)" }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <span className="text-xs text-muted">Exploration time</span>
            <span
              className="text-xs"
              style={{ color: seconds >= gate.min_exploration_seconds ? "var(--color-success)" : "var(--color-text-secondary)" }}
            >
              <strong>{fmtSeconds(seconds)}</strong> / {fmtSeconds(gate.min_exploration_seconds)}
            </span>
          </div>
          <ProgressBar value={seconds} max={gate.min_exploration_seconds} />
        </div>
      </div>

      <p className="text-xs text-muted" style={{ borderTop: "1px solid var(--color-border)", paddingTop: "var(--space-3)" }}>
        Failing is fine — exploring is required. Low-effort or off-task submissions do not count
        toward genuine attempts.
      </p>
    </div>
  );
}

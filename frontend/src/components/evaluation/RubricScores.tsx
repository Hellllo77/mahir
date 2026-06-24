import type { RubricScore } from "@/lib/api-types";

interface Props {
  scores: RubricScore[];
}

const SEVERITY_COLOR: Record<string, string> = {
  minor: "var(--color-warning)",
  major: "var(--color-error)",
  critical: "#7f1d1d",
};

export function RubricScores({ scores }: Props) {
  if (scores.length === 0) return null;

  return (
    <div className="stack" style={{ gap: "var(--space-3)" }}>
      <h4>Rubric breakdown</h4>
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
        {scores.map((s) => (
          <div
            key={s.criterion_id}
            className="card"
            style={{ padding: "var(--space-4)", gap: "var(--space-2)", display: "flex", flexDirection: "column" }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "var(--space-2)" }}>
              <span className="text-sm" style={{ fontWeight: "var(--font-weight-medium)", fontFamily: "var(--font-family-mono)" }}>
                {s.criterion_id}
              </span>
              <div className="cluster">
                <span
                  className="badge"
                  style={{
                    background: s.met ? "var(--color-signal-productive-bg)" : "var(--color-signal-off-task-bg)",
                    color: s.met ? "var(--color-signal-productive-text)" : "var(--color-signal-off-task-text)",
                  }}
                >
                  {s.met ? "Met" : "Not met"}
                </span>
                {!s.met && (
                  <span
                    className="badge"
                    style={{
                      background: "var(--color-error-bg)",
                      color: SEVERITY_COLOR[s.severity] ?? "var(--color-error)",
                    }}
                  >
                    {s.severity}
                  </span>
                )}
                <span className="text-xs text-muted">score: {(s.score * 100).toFixed(0)}%</span>
              </div>
            </div>
            {s.evidence && (
              <p className="text-xs text-muted" style={{ borderLeft: "2px solid var(--color-border)", paddingLeft: "var(--space-3)" }}>
                {s.evidence}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

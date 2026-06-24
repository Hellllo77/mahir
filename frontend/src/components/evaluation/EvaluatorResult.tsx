"use client";

import ReactMarkdown from "react-markdown";
import type { EvaluationResult } from "@/lib/api-types";
import { PFSignalBadge } from "@/components/ui/PFSignalBadge";
import { RubricScores } from "./RubricScores";

interface Props {
  result: EvaluationResult;
}

export function EvaluatorResult({ result }: Props) {
  const passedScenarios = result.scenario_results?.filter((s) => s.passed).length ?? 0;
  const totalScenarios = result.scenario_results?.length ?? 0;

  return (
    <div className="stack">
      {/* Summary row */}
      <div className="card" style={{ display: "flex", gap: "var(--space-6)", flexWrap: "wrap", alignItems: "flex-start" }}>
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-1)", flex: 1 }}>
          <span className="text-xs text-muted">Overall score</span>
          <span style={{ fontSize: "var(--font-size-2xl)", fontWeight: "var(--font-weight-bold)" }}>
            {(result.overall_score * 100).toFixed(0)}%
          </span>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-1)", flex: 1 }}>
          <span className="text-xs text-muted">PF signal</span>
          <PFSignalBadge signal={result.productive_failure_signal} />
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-1)", flex: 1 }}>
          <span className="text-xs text-muted">Agent ran</span>
          <span
            className="badge"
            style={{
              background: result.ran ? "var(--color-signal-productive-bg)" : "var(--color-error-bg)",
              color: result.ran ? "var(--color-signal-productive-text)" : "var(--color-error)",
            }}
          >
            {result.ran ? "Yes" : "No"}
          </span>
        </div>

        {totalScenarios > 0 && (
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-1)", flex: 1 }}>
            <span className="text-xs text-muted">Scenarios</span>
            <span style={{ fontWeight: "var(--font-weight-medium)" }}>
              {passedScenarios} / {totalScenarios} passed
            </span>
          </div>
        )}

        {result.detected_approach && (
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-1)", flex: 1 }}>
            <span className="text-xs text-muted">Approach detected</span>
            <code className="text-sm">{result.detected_approach}</code>
          </div>
        )}
      </div>

      {/* Feedback */}
      {result.feedback_markdown && (
        <div className="card">
          <h4 style={{ marginBottom: "var(--space-4)" }}>Feedback</h4>
          <div className="prose text-sm">
            <ReactMarkdown>{result.feedback_markdown}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* Scenario results */}
      {result.scenario_results && result.scenario_results.length > 0 && (
        <div className="card">
          <h4 style={{ marginBottom: "var(--space-4)" }}>Scenario results</h4>
          <div className="stack" style={{ gap: "var(--space-2)" }}>
            {result.scenario_results.map((sr) => (
              <div
                key={sr.scenario_id}
                style={{
                  display: "flex",
                  gap: "var(--space-3)",
                  alignItems: "flex-start",
                  padding: "var(--space-3)",
                  borderRadius: "var(--radius-md)",
                  background: sr.passed ? "var(--color-signal-productive-bg)" : "var(--color-error-bg)",
                }}
              >
                <span style={{ fontSize: "var(--font-size-sm)", color: sr.passed ? "var(--color-success)" : "var(--color-error)" }}>
                  {sr.passed ? "✓" : "✗"}
                </span>
                <div>
                  <code className="text-xs">{sr.scenario_id}</code>
                  {sr.detail && <p className="text-xs text-muted" style={{ marginTop: "var(--space-1)" }}>{sr.detail}</p>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Rubric */}
      {result.rubric_scores && result.rubric_scores.length > 0 && (
        <div className="card">
          <RubricScores scores={result.rubric_scores} />
        </div>
      )}

      {/* Meta */}
      <div className="text-xs text-muted cluster" style={{ gap: "var(--space-4)" }}>
        {result.judge_model && <span>Judge: {result.judge_model}{result.judge_escalated ? " (escalated)" : ""}</span>}
        {result.evaluated_at && <span>Evaluated: {new Date(result.evaluated_at).toLocaleString()}</span>}
        {result.cost_micro_usd !== undefined && (
          <span>Cost: ${(result.cost_micro_usd / 1_000_000).toFixed(4)}</span>
        )}
      </div>
    </div>
  );
}

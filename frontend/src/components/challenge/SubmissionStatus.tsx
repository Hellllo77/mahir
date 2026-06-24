"use client";

import type { SubmissionStatus as TStatus } from "@/lib/api-types";

interface Props {
  status: TStatus;
  attemptNumber: number;
}

const STATUS_ICON: Record<TStatus, string> = {
  queued: "⏳",
  running: "⚙️",
  evaluated: "✅",
  failed: "❌",
};

const STATUS_LABEL: Record<TStatus, string> = {
  queued: "Queued for evaluation",
  running: "Evaluating your agent…",
  evaluated: "Evaluation complete",
  failed: "Evaluation failed",
};

const STATUS_CLASS: Record<TStatus, string> = {
  queued: "alert alert-info",
  running: "alert alert-info",
  evaluated: "alert alert-success",
  failed: "alert alert-error",
};

export function SubmissionStatus({ status, attemptNumber }: Props) {
  const isActive = status === "queued" || status === "running";

  return (
    <div className={STATUS_CLASS[status]}>
      <span style={{ fontSize: "1.25rem" }}>{STATUS_ICON[status]}</span>
      <div>
        <div style={{ fontWeight: "var(--font-weight-medium)" }}>
          Attempt #{attemptNumber} — {STATUS_LABEL[status]}
        </div>
        {isActive && (
          <div className="text-xs" style={{ marginTop: "var(--space-1)", opacity: 0.8 }}>
            <span className="spinner" style={{ marginRight: "var(--space-2)" }} />
            Your agent is being run against test scenarios and scored by the LLM judge. This may take a moment.
          </div>
        )}
        {status === "failed" && (
          <div className="text-xs" style={{ marginTop: "var(--space-1)" }}>
            The evaluation infrastructure encountered an error (not your agent). You can resubmit.
          </div>
        )}
      </div>
    </div>
  );
}

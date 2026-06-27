"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
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
  queued: "Queued for review",
  running: "Reviewing your response…",
  evaluated: "Review complete",
  failed: "Review failed",
};

const STATUS_CLASS: Record<TStatus, string> = {
  queued: "alert alert-info",
  running: "alert alert-info",
  evaluated: "alert alert-success",
  failed: "alert alert-error",
};

export function SubmissionStatus({ status, attemptNumber }: Props) {
  const isActive = status === "queued" || status === "running";
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    if (!isActive) {
      setElapsed(0);
      return;
    }
    const interval = setInterval(() => setElapsed((e) => e + 1), 1000);
    return () => clearInterval(interval);
  }, [isActive]);

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
            {elapsed < 15
              ? "Your response is being reviewed. This may take a moment."
              : "Still evaluating — this usually takes under a minute. Don't close this tab."}
          </div>
        )}
        {isActive && elapsed >= 60 && (
          <div style={{ marginTop: "var(--space-2)" }}>
            <Link
              href="/dashboard"
              className="text-xs"
              style={{ color: "inherit", textDecoration: "underline" }}
            >
              Check back later →
            </Link>
          </div>
        )}
        {status === "failed" && (
          <div className="text-xs" style={{ marginTop: "var(--space-1)" }}>
            The automated reviewer encountered an error (not your response). You can resubmit.
          </div>
        )}
      </div>
    </div>
  );
}

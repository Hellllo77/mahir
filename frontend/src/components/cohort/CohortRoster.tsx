"use client";

import { useState } from "react";
import type {
  LearnerProgressSummary,
  LearnerDetailProgress,
  Phase,
  PFSignal,
} from "@/lib/api-types";
import { getLearnerProgress, overrideGate, ApiClientError } from "@/lib/api-client";
import { PhaseTag } from "@/components/ui/PhaseTag";
import { PFSignalBadge } from "@/components/ui/PFSignalBadge";

interface Props {
  cohortId: string;
  learners: LearnerProgressSummary[];
  exerciseTitles?: Record<string, string>;
}

const OVERRIDE_LABELS: Record<string, string> = {
  unlock_consolidation: "Unlock Consolidation",
  mark_completed: "Mark Completed",
  reset_exploring: "Reset",
};

export function CohortRoster({ cohortId, learners, exerciseTitles = {} }: Props) {
  const [filter, setFilter] = useState<Phase | "all">("all");

  const allExerciseIds = Array.from(
    new Set(learners.flatMap((l) => l.exercises.map((e) => e.exercise_id)))
  );

  const filtered = learners.filter((l) => {
    if (filter === "all") return true;
    return l.exercises.some((e) => e.phase === filter);
  });

  return (
    <div className="stack">
      <div className="cluster">
        <span className="text-sm text-muted">Filter by phase:</span>
        {(["all", "not_started", "exploring", "consolidation_unlocked", "completed"] as const).map((f) => (
          <button
            key={f}
            className={`btn btn-sm ${filter === f ? "btn-primary" : "btn-secondary"}`}
            onClick={() => setFilter(f)}
          >
            {f === "all" ? "All" : f.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "var(--font-size-sm)" }}>
          <thead>
            <tr style={{ borderBottom: "2px solid var(--color-border)" }}>
              <th style={{ textAlign: "left", padding: "var(--space-3) var(--space-4)", fontWeight: "var(--font-weight-semibold)", whiteSpace: "nowrap" }}>
                Student
              </th>
              {allExerciseIds.map((id) => (
                <th
                  key={id}
                  style={{ textAlign: "left", padding: "var(--space-3) var(--space-4)", fontWeight: "var(--font-weight-semibold)", whiteSpace: "nowrap", minWidth: "9rem" }}
                >
                  {exerciseTitles[id] ?? id.slice(0, 8) + "…"}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((learner) => (
              <LearnerRow
                key={learner.user_id}
                cohortId={cohortId}
                learner={learner}
                exerciseIds={allExerciseIds}
                exerciseTitles={exerciseTitles}
              />
            ))}
            {filtered.length === 0 && (
              <tr>
                <td
                  colSpan={allExerciseIds.length + 1}
                  style={{ textAlign: "center", padding: "var(--space-8)", color: "var(--color-text-muted)" }}
                >
                  No students match this filter.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <p className="text-xs text-muted">
        {filtered.length} of {learners.length} student{learners.length !== 1 ? "s" : ""} shown.
        Teacher overrides can be applied on the individual exercise view.
      </p>
    </div>
  );
}

function LearnerRow({
  cohortId,
  learner,
  exerciseIds,
  exerciseTitles,
}: {
  cohortId: string;
  learner: LearnerProgressSummary;
  exerciseIds: string[];
  exerciseTitles: Record<string, string>;
}) {
  const [expanded, setExpanded] = useState(false);
  const [detail, setDetail] = useState<LearnerDetailProgress | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [detailError, setDetailError] = useState<string | null>(null);

  const byExercise = Object.fromEntries(learner.exercises.map((e) => [e.exercise_id, e]));

  function toggle() {
    if (expanded) {
      setExpanded(false);
      return;
    }
    if (detail) {
      setExpanded(true);
      return;
    }
    setLoadingDetail(true);
    setDetailError(null);
    getLearnerProgress(cohortId, learner.user_id)
      .then((d) => {
        setDetail(d);
        setExpanded(true);
      })
      .catch((err) => {
        setDetailError(err instanceof Error ? err.message : "Failed to load progress.");
      })
      .finally(() => setLoadingDetail(false));
  }

  return (
    <>
      <tr
        onClick={toggle}
        style={{
          borderBottom: expanded ? "none" : "1px solid var(--color-border)",
          cursor: "pointer",
        }}
      >
        <td style={{ padding: "var(--space-3) var(--space-4)", fontWeight: "var(--font-weight-medium)", whiteSpace: "nowrap" }}>
          <span style={{ marginRight: "var(--space-2)", color: "var(--color-text-muted)", fontSize: "var(--font-size-xs)" }}>
            {loadingDetail ? "⋯" : expanded ? "▼" : "▶"}
          </span>
          {learner.display_name}
        </td>
        {exerciseIds.map((id) => {
          const ex = byExercise[id];
          if (!ex) {
            return (
              <td key={id} style={{ padding: "var(--space-3) var(--space-4)", color: "var(--color-text-muted)" }}>
                —
              </td>
            );
          }
          return (
            <td key={id} style={{ padding: "var(--space-3) var(--space-4)" }}>
              <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-1)" }}>
                <PhaseTag phase={ex.phase} />
                <span className="text-xs text-muted">
                  {ex.attempts_genuine}/{ex.attempts_total} genuine
                </span>
                {ex.latest_signal && (
                  <PFSignalBadge signal={ex.latest_signal as PFSignal} />
                )}
                {!ex.explored && ex.phase !== "not_started" && ex.phase !== "exploring" && (
                  <span className="badge" style={{ background: "var(--color-warning-bg)", color: "var(--color-warning)", fontSize: "var(--font-size-xs)" }}>
                    Fast-unlocked
                  </span>
                )}
              </div>
            </td>
          );
        })}
      </tr>

      {expanded && (
        <tr style={{ borderBottom: "1px solid var(--color-border)" }}>
          <td
            colSpan={exerciseIds.length + 1}
            style={{ padding: "0 var(--space-4) var(--space-4)", background: "var(--color-bg-subtle, #f9fafb)" }}
            onClick={(e) => e.stopPropagation()}
          >
            {detailError && (
              <div className="alert alert-error text-sm" style={{ marginTop: "var(--space-3)" }}>
                {detailError}
              </div>
            )}
            {detail && (
              <DrillDownPanel
                detail={detail}
                exerciseTitles={exerciseTitles}
              />
            )}
          </td>
        </tr>
      )}
    </>
  );
}

function DrillDownPanel({
  detail,
  exerciseTitles,
}: {
  detail: LearnerDetailProgress;
  exerciseTitles: Record<string, string>;
}) {
  return (
    <div style={{ paddingTop: "var(--space-3)" }}>
      <p className="text-xs text-muted" style={{ marginBottom: "var(--space-3)" }}>
        Detailed progress for {detail.display_name}
      </p>
      <div className="stack" style={{ gap: "var(--space-3)" }}>
        {detail.exercises.map((ex) => (
          <ExerciseOverrideRow
            key={ex.exercise_id}
            progressId={ex.progress_id ?? null}
            exerciseId={ex.exercise_id}
            title={exerciseTitles[ex.exercise_id]}
            phase={ex.phase}
            attemptsTotal={ex.attempts_total}
            attemptsGenuine={ex.attempts_genuine}
            latestSignal={ex.latest_signal as PFSignal | null}
          />
        ))}
      </div>
    </div>
  );
}

function ExerciseOverrideRow({
  progressId,
  exerciseId,
  title,
  phase,
  attemptsTotal,
  attemptsGenuine,
  latestSignal,
}: {
  progressId: string | null;
  exerciseId: string;
  title?: string;
  phase: Phase;
  attemptsTotal: number;
  attemptsGenuine: number;
  latestSignal: PFSignal | null;
}) {
  const [pending, setPending] = useState<"unlock_consolidation" | "mark_completed" | "reset_exploring" | null>(null);
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [overrideError, setOverrideError] = useState<string | null>(null);

  async function applyOverride() {
    if (!progressId || !pending) return;
    setBusy(true);
    setOverrideError(null);
    try {
      await overrideGate(progressId, { action: pending, reason: reason.trim() });
      setSuccessMsg(`${OVERRIDE_LABELS[pending]} applied`);
      setPending(null);
      setReason("");
    } catch (err) {
      setOverrideError(
        err instanceof ApiClientError ? err.message : "Override failed. Please try again."
      );
    } finally {
      setBusy(false);
    }
  }

  const disabled = !progressId || busy;

  return (
    <div
      style={{
        borderLeft: "3px solid var(--color-border)",
        paddingLeft: "var(--space-3)",
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-2)",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", flexWrap: "wrap" }}>
        <span style={{ fontWeight: "var(--font-weight-medium)", fontSize: "var(--font-size-sm)" }}>
          {title ?? exerciseId.slice(0, 12) + "…"}
        </span>
        <PhaseTag phase={phase} />
        {latestSignal && <PFSignalBadge signal={latestSignal} />}
        <span className="text-xs text-muted">
          {attemptsGenuine}/{attemptsTotal} genuine attempts
        </span>
        {successMsg && (
          <span className="badge" style={{ background: "var(--color-success-bg, #d1fae5)", color: "var(--color-success, #065f46)", fontSize: "var(--font-size-xs)" }}>
            ✓ {successMsg}
          </span>
        )}
      </div>

      <div className="cluster" style={{ gap: "var(--space-2)", flexWrap: "wrap" }}>
        {(["unlock_consolidation", "mark_completed", "reset_exploring"] as const).map((action) => (
          <button
            key={action}
            className="btn btn-sm btn-secondary"
            disabled={disabled || pending === action}
            onClick={() => { setPending(action); setReason(""); setSuccessMsg(null); setOverrideError(null); }}
            title={!progressId ? "No progress record yet" : undefined}
          >
            {OVERRIDE_LABELS[action]}
          </button>
        ))}
      </div>

      {pending && (
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
          <textarea
            className="form-input"
            rows={2}
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder={`Reason for "${OVERRIDE_LABELS[pending]}"…`}
            disabled={busy}
            style={{ resize: "vertical", fontSize: "var(--font-size-sm)" }}
          />
          <div className="cluster" style={{ gap: "var(--space-2)" }}>
            <button
              className="btn btn-sm btn-primary"
              onClick={applyOverride}
              disabled={busy || !reason.trim()}
            >
              {busy ? <><span className="spinner" aria-hidden="true" /> Applying…</> : "Confirm"}
            </button>
            <button
              className="btn btn-sm btn-secondary"
              onClick={() => { setPending(null); setReason(""); }}
              disabled={busy}
            >
              Cancel
            </button>
          </div>
          {overrideError && (
            <span className="text-sm" style={{ color: "var(--color-error, #dc2626)" }}>
              {overrideError}
            </span>
          )}
        </div>
      )}
    </div>
  );
}

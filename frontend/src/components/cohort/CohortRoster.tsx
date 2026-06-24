"use client";

import { useState } from "react";
import type { LearnerProgressSummary, Phase, PFSignal } from "@/lib/api-types";
import { PhaseTag } from "@/components/ui/PhaseTag";
import { PFSignalBadge } from "@/components/ui/PFSignalBadge";

interface Props {
  learners: LearnerProgressSummary[];
  exerciseTitles?: Record<string, string>;
}

const PHASE_ORDER: Record<Phase, number> = {
  not_started: 0,
  exploring: 1,
  consolidation_unlocked: 2,
  completed: 3,
};

export function CohortRoster({ learners, exerciseTitles = {} }: Props) {
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
                Learner
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
                learner={learner}
                exerciseIds={allExerciseIds}
              />
            ))}
            {filtered.length === 0 && (
              <tr>
                <td
                  colSpan={allExerciseIds.length + 1}
                  style={{ textAlign: "center", padding: "var(--space-8)", color: "var(--color-text-muted)" }}
                >
                  No learners match this filter.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <p className="text-xs text-muted">
        {filtered.length} of {learners.length} learner{learners.length !== 1 ? "s" : ""} shown.
        Facilitator overrides can be applied on the individual exercise view.
      </p>
    </div>
  );
}

function LearnerRow({ learner, exerciseIds }: { learner: LearnerProgressSummary; exerciseIds: string[] }) {
  const byExercise = Object.fromEntries(learner.exercises.map((e) => [e.exercise_id, e]));

  return (
    <tr style={{ borderBottom: "1px solid var(--color-border)" }}>
      <td style={{ padding: "var(--space-3) var(--space-4)", fontWeight: "var(--font-weight-medium)", whiteSpace: "nowrap" }}>
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
  );
}

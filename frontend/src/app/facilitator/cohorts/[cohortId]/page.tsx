"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getCohortRoster, getModules, getMe, ApiClientError } from "@/lib/api-client";
import type { LearnerProgressSummary, Module, Me } from "@/lib/api-types";
import { AppShell } from "@/components/layout/AppShell";
import { CohortRoster } from "@/components/cohort/CohortRoster";

export default function FacilitatorCohortPage() {
  const { cohortId } = useParams<{ cohortId: string }>();
  const [me, setMe] = useState<Me | null>(null);
  const [roster, setRoster] = useState<LearnerProgressSummary[]>([]);
  const [modules, setModules] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const [meData, rosterData, modulesData] = await Promise.all([
          getMe(),
          getCohortRoster(cohortId),
          getModules(cohortId),
        ]);
        setMe(meData);
        setRoster(rosterData);
        setModules(modulesData);
      } catch (err) {
        if (err instanceof ApiClientError && err.status === 401) {
          window.location.href = "/login";
        } else if (err instanceof ApiClientError && err.status === 403) {
          setError("You don't have facilitator access to this cohort.");
        } else {
          setError(err instanceof Error ? err.message : "Failed to load cohort roster.");
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [cohortId]);

  const exerciseTitles = Object.fromEntries(
    modules.flatMap((m) => (m.exercises ?? []).map((e) => [e.id, e.title]))
  );

  const totalExercises = modules.reduce((sum, m) => sum + (m.exercises?.length ?? 0), 0);
  const completedLearners = roster.filter(
    (l) => l.exercises.filter((e) => e.phase === "completed").length === totalExercises && totalExercises > 0
  ).length;

  return (
    <AppShell userName={me?.display_name}>
      {loading && (
        <div className="empty-state">
          <span className="spinner" style={{ fontSize: "1.5rem" }} />
          <p>Loading cohort data…</p>
        </div>
      )}

      {error && <div className="alert alert-error">{error}</div>}

      {!loading && !error && (
        <div className="stack" style={{ maxWidth: "72rem" }}>
          <Link href="/facilitator/cohorts" className="text-sm text-muted" style={{ textDecoration: "none" }}>
            ← Back to Cohorts
          </Link>

          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "var(--space-4)", flexWrap: "wrap" }}>
            <div>
              <h1>Cohort overview</h1>
              <p className="text-muted" style={{ marginTop: "var(--space-2)" }}>
                Real-time Productive Failure signals for your cohort.
              </p>
            </div>
            <Link href={`/cohorts/${cohortId}`} className="btn btn-secondary">
              ← Learner view
            </Link>
          </div>

          {/* Summary stats */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(10rem, 1fr))", gap: "var(--space-4)" }}>
            <div className="card" style={{ textAlign: "center" }}>
              <div style={{ fontSize: "var(--font-size-3xl)", fontWeight: "var(--font-weight-bold)", color: "var(--color-brand-primary)" }}>
                {roster.length}
              </div>
              <div className="text-sm text-muted">Enrolled</div>
            </div>
            <div className="card" style={{ textAlign: "center" }}>
              <div style={{ fontSize: "var(--font-size-3xl)", fontWeight: "var(--font-weight-bold)", color: "var(--color-phase-exploring-text)" }}>
                {roster.filter((l) => l.exercises.some((e) => e.phase === "exploring")).length}
              </div>
              <div className="text-sm text-muted">Exploring</div>
            </div>
            <div className="card" style={{ textAlign: "center" }}>
              <div style={{ fontSize: "var(--font-size-3xl)", fontWeight: "var(--font-weight-bold)", color: "var(--color-success)" }}>
                {completedLearners}
              </div>
              <div className="text-sm text-muted">All exercises done</div>
            </div>
            <div className="card" style={{ textAlign: "center" }}>
              <div style={{ fontSize: "var(--font-size-3xl)", fontWeight: "var(--font-weight-bold)", color: "var(--color-warning)" }}>
                {roster.filter((l) => l.exercises.some((e) => e.latest_signal === "low_effort" || e.latest_signal === "off_task")).length}
              </div>
              <div className="text-sm text-muted">Needs attention</div>
            </div>
          </div>

          {/* Roster table */}
          <div className="card" style={{ padding: "var(--space-6)", overflow: "hidden" }}>
            <h2 style={{ marginBottom: "var(--space-6)" }}>Learner roster</h2>
            {roster.length > 0 ? (
              <CohortRoster learners={roster} exerciseTitles={exerciseTitles} />
            ) : (
              <div className="empty-state">
                <p>No learners enrolled yet.</p>
              </div>
            )}
          </div>

          {/* PF signal legend */}
          <div className="card">
            <h4 style={{ marginBottom: "var(--space-4)" }}>Signal legend</h4>
            <div className="cluster" style={{ gap: "var(--space-6)", flexWrap: "wrap" }}>
              <div className="cluster">
                <span className="badge" style={{ background: "var(--color-signal-productive-bg)", color: "var(--color-signal-productive-text)" }}>Productive</span>
                <span className="text-sm text-muted">Genuine attempt, counts toward gate</span>
              </div>
              <div className="cluster">
                <span className="badge" style={{ background: "var(--color-signal-low-effort-bg)", color: "var(--color-signal-low-effort-text)" }}>Low effort</span>
                <span className="text-sm text-muted">Submitted but does not count toward gate</span>
              </div>
              <div className="cluster">
                <span className="badge" style={{ background: "var(--color-signal-off-task-bg)", color: "var(--color-signal-off-task-text)" }}>Off-task</span>
                <span className="text-sm text-muted">Not addressing the problem</span>
              </div>
              <div className="cluster">
                <span className="badge" style={{ background: "var(--color-warning-bg)", color: "var(--color-warning)" }}>Fast-unlocked</span>
                <span className="text-sm text-muted">Passed on attempt 1 — PF bypassed (audited)</span>
              </div>
            </div>
          </div>

          <p className="text-xs text-muted">
            Facilitator gate overrides are available on each learner&apos;s individual exercise view.
            All overrides are recorded for grant audit purposes.
          </p>
        </div>
      )}
    </AppShell>
  );
}

"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getModules, getMyProgress, getMe, ApiClientError } from "@/lib/api-client";
import type { Module, ExerciseProgress, Me } from "@/lib/api-types";
import { AppShell } from "@/components/layout/AppShell";
import { ModuleNav } from "@/components/nav/ModuleNav";
import { PhaseTag } from "@/components/ui/PhaseTag";
import { ProgressBar } from "@/components/ui/ProgressBar";

export default function CohortPage() {
  const { cohortId } = useParams<{ cohortId: string }>();
  const [me, setMe] = useState<Me | null>(null);
  const [modules, setModules] = useState<Module[]>([]);
  const [progress, setProgress] = useState<ExerciseProgress[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const [meData, modulesData] = await Promise.all([getMe(), getModules(cohortId)]);
        setMe(meData);
        setModules(modulesData);
        const enrolment = meData.enrolments.find((e) => e.cohort_id === cohortId && e.status === "active");
        if (enrolment) {
          const prog = await getMyProgress(enrolment.id);
          setProgress(prog);
        }
      } catch (err) {
        if (err instanceof ApiClientError && err.status === 401) {
          window.location.href = "/login";
        } else {
          setError(err instanceof Error ? err.message : "Failed to load cohort.");
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [cohortId]);

  const progressById = Object.fromEntries(progress.map((p) => [p.exercise_id, p]));
  const isFacilitator = me?.global_role === "facilitator" || me?.global_role === "org_admin" || me?.global_role === "super_admin";

  const allExercises = modules.flatMap((m) => m.exercises ?? []);
  const completed = allExercises.filter((e) => progressById[e.id]?.phase === "completed").length;

  const sidebar = modules.length > 0 ? (
    <ModuleNav
      cohortId={cohortId}
      modules={modules.map((m) => ({
        ...m,
        exercises: m.exercises?.map((e) => ({
          ...e,
          phase: progressById[e.id]?.phase ?? "not_started",
        })),
      }))}
    />
  ) : undefined;

  return (
    <AppShell
      sidebar={sidebar}
      userName={me?.display_name}
      isFacilitator={isFacilitator}
      cohortId={cohortId}
    >
      {loading && (
        <div className="empty-state">
          <span className="spinner" style={{ fontSize: "1.5rem" }} />
          <p>Loading your curriculum…</p>
        </div>
      )}

      {error && <div className="alert alert-error">{error}</div>}

      {!loading && !error && (
        <div className="stack" style={{ maxWidth: "var(--content-max-width)" }}>
          <div>
            <h1>Your learning path</h1>
            <p className="text-muted" style={{ marginTop: "var(--space-2)" }}>
              Build AI agents step by step. Explore each problem before the canonical solution is revealed.
            </p>
          </div>

          {allExercises.length > 0 && (
            <div className="card" style={{ display: "flex", gap: "var(--space-4)", alignItems: "center" }}>
              <div style={{ flex: 1 }}>
                <ProgressBar value={completed} max={allExercises.length} showFraction label="Overall progress" />
              </div>
            </div>
          )}

          <div className="stack">
            {modules
              .slice()
              .sort((a, b) => a.sequence_index - b.sequence_index)
              .map((mod) => (
                <div key={mod.id} className="card">
                  <h2 style={{ marginBottom: "var(--space-2)" }}>
                    {mod.sequence_index + 1}. {mod.title}
                  </h2>
                  {mod.summary_markdown && (
                    <p className="text-sm text-muted" style={{ marginBottom: "var(--space-4)" }}>
                      {mod.summary_markdown}
                    </p>
                  )}

                  {mod.exercises && mod.exercises.length > 0 ? (
                    <ul style={{ listStyle: "none", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                      {mod.exercises
                        .slice()
                        .sort((a, b) => a.sequence_index - b.sequence_index)
                        .map((ex) => {
                          const phase = progressById[ex.id]?.phase ?? "not_started";
                          return (
                            <li key={ex.id}>
                              <Link
                                href={`/exercises/${ex.id}`}
                                style={{
                                  display: "flex",
                                  justifyContent: "space-between",
                                  alignItems: "center",
                                  padding: "var(--space-3) var(--space-4)",
                                  borderRadius: "var(--radius-md)",
                                  border: "1px solid var(--color-border)",
                                  textDecoration: "none",
                                  color: "var(--color-text-primary)",
                                  background: "var(--color-bg-surface-raised)",
                                  transition: "border-color var(--transition-fast)",
                                }}
                              >
                                <span style={{ fontWeight: "var(--font-weight-medium)" }}>{ex.title}</span>
                                <PhaseTag phase={phase} />
                              </Link>
                            </li>
                          );
                        })}
                    </ul>
                  ) : (
                    <p className="text-sm text-muted">No exercises in this module yet.</p>
                  )}
                </div>
              ))}
          </div>
        </div>
      )}
    </AppShell>
  );
}

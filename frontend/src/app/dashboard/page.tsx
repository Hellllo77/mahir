"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getMe, getCurriculum, ApiClientError } from "@/lib/api-client";
import type { Me, CurriculumResponse } from "@/lib/api-types";
import { AppShell } from "@/components/layout/AppShell";
import { PhaseTag } from "@/components/ui/PhaseTag";
import { ProgressBar } from "@/components/ui/ProgressBar";

export default function DashboardPage() {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);
  const [curriculum, setCurriculum] = useState<CurriculumResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [noCurriculum, setNoCurriculum] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    setNoCurriculum(false);
    try {
      const meData = await getMe();
      const isStaff =
        meData.global_role === "org_admin" ||
        meData.global_role === "super_admin" ||
        meData.global_role === "facilitator";
      if (isStaff) {
        router.replace("/facilitator/cohorts");
        return;
      }
      setMe(meData);
      try {
        const data = await getCurriculum();
        setCurriculum(data);
      } catch (currErr) {
        if (currErr instanceof ApiClientError && (currErr.status === 404 || currErr.status === 403)) {
          setNoCurriculum(true);
        } else {
          throw currErr;
        }
      }
    } catch (err) {
      if (err instanceof ApiClientError && err.status === 401) {
        router.replace("/login");
      } else {
        setError(err instanceof Error ? err.message : "Couldn't load your learning path.");
      }
    } finally {
      setLoading(false);
    }
  }, [router]);

  useEffect(() => {
    load();
  }, [load]);

  const sortedModules = curriculum
    ? curriculum.modules.slice().sort((a, b) => a.sequence_index - b.sequence_index)
    : [];
  const allExercises = sortedModules.flatMap((m) =>
    m.exercises.slice().sort((a, b) => a.sequence_index - b.sequence_index)
  );
  const completed = allExercises.filter((e) => e.phase === "completed").length;
  const firstIncomplete = allExercises.find((e) => e.phase !== "completed");

  return (
    <AppShell userName={me?.display_name}>
      {loading && (
        <div className="empty-state">
          <span className="spinner" style={{ fontSize: "1.5rem" }} />
          <p>Loading your learning path…</p>
        </div>
      )}

      {!loading && error && (
        <div className="stack" style={{ maxWidth: "36rem" }}>
          <div className="alert alert-error">
            <span>⚠️</span>
            <div>
              <div style={{ fontWeight: "var(--font-weight-medium)" }}>Couldn't load your learning path</div>
              <div className="text-xs" style={{ marginTop: "var(--space-1)" }}>{error}</div>
            </div>
          </div>
          <button className="btn btn-secondary" onClick={() => void load()}>Try again</button>
        </div>
      )}

      {!loading && !error && noCurriculum && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            minHeight: "60vh",
            gap: "var(--space-4)",
            textAlign: "center",
          }}
        >
          <div className="card" style={{ maxWidth: "28rem", width: "100%" }}>
            <h2 style={{ color: "var(--color-brand-primary)", marginBottom: "var(--space-3)" }}>
              No learning path yet
            </h2>
            <p className="text-sm text-muted">
              Your learning path hasn&apos;t been set up yet. Contact your administrator to get started.
            </p>
          </div>
        </div>
      )}

      {!loading && !error && curriculum && (
        <div className="stack" style={{ maxWidth: "var(--content-max-width)" }}>
          <div>
            <h1>{curriculum.curriculum.title}</h1>
            <p className="text-muted" style={{ marginTop: "var(--space-2)" }}>
              Build AI agents step by step. Explore each problem before the canonical solution is revealed.
            </p>
          </div>

          {allExercises.length > 0 && (
            <div className="card" style={{ display: "flex", gap: "var(--space-6)", alignItems: "center", flexWrap: "wrap" }}>
              <div style={{ flex: 1, minWidth: "12rem" }}>
                <ProgressBar value={completed} max={allExercises.length} showFraction label="Overall progress" />
              </div>
              {firstIncomplete && (
                <Link
                  href={`/exercises/${firstIncomplete.id}`}
                  className="btn btn-primary"
                  style={{ whiteSpace: "nowrap", flexShrink: 0 }}
                >
                  Continue →
                </Link>
              )}
            </div>
          )}

          <div className="stack">
            {sortedModules.map((mod, modIdx) => {
              const modExercises = mod.exercises.slice().sort((a, b) => a.sequence_index - b.sequence_index);
              const hasActive = modExercises.some((ex) => ex.phase === "exploring" || ex.phase === "not_started");
              const isFirst = modIdx === 0;
              return (
                <details key={mod.id} className="card" open={isFirst || hasActive}>
                  <summary style={{ cursor: "pointer", listStyle: "none", display: "flex", alignItems: "center", gap: "var(--space-3)" }}>
                    <h2 style={{ margin: 0, flex: 1 }}>
                      {mod.sequence_index}. {mod.title}
                    </h2>
                    <span className="text-xs text-muted">
                      {modExercises.filter((ex) => ex.phase === "completed").length} / {modExercises.length} done
                    </span>
                  </summary>

                  <div style={{ marginTop: "var(--space-4)" }}>
                    {mod.summary_markdown && (
                      <p className="text-sm text-muted" style={{ marginBottom: "var(--space-4)" }}>
                        {mod.summary_markdown}
                      </p>
                    )}

                    {modExercises.length > 0 ? (
                      <ul style={{ listStyle: "none", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                        {modExercises.map((ex) => (
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
                              <PhaseTag phase={ex.phase} />
                            </Link>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-sm text-muted">No beats in this module yet.</p>
                    )}
                  </div>
                </details>
              );
            })}
          </div>
        </div>
      )}
    </AppShell>
  );
}

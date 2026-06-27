"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import ReactMarkdown from "react-markdown";
import {
  getExercise,
  getExerciseProgress,
  getConsolidation,
  submitAgent,
  listSubmissions,
  getMe,
  getModules,
  getModuleExercises,
  ApiClientError,
  PhaseLocked,
} from "@/lib/api-client";
import type {
  Exercise,
  ExerciseProgress,
  Submission,
  SubmissionCreate,
  Me,
  Module,
  ConsolidationContent,
} from "@/lib/api-types";
import { AppShell } from "@/components/layout/AppShell";
import { ModuleNav } from "@/components/nav/ModuleNav";
import { PhaseTag } from "@/components/ui/PhaseTag";
import { PFGateProgress } from "@/components/evaluation/PFGateProgress";
import { AgentBuilder } from "@/components/challenge/AgentBuilder";
import { SubmissionStatus } from "@/components/challenge/SubmissionStatus";
import { useSubmission } from "@/lib/hooks/useSubmission";
import { EvaluatorResult } from "@/components/evaluation/EvaluatorResult";

export default function ExercisePage() {
  const { exerciseId } = useParams<{ exerciseId: string }>();

  const [me, setMe] = useState<Me | null>(null);
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [moduleExercises, setModuleExercises] = useState<Exercise[]>([]);
  const [progress, setProgress] = useState<ExerciseProgress | null>(null);
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [consolidation, setConsolidation] = useState<ConsolidationContent | null>(null);
  const [modules, setModules] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [latestSubId, setLatestSubId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"challenge" | "consolidation">("challenge");

  const { data: latestSubDetail } = useSubmission(latestSubId);

  const refreshProgress = useCallback(async () => {
    try {
      const p = await getExerciseProgress(exerciseId);
      setProgress(p);
      // once consolidation unlocked, try to fetch consolidation content
      if (p.phase === "consolidation_unlocked" || p.phase === "completed") {
        try {
          const c = await getConsolidation(exerciseId);
          setConsolidation(c);
        } catch (e) {
          if (!(e instanceof PhaseLocked)) throw e;
        }
      }
    } catch (e) {
      console.error("refreshProgress failed", e);
    }
  }, [exerciseId]);

  useEffect(() => {
    async function load() {
      try {
        const meData = await getMe();
        setMe(meData);

        const [exData, progData, subsData] = await Promise.all([
          getExercise(exerciseId),
          getExerciseProgress(exerciseId).catch(() => null),
          listSubmissions(exerciseId).catch(() => []),
        ]);
        setExercise(exData);
        setProgress(progData);
        setSubmissions(subsData);

        // Load sidebar modules + sibling beat exercises
        const activeEnrolment = meData.enrolments.find((e) => e.status === "active");
        if (activeEnrolment) {
          const mods = await getModules(activeEnrolment.cohort_id);
          setModules(mods);
          // Fetch all exercises in the same module so AgentBuilder can show all beats
          if (exData.module_id) {
            const siblings = await getModuleExercises(activeEnrolment.cohort_id, exData.module_id).catch(() => []);
            setModuleExercises(siblings);
          }
        }

        // Fetch consolidation if already unlocked
        if (progData && (progData.phase === "consolidation_unlocked" || progData.phase === "completed")) {
          try {
            const c = await getConsolidation(exerciseId);
            setConsolidation(c);
          } catch (e) {
            if (!(e instanceof PhaseLocked)) throw e;
          }
        }
      } catch (err) {
        if (err instanceof ApiClientError && err.status === 401) {
          window.location.href = "/login";
        } else {
          setError(err instanceof Error ? err.message : "Failed to load exercise.");
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [exerciseId]);

  // After polling completes on an evaluated submission, refresh progress
  useEffect(() => {
    if (latestSubDetail?.status === "evaluated") {
      setSubmissions((prev) => {
        const exists = prev.find((s) => s.id === latestSubDetail.id);
        return exists ? prev.map((s) => (s.id === latestSubDetail.id ? latestSubDetail : s)) : [latestSubDetail, ...prev];
      });
      refreshProgress();
    }
  }, [latestSubDetail, refreshProgress]);

  async function handleSubmit(body: SubmissionCreate, idempotencyKey: string) {
    setSubmitting(true);
    setError(null);
    try {
      const sub = await submitAgent(exerciseId, body, idempotencyKey);
      setSubmissions((prev) => [sub, ...prev]);
      setLatestSubId(sub.id);
      await refreshProgress();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Submission failed.");
    } finally {
      setSubmitting(false);
    }
  }

  const activeEnrolment = me?.enrolments.find((e) => e.status === "active");
  const isFacilitator =
    me?.global_role === "facilitator" ||
    me?.global_role === "org_admin" ||
    me?.global_role === "super_admin";

  const consolidationUnlocked =
    progress?.phase === "consolidation_unlocked" || progress?.phase === "completed";

  const progressByExercise = Object.fromEntries(
    modules.flatMap((m) =>
      (m.exercises ?? []).map((e) => [e.id, { ...e, phase: e.phase ?? "not_started" }])
    )
  );

  const sidebar = modules.length > 0 ? (
    <ModuleNav
      cohortId={activeEnrolment?.cohort_id ?? ""}
      modules={modules.map((m) => ({
        ...m,
        exercises: m.exercises?.map((e) => ({
          ...e,
          phase: progressByExercise[e.id]?.phase ?? "not_started",
        })),
      }))}
    />
  ) : undefined;

  return (
    <AppShell
      sidebar={sidebar}
      userName={me?.display_name}
      isFacilitator={isFacilitator}
      cohortId={activeEnrolment?.cohort_id}
    >
      {loading && (
        <div className="empty-state">
          <span className="spinner" style={{ fontSize: "1.5rem" }} />
          <p>Loading exercise…</p>
        </div>
      )}

      {error && <div className="alert alert-error">{error}</div>}

      {!loading && exercise && (
        <div style={{ maxWidth: "var(--content-max-width)" }}>
          {/* Header */}
          <div style={{ marginBottom: "var(--space-6)", display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "var(--space-4)", flexWrap: "wrap" }}>
            <div>
              <h1 style={{ marginBottom: "var(--space-2)" }}>{exercise.title}</h1>
              {progress && <PhaseTag phase={progress.phase} />}
            </div>
            {consolidationUnlocked && (
              <div className="cluster" style={{ gap: "var(--space-1)" }}>
                <button
                  className={`btn ${activeTab === "challenge" ? "btn-primary" : "btn-secondary"}`}
                  onClick={() => setActiveTab("challenge")}
                >
                  Challenge
                </button>
                <button
                  className={`btn ${activeTab === "consolidation" ? "btn-primary" : "btn-secondary"}`}
                  onClick={() => setActiveTab("consolidation")}
                >
                  Canonical solution
                </button>
              </div>
            )}
          </div>

          {/* Consolidation unlocked banner */}
          {consolidationUnlocked && activeTab === "challenge" && (
            <div className="alert alert-success" style={{ marginBottom: "var(--space-6)" }}>
              <span style={{ fontSize: "1.25rem" }}>🎉</span>
              <div>
                <strong>Exploration gate satisfied!</strong> The canonical solution is now available.
                Compare your approaches to the reference design.
              </div>
            </div>
          )}

          {activeTab === "consolidation" && consolidation ? (
            /* ── Consolidation view ── */
            <div className="stack">
              <div className="alert alert-info">
                <span>ℹ️</span>
                <span className="text-sm">
                  You earned this by exploring the problem first. Compare your attempts to the
                  reference design below.
                </span>
              </div>
              <div className="card">
                <h2 style={{ marginBottom: "var(--space-6)" }}>Canonical solution</h2>
                <div className="prose">
                  <ReactMarkdown>{consolidation.body_markdown}</ReactMarkdown>
                </div>
              </div>
              {consolidation.reference_build && (
                <div className="card">
                  <h3 style={{ marginBottom: "var(--space-4)" }}>Reference agent build</h3>
                  <pre style={{ fontSize: "var(--font-size-xs)" }}>
                    {JSON.stringify(consolidation.reference_build, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          ) : (
            /* ── Challenge view ── */
            <div className="stack">
              {/* Problem statement */}
              <div className="card">
                <h2 style={{ marginBottom: "var(--space-4)" }}>The challenge</h2>
                <div className="prose">
                  <ReactMarkdown>{exercise.prompt_markdown}</ReactMarkdown>
                </div>
              </div>

              {/* Build spec */}
              {Object.keys(exercise.build_spec).length > 0 && (
                <details className="card">
                  <summary style={{ cursor: "pointer", fontWeight: "var(--font-weight-medium)", fontSize: "var(--font-size-sm)" }}>
                    Build specification
                  </summary>
                  <pre style={{ marginTop: "var(--space-4)", fontSize: "var(--font-size-xs)" }}>
                    {JSON.stringify(exercise.build_spec, null, 2)}
                  </pre>
                </details>
              )}

              {/* PF gate progress */}
              {progress && progress.gate && <PFGateProgress progress={progress} />}

              {/* Latest submission status */}
              {latestSubId && latestSubDetail && (
                <SubmissionStatus
                  status={latestSubDetail.status}
                  attemptNumber={latestSubDetail.attempt_number}
                />
              )}

              {/* Latest evaluation result */}
              {latestSubDetail?.status === "evaluated" && latestSubDetail.result && (
                <EvaluatorResult result={latestSubDetail.result} />
              )}

              {/* Agent builder */}
              {progress?.phase !== "completed" && (
                <div className="card">
                  <h3 style={{ marginBottom: "var(--space-4)" }}>
                    Submit attempt #{(progress?.attempts_total ?? 0) + 1}
                  </h3>
                  <AgentBuilder
                    exercise={exercise}
                    moduleExercises={moduleExercises}
                    onSubmit={handleSubmit}
                    submitting={submitting}
                  />
                </div>
              )}

              {progress?.phase === "completed" && (
                <div className="alert alert-success">
                  <span>✅</span>
                  <span>You have completed this exercise. Well done!</span>
                </div>
              )}

              {/* Previous submissions */}
              {submissions.length > 1 && (
                <details className="card">
                  <summary style={{ cursor: "pointer", fontWeight: "var(--font-weight-medium)", fontSize: "var(--font-size-sm)" }}>
                    Previous attempts ({submissions.length})
                  </summary>
                  <div className="stack" style={{ marginTop: "var(--space-4)", gap: "var(--space-2)" }}>
                    {submissions.map((sub) => (
                      <div
                        key={sub.id}
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          padding: "var(--space-3)",
                          borderRadius: "var(--radius-md)",
                          background: "var(--color-bg-surface-raised)",
                          fontSize: "var(--font-size-sm)",
                        }}
                      >
                        <span>Attempt #{sub.attempt_number}</span>
                        <span
                          className="badge"
                          style={{
                            background: `var(--color-status-${sub.status.replace("_", "-")}-bg, var(--color-bg-surface-raised))`,
                            color: `var(--color-status-${sub.status.replace("_", "-")}-text, var(--color-text-secondary))`,
                          }}
                        >
                          {sub.status}
                        </span>
                        <span className="text-xs text-muted">
                          {new Date(sub.submitted_at).toLocaleString()}
                        </span>
                      </div>
                    ))}
                  </div>
                </details>
              )}
            </div>
          )}
        </div>
      )}
    </AppShell>
  );
}

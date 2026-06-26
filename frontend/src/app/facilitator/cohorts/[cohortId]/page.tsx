"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  getCohort,
  getCohortRoster,
  getModules,
  getMe,
  updateCohort,
  getCohortInviteLink,
  ApiClientError,
} from "@/lib/api-client";
import type { CohortDetail, LearnerProgressSummary, Module, Me } from "@/lib/api-types";
import { AppShell } from "@/components/layout/AppShell";
import { CohortRoster } from "@/components/cohort/CohortRoster";

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, { bg: string; color: string }> = {
    active:   { bg: "var(--color-success-bg, #d1fae5)", color: "var(--color-success, #065f46)" },
    archived: { bg: "var(--color-bg-muted, #f3f4f6)", color: "var(--color-text-muted, #6b7280)" },
    draft:    { bg: "var(--color-warning-bg, #fef3c7)", color: "var(--color-warning, #92400e)" },
  };
  const s = styles[status] ?? styles.draft;
  return (
    <span className="badge" style={{ background: s.bg, color: s.color, textTransform: "capitalize" }}>
      {status}
    </span>
  );
}

function EditCohortForm({
  cohort,
  onSaved,
  onCancel,
}: {
  cohort: CohortDetail;
  onSaved: (updated: CohortDetail) => void;
  onCancel: () => void;
}) {
  const [name, setName] = useState(cohort.name);
  const [description, setDescription] = useState(cohort.description ?? "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSaving(true);
    try {
      const updated = await updateCohort(cohort.id, {
        name: name.trim(),
        description: description.trim() || undefined,
      });
      onSaved(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save cohort.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="card" style={{ marginTop: "var(--space-4)" }}>
      <h2 style={{ marginBottom: "var(--space-6)" }}>Edit cohort</h2>
      <form onSubmit={handleSubmit} className="stack">
        <div className="form-group">
          <label className="form-label" htmlFor="edit-cohort-name">
            Name <span aria-hidden="true">*</span>
          </label>
          <input
            id="edit-cohort-name"
            type="text"
            className="form-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            disabled={saving}
          />
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="edit-cohort-description">
            Description <span className="text-muted">(optional)</span>
          </label>
          <input
            id="edit-cohort-description"
            type="text"
            className="form-input"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Brief description of this cohort"
            disabled={saving}
          />
        </div>
        {error && <div className="alert alert-error text-sm">{error}</div>}
        <div className="cluster" style={{ gap: "var(--space-3)", justifyContent: "flex-end" }}>
          <button type="button" className="btn btn-secondary" onClick={onCancel} disabled={saving}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={saving || !name.trim()}>
            {saving ? <><span className="spinner" aria-hidden="true" /> Saving…</> : "Save"}
          </button>
        </div>
      </form>
    </div>
  );
}

export default function FacilitatorCohortPage() {
  const { cohortId } = useParams<{ cohortId: string }>();
  const [me, setMe] = useState<Me | null>(null);
  const [cohort, setCohort] = useState<CohortDetail | null>(null);
  const [roster, setRoster] = useState<LearnerProgressSummary[]>([]);
  const [modules, setModules] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // F-M-004: inline edit
  const [showEditForm, setShowEditForm] = useState(false);

  // F-M-003: publish state
  const [publishing, setPublishing] = useState(false);
  const [publishError, setPublishError] = useState<string | null>(null);

  // F-M-002: invite link copy
  const [copyState, setCopyState] = useState<"idle" | "loading" | "copied" | "error">("idle");

  const load = useCallback(async () => {
    try {
      const [meData, cohortData, rosterData, modulesData] = await Promise.all([
        getMe(),
        getCohort(cohortId),
        getCohortRoster(cohortId),
        getModules(cohortId),
      ]);
      setMe(meData);
      setCohort(cohortData);
      setRoster(rosterData);
      setModules(modulesData);
    } catch (err) {
      if (err instanceof ApiClientError && err.status === 401) {
        window.location.href = "/login";
      } else if (err instanceof ApiClientError && err.status === 403) {
        setError("You don't have facilitator access to this cohort.");
      } else {
        setError(err instanceof Error ? err.message : "Failed to load cohort.");
      }
    } finally {
      setLoading(false);
    }
  }, [cohortId]);

  useEffect(() => { load(); }, [load]);

  async function handlePublish() {
    if (!cohort) return;
    setPublishError(null);
    setPublishing(true);
    try {
      const updated = await updateCohort(cohort.id, { status: "active" });
      setCohort(updated);
    } catch (err) {
      setPublishError(err instanceof Error ? err.message : "Failed to publish cohort.");
    } finally {
      setPublishing(false);
    }
  }

  async function handleCopyInviteLink() {
    setCopyState("loading");
    try {
      const { url } = await getCohortInviteLink(cohortId);
      await navigator.clipboard.writeText(url);
      setCopyState("copied");
      setTimeout(() => setCopyState("idle"), 2500);
    } catch {
      setCopyState("error");
      setTimeout(() => setCopyState("idle"), 3000);
    }
  }

  const exerciseTitles = Object.fromEntries(
    modules.flatMap((m) => (m.exercises ?? []).map((e) => [e.id, e.title]))
  );

  const totalExercises = modules.reduce((sum, m) => sum + (m.exercises?.length ?? 0), 0);
  const completedLearners = roster.filter(
    (l) => l.exercises.filter((e) => e.phase === "completed").length === totalExercises && totalExercises > 0
  ).length;

  const copyLabel =
    copyState === "loading" ? "Copying…" :
    copyState === "copied"  ? "✓ Copied!" :
    copyState === "error"   ? "Copy failed" :
    "Copy invite link";

  return (
    <AppShell userName={me?.display_name}>
      {loading && (
        <div className="empty-state">
          <span className="spinner" style={{ fontSize: "1.5rem" }} />
          <p>Loading cohort data…</p>
        </div>
      )}

      {error && <div className="alert alert-error">{error}</div>}

      {!loading && !error && cohort && (
        <div className="stack" style={{ maxWidth: "72rem" }}>
          <Link href="/facilitator/cohorts" className="text-sm text-muted" style={{ textDecoration: "none" }}>
            ← Back to Cohorts
          </Link>

          {/* Header */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "var(--space-4)", flexWrap: "wrap" }}>
            <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
              <div className="cluster" style={{ gap: "var(--space-3)", alignItems: "center" }}>
                <h1 style={{ margin: 0 }}>{cohort.name}</h1>
                <StatusBadge status={cohort.status} />
              </div>
              {cohort.description && (
                <p className="text-muted" style={{ margin: 0 }}>{cohort.description}</p>
              )}
            </div>
            <div className="cluster" style={{ gap: "var(--space-3)", flexWrap: "wrap" }}>
              {/* F-M-003: Publish button — only when draft */}
              {cohort.status === "draft" && (
                <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: "var(--space-1)" }}>
                  <button
                    className="btn btn-primary"
                    onClick={handlePublish}
                    disabled={publishing}
                  >
                    {publishing ? <><span className="spinner" aria-hidden="true" /> Publishing…</> : "Publish cohort"}
                  </button>
                  {publishError && (
                    <span className="text-sm" style={{ color: "var(--color-error, #dc2626)" }}>{publishError}</span>
                  )}
                </div>
              )}
              {/* F-M-004: Edit button */}
              {!showEditForm && (
                <button className="btn btn-secondary" onClick={() => setShowEditForm(true)}>
                  Edit
                </button>
              )}
              <Link href={`/cohorts/${cohortId}`} className="btn btn-secondary">
                ← Learner view
              </Link>
            </div>
          </div>

          {/* F-M-004: Inline edit form */}
          {showEditForm && (
            <EditCohortForm
              cohort={cohort}
              onSaved={(updated) => { setCohort(updated); setShowEditForm(false); }}
              onCancel={() => setShowEditForm(false)}
            />
          )}

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
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "var(--space-6)", gap: "var(--space-4)", flexWrap: "wrap" }}>
              <h2 style={{ margin: 0 }}>Learner roster</h2>
              {/* F-M-002: Copy invite link — always visible in roster header */}
              <button
                className="btn btn-secondary"
                onClick={handleCopyInviteLink}
                disabled={copyState === "loading"}
                style={copyState === "copied" ? { color: "var(--color-success, #065f46)" } : undefined}
              >
                {copyState === "loading" && <span className="spinner" aria-hidden="true" />}
                {copyLabel}
              </button>
            </div>
            {roster.length > 0 ? (
              <CohortRoster learners={roster} exerciseTitles={exerciseTitles} />
            ) : (
              <div className="empty-state">
                <p>No learners enrolled yet.</p>
                <p className="text-sm text-muted" style={{ marginTop: "var(--space-2)" }}>
                  Share the invite link so learners can join this cohort.
                </p>
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

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
    archived: { bg: "#f3f4f6", color: "#6b7280" },
    draft:    { bg: "#f3f4f6", color: "#6b7280" },
    running:  { bg: "var(--color-warning-bg, #fef3c7)", color: "var(--color-warning, #92400e)" },
  };
  const s = styles[status] ?? { bg: "#f3f4f6", color: "#6b7280" };
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
      setError(err instanceof Error ? err.message : "Failed to save group.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="card" style={{ marginTop: "var(--space-4)" }}>
      <h2 style={{ marginBottom: "var(--space-6)" }}>Edit group</h2>
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
        setError("You don't have teacher access to this group.");
      } else {
        setError(err instanceof Error ? err.message : "Failed to load group.");
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
            ← Back to Groups
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
                    {publishing ? <><span className="spinner" aria-hidden="true" /> Publishing…</> : "Publish group"}
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
                Student view →
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

          {/* Summary stats — A7: color only when value > 0 */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(10rem, 1fr))", gap: "var(--space-4)" }}>
            {(() => {
              const exploring = roster.filter((l) => l.exercises.some((e) => e.phase === "exploring")).length;
              const needsAttention = roster.filter((l) => l.exercises.some((e) => e.latest_signal === "low_effort" || e.latest_signal === "off_task")).length;
              return (
                <>
                  <div className="card" style={{ textAlign: "center" }}>
                    <div style={{ fontSize: "var(--font-size-3xl)", fontWeight: "var(--font-weight-bold)", color: roster.length > 0 ? "var(--color-brand-primary)" : "var(--color-text-muted)" }}>
                      {roster.length}
                    </div>
                    <div className="text-sm text-muted">Enrolled</div>
                  </div>
                  <div className="card" style={{ textAlign: "center" }}>
                    <div style={{ fontSize: "var(--font-size-3xl)", fontWeight: "var(--font-weight-bold)", color: exploring > 0 ? "var(--color-phase-exploring-text)" : "var(--color-text-muted)" }}>
                      {exploring}
                    </div>
                    <div className="text-sm text-muted">Exploring</div>
                  </div>
                  <div className="card" style={{ textAlign: "center" }}>
                    <div style={{ fontSize: "var(--font-size-3xl)", fontWeight: "var(--font-weight-bold)", color: completedLearners > 0 ? "var(--color-success)" : "var(--color-text-muted)" }}>
                      {completedLearners}
                    </div>
                    <div className="text-sm text-muted">All exercises done</div>
                  </div>
                  <div className="card" style={{ textAlign: "center" }}>
                    <div style={{ fontSize: "var(--font-size-3xl)", fontWeight: "var(--font-weight-bold)", color: needsAttention > 0 ? "var(--color-warning)" : "var(--color-text-muted)" }}>
                      {needsAttention}
                    </div>
                    <div className="text-sm text-muted">Needs attention</div>
                  </div>
                </>
              );
            })()}
          </div>

          {/* Roster table — A6: signal legend moved above roster */}
          <div className="card" style={{ padding: "var(--space-6)", overflow: "hidden" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "var(--space-4)", gap: "var(--space-4)", flexWrap: "wrap" }}>
              <h2 style={{ margin: 0 }}>Student roster</h2>
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

            {/* Signal legend inline with roster header — A6 */}
            <div style={{ display: "flex", gap: "var(--space-4)", flexWrap: "wrap", alignItems: "center", marginBottom: "var(--space-6)", padding: "var(--space-3) var(--space-4)", background: "var(--color-bg-surface-raised)", borderRadius: "var(--radius-md)", fontSize: "var(--font-size-xs)", color: "var(--color-text-secondary)" }}>
              <span style={{ fontWeight: "var(--font-weight-medium)" }}>Signal:</span>
              <span style={{ display: "inline-flex", alignItems: "center", gap: "var(--space-2)" }}>
                <span className="badge" style={{ background: "var(--color-signal-productive-bg)", color: "var(--color-signal-productive-text)" }}>Productive</span>
                counts toward gate
              </span>
              <span style={{ display: "inline-flex", alignItems: "center", gap: "var(--space-2)" }}>
                <span className="badge" style={{ background: "var(--color-signal-low-effort-bg)", color: "var(--color-signal-low-effort-text)" }}>Low effort</span>
                does not count
              </span>
              <span style={{ display: "inline-flex", alignItems: "center", gap: "var(--space-2)" }}>
                <span className="badge" style={{ background: "var(--color-signal-off-task-bg)", color: "var(--color-signal-off-task-text)" }}>Off-task</span>
                not addressing problem
              </span>
              <span style={{ display: "inline-flex", alignItems: "center", gap: "var(--space-2)" }}>
                <span className="badge" style={{ background: "var(--color-warning-bg)", color: "var(--color-warning)" }} title="Student passed on first attempt — Productive Failure process was bypassed">Fast-unlocked</span>
                PF bypassed
              </span>
            </div>

            {roster.length > 0 ? (
              <CohortRoster cohortId={cohortId} learners={roster} exerciseTitles={exerciseTitles} />
            ) : (
              <div className="empty-state">
                <p>No students enrolled yet.</p>
                <p className="text-sm text-muted" style={{ marginTop: "var(--space-2)" }}>
                  Share the invite link so students can join this group.
                </p>
              </div>
            )}
          </div>

          <p className="text-xs text-muted">
            Facilitator gate overrides are available on each student&apos;s individual exercise view.
            All overrides are recorded for grant audit purposes.
          </p>
        </div>
      )}
    </AppShell>
  );
}

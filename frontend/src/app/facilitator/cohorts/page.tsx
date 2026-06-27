"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  getCohorts,
  createCohort,
  updateCohort,
  deleteCohort,
  getMe,
  ApiClientError,
} from "@/lib/api-client";
import type { CohortSummary, CohortDetail, Me } from "@/lib/api-types";
import { AppShell } from "@/components/layout/AppShell";

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

function CreateCohortForm({ onCreated, onCancel }: { onCreated: (c: CohortDetail) => void; onCancel: () => void }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [startDate, setStartDate] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const cohort = await createCohort({
        name: name.trim(),
        description: description.trim() || undefined,
        start_date: startDate || undefined,
      });
      onCreated(cohort);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create group.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="card" style={{ marginTop: "var(--space-4)" }}>
      <h2 style={{ marginBottom: "var(--space-6)" }}>New group</h2>
      <form onSubmit={handleSubmit} className="stack">
        <div className="form-group">
          <label className="form-label" htmlFor="cohort-name">Name <span aria-hidden="true">*</span></label>
          <input id="cohort-name" type="text" className="form-input" value={name}
            onChange={(e) => setName(e.target.value)} required
            placeholder="e.g. Group A — Q3 2026" disabled={submitting} />
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="cohort-description">Description <span className="text-muted">(optional)</span></label>
          <input id="cohort-description" type="text" className="form-input" value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Brief description of this group" disabled={submitting} />
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="cohort-start-date">Start date <span className="text-muted">(optional)</span></label>
          <input id="cohort-start-date" type="date" className="form-input" value={startDate}
            onChange={(e) => setStartDate(e.target.value)} disabled={submitting} />
        </div>
        {error && <div className="alert alert-error text-sm">{error}</div>}
        <div className="cluster" style={{ gap: "var(--space-3)", justifyContent: "flex-end" }}>
          <button type="button" className="btn btn-secondary" onClick={onCancel} disabled={submitting}>Cancel</button>
          <button type="submit" className="btn btn-primary" disabled={submitting || !name.trim()}>
            {submitting ? <><span className="spinner" aria-hidden="true" /> Creating…</> : "Create group"}
          </button>
        </div>
      </form>
    </div>
  );
}

function CohortRow({
  cohort,
  onArchive,
  onDelete,
}: {
  cohort: CohortSummary;
  onArchive: (id: string) => Promise<void>;
  onDelete: (id: string, force?: boolean) => Promise<void>;
}) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [confirmForce, setConfirmForce] = useState(false);
  const [busy, setBusy] = useState(false);
  const [rowError, setRowError] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!menuOpen) return;
    function handler(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [menuOpen]);

  async function handleArchive() {
    setMenuOpen(false);
    setBusy(true);
    setRowError(null);
    try {
      await onArchive(cohort.id);
    } catch (err) {
      setRowError(err instanceof Error ? err.message : "Archive failed.");
    } finally {
      setBusy(false);
    }
  }

  async function handleDelete(force = false) {
    setBusy(true);
    setRowError(null);
    try {
      await onDelete(cohort.id, force);
    } catch (err) {
      if (err instanceof ApiClientError && err.status === 409) {
        setConfirmForce(true);
        setRowError(null);
      } else {
        setRowError(err instanceof Error ? err.message : "Delete failed.");
      }
      setBusy(false);
    }
  }

  if (confirmForce) {
    return (
      <div className="card" style={{ borderColor: "var(--color-error, #dc2626)" }}>
        <p style={{ fontWeight: "var(--font-weight-medium)", marginBottom: "var(--space-3)" }}>
          This group has active students.
        </p>
        <p className="text-sm text-muted" style={{ marginBottom: "var(--space-4)" }}>
          Deleting will remove all enrolled students and their progress data. This cannot be undone.
        </p>
        {rowError && <div className="alert alert-error text-sm" style={{ marginBottom: "var(--space-3)" }}>{rowError}</div>}
        <div className="cluster" style={{ gap: "var(--space-3)" }}>
          <button
            className="btn btn-primary"
            style={{ background: "var(--color-error, #dc2626)", borderColor: "var(--color-error, #dc2626)" }}
            onClick={() => handleDelete(true)}
            disabled={busy}
          >
            {busy ? <><span className="spinner" aria-hidden="true" /> Deleting…</> : "Delete anyway"}
          </button>
          <button className="btn btn-secondary" onClick={() => { setConfirmForce(false); setConfirmDelete(false); setRowError(null); }} disabled={busy}>
            Cancel
          </button>
        </div>
      </div>
    );
  }

  if (confirmDelete) {
    return (
      <div className="card" style={{ borderColor: "var(--color-error, #dc2626)" }}>
        <p style={{ fontWeight: "var(--font-weight-medium)", marginBottom: "var(--space-3)" }}>
          Delete <strong>{cohort.name}</strong>?
        </p>
        <p className="text-sm text-muted" style={{ marginBottom: "var(--space-4)" }}>
          Delete this group and all student data? This cannot be undone.
        </p>
        {rowError && <div className="alert alert-error text-sm" style={{ marginBottom: "var(--space-3)" }}>{rowError}</div>}
        <div className="cluster" style={{ gap: "var(--space-3)" }}>
          <button
            className="btn btn-primary"
            style={{ background: "var(--color-error, #dc2626)", borderColor: "var(--color-error, #dc2626)" }}
            onClick={() => handleDelete(false)}
            disabled={busy}
          >
            {busy ? <><span className="spinner" aria-hidden="true" /> Deleting…</> : "Delete"}
          </button>
          <button className="btn btn-secondary" onClick={() => { setConfirmDelete(false); setRowError(null); }} disabled={busy}>
            Cancel
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="card" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "var(--space-4)", position: "relative" }}>
      <Link
        href={`/facilitator/cohorts/${cohort.id}`}
        style={{ textDecoration: "none", display: "flex", alignItems: "center", gap: "var(--space-3)", flex: 1, minWidth: 0 }}
      >
        <StatusBadge status={cohort.status} />
        <span style={{ fontWeight: "var(--font-weight-medium)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {cohort.name}
        </span>
      </Link>

      <div style={{ display: "flex", alignItems: "center", gap: "var(--space-4)", flexShrink: 0 }}>
        <span className="text-sm text-muted">
          {cohort.learner_count} student{cohort.learner_count !== 1 ? "s" : ""}
        </span>
        <Link href={`/facilitator/cohorts/${cohort.id}`} className="text-muted" aria-hidden="true" style={{ textDecoration: "none" }}>→</Link>

        {/* Kebab menu */}
        <div ref={menuRef} style={{ position: "relative" }}>
          <button
            className="btn btn-secondary btn-sm"
            style={{ padding: "0 var(--space-2)", minWidth: "2rem" }}
            onClick={(e) => { e.preventDefault(); setMenuOpen((o) => !o); }}
            aria-label="Group actions"
            disabled={busy}
          >
            {busy ? <span className="spinner" aria-hidden="true" style={{ fontSize: "0.75rem" }} /> : "…"}
          </button>
          {menuOpen && (
            <div
              style={{
                position: "absolute",
                right: 0,
                top: "calc(100% + var(--space-1))",
                background: "var(--color-bg-surface)",
                border: "1px solid var(--color-border)",
                borderRadius: "var(--radius-md)",
                boxShadow: "0 4px 12px rgba(0,0,0,0.12)",
                zIndex: 10,
                minWidth: "9rem",
                overflow: "hidden",
              }}
            >
              <button
                style={{ display: "block", width: "100%", textAlign: "left", padding: "var(--space-3) var(--space-4)", background: "none", border: "none", cursor: "pointer", fontSize: "var(--font-size-sm)" }}
                onClick={handleArchive}
              >
                Archive
              </button>
              <button
                style={{ display: "block", width: "100%", textAlign: "left", padding: "var(--space-3) var(--space-4)", background: "none", border: "none", cursor: "pointer", fontSize: "var(--font-size-sm)", color: "var(--color-error, #dc2626)" }}
                onClick={() => { setMenuOpen(false); setConfirmDelete(true); }}
              >
                Delete
              </button>
            </div>
          )}
        </div>
      </div>

      {rowError && !confirmDelete && (
        <div className="alert alert-error text-sm" style={{ position: "absolute", bottom: "calc(100% + var(--space-1))", left: 0, right: 0 }}>
          {rowError}
        </div>
      )}
    </div>
  );
}

export default function FacilitatorCohortsPage() {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);
  const [cohorts, setCohorts] = useState<CohortSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showArchived, setShowArchived] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const [meData, cohortsData] = await Promise.all([getMe(), getCohorts()]);
        setMe(meData);
        setCohorts(cohortsData);
      } catch (err) {
        if (err instanceof ApiClientError && err.status === 401) {
          router.replace("/login");
        } else {
          setError(err instanceof Error ? err.message : "Failed to load groups.");
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  function handleCohortCreated(newCohort: CohortDetail) {
    const summary: CohortSummary = {
      id: newCohort.id,
      name: newCohort.name,
      status: newCohort.status,
      learner_count: newCohort.enrollment_count,
    };
    setCohorts((prev) => [summary, ...prev]);
    setShowCreateForm(false);
  }

  async function handleArchive(id: string) {
    const updated = await updateCohort(id, { status: "archived" });
    setCohorts((prev) =>
      prev.map((c) => (c.id === id ? { ...c, status: updated.status } : c))
    );
  }

  async function handleDelete(id: string, force = false) {
    await deleteCohort(id, force);
    setCohorts((prev) => prev.filter((c) => c.id !== id));
  }

  const activeGroups = cohorts.filter((c) => c.status !== "archived");
  const archivedGroups = cohorts.filter((c) => c.status === "archived");

  return (
    <AppShell userName={me?.display_name}>
      {loading && (
        <div className="empty-state">
          <span className="spinner" style={{ fontSize: "1.5rem" }} />
          <p>Loading groups…</p>
        </div>
      )}

      {error && <div className="alert alert-error">{error}</div>}

      {!loading && !error && (
        <div className="stack" style={{ maxWidth: "48rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "var(--space-4)", flexWrap: "wrap" }}>
            <div>
              <h1>Groups</h1>
              <p className="text-muted" style={{ marginTop: "var(--space-2)" }}>
                Select a group to view student progress and manage gate overrides.
              </p>
            </div>
            {!showCreateForm && (
              <button className="btn btn-primary" onClick={() => setShowCreateForm(true)}>
                + Create group
              </button>
            )}
          </div>

          {showCreateForm && (
            <CreateCohortForm
              onCreated={handleCohortCreated}
              onCancel={() => setShowCreateForm(false)}
            />
          )}

          {activeGroups.length === 0 && !showCreateForm ? (
            <div className="empty-state">
              <p>No groups yet.</p>
            </div>
          ) : (
            <div className="stack">
              {activeGroups.map((cohort) => (
                <CohortRow
                  key={cohort.id}
                  cohort={cohort}
                  onArchive={handleArchive}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          )}

          {/* Archived section */}
          {archivedGroups.length > 0 && (
            <div>
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => setShowArchived((s) => !s)}
                style={{ marginBottom: "var(--space-3)" }}
              >
                {showArchived ? "Hide" : "Show"} archived ({archivedGroups.length})
              </button>
              {showArchived && (
                <div className="stack">
                  {archivedGroups.map((cohort) => (
                    <div
                      key={cohort.id}
                      className="card"
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        gap: "var(--space-4)",
                        opacity: 0.5,
                      }}
                    >
                      <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)" }}>
                        <StatusBadge status={cohort.status} />
                        <span style={{ fontWeight: "var(--font-weight-medium)" }}>{cohort.name}</span>
                      </div>
                      <span className="text-sm text-muted">
                        {cohort.learner_count} student{cohort.learner_count !== 1 ? "s" : ""}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </AppShell>
  );
}

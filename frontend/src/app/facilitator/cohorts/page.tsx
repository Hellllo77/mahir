"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getCohorts, createCohort, getMe, ApiClientError } from "@/lib/api-client";
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
    <span
      className="badge"
      style={{ background: s.bg, color: s.color, textTransform: "capitalize" }}
    >
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
          <input
            id="cohort-name"
            type="text"
            className="form-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            placeholder="e.g. Group A — Q3 2026"
            disabled={submitting}
          />
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="cohort-description">Description <span className="text-muted">(optional)</span></label>
          <input
            id="cohort-description"
            type="text"
            className="form-input"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Brief description of this group"
            disabled={submitting}
          />
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="cohort-start-date">Start date <span className="text-muted">(optional)</span></label>
          <input
            id="cohort-start-date"
            type="date"
            className="form-input"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            disabled={submitting}
          />
        </div>

        {error && <div className="alert alert-error text-sm">{error}</div>}

        <div className="cluster" style={{ gap: "var(--space-3)", justifyContent: "flex-end" }}>
          <button type="button" className="btn btn-secondary" onClick={onCancel} disabled={submitting}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={submitting || !name.trim()}>
            {submitting ? (
              <><span className="spinner" aria-hidden="true" /> Creating…</>
            ) : (
              "Create group"
            )}
          </button>
        </div>
      </form>
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

          {cohorts.length === 0 && !showCreateForm ? (
            <div className="empty-state">
              <p>No groups yet.</p>
            </div>
          ) : (
            <div className="stack">
              {cohorts.map((cohort) => (
                <Link
                  key={cohort.id}
                  href={`/facilitator/cohorts/${cohort.id}`}
                  style={{ textDecoration: "none" }}
                >
                  <div
                    className="card"
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      gap: "var(--space-4)",
                      cursor: "pointer",
                    }}
                  >
                    <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)" }}>
                      <StatusBadge status={cohort.status} />
                      <span style={{ fontWeight: "var(--font-weight-medium)" }}>{cohort.name}</span>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: "var(--space-6)" }}>
                      <span className="text-sm text-muted">
                        {cohort.learner_count} student{cohort.learner_count !== 1 ? "s" : ""}
                      </span>
                      <span className="text-muted" aria-hidden="true">→</span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      )}
    </AppShell>
  );
}

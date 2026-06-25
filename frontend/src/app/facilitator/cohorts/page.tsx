"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getCohorts, getMe, ApiClientError } from "@/lib/api-client";
import type { CohortSummary, Me } from "@/lib/api-types";
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

export default function FacilitatorCohortsPage() {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);
  const [cohorts, setCohorts] = useState<CohortSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
          setError(err instanceof Error ? err.message : "Failed to load cohorts.");
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  return (
    <AppShell userName={me?.display_name}>
      {loading && (
        <div className="empty-state">
          <span className="spinner" style={{ fontSize: "1.5rem" }} />
          <p>Loading cohorts…</p>
        </div>
      )}

      {error && <div className="alert alert-error">{error}</div>}

      {!loading && !error && (
        <div className="stack" style={{ maxWidth: "48rem" }}>
          <div>
            <h1>Cohorts</h1>
            <p className="text-muted" style={{ marginTop: "var(--space-2)" }}>
              Select a cohort to view learner progress and manage gate overrides.
            </p>
          </div>

          {cohorts.length === 0 ? (
            <div className="empty-state">
              <p>No cohorts yet.</p>
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
                        {cohort.learner_count} learner{cohort.learner_count !== 1 ? "s" : ""}
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

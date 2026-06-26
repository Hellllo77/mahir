"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getMe, ApiClientError } from "@/lib/api-client";
import type { Me } from "@/lib/api-types";
import { AppShell } from "@/components/layout/AppShell";

export default function DashboardPage() {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
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
        const activeEnrolment = meData.enrolments.find((en) => en.status === "active");
        if (activeEnrolment) {
          router.replace(`/cohorts/${activeEnrolment.cohort_id}`);
          return;
        }
        setMe(meData);
      } catch (err) {
        if (err instanceof ApiClientError && err.status === 401) {
          router.replace("/login");
        } else {
          router.replace("/login");
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  if (loading || !me) return null;

  return (
    <AppShell userName={me.display_name}>
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
            No Active Course
          </h2>
          <p className="text-sm text-muted">
            You haven&apos;t joined a group yet. Ask your teacher for an invite link to get started.
          </p>
        </div>
      </div>
    </AppShell>
  );
}

"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { getRole } from "@/lib/api-client";

interface Props {
  sidebar?: React.ReactNode;
  children: React.ReactNode;
  userName?: string;
  isFacilitator?: boolean;
  cohortId?: string;
}

function getLogoHref(): string {
  if (typeof window === "undefined") return "/";
  const token = localStorage.getItem("mahir_token");
  if (!token) return "/";
  const role = getRole();
  const isStaff = role === "org_admin" || role === "super_admin" || role === "facilitator";
  return isStaff ? "/facilitator/cohorts" : "/dashboard";
}

function isStaffRole(): boolean {
  if (typeof window === "undefined") return false;
  const role = getRole();
  return role === "org_admin" || role === "super_admin" || role === "facilitator";
}

export function AppShell({ sidebar, children, userName, isFacilitator, cohortId }: Props) {
  const [logoHref, setLogoHref] = useState("/");
  const [showCohortsNav, setShowCohortsNav] = useState(false);

  useEffect(() => {
    setLogoHref(getLogoHref());
    setShowCohortsNav(isStaffRole());
  }, []);

  return (
    <div className={sidebar ? "app-shell" : undefined} style={!sidebar ? { minHeight: "100vh", display: "flex", flexDirection: "column" } : undefined}>
      <header className="app-header">
        <Link
          href={logoHref}
          style={{
            fontWeight: "var(--font-weight-bold)",
            fontSize: "var(--font-size-xl)",
            color: "var(--color-brand-primary)",
            textDecoration: "none",
          }}
        >
          Mahir
        </Link>
        <span className="text-xs text-muted" style={{ marginLeft: "var(--space-1)" }}>
          Co-Worker
        </span>

        {showCohortsNav && (
          <nav style={{ marginLeft: "var(--space-6)" }}>
            <Link href="/facilitator/cohorts" className="text-sm text-muted" style={{ textDecoration: "none" }}>
              Cohorts
            </Link>
          </nav>
        )}

        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: "var(--space-4)" }}>
          {isFacilitator && cohortId && (
            <Link href={`/facilitator/cohorts/${cohortId}`} className="text-sm text-muted">
              Cohort view
            </Link>
          )}
          {userName && (
            <span className="text-sm text-muted">{userName}</span>
          )}
          <Link href="/logout" className="btn btn-secondary btn-sm">
            Sign out
          </Link>
        </div>
      </header>

      {sidebar && (
        <aside className="app-sidebar">
          {sidebar}
        </aside>
      )}

      <main className={sidebar ? "app-main" : undefined} style={!sidebar ? { flex: 1, padding: "var(--space-8) var(--space-6)" } : undefined}>
        {children}
      </main>
    </div>
  );
}

"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { getRole, saveRole, getMe } from "@/lib/api-client";

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
    if (getRole()) {
      setLogoHref(getLogoHref());
      setShowCohortsNav(isStaffRole());
    } else if (typeof window !== "undefined" && localStorage.getItem("mahir_token")) {
      // Role not cached (old session pre-saveRole) — fetch and cache it
      getMe().then((me) => {
        saveRole(me.global_role);
        const isStaff = me.global_role === "org_admin" || me.global_role === "super_admin" || me.global_role === "facilitator";
        setShowCohortsNav(isStaff);
        setLogoHref(isStaff ? "/facilitator/cohorts" : "/dashboard");
      }).catch(() => {/* token invalid — leave nav hidden, sign-out will redirect */});
    }
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
        <span className="text-xs text-muted header-subtitle" style={{ marginLeft: "var(--space-1)" }}>
          Co-Worker
        </span>

        {showCohortsNav && (
          <nav style={{ marginLeft: "var(--space-6)" }}>
            <Link href="/facilitator/cohorts" className="text-sm text-muted" style={{ textDecoration: "none" }}>
              Groups
            </Link>
          </nav>
        )}

        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: "var(--space-4)" }}>
          {isFacilitator && cohortId && (
            <Link href={`/facilitator/cohorts/${cohortId}`} className="text-sm text-muted">
              Group view
            </Link>
          )}
          {userName && (
            <span className="text-sm text-muted">{userName}</span>
          )}
          <Link href="/logout" className="btn btn-secondary btn-sm" style={{ whiteSpace: "nowrap" }}>
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

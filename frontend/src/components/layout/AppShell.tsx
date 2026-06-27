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

function isAdminRole(): boolean {
  if (typeof window === "undefined") return false;
  const role = getRole();
  return role === "org_admin" || role === "super_admin";
}

export function AppShell({ sidebar, children, userName, isFacilitator, cohortId }: Props) {
  const [logoHref, setLogoHref] = useState("/");
  const [showCohortsNav, setShowCohortsNav] = useState(false);
  const [showAdminNav, setShowAdminNav] = useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  useEffect(() => {
    if (getRole()) {
      setLogoHref(getLogoHref());
      setShowCohortsNav(isStaffRole());
      setShowAdminNav(isAdminRole());
    } else if (typeof window !== "undefined" && localStorage.getItem("mahir_token")) {
      getMe().then((me) => {
        saveRole(me.global_role);
        const isStaff = me.global_role === "org_admin" || me.global_role === "super_admin" || me.global_role === "facilitator";
        const isAdmin = me.global_role === "org_admin" || me.global_role === "super_admin";
        setShowCohortsNav(isStaff);
        setShowAdminNav(isAdmin);
        setLogoHref(isStaff ? "/facilitator/cohorts" : "/dashboard");
      }).catch(() => {});
    }
  }, []);

  return (
    <div className={sidebar ? "app-shell" : undefined} style={!sidebar ? { minHeight: "100vh", display: "flex", flexDirection: "column" } : undefined}>
      <header className="app-header">
        {/* Mobile hamburger — only when sidebar exists */}
        {sidebar && (
          <button
            className="mobile-menu-btn"
            onClick={() => setMobileSidebarOpen((o) => !o)}
            aria-label="Toggle navigation"
            aria-expanded={mobileSidebarOpen}
          >
            {mobileSidebarOpen ? "✕" : "☰"}
          </button>
        )}

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
          <nav style={{ marginLeft: "var(--space-6)", display: "flex", gap: "var(--space-5)", alignItems: "center" }}>
            <Link href="/facilitator/cohorts" className="text-sm text-muted" style={{ textDecoration: "none" }}>
              Groups
            </Link>
            {showAdminNav && (
              <Link href="/admin/settings" className="text-sm text-muted" style={{ textDecoration: "none" }}>
                Settings
              </Link>
            )}
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
        <aside className={`app-sidebar${mobileSidebarOpen ? " mobile-open" : ""}`}>
          {sidebar}
        </aside>
      )}

      <main
        className={sidebar ? "app-main" : undefined}
        style={!sidebar ? { flex: 1, padding: "var(--space-8) var(--space-6)" } : undefined}
        onClick={() => { if (mobileSidebarOpen) setMobileSidebarOpen(false); }}
      >
        {children}
      </main>
    </div>
  );
}

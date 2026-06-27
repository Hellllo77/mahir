"use client";

import Link from "next/link";
import { AppShell } from "@/components/layout/AppShell";

export default function NotFound() {
  return (
    <AppShell>
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
          <h1
            style={{
              fontSize: "var(--font-size-3xl)",
              color: "var(--color-text-muted)",
              marginBottom: "var(--space-3)",
            }}
          >
            404
          </h1>
          <h2 style={{ marginBottom: "var(--space-3)" }}>Page not found</h2>
          <p className="text-sm text-muted" style={{ marginBottom: "var(--space-6)" }}>
            This page doesn&apos;t exist or you don&apos;t have access to it.
          </p>
          <Link href="/dashboard" className="btn btn-primary">
            ← Back to your learning path
          </Link>
        </div>
      </div>
    </AppShell>
  );
}

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login, saveToken, saveRole, getMe } from "@/lib/api-client";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const { access_token } = await login(email, password);
      saveToken(access_token);
      const me = await getMe();
      saveRole(me.global_role);
      const isStaff = me.global_role === "org_admin" || me.global_role === "super_admin" || me.global_role === "facilitator";
      if (isStaff) {
        router.push("/facilitator/cohorts");
      } else {
        const activeEnrolment = me.enrolments.find((en) => en.status === "active");
        if (activeEnrolment) {
          router.push(`/cohorts/${activeEnrolment.cohort_id}`);
        } else {
          router.push("/dashboard");
        }
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Login failed. Check your credentials.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--color-bg-base)",
      }}
    >
      <div style={{ width: "100%", maxWidth: "24rem", padding: "var(--space-4)" }}>
        <div className="card">
          <div style={{ textAlign: "center", marginBottom: "var(--space-8)" }}>
            <h1 style={{ color: "var(--color-brand-primary)", marginBottom: "var(--space-2)" }}>
              Mahir
            </h1>
            <p className="text-sm text-muted">AI Agent Training — Co-Worker Edition</p>
          </div>

          <form onSubmit={handleSubmit} className="stack">
            <div className="form-group">
              <label className="form-label" htmlFor="email">Work email</label>
              <input
                id="email"
                type="email"
                className="form-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="username"
                placeholder="you@company.com"
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                className="form-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
                disabled={loading}
              />
            </div>

            {error && <div className="alert alert-error text-sm">{error}</div>}

            <button type="submit" className="btn btn-primary btn-lg" disabled={loading} style={{ width: "100%" }}>
              {loading ? (
                <>
                  <span className="spinner" aria-hidden="true" />
                  Signing in…
                </>
              ) : (
                "Sign in"
              )}
            </button>
          </form>

        </div>
      </div>
    </div>
  );
}

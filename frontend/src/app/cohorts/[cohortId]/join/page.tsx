"use client";

import { useEffect, useState } from "react";
import { useParams, useSearchParams, useRouter } from "next/navigation";
import { enrolWithToken, saveToken, saveRole, getMe, ApiClientError } from "@/lib/api-client";

export default function JoinPage() {
  const { cohortId } = useParams<{ cohortId: string }>();
  const searchParams = useSearchParams();
  const router = useRouter();

  const token = searchParams.get("token") ?? "";

  const [email, setEmail] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [checking, setChecking] = useState(true);

  // If already logged in and enrolled in this cohort, skip to dashboard.
  useEffect(() => {
    if (!token) {
      setError("This invite link is missing a token. Please ask your teacher for a valid link.");
      setChecking(false);
      return;
    }
    const stored = typeof window !== "undefined" ? localStorage.getItem("mahir_token") : null;
    if (!stored) { setChecking(false); return; }
    getMe()
      .then((me) => {
        const enrolled = me.enrolments.some(
          (e) => e.cohort_id === cohortId && e.status === "active"
        );
        if (enrolled) router.replace("/dashboard");
        else setChecking(false);
      })
      .catch(() => setChecking(false));
  }, [cohortId, token, router]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const res = await enrolWithToken(cohortId, token, {
        email: email.trim(),
        display_name: displayName.trim() || undefined,
        password: password || undefined,
      });
      saveToken(res.access_token);
      saveRole("learner");
      router.replace("/dashboard");
    } catch (err) {
      if (err instanceof ApiClientError) {
        if (err.status === 401) {
          setError("This invite link has expired or is no longer valid. Ask your teacher for a new one.");
        } else if (err.status === 403) {
          setError("This group isn't open for joining yet. Check with your teacher.");
        } else if (err.status === 409) {
          setError("You are already enrolled in this group. Sign in to continue.");
        } else if (err.status === 400) {
          setError("Please fill in your name and choose a password to create your account.");
        } else {
          setError("Something went wrong. Please try again.");
        }
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  if (checking) return null;

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "var(--space-6)",
        background: "var(--color-bg, #f9fafb)",
      }}
    >
      <div style={{ width: "100%", maxWidth: "24rem" }}>
        <div style={{ textAlign: "center", marginBottom: "var(--space-8)" }}>
          <span
            style={{
              fontWeight: "var(--font-weight-bold)",
              fontSize: "var(--font-size-xl)",
              color: "var(--color-brand-primary)",
            }}
          >
            Mahir
          </span>
        </div>

        <div className="card">
          <h1
            style={{
              fontSize: "var(--font-size-xl)",
              fontWeight: "var(--font-weight-semibold)",
              marginBottom: "var(--space-2)",
            }}
          >
            Join your group
          </h1>
          <p className="text-sm text-muted" style={{ marginBottom: "var(--space-6)" }}>
            Enter your details to get started. If you already have an account, just enter your email.
          </p>

          {!token ? (
            <div className="alert alert-error">{error}</div>
          ) : (
            <form onSubmit={handleSubmit} className="stack">
              <div className="form-group">
                <label className="form-label" htmlFor="join-email">
                  Email <span aria-hidden="true">*</span>
                </label>
                <input
                  id="join-email"
                  type="email"
                  className="form-input"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  autoComplete="email"
                  placeholder="you@example.com"
                  disabled={submitting}
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="join-name">
                  Your name <span className="text-muted">(new accounts only)</span>
                </label>
                <input
                  id="join-name"
                  type="text"
                  className="form-input"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  autoComplete="name"
                  placeholder="First Last"
                  disabled={submitting}
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="join-password">
                  Password <span className="text-muted">(new accounts only)</span>
                </label>
                <input
                  id="join-password"
                  type="password"
                  className="form-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="new-password"
                  placeholder="Choose a password"
                  disabled={submitting}
                />
              </div>

              {error && <div className="alert alert-error text-sm">{error}</div>}

              <button
                type="submit"
                className="btn btn-primary"
                disabled={submitting || !email.trim()}
                style={{ width: "100%" }}
              >
                {submitting ? (
                  <><span className="spinner" aria-hidden="true" /> Joining…</>
                ) : (
                  "Join group"
                )}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

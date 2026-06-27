"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getAdminSettings, updateAdminSettings, getMe, ApiClientError } from "@/lib/api-client";
import type { AdminSettings, Me } from "@/lib/api-types";
import { AppShell } from "@/components/layout/AppShell";

export default function AdminSettingsPage() {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);
  const [settings, setSettings] = useState<AdminSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Edit state
  const [editing, setEditing] = useState(false);
  const [draftKey, setDraftKey] = useState("");
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const [meData, settingsData] = await Promise.all([getMe(), getAdminSettings()]);
        if (meData.global_role !== "org_admin" && meData.global_role !== "super_admin") {
          router.replace("/dashboard");
          return;
        }
        setMe(meData);
        setSettings(settingsData);
      } catch (err) {
        if (err instanceof ApiClientError && err.status === 401) {
          router.replace("/login");
        } else if (err instanceof ApiClientError && err.status === 403) {
          router.replace("/dashboard");
        } else {
          setError(err instanceof Error ? err.message : "Failed to load settings.");
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  function startEdit() {
    setDraftKey("");
    setSaveError(null);
    setSaveSuccess(false);
    setEditing(true);
  }

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setSaveError(null);
    setSaveSuccess(false);
    setSaving(true);
    try {
      const updated = await updateAdminSettings({ resend_api_key: draftKey.trim() });
      if (updated != null) {
        setSettings(updated);
      } else {
        // PUT returned 204 or non-JSON 200 — re-fetch to stay current
        try { setSettings(await getAdminSettings()); } catch { /* best-effort */ }
      }
      setEditing(false);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 5000);
    } catch (err) {
      setSaveError(err instanceof Error ? err.message : "Failed to save.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <AppShell userName={me?.display_name}>
      {loading && (
        <div className="empty-state">
          <span className="spinner" style={{ fontSize: "1.5rem" }} />
          <p>Loading settings…</p>
        </div>
      )}

      {error && <div className="alert alert-error">{error}</div>}

      {saveSuccess && (
        <div
          style={{
            position: "fixed",
            top: "1.25rem",
            right: "1.25rem",
            background: "#d1fae5",
            border: "1.5px solid #065f46",
            borderRadius: "8px",
            padding: "12px 20px",
            color: "#065f46",
            fontWeight: 600,
            fontSize: "14px",
            zIndex: 1000,
            boxShadow: "0 4px 12px rgba(0,0,0,0.12)",
          }}
        >
          ✓ Settings saved
        </div>
      )}

      {!loading && !error && settings && (
        <div className="stack" style={{ maxWidth: "36rem" }}>
          <div>
            <h1>Admin Settings</h1>
            <p className="text-muted" style={{ marginTop: "var(--space-2)" }}>
              Organisation-wide configuration.
            </p>
          </div>

          <div className="card">
            <h2 style={{ marginBottom: "var(--space-6)" }}>Email</h2>

            <div className="stack">
              <div>
                <p className="form-label" style={{ marginBottom: "var(--space-2)" }}>Resend API key</p>
                <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", flexWrap: "wrap" }}>
                  {settings.resend_api_key ? (
                    <span style={{ fontFamily: "var(--font-family-mono)", fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
                      {settings.resend_api_key}
                    </span>
                  ) : (
                    <span className="text-sm text-muted">Not configured — magic-link emails are disabled.</span>
                  )}
                </div>
              </div>

              {!editing ? (
                <button className="btn btn-secondary" onClick={startEdit} style={{ alignSelf: "flex-start" }}>
                  {settings.resend_api_key ? "Update key" : "Add key"}
                </button>
              ) : (
                <form onSubmit={handleSave} className="stack">
                  <div className="form-group">
                    <label className="form-label" htmlFor="resend-key">
                      New API key
                    </label>
                    <input
                      id="resend-key"
                      type="password"
                      className="form-input"
                      value={draftKey}
                      onChange={(e) => setDraftKey(e.target.value)}
                      placeholder="re_xxxxxxxxxxxxxxxx"
                      autoComplete="off"
                      disabled={saving}
                      required
                    />
                    <p className="text-xs text-muted">
                      The key will be masked after saving. Only the first 3 and last 3 characters are shown.
                    </p>
                  </div>
                  {saveError && <div className="alert alert-error text-sm">{saveError}</div>}
                  <div className="cluster" style={{ gap: "var(--space-3)" }}>
                    <button
                      type="submit"
                      className="btn btn-primary"
                      disabled={saving || !draftKey.trim()}
                    >
                      {saving ? <><span className="spinner" aria-hidden="true" /> Saving…</> : "Save"}
                    </button>
                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={() => setEditing(false)}
                      disabled={saving}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              )}
            </div>
          </div>
        </div>
      )}
    </AppShell>
  );
}

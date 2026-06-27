"use client";

import { useState } from "react";
import type { Exercise, SubmissionCreate } from "@/lib/api-types";

interface Props {
  exercise: Exercise;
  moduleExercises: Exercise[];
  onSubmit: (body: SubmissionCreate, idempotencyKey: string) => Promise<void>;
  submitting: boolean;
}

export function AgentBuilder({ exercise, moduleExercises, onSubmit, submitting }: Props) {
  // Map exercise_id → student response text
  const [responses, setResponses] = useState<Record<string, string>>(() =>
    Object.fromEntries(moduleExercises.map((ex) => [ex.id, ""]))
  );
  const [error, setError] = useState<string | null>(null);

  // Use moduleExercises if available; fall back to the single exercise
  const beats = moduleExercises.length > 0 ? moduleExercises : [exercise];

  function setResponse(exerciseId: string, value: string) {
    setResponses((prev) => ({ ...prev, [exerciseId]: value }));
  }

  const allFilled = beats.every((ex) => (responses[ex.id] ?? "").trim().length > 0);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    const beatsPayload = beats.map((ex) => ({
      prompt: ex.prompt_markdown,
      response: (responses[ex.id] ?? "").trim(),
    }));

    // Placeholder payload shape — Felix will confirm correct field name
    const payload = { beats: beatsPayload };

    const key = `${exercise.id}-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    onSubmit({ payload }, key).catch((err: Error) => setError(err.message));
  }

  return (
    <form onSubmit={handleSubmit} className="stack">
      {beats.map((ex, i) => (
        <div key={ex.id} className="stack" style={{ gap: "var(--space-3)" }}>
          {/* Beat label */}
          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)" }}>
            <span
              className="badge"
              style={{
                background: "var(--color-brand-primary)",
                color: "var(--color-text-inverse)",
                flexShrink: 0,
              }}
            >
              {ex.title}
            </span>
          </div>

          {/* Beat prompt as context */}
          {ex.prompt_markdown && (
            <div
              style={{
                background: "var(--color-bg-surface-raised)",
                border: "1px solid var(--color-border)",
                borderRadius: "var(--radius-md)",
                padding: "var(--space-4)",
                fontSize: "var(--font-size-sm)",
                color: "var(--color-text-secondary)",
                lineHeight: "var(--line-height-relaxed)",
                whiteSpace: "pre-wrap",
              }}
            >
              {ex.prompt_markdown}
            </div>
          )}

          {/* Student response textarea */}
          <div className="form-group">
            <label
              className="form-label"
              htmlFor={`beat-response-${ex.id}`}
            >
              Your response
            </label>
            <textarea
              id={`beat-response-${ex.id}`}
              className="form-input"
              rows={5}
              value={responses[ex.id] ?? ""}
              onChange={(e) => setResponse(ex.id, e.target.value)}
              placeholder={`Write your response for ${ex.title}…`}
              disabled={submitting}
              style={{ resize: "vertical" }}
            />
          </div>

          {/* Divider between beats */}
          {i < beats.length - 1 && <hr className="divider" />}
        </div>
      ))}

      {error && <div className="alert alert-error text-sm">{error}</div>}

      <div className="cluster" style={{ justifyContent: "flex-end" }}>
        <button
          type="submit"
          className="btn btn-primary btn-lg"
          disabled={submitting || !allFilled}
        >
          {submitting ? (
            <>
              <span className="spinner" aria-hidden="true" />
              Submitting…
            </>
          ) : (
            "Submit"
          )}
        </button>
      </div>

      <p className="text-xs text-muted">
        Fill in all {beats.length} beat{beats.length !== 1 ? "s" : ""} before submitting.
        Results appear below when ready.
      </p>
    </form>
  );
}

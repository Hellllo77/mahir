"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import type { Exercise, SubmissionCreate } from "@/lib/api-types";

interface Props {
  exercise: Exercise;
  moduleExercises: Exercise[];
  onSubmit: (body: SubmissionCreate, idempotencyKey: string) => Promise<void>;
  submitting: boolean;
}

export function AgentBuilder({ exercise, moduleExercises, onSubmit, submitting }: Props) {
  // Use module exercises sorted by sequence_index; fall back to single exercise
  const beats = (moduleExercises.length > 0 ? moduleExercises : [exercise])
    .slice()
    .sort((a, b) => a.sequence_index - b.sequence_index);

  const [responses, setResponses] = useState<Record<string, string>>(() =>
    Object.fromEntries(beats.map((ex) => [ex.id, ""]))
  );
  const [error, setError] = useState<string | null>(null);

  function setResponse(id: string, value: string) {
    setResponses((prev) => ({ ...prev, [id]: value }));
  }

  const allFilled = beats.every((ex) => (responses[ex.id] ?? "").trim().length > 0);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    const payload: Record<string, unknown> = { schema_version: "beat_responses_1.0" };
    for (const ex of beats) {
      payload[`beat_${ex.sequence_index}`] = (responses[ex.id] ?? "").trim();
    }

    const key = `${exercise.id}-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    onSubmit({ payload, artifact_refs: null }, key).catch((err: Error) => setError(err.message));
  }

  return (
    <form onSubmit={handleSubmit} className="stack">
      {beats.map((ex, i) => (
        <div key={ex.id} className="stack" style={{ gap: "var(--space-3)" }}>
          {/* Beat label */}
          <span
            className="badge"
            style={{
              background: "var(--color-brand-primary)",
              color: "var(--color-text-inverse)",
              alignSelf: "flex-start",
            }}
          >
            {ex.title}
          </span>

          {/* Beat prompt as context — rendered via ReactMarkdown to avoid raw ** or > */}
          {ex.prompt_markdown && (
            <div
              className="prose"
              style={{
                background: "var(--color-bg-surface-raised)",
                border: "1px solid var(--color-border)",
                borderRadius: "var(--radius-md)",
                padding: "var(--space-4)",
                fontSize: "var(--font-size-sm)",
                color: "var(--color-text-secondary)",
              }}
            >
              <ReactMarkdown>{ex.prompt_markdown}</ReactMarkdown>
            </div>
          )}

          {/* Student response textarea */}
          <div className="form-group">
            <label className="form-label" htmlFor={`beat-response-${ex.id}`}>
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

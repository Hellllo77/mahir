"use client";

import { useState } from "react";
import type { Exercise, SubmissionCreate } from "@/lib/api-types";

const MODEL_OPTIONS = [
  { value: "claude-haiku-4-5", label: "Claude Haiku 4.5 (fast)" },
  { value: "claude-sonnet-4-6", label: "Claude Sonnet 4.6 (balanced)" },
];

interface Props {
  exercise: Exercise;
  onSubmit: (body: SubmissionCreate, idempotencyKey: string) => Promise<void>;
  submitting: boolean;
}

export function AgentBuilder({ exercise, onSubmit, submitting }: Props) {
  const [systemPrompt, setSystemPrompt] = useState("");
  const [userPromptTemplate, setUserPromptTemplate] = useState("");
  const [model, setModel] = useState(MODEL_OPTIONS[0].value);
  const [showBeatPrompt, setShowBeatPrompt] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const beatIndex = typeof exercise.build_spec?.beat_index === "number"
    ? exercise.build_spec.beat_index as number
    : null;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!systemPrompt.trim()) {
      setError("System prompt is required.");
      return;
    }

    const payload = {
      schema_version: "1.0",
      agent_type: "single-prompt",
      system_prompt: systemPrompt.trim(),
      user_prompt_template: userPromptTemplate.trim(),
      model,
      tools: [],
      config: {},
    };

    const key = `${exercise.id}-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    onSubmit({ payload }, key).catch((err: Error) => setError(err.message));
  }

  return (
    <form onSubmit={handleSubmit} className="stack">
      {/* Beat header */}
      <div style={{ display: "flex", alignItems: "baseline", gap: "var(--space-3)" }}>
        {beatIndex !== null && (
          <span className="badge" style={{ background: "var(--color-bg-surface-raised)", color: "var(--color-text-secondary)", flexShrink: 0 }}>
            Beat {beatIndex}
          </span>
        )}
        <span style={{ fontWeight: "var(--font-weight-medium)", fontSize: "var(--font-size-sm)" }}>
          {exercise.title}
        </span>
      </div>

      {/* Collapsible beat prompt */}
      {exercise.prompt_markdown && (
        <details
          open={showBeatPrompt}
          onToggle={(e) => setShowBeatPrompt((e.target as HTMLDetailsElement).open)}
          style={{ background: "var(--color-bg-surface-raised)", borderRadius: "var(--radius-md)", padding: "var(--space-4)", border: "1px solid var(--color-border)" }}
        >
          <summary style={{ cursor: "pointer", fontSize: "var(--font-size-sm)", fontWeight: "var(--font-weight-medium)", color: "var(--color-text-secondary)" }}>
            Beat prompt
          </summary>
          <div className="prose" style={{ marginTop: "var(--space-3)", fontSize: "var(--font-size-sm)" }}>
            <pre style={{ whiteSpace: "pre-wrap", fontFamily: "inherit", background: "none", border: "none", padding: 0, margin: 0, fontSize: "inherit" }}>
              {exercise.prompt_markdown}
            </pre>
          </div>
        </details>
      )}

      {/* System prompt */}
      <div className="form-group">
        <label className="form-label" htmlFor="system-prompt">
          System prompt <span aria-hidden="true">*</span>
        </label>
        <p className="text-xs text-muted">
          Tell the agent who it is and what it should do.
        </p>
        <textarea
          id="system-prompt"
          className="form-input"
          rows={6}
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          placeholder="You are a helpful assistant that…"
          disabled={submitting}
          style={{ resize: "vertical", fontFamily: "var(--font-family-mono)", fontSize: "var(--font-size-sm)" }}
        />
      </div>

      {/* User prompt template */}
      <div className="form-group">
        <label className="form-label" htmlFor="user-prompt-template">
          User prompt template <span className="text-muted">(optional)</span>
        </label>
        <p className="text-xs text-muted">
          The message sent to the agent. Use <code>{"{{input}}"}</code> as a placeholder for the test input.
        </p>
        <textarea
          id="user-prompt-template"
          className="form-input"
          rows={4}
          value={userPromptTemplate}
          onChange={(e) => setUserPromptTemplate(e.target.value)}
          placeholder={"Please help me with: {{input}}"}
          disabled={submitting}
          style={{ resize: "vertical", fontFamily: "var(--font-family-mono)", fontSize: "var(--font-size-sm)" }}
        />
      </div>

      {/* Model selector */}
      <div className="form-group">
        <label className="form-label" htmlFor="model-select">Model</label>
        <select
          id="model-select"
          className="form-input"
          value={model}
          onChange={(e) => setModel(e.target.value)}
          disabled={submitting}
          style={{ cursor: "pointer" }}
        >
          {MODEL_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
      </div>

      {error && <div className="alert alert-error text-sm">{error}</div>}

      <div className="cluster" style={{ justifyContent: "flex-end" }}>
        <button
          type="submit"
          className="btn btn-primary btn-lg"
          disabled={submitting || !systemPrompt.trim()}
        >
          {submitting ? (
            <>
              <span className="spinner" aria-hidden="true" />
              Submitting…
            </>
          ) : (
            "Submit agent"
          )}
        </button>
      </div>

      <p className="text-xs text-muted">
        Your submission is async — we&apos;ll run it against test scenarios and score it with an LLM judge.
        Results appear below when ready (usually under a minute).
      </p>
    </form>
  );
}

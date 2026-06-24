"use client";

import { useState } from "react";
import type { SubmissionCreate } from "@/lib/api-types";

interface Props {
  exerciseId: string;
  onSubmit: (body: SubmissionCreate, idempotencyKey: string) => Promise<void>;
  submitting: boolean;
}

const DEFAULT_PAYLOAD = JSON.stringify(
  {
    schema_version: "1.0",
    agent_type: "single-prompt",
    system_prompt: "",
    user_prompt_template: "",
    model: "claude-haiku-4-5",
    tools: [],
    config: {},
  },
  null,
  2
);

export function AgentBuilder({ exerciseId, onSubmit, submitting }: Props) {
  const [payloadText, setPayloadText] = useState(DEFAULT_PAYLOAD);
  const [error, setError] = useState<string | null>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    let parsed: Record<string, unknown>;
    try {
      parsed = JSON.parse(payloadText);
    } catch {
      setError("Invalid JSON — check your agent payload.");
      return;
    }

    const key = `${exerciseId}-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    onSubmit({ payload: parsed }, key).catch((err: Error) => setError(err.message));
  }

  return (
    <form onSubmit={handleSubmit} className="stack">
      <div className="form-group">
        <label className="form-label" htmlFor="agent-payload">
          Agent payload (JSON)
        </label>
        <p className="text-xs text-muted">
          Define your agent: system prompt, user prompt template, model, tools, config.
          See the build spec above for constraints.
        </p>
        <textarea
          id="agent-payload"
          className="form-textarea"
          style={{ minHeight: "16rem" }}
          value={payloadText}
          onChange={(e) => setPayloadText(e.target.value)}
          spellCheck={false}
          disabled={submitting}
          aria-label="Agent payload JSON"
        />
      </div>

      {error && (
        <div className="alert alert-error text-sm">{error}</div>
      )}

      <div className="cluster" style={{ justifyContent: "flex-end" }}>
        <button
          type="submit"
          className="btn btn-primary btn-lg"
          disabled={submitting}
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

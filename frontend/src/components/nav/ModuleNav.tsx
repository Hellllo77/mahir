"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { Module } from "@/lib/api-types";
import { PhaseTag } from "@/components/ui/PhaseTag";

interface Props {
  cohortId: string;
  modules: Module[];
  pendingExerciseId?: string;
}

export function ModuleNav({ cohortId, modules, pendingExerciseId }: Props) {
  const pathname = usePathname();

  return (
    <nav aria-label="Curriculum modules">
      <div style={{ padding: "0 var(--space-4) var(--space-2)", marginBottom: "var(--space-2)" }}>
        <Link
          href={`/cohorts/${cohortId}`}
          className="text-xs text-muted"
          style={{ textTransform: "uppercase", letterSpacing: "0.05em", fontWeight: "var(--font-weight-semibold)" }}
        >
          Modules
        </Link>
      </div>

      {modules
        .slice()
        .sort((a, b) => a.sequence_index - b.sequence_index)
        .map((mod) => (
          <div key={mod.id} style={{ marginBottom: "var(--space-4)" }}>
            <div
              style={{
                padding: "var(--space-2) var(--space-4)",
                fontSize: "var(--font-size-xs)",
                fontWeight: "var(--font-weight-semibold)",
                color: "var(--color-text-secondary)",
                textTransform: "uppercase",
                letterSpacing: "0.05em",
              }}
            >
              {mod.sequence_index}. {mod.title}
            </div>

            {mod.exercises && (
              <ul style={{ listStyle: "none" }}>
                {mod.exercises
                  .slice()
                  .sort((a, b) => a.sequence_index - b.sequence_index)
                  .map((ex) => {
                    const href = `/exercises/${ex.id}`;
                    const active = pathname === href;
                    return (
                      <li key={ex.id}>
                        <Link
                          href={href}
                          style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "var(--space-1)",
                            padding: "var(--space-2) var(--space-4) var(--space-2) var(--space-6)",
                            fontSize: "var(--font-size-sm)",
                            borderRight: active ? "3px solid var(--color-brand-primary)" : "3px solid transparent",
                            background: active ? "var(--color-bg-surface-raised)" : "transparent",
                            color: active ? "var(--color-brand-primary)" : "var(--color-text-primary)",
                            textDecoration: "none",
                            transition: "background var(--transition-fast)",
                          }}
                          aria-current={active ? "page" : undefined}
                          title={ex.title}
                        >
                          <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                            Beat {ex.sequence_index}
                          </span>
                          {ex.id === pendingExerciseId ? (
                            <span
                              className="badge"
                              style={{
                                background: "var(--color-warning-bg, #fffbeb)",
                                color: "var(--color-warning, #d97706)",
                              }}
                            >
                              Submitted
                            </span>
                          ) : (
                            ex.phase && ex.phase !== "not_started" && (
                              <PhaseTag phase={ex.phase} />
                            )
                          )}
                        </Link>
                      </li>
                    );
                  })}
              </ul>
            )}
          </div>
        ))}
    </nav>
  );
}

import type { Phase } from "@/lib/api-types";

const PHASE_LABELS: Record<Phase, string> = {
  not_started: "Not started",
  exploring: "Exploring",
  consolidation_unlocked: "Consolidation unlocked",
  completed: "Completed",
};

const PHASE_CLASSES: Record<Phase, string> = {
  not_started: "badge phase-not-started",
  exploring: "badge phase-exploring",
  consolidation_unlocked: "badge phase-unlocked",
  completed: "badge phase-completed",
};

export function PhaseTag({ phase }: { phase: Phase }) {
  return <span className={PHASE_CLASSES[phase]}>{PHASE_LABELS[phase]}</span>;
}

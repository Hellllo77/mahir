import type { PFSignal } from "@/lib/api-types";

const LABELS: Record<PFSignal, string> = {
  productive: "Productive",
  low_effort: "Low effort",
  off_task: "Off-task",
};

const CLASSES: Record<PFSignal, string> = {
  productive: "badge signal-productive",
  low_effort: "badge signal-low-effort",
  off_task: "badge signal-off-task",
};

export function PFSignalBadge({ signal }: { signal: PFSignal }) {
  return <span className={CLASSES[signal]}>{LABELS[signal]}</span>;
}

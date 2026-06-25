// TypeScript types derived from api/mahir-api.yaml and data-model.md
// Source of truth: agents/atlas-architect/deliverables/contracts/api/mahir-api.yaml

export type Phase = "not_started" | "exploring" | "consolidation_unlocked" | "completed";
export type PFSignal = "productive" | "low_effort" | "off_task";
export type SubmissionStatus = "queued" | "running" | "evaluated" | "failed";
export type GlobalRole = "learner" | "facilitator" | "org_admin" | "super_admin";
export type EnrolmentRole = "learner" | "facilitator";
export type EnrolmentStatus = "active" | "withdrawn" | "completed";

export interface TokenResponse {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
}

export interface EnrolmentRef {
  id: string;
  cohort_id: string;
  role: EnrolmentRole;
  status: EnrolmentStatus;
}

export interface Me {
  id: string;
  email: string;
  display_name: string;
  organization_id: string;
  global_role: GlobalRole;
  enrolments: EnrolmentRef[];
}

export interface PfGateConfig {
  min_attempts: number;
  min_distinct_approaches: number;
  min_exploration_seconds: number;
  allow_fast_unlock: boolean;
}

export interface ExerciseSummary {
  id: string;
  title: string;
  sequence_index: number;
  phase: Phase;
}

export interface Module {
  id: string;
  title: string;
  sequence_index: number;
  summary_markdown?: string;
  exercises?: ExerciseSummary[];
}

export interface Exercise {
  id: string;
  module_id: string;
  title: string;
  sequence_index: number;
  prompt_markdown: string;
  build_spec: Record<string, unknown>;
  prerequisite_exercise_ids?: string[];
  gate?: PfGateConfig;
}

export interface ConsolidationContent {
  exercise_id: string;
  body_markdown: string;
  reference_build?: Record<string, unknown>;
  check_questions?: Array<Record<string, unknown>>;
}

export interface ExerciseProgress {
  id: string;
  exercise_id: string;
  phase: Phase;
  attempts_total?: number;
  attempts_genuine?: number;
  distinct_approaches?: number;
  exploration_seconds?: number;
  explored?: boolean;
  unlocked_at?: string | null;
  completed_at?: string | null;
  mastery_score?: number | null;
  gate?: PfGateConfig;
}

export interface ScenarioResult {
  scenario_id: string;
  passed: boolean;
  detail?: string;
}

export interface RubricScore {
  criterion_id: string;
  met: boolean;
  score: number;
  confidence: number;
  severity: "minor" | "major" | "critical";
  evidence: string;
}

export interface EvaluationResultUsage {
  input_tokens: number;
  output_tokens: number;
  cache_read_input_tokens: number;
}

export interface EvaluationResult {
  submission_id: string;
  schema_version: string;
  ran: boolean;
  scenario_results?: ScenarioResult[];
  rubric_scores?: RubricScore[];
  overall_score: number;
  productive_failure_signal: PFSignal;
  detected_approach?: string;
  confidence?: number;
  passed: boolean;
  feedback_markdown?: string;
  judge_model?: string;
  judge_escalated?: boolean;
  usage?: EvaluationResultUsage;
  cost_micro_usd?: number;
  evaluated_at?: string;
}

export interface Submission {
  id: string;
  exercise_id: string;
  attempt_number: number;
  status: SubmissionStatus;
  submitted_at: string;
}

export interface SubmissionDetail extends Submission {
  result: EvaluationResult | null;
}

export interface SubmissionCreate {
  payload: Record<string, unknown>;
  artifact_refs?: Array<Record<string, unknown>>;
}

export interface LearnerExerciseSummary {
  exercise_id: string;
  phase: Phase;
  attempts_total: number;
  attempts_genuine: number;
  explored: boolean;
  latest_signal: PFSignal | null;
}

export interface LearnerProgressSummary {
  user_id: string;
  display_name: string;
  enrolment_id: string;
  exercises: LearnerExerciseSummary[];
}

export interface CohortSummary {
  id: string;
  name: string;
  status: string;
  learner_count: number;
}

export interface GateOverride {
  action: "unlock_consolidation" | "mark_completed" | "reset_exploring";
  reason: string;
}

export interface ApiError {
  type: string;
  message: string;
  details?: Record<string, unknown>;
}

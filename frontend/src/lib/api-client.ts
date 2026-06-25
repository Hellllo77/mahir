// Typed API client for the Mahir API.
// All methods throw ApiClientError on non-2xx. Callers catch and handle.

import type {
  TokenResponse,
  Me,
  CohortSummary,
  CohortCreate,
  Module,
  Exercise,
  ConsolidationContent,
  ExerciseProgress,
  Submission,
  SubmissionDetail,
  SubmissionCreate,
  LearnerProgressSummary,
  GateOverride,
} from "./api-types";

const API_BASE =
  typeof window !== "undefined"
    ? (process.env.NEXT_PUBLIC_API_BASE ?? "https://api.mahir.example/v1")
    : (process.env.NEXT_PUBLIC_API_BASE ?? "https://api.mahir.example/v1");

export class ApiClientError extends Error {
  constructor(
    public readonly status: number,
    public readonly type: string,
    message: string,
    public readonly details?: Record<string, unknown>
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

export class PhaseLocked extends ApiClientError {
  constructor() {
    super(409, "phase_locked", "Complete the exploration phase before consolidation unlocks.");
    this.name = "PhaseLocked";
  }
}

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("mahir_token");
}

export function saveToken(token: string): void {
  localStorage.setItem("mahir_token", token);
}

export function clearToken(): void {
  localStorage.removeItem("mahir_token");
}

export function saveRole(role: string): void {
  localStorage.setItem("mahir_role", role);
}

export function getRole(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("mahir_role");
}

export function clearRole(): void {
  localStorage.removeItem("mahir_role");
}

async function request<T>(
  path: string,
  options: RequestInit & { skipAuth?: boolean } = {}
): Promise<T> {
  const { skipAuth, ...fetchOptions } = options;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(fetchOptions.headers as Record<string, string> ?? {}),
  };

  if (!skipAuth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, { ...fetchOptions, headers });

  if (!res.ok) {
    let errorBody: { type?: string; message?: string; detail?: string | { type?: string; message?: string }; details?: Record<string, unknown> } = {};
    try {
      errorBody = await res.json();
    } catch {
      // non-JSON error body
    }
    const detailObj = typeof errorBody.detail === "object" ? errorBody.detail : undefined;
    const errorType = detailObj?.type ?? errorBody.type ?? "unknown_error";
    if (res.status === 409 && errorType === "phase_locked") throw new PhaseLocked();
    const humanMessage =
      detailObj?.message ??
      (typeof errorBody.detail === "string" ? errorBody.detail : undefined) ??
      errorBody.message ??
      `Request failed with status ${res.status}`;
    throw new ApiClientError(res.status, errorType, humanMessage, errorBody.details);
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

// --- Auth ---

export async function login(email: string, password: string): Promise<TokenResponse> {
  return request<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
    skipAuth: true,
  });
}

export async function getMe(): Promise<Me> {
  return request<Me>("/me");
}

// --- Cohorts ---

export async function getCohorts(): Promise<CohortSummary[]> {
  return request<CohortSummary[]>("/cohorts");
}

export async function createCohort(body: CohortCreate): Promise<CohortSummary> {
  return request<CohortSummary>("/cohorts", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

// --- Curriculum ---

export async function getModules(cohortId: string): Promise<Module[]> {
  return request<Module[]>(`/cohorts/${cohortId}/modules`);
}

export async function getExercise(exerciseId: string): Promise<Exercise> {
  return request<Exercise>(`/exercises/${exerciseId}`);
}

export async function getConsolidation(exerciseId: string): Promise<ConsolidationContent> {
  return request<ConsolidationContent>(`/exercises/${exerciseId}/consolidation`);
}

// --- Submissions ---

export async function submitAgent(
  exerciseId: string,
  body: SubmissionCreate,
  idempotencyKey: string
): Promise<Submission> {
  return request<Submission>(`/exercises/${exerciseId}/submissions`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: { "Idempotency-Key": idempotencyKey },
  });
}

export async function listSubmissions(exerciseId: string): Promise<Submission[]> {
  return request<Submission[]>(`/exercises/${exerciseId}/submissions`);
}

export async function getSubmission(submissionId: string): Promise<SubmissionDetail> {
  return request<SubmissionDetail>(`/submissions/${submissionId}`);
}

// --- Progress ---

export async function getMyProgress(enrolmentId: string): Promise<ExerciseProgress[]> {
  return request<ExerciseProgress[]>(`/me/progress?enrolment_id=${enrolmentId}`);
}

export async function getExerciseProgress(exerciseId: string): Promise<ExerciseProgress> {
  return request<ExerciseProgress>(`/exercises/${exerciseId}/progress`);
}

// --- Facilitator ---

export async function getCohortRoster(cohortId: string): Promise<LearnerProgressSummary[]> {
  return request<LearnerProgressSummary[]>(`/facilitator/cohorts/${cohortId}/learners`);
}

export async function overrideGate(
  progressId: string,
  body: GateOverride
): Promise<ExerciseProgress> {
  return request<ExerciseProgress>(`/facilitator/progress/${progressId}/override`, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

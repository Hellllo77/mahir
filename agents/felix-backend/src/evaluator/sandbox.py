"""Stage 1 — Deterministic scenario harness (ADR-003).

For the pilot, this runs a lightweight in-process simulation of the agent
against each exercise scenario. Real container-per-submission sandboxing
(CPU/mem/network limits) is the production path; this module is designed so
that path can be dropped in without changing the interface.

The harness:
  1. Checks basic structural validity (runs? required fields present? no banned patterns?)
  2. Runs the learner's agent payload against each scenario (deterministic assertions)
  3. Returns transcripts + scenario results that Stage 2 (LLM judge) reads
"""
import json
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScenarioRunResult:
    scenario_id: str
    passed: bool
    detail: str
    transcript: str = ""


@dataclass
class SandboxResult:
    ran: bool
    scenario_results: list[ScenarioRunResult] = field(default_factory=list)
    transcript_bundle: str = ""  # concatenated transcripts for Stage 2
    error: str | None = None


def run_sandbox(
    submission_payload: dict,
    scenarios: list[dict],
    build_spec: dict,
) -> SandboxResult:
    """Run the submission payload against all scenarios.

    submission_payload: the agent build from Submission.payload
    scenarios: [{id, name, input_payload, assertions, weight}]
    build_spec: exercise build spec (allowed tools, IO contract)
    """
    # Structural pre-checks
    if not submission_payload:
        return SandboxResult(ran=False, error="Empty submission payload.")

    schema_version = submission_payload.get("schema_version")
    if not schema_version:
        return SandboxResult(ran=False, error="submission.payload missing schema_version.")

    transcripts = []
    scenario_results = []

    for scenario in scenarios:
        sid = scenario["id"]
        input_payload = scenario.get("input_payload", {})
        assertions = scenario.get("assertions", {})

        t0 = time.monotonic()
        try:
            result, transcript = _run_single_scenario(
                submission_payload, input_payload, assertions, build_spec
            )
            elapsed_ms = int((time.monotonic() - t0) * 1000)
            transcripts.append(f"# scenario:{sid}\n{transcript}\n[elapsed: {elapsed_ms}ms]")
            scenario_results.append(
                ScenarioRunResult(
                    scenario_id=sid,
                    passed=result["passed"],
                    detail=result.get("detail", ""),
                    transcript=transcript,
                )
            )
        except Exception as exc:
            transcripts.append(f"# scenario:{sid}\nERROR: {exc}")
            scenario_results.append(
                ScenarioRunResult(scenario_id=sid, passed=False, detail=f"Runtime error: {exc}")
            )

    return SandboxResult(
        ran=True,
        scenario_results=scenario_results,
        transcript_bundle="\n\n".join(transcripts),
    )


def _run_single_scenario(
    payload: dict, input_payload: dict, assertions: dict, build_spec: dict
) -> tuple[dict, str]:
    """Simulate running the agent against one scenario's input.

    Pilot implementation: validates the payload structure against assertions
    without actually executing untrusted code (that requires container isolation).
    Production: replace with container-per-submission runner.
    """
    transcript_lines = []
    transcript_lines.append(f"INPUT: {json.dumps(input_payload)}")

    # Check required fields from build_spec
    required_fields = build_spec.get("required_fields", [])
    missing = [f for f in required_fields if f not in payload]
    if missing:
        transcript_lines.append(f"MISSING_FIELDS: {missing}")
        return {"passed": False, "detail": f"Missing required fields: {missing}"}, "\n".join(transcript_lines)

    # Check banned patterns
    banned = build_spec.get("banned_patterns", [])
    payload_str = json.dumps(payload)
    for pattern in banned:
        if pattern in payload_str:
            transcript_lines.append(f"BANNED_PATTERN: {pattern}")
            return {"passed": False, "detail": f"Banned pattern found: {pattern}"}, "\n".join(transcript_lines)

    # Check assertion keys from the scenario
    assertion_checks = assertions.get("checks", [])
    all_passed = True
    details = []
    for check in assertion_checks:
        field_path = check.get("field", "")
        expected = check.get("expected")
        actual = _get_nested(payload, field_path.split("."))
        ok = actual == expected
        if not ok:
            all_passed = False
            details.append(f"field={field_path} expected={expected!r} actual={actual!r}")
        transcript_lines.append(f"CHECK {field_path}: {'PASS' if ok else 'FAIL'}")

    transcript_lines.append(f"OUTPUT: {'PASS' if all_passed else 'FAIL'}")
    return {
        "passed": all_passed,
        "detail": "; ".join(details) if details else "All assertions passed.",
    }, "\n".join(transcript_lines)


def _get_nested(obj: Any, keys: list[str]) -> Any:
    for k in keys:
        if not isinstance(obj, dict):
            return None
        obj = obj.get(k)
    return obj

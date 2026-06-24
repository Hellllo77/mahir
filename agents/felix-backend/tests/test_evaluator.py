"""Evaluator unit tests — sandbox, judge schemas, PF signal logic."""
import json

import pytest

from src.evaluator.sandbox import SandboxResult, run_sandbox
from src.evaluator.schemas import JudgeOutput


# ── Sandbox ─────────────────────────────────────────────────────────────────

def test_sandbox_empty_payload():
    result = run_sandbox({}, [], {})
    assert result.ran is False
    assert "Empty" in result.error


def test_sandbox_missing_schema_version():
    result = run_sandbox({"model": "claude-haiku-4-5"}, [], {})
    assert result.ran is False
    assert "schema_version" in result.error


def test_sandbox_missing_required_field():
    build_spec = {"required_fields": ["model", "tools"]}
    payload = {"schema_version": "1.0", "model": "claude-haiku-4-5"}  # missing tools
    result = run_sandbox(payload, [], build_spec)
    assert result.ran is True
    assert result.scenario_results == []  # no scenarios, but ran


def test_sandbox_banned_pattern():
    build_spec = {"required_fields": [], "banned_patterns": ["os.environ"]}
    payload = {"schema_version": "1.0", "code": "import os; os.environ['SECRET']"}
    scenarios = [{"id": "s1", "name": "t", "input_payload": {}, "assertions": {"checks": []}}]
    result = run_sandbox(payload, scenarios, build_spec)
    assert result.ran is True
    # The scenario should fail due to banned pattern
    assert result.scenario_results[0].passed is False
    assert "os.environ" in result.scenario_results[0].detail


def test_sandbox_assertion_pass():
    build_spec = {"required_fields": ["model"]}
    payload = {"schema_version": "1.0", "model": "claude-haiku-4-5"}
    scenarios = [{
        "id": "s1",
        "name": "field check",
        "input_payload": {"text": "hello"},
        "assertions": {"checks": [{"field": "model", "expected": "claude-haiku-4-5"}]},
    }]
    result = run_sandbox(payload, scenarios, build_spec)
    assert result.ran is True
    assert result.scenario_results[0].passed is True


def test_sandbox_assertion_fail():
    build_spec = {"required_fields": ["model"]}
    payload = {"schema_version": "1.0", "model": "gpt-4"}  # wrong model
    scenarios = [{
        "id": "s1",
        "name": "field check",
        "input_payload": {},
        "assertions": {"checks": [{"field": "model", "expected": "claude-haiku-4-5"}]},
    }]
    result = run_sandbox(payload, scenarios, build_spec)
    assert result.scenario_results[0].passed is False


def test_sandbox_transcript_bundle():
    build_spec = {"required_fields": []}
    payload = {"schema_version": "1.0"}
    scenarios = [
        {"id": "s1", "name": "a", "input_payload": {}, "assertions": {"checks": []}},
        {"id": "s2", "name": "b", "input_payload": {}, "assertions": {"checks": []}},
    ]
    result = run_sandbox(payload, scenarios, build_spec)
    assert "scenario:s1" in result.transcript_bundle
    assert "scenario:s2" in result.transcript_bundle


# ── JudgeOutput schema ───────────────────────────────────────────────────────

def test_judge_output_valid():
    j = JudgeOutput(
        ran=True,
        overall_score=0.7,
        productive_failure_signal="productive",
        confidence=0.85,
        passed=True,
        feedback_markdown="Good work exploring different approaches.",
        rubric_scores=[],
        scenario_results=[],
    )
    assert j.passed is True
    assert j.schema_version == "1.0"


def test_judge_output_score_bounds():
    with pytest.raises(Exception):
        JudgeOutput(
            ran=True,
            overall_score=1.5,  # out of range
            productive_failure_signal="productive",
            confidence=0.8,
            passed=True,
            feedback_markdown="ok",
        )


def test_judge_output_pf_signal_enum():
    with pytest.raises(Exception):
        JudgeOutput(
            ran=True,
            overall_score=0.5,
            productive_failure_signal="invalid_value",  # not in Literal
            confidence=0.8,
            passed=False,
            feedback_markdown="ok",
        )

"""Replay engine for the public OmarAGI Reliability BYOK Replay demonstration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .policy import (
    PUBLIC_POLICY_LABEL,
    PublicPolicyError,
    apply_adoption_gate,
    build_runtime_case,
    decide_route,
    execute_candidate,
    lock_decision,
    make_event_log,
    score_after_decision_lock,
    score_artifact,
    validate_case,
    verify_execution,
)


class ReplayArtifactError(ValueError):
    """Raised when the public replay artifact fails its schema boundary."""


def load_artifact(path: str | Path) -> dict[str, Any]:
    artifact_path = Path(path)
    try:
        payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReplayArtifactError(f"artifact not found: {artifact_path}") from exc
    except json.JSONDecodeError as exc:
        raise ReplayArtifactError(f"invalid JSON at line {exc.lineno}, column {exc.colno}") from exc

    if not isinstance(payload, dict):
        raise ReplayArtifactError("artifact root must be an object")
    if payload.get("artifact_kind") != "omaragi_reliability_replay_public_demo":
        raise ReplayArtifactError("artifact_kind is not the public replay demo schema")
    if payload.get("synthetic") is not True:
        raise ReplayArtifactError("only explicitly synthetic public artifacts are accepted")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ReplayArtifactError("cases must be a non-empty list")

    seen: set[str] = set()
    try:
        for case in cases:
            if not isinstance(case, dict):
                raise ReplayArtifactError("every case must be an object")
            validate_case(case)
            case_id = str(case["case_id"])
            if case_id in seen:
                raise ReplayArtifactError(f"duplicate case_id: {case_id}")
            seen.add(case_id)
    except PublicPolicyError as exc:
        raise ReplayArtifactError(str(exc)) from exc
    return payload


def classify_outcome(baseline_correct: bool, final_correct: bool) -> str:
    if not baseline_correct and final_correct:
        return "beneficial_flip"
    if baseline_correct and not final_correct:
        return "harmful_flip"
    if baseline_correct and final_correct:
        return "unchanged_correct"
    return "unchanged_incorrect"


def _run_case(case: dict[str, Any]) -> dict[str, Any]:
    # Runtime stages receive an explicit projection that excludes the scoring
    # target.  ``post_lock_scoring`` is first read after the decision receipt.
    runtime_case = build_runtime_case(case)
    router_result = decide_route(runtime_case)
    executor_result = execute_candidate(runtime_case, router_result)
    runtime_verifier_result = verify_execution(
        executor_result,
        router_result,
        runtime_case["runtime_verification"],
    )
    adoption_gate_result = apply_adoption_gate(
        runtime_case["baseline_output"],
        executor_result,
        router_result,
        runtime_verifier_result,
    )
    decision_lock = lock_decision(
        case_id=runtime_case["case_id"],
        baseline_output=runtime_case["baseline_output"],
        router_result=router_result,
        executor_result=executor_result,
        runtime_verifier_result=runtime_verifier_result,
        adoption_gate_result=adoption_gate_result,
    )
    post_lock_scorer_result = score_after_decision_lock(
        baseline_output=runtime_case["baseline_output"],
        final_output=adoption_gate_result["final_answer"],
        post_lock_scoring=case["post_lock_scoring"],
        decision_lock=decision_lock,
    )
    baseline_passed = post_lock_scorer_result["baseline"]["passed"]
    final_passed = post_lock_scorer_result["final"]["passed"]
    outcome = classify_outcome(baseline_passed, final_passed)
    artifact_score = score_artifact(
        baseline_passed=baseline_passed,
        final_passed=final_passed,
        adoption_gate_result=adoption_gate_result,
    )

    return {
        "case_id": str(case["case_id"]),
        "prompt": str(case["prompt"]),
        "baseline_output": str(case["baseline_output"]),
        "governed_candidate": str(case["governed_candidate"]),
        "router_result": router_result,
        "executor_result": executor_result,
        "runtime_verifier_result": runtime_verifier_result,
        "adoption_gate_result": adoption_gate_result,
        "decision_lock": decision_lock,
        "post_lock_scorer_result": post_lock_scorer_result,
        "artifact_score": artifact_score,
        "final_answer": adoption_gate_result["final_answer"],
        "baseline_correct": baseline_passed,
        "final_correct": final_passed,
        "outcome": outcome,
        "beneficial_flip": artifact_score["beneficial_flip"],
        "harmful_flip": artifact_score["harmful_flip"],
        "preserved_baseline": adoption_gate_result["source"] == "baseline_output",
        "event_log": make_event_log(
            case_id=str(case["case_id"]),
            router_result=router_result,
            executor_result=executor_result,
            runtime_verifier_result=runtime_verifier_result,
            adoption_gate_result=adoption_gate_result,
            decision_lock=decision_lock,
            post_lock_scorer_result=post_lock_scorer_result,
            artifact_score=artifact_score,
        ),
    }


def _summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    baseline_correct = sum(bool(item["baseline_correct"]) for item in results)
    governed_correct = sum(bool(item["final_correct"]) for item in results)
    delta = governed_correct - baseline_correct
    delta_points = (delta / total) * 100.0
    artifact_scores = [int(item["artifact_score"]["score"]) for item in results]
    return {
        "case_count": total,
        "baseline_correct": baseline_correct,
        "baseline_score_percent": round((baseline_correct / total) * 100.0, 2),
        "governed_correct": governed_correct,
        "governed_score_percent": round((governed_correct / total) * 100.0, 2),
        "absolute_delta_correct": delta,
        "delta_percentage_points": round(delta_points, 2),
        "direction": "uplift" if delta > 0 else "regression" if delta < 0 else "unchanged",
        "adoption_count": sum(
            item["adoption_gate_result"]["decision"] == "candidate_adopted"
            for item in results
        ),
        "preserved_baseline_count": sum(bool(item["preserved_baseline"]) for item in results),
        "beneficial_flip_count": sum(bool(item["beneficial_flip"]) for item in results),
        "harmful_flip_count": sum(bool(item["harmful_flip"]) for item in results),
        "floor_preserved_count": sum(
            bool(item["artifact_score"]["floor_preserved"]) for item in results
        ),
        "unchanged_correct_count": sum(item["outcome"] == "unchanged_correct" for item in results),
        "unchanged_incorrect_count": sum(item["outcome"] == "unchanged_incorrect" for item in results),
        "artifact_score": {
            "label": "public_demonstration_artifact_score",
            "benchmark_metric": False,
            "mean": round(sum(artifact_scores) / total, 2),
            "minimum": min(artifact_scores),
            "maximum": max(artifact_scores),
        },
    }


def run_replay(artifact: dict[str, Any]) -> dict[str, Any]:
    """Execute the public policy over an already-validated synthetic artifact."""

    results = [_run_case(case) for case in artifact["cases"]]
    return {
        "schema_version": "omaragi-reliability-replay-report-v3",
        "title": str(artifact.get("title") or "OmarAGI Reliability BYOK Replay"),
        "artifact_kind": artifact["artifact_kind"],
        "synthetic": True,
        "policy_label": PUBLIC_POLICY_LABEL,
        "runtime_boundary": {
            "live_product": (
                "OmarAGI BYOK reliability workflow with a user-supplied API key "
                "and actual model execution."
            ),
            "public_repository": (
                "Sanitized deterministic offline replay with a target-blind runtime "
                "verifier, pre-score decision lock, and no credentials, external "
                "calls, or live generation."
            ),
            "evidence_status": (
                "Synthetic benchmark-shaped architecture demonstration; not "
                "benchmark evidence or independent validation."
            ),
        },
        "claim_boundary": (
            "Public demonstration sample only. The included cases are synthetic; "
            "this report and its artifact score are not benchmark evidence or a "
            "disclosure of private production logic, and they do not prove "
            "universal uplift."
        ),
        "summary": _summary(results),
        "cases": results,
    }

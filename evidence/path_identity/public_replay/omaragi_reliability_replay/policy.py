"""Transparent public policy for the OmarAGI Reliability BYOK Replay demo.

The public fixture deliberately separates the runtime decision path from the
post-lock scorer.  Runtime stages receive task evidence and constraints, but
they never receive ``post_lock_scoring``.  The scorer is called only after an
immutable decision receipt has been created.

This remains a small, synthetic demonstration policy.  It does not reproduce
private OmarAGI production logic.
"""

from __future__ import annotations

import ast
import hashlib
import json
import math
import operator
import re
from typing import Any


PUBLIC_POLICY_LABEL = (
    "This is a simplified public demonstration policy, not OmarAGI production logic."
)

SUPPORTED_RUNTIME_VERIFIERS = frozenset(
    {"arithmetic_expression", "source_contains", "contains_all"}
)
SUPPORTED_POST_LOCK_SCORERS = frozenset(
    {"exact_match", "numeric_match", "contains_all"}
)


class PublicPolicyError(ValueError):
    """Raised when a sanitized public replay artifact is malformed."""


def normalize_text(value: Any) -> str:
    """Normalize superficial whitespace and case for public demo comparison."""

    return " ".join(str(value).strip().casefold().split())


def validate_case(case: dict[str, Any]) -> None:
    required = {
        "case_id",
        "prompt",
        "baseline_output",
        "governed_candidate",
        "route_request",
        "runtime_verification",
        "post_lock_scoring",
    }
    missing = sorted(required.difference(case))
    if missing:
        raise PublicPolicyError(f"case is missing required fields: {', '.join(missing)}")
    if not isinstance(case["route_request"], dict):
        raise PublicPolicyError("route_request must be an object")
    if not isinstance(case["runtime_verification"], dict):
        raise PublicPolicyError("runtime_verification must be an object")
    if not isinstance(case["post_lock_scoring"], dict):
        raise PublicPolicyError("post_lock_scoring must be an object")
    if not str(case["case_id"]).strip():
        raise PublicPolicyError("case_id must not be blank")

    runtime_method = str(case["runtime_verification"].get("method", "")).strip()
    if runtime_method not in SUPPORTED_RUNTIME_VERIFIERS:
        raise PublicPolicyError(
            f"unsupported runtime verifier: {runtime_method or 'missing'}"
        )
    scorer_method = str(case["post_lock_scoring"].get("method", "")).strip()
    if scorer_method not in SUPPORTED_POST_LOCK_SCORERS:
        raise PublicPolicyError(
            f"unsupported post-lock scorer: {scorer_method or 'missing'}"
        )


def build_runtime_case(case: dict[str, Any]) -> dict[str, Any]:
    """Return the only fields visible to routing, execution, and verification.

    ``post_lock_scoring`` is intentionally absent.  This explicit projection is
    the public demo's structural target-separation boundary.
    """

    return {
        "case_id": str(case["case_id"]),
        "prompt": str(case["prompt"]),
        "baseline_output": str(case["baseline_output"]),
        "governed_candidate": str(case["governed_candidate"]),
        "route_request": dict(case["route_request"]),
        "runtime_verification": dict(case["runtime_verification"]),
    }


def decide_route(runtime_case: dict[str, Any]) -> dict[str, Any]:
    """Allow only explicit, supported, non-empty public demo routes."""

    request = runtime_case["route_request"]
    verifier = str(runtime_case["runtime_verification"].get("method", "")).strip()
    candidate = str(runtime_case.get("governed_candidate", "")).strip()

    if request.get("enabled") is not True:
        return {
            "allowed": False,
            "decision": "route_denied",
            "reason": str(request.get("reason") or "route disabled by sanitized artifact"),
        }
    if verifier not in SUPPORTED_RUNTIME_VERIFIERS:
        return {
            "allowed": False,
            "decision": "route_denied",
            "reason": f"unsupported public runtime verifier: {verifier or 'missing'}",
        }
    if not candidate:
        return {
            "allowed": False,
            "decision": "route_denied",
            "reason": "candidate is empty",
        }
    return {
        "allowed": True,
        "decision": "route_allowed",
        "reason": str(request.get("reason") or "sanitized artifact permits public demo route"),
    }


def execute_candidate(
    runtime_case: dict[str, Any], router_result: dict[str, Any]
) -> dict[str, Any]:
    """Run the offline public executor over a sanitized replay candidate."""

    if not router_result["allowed"]:
        return {
            "status": "skipped_by_route",
            "executor": "public_sanitized_executor",
            "mode": "deterministic_replay",
            "generated_live": False,
            "input_source": "sanitized_replay_artifact",
            "output": "",
            "reason": "router denied execution before candidate loading",
        }
    return {
        "status": "executed",
        "executor": "public_sanitized_executor",
        "mode": "deterministic_replay",
        "generated_live": False,
        "input_source": "sanitized_replay_artifact",
        "output": str(runtime_case["governed_candidate"]),
        "reason": "sanitized pre-generated candidate loaded by the offline public executor",
    }


def _single_number(value: Any) -> float | None:
    matches = re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", str(value).replace(",", ""))
    if len(matches) != 1:
        return None
    try:
        parsed = float(matches[0])
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


_ARITHMETIC_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _evaluate_arithmetic_expression(expression: str) -> float:
    """Evaluate a tiny numeric expression without ``eval`` or name access."""

    if len(expression) > 120:
        raise PublicPolicyError("arithmetic_expression is too long")
    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise PublicPolicyError("arithmetic_expression is invalid") from exc

    def visit(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            value = float(node.value)
            if not math.isfinite(value):
                raise PublicPolicyError("arithmetic_expression must be finite")
            return value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = visit(node.operand)
            return operand if isinstance(node.op, ast.UAdd) else -operand
        if isinstance(node, ast.BinOp) and type(node.op) in _ARITHMETIC_OPERATORS:
            left = visit(node.left)
            right = visit(node.right)
            try:
                result = _ARITHMETIC_OPERATORS[type(node.op)](left, right)
            except ZeroDivisionError as exc:
                raise PublicPolicyError("arithmetic_expression divides by zero") from exc
            if not math.isfinite(result):
                raise PublicPolicyError("arithmetic_expression result must be finite")
            return result
        raise PublicPolicyError("arithmetic_expression contains an unsupported operation")

    return visit(parsed)


def verify_runtime_output(
    output: Any, runtime_verification: dict[str, Any]
) -> dict[str, Any]:
    """Verify a candidate from task evidence without post-lock target access."""

    method = str(runtime_verification.get("method", "")).strip()
    if method not in SUPPORTED_RUNTIME_VERIFIERS:
        return {
            "status": "unsupported",
            "passed": False,
            "method": method or "missing",
            "target_accessed": False,
            "reason": "runtime verifier is outside the public demonstration allowlist",
        }

    if method == "arithmetic_expression":
        expression = str(runtime_verification.get("expression", "")).strip()
        if not expression:
            raise PublicPolicyError(
                "arithmetic_expression requires runtime_verification.expression"
            )
        expected_number = _evaluate_arithmetic_expression(expression)
        actual_number = _single_number(output)
        passed = actual_number is not None and math.isclose(
            actual_number, expected_number, rel_tol=0.0, abs_tol=1e-9
        )
        reason = (
            "candidate matches the independently evaluated expression"
            if passed
            else "candidate does not match the independently evaluated expression"
        )
    elif method == "source_contains":
        source_text = normalize_text(runtime_verification.get("source_text", ""))
        candidate_text = normalize_text(output)
        if not source_text:
            raise PublicPolicyError("source_contains requires runtime_verification.source_text")
        passed = bool(candidate_text) and candidate_text in source_text
        reason = (
            "candidate is directly present in the supplied source evidence"
            if passed
            else "candidate is not present in the supplied source evidence"
        )
    else:
        terms = runtime_verification.get("required_terms")
        if not isinstance(terms, list) or not terms:
            raise PublicPolicyError(
                "contains_all requires runtime_verification.required_terms"
            )
        normalized_output = normalize_text(output)
        missing = [str(term) for term in terms if normalize_text(term) not in normalized_output]
        passed = not missing
        reason = (
            "all runtime-required fields are present"
            if passed
            else f"missing runtime-required fields: {', '.join(missing)}"
        )

    return {
        "status": "verified",
        "passed": passed,
        "method": method,
        "target_accessed": False,
        "reason": reason,
    }


def verify_execution(
    executor_result: dict[str, Any],
    router_result: dict[str, Any],
    runtime_verification: dict[str, Any],
) -> dict[str, Any]:
    if not router_result["allowed"]:
        return {
            "status": "not_run",
            "passed": False,
            "method": str(runtime_verification.get("method", "missing")),
            "target_accessed": False,
            "reason": "router denied execution before runtime verification",
        }
    return verify_runtime_output(executor_result["output"], runtime_verification)


def apply_adoption_gate(
    baseline_output: Any,
    executor_result: dict[str, Any],
    router_result: dict[str, Any],
    runtime_verifier_result: dict[str, Any],
) -> dict[str, Any]:
    """Adopt only a routed candidate that passes the runtime verifier."""

    if router_result["allowed"] and runtime_verifier_result["passed"]:
        return {
            "decision": "candidate_adopted",
            "source": "executor_output",
            "final_answer": executor_result["output"],
            "reason": "router allowed execution and the target-blind runtime verifier passed",
        }
    return {
        "decision": "baseline_preserved",
        "source": "baseline_output",
        "final_answer": str(baseline_output),
        "reason": "baseline preserved because routing or runtime verification did not pass",
    }


def lock_decision(
    *,
    case_id: str,
    baseline_output: str,
    router_result: dict[str, Any],
    executor_result: dict[str, Any],
    runtime_verifier_result: dict[str, Any],
    adoption_gate_result: dict[str, Any],
) -> dict[str, Any]:
    """Create an immutable receipt before any scoring target is consulted."""

    locked_payload = {
        "case_id": case_id,
        "baseline_output": baseline_output,
        "router_result": router_result,
        "executor_result": executor_result,
        "runtime_verifier_result": runtime_verifier_result,
        "adoption_gate_result": adoption_gate_result,
    }
    canonical = json.dumps(
        locked_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return {
        "status": "locked",
        "lock_version": "public-decision-lock-v1",
        "hash_algorithm": "sha256",
        "decision_sha256": hashlib.sha256(canonical).hexdigest(),
        "locked_before_scoring": True,
        "scorer_accessed": False,
        "gold_accessed": False,
        "reason": "route, execution, verification, and adoption were frozen before scoring",
    }


def _score_output(output: Any, scoring: dict[str, Any]) -> dict[str, Any]:
    method = str(scoring.get("method", "")).strip()
    if method not in SUPPORTED_POST_LOCK_SCORERS:
        raise PublicPolicyError(f"unsupported post-lock scorer: {method or 'missing'}")

    if method == "exact_match":
        if "expected" not in scoring:
            raise PublicPolicyError("exact_match requires post_lock_scoring.expected")
        passed = normalize_text(output) == normalize_text(scoring["expected"])
        reason = "normalized exact match" if passed else "normalized values differ"
    elif method == "numeric_match":
        if "expected" not in scoring:
            raise PublicPolicyError("numeric_match requires post_lock_scoring.expected")
        actual_number = _single_number(output)
        expected_number = _single_number(scoring["expected"])
        if expected_number is None:
            raise PublicPolicyError("numeric_match expected value must contain one finite number")
        passed = actual_number is not None and math.isclose(
            actual_number, expected_number, rel_tol=0.0, abs_tol=1e-9
        )
        reason = "numeric values match" if passed else "numeric values differ or are ambiguous"
    else:
        terms = scoring.get("required_terms")
        if not isinstance(terms, list) or not terms:
            raise PublicPolicyError(
                "contains_all requires post_lock_scoring.required_terms"
            )
        normalized_output = normalize_text(output)
        missing = [str(term) for term in terms if normalize_text(term) not in normalized_output]
        passed = not missing
        reason = "all required terms present" if passed else f"missing terms: {', '.join(missing)}"

    return {"passed": passed, "method": method, "reason": reason}


def score_after_decision_lock(
    *,
    baseline_output: Any,
    final_output: Any,
    post_lock_scoring: dict[str, Any],
    decision_lock: dict[str, Any],
) -> dict[str, Any]:
    """Score baseline and final outputs only after the decision receipt exists."""

    if decision_lock.get("status") != "locked":
        raise PublicPolicyError("post-lock scorer requires a valid decision lock")
    baseline = _score_output(baseline_output, post_lock_scoring)
    final = _score_output(final_output, post_lock_scoring)
    return {
        "status": "scored_after_decision_lock",
        "scorer": "public_demo_post_lock_scorer",
        "lock_verified": True,
        "decision_sha256": decision_lock["decision_sha256"],
        "baseline": baseline,
        "final": final,
        "reason": "target-based scoring executed after route and adoption were locked",
    }


def score_artifact(
    *,
    baseline_passed: bool,
    final_passed: bool,
    adoption_gate_result: dict[str, Any],
) -> dict[str, Any]:
    """Assign a transparent, deterministic public demonstration artifact score."""

    beneficial_flip = not baseline_passed and final_passed
    harmful_flip = baseline_passed and not final_passed
    candidate_adopted = adoption_gate_result["decision"] == "candidate_adopted"
    floor_preserved = not harmful_flip

    if harmful_flip:
        score = 0
        reason = "harmful flip: a correct baseline became incorrect"
    elif beneficial_flip and candidate_adopted:
        score = 100
        reason = "verified candidate adoption improved an incorrect baseline"
    elif baseline_passed and final_passed and not candidate_adopted:
        score = 90
        reason = "correct baseline preserved against a rejected or denied candidate"
    elif final_passed:
        score = 70
        reason = "correct result retained without a measured improvement"
    else:
        score = 40
        reason = "incorrect baseline preserved because no verified improvement was available"

    return {
        "label": "public_demonstration_artifact_score",
        "benchmark_metric": False,
        "baseline_passed": baseline_passed,
        "final_passed": final_passed,
        "beneficial_flip": beneficial_flip,
        "harmful_flip": harmful_flip,
        "floor_preserved": floor_preserved,
        "candidate_adopted": candidate_adopted,
        "score": score,
        "reason": reason,
    }


def make_event_log(
    *,
    case_id: str,
    router_result: dict[str, Any],
    executor_result: dict[str, Any],
    runtime_verifier_result: dict[str, Any],
    adoption_gate_result: dict[str, Any],
    decision_lock: dict[str, Any],
    post_lock_scorer_result: dict[str, Any],
    artifact_score: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return the ordered public path, including the score-access boundary."""

    return [
        {"step": 1, "stage": "route", **router_result},
        {"step": 2, "stage": "execute", **executor_result},
        {"step": 3, "stage": "runtime_verify", **runtime_verifier_result},
        {"step": 4, "stage": "adoption_gate", **adoption_gate_result},
        {"step": 5, "stage": "decision_lock", **decision_lock},
        {"step": 6, "stage": "post_lock_score", **post_lock_scorer_result},
        {"step": 7, "stage": "artifact_score", **artifact_score},
        {
            "step": 8,
            "stage": "log",
            "status": "recorded",
            "case_id": case_id,
            "policy": PUBLIC_POLICY_LABEL,
        },
    ]

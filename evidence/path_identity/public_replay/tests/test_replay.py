from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from omaragi_reliability_replay.cli import build_parser
from omaragi_reliability_replay.engine import (
    ReplayArtifactError,
    classify_outcome,
    load_artifact,
    run_replay,
)
from omaragi_reliability_replay.policy import (
    PUBLIC_POLICY_LABEL,
    build_runtime_case,
    score_artifact,
)
from omaragi_reliability_replay.reports import export_reports


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "samples" / "public_demo_replay.json"
EXAMPLE_REPORT = ROOT / "examples" / "example_report.json"


class ReliabilityReplayTests(unittest.TestCase):
    def test_cli_help_uses_exact_public_project_name(self) -> None:
        help_text = build_parser().format_help()
        self.assertIn("OmarAGI Reliability BYOK Replay", help_text)

    def test_committed_example_matches_current_replay(self) -> None:
        generated = run_replay(load_artifact(SAMPLE))
        committed = json.loads(EXAMPLE_REPORT.read_text(encoding="utf-8"))
        self.assertEqual(committed, generated)

    def test_public_demo_sample_summary_is_stable(self) -> None:
        report = run_replay(load_artifact(SAMPLE))
        summary = report["summary"]
        self.assertEqual(report["schema_version"], "omaragi-reliability-replay-report-v3")
        self.assertEqual(
            report["title"],
            "OmarAGI Reliability BYOK Replay — Public Demonstration Sample",
        )
        self.assertIn("user-supplied API key", report["runtime_boundary"]["live_product"])
        self.assertIn("offline replay", report["runtime_boundary"]["public_repository"])
        self.assertIn("target-blind runtime verifier", report["runtime_boundary"]["public_repository"])
        self.assertIn("not benchmark evidence", report["runtime_boundary"]["evidence_status"])
        self.assertEqual(summary["case_count"], 5)
        self.assertEqual(summary["baseline_correct"], 2)
        self.assertEqual(summary["governed_correct"], 4)
        self.assertEqual(summary["delta_percentage_points"], 40.0)
        self.assertEqual(summary["adoption_count"], 2)
        self.assertEqual(summary["preserved_baseline_count"], 3)
        self.assertEqual(summary["beneficial_flip_count"], 2)
        self.assertEqual(summary["harmful_flip_count"], 0)
        self.assertEqual(summary["floor_preserved_count"], 5)
        self.assertEqual(summary["artifact_score"]["mean"], 84.0)
        self.assertFalse(summary["artifact_score"]["benchmark_metric"])

    def test_verified_candidate_adoption_has_executor_and_score(self) -> None:
        report = run_replay(load_artifact(SAMPLE))
        case = next(item for item in report["cases"] if item["case_id"] == "demo-checklist-count")
        self.assertEqual(case["router_result"]["decision"], "route_allowed")
        self.assertEqual(case["executor_result"]["status"], "executed")
        self.assertEqual(case["executor_result"]["executor"], "public_sanitized_executor")
        self.assertEqual(case["executor_result"]["mode"], "deterministic_replay")
        self.assertFalse(case["executor_result"]["generated_live"])
        self.assertTrue(case["runtime_verifier_result"]["passed"])
        self.assertFalse(case["runtime_verifier_result"]["target_accessed"])
        self.assertEqual(case["adoption_gate_result"]["decision"], "candidate_adopted")
        self.assertEqual(case["decision_lock"]["status"], "locked")
        self.assertTrue(case["decision_lock"]["locked_before_scoring"])
        self.assertFalse(case["decision_lock"]["scorer_accessed"])
        self.assertEqual(
            case["post_lock_scorer_result"]["status"],
            "scored_after_decision_lock",
        )
        self.assertTrue(case["post_lock_scorer_result"]["lock_verified"])
        self.assertEqual(case["artifact_score"]["score"], 100)
        self.assertTrue(case["artifact_score"]["beneficial_flip"])
        self.assertFalse(case["artifact_score"]["harmful_flip"])

    def test_failed_verification_preserves_baseline_and_scores_90(self) -> None:
        report = run_replay(load_artifact(SAMPLE))
        case = next(item for item in report["cases"] if item["case_id"] == "demo-release-date")
        self.assertEqual(case["executor_result"]["status"], "executed")
        self.assertFalse(case["runtime_verifier_result"]["passed"])
        self.assertEqual(case["adoption_gate_result"]["decision"], "baseline_preserved")
        self.assertEqual(case["final_answer"], case["baseline_output"])
        self.assertTrue(case["preserved_baseline"])
        self.assertEqual(case["artifact_score"]["score"], 90)
        self.assertTrue(case["artifact_score"]["floor_preserved"])

    def test_denied_route_skips_executor_and_preserves_baseline(self) -> None:
        report = run_replay(load_artifact(SAMPLE))
        case = next(item for item in report["cases"] if item["case_id"] == "demo-human-review-hold")
        self.assertEqual(case["router_result"]["decision"], "route_denied")
        self.assertEqual(case["executor_result"]["status"], "skipped_by_route")
        self.assertEqual(case["executor_result"]["output"], "")
        self.assertEqual(case["runtime_verifier_result"]["status"], "not_run")
        self.assertEqual(case["adoption_gate_result"]["decision"], "baseline_preserved")
        self.assertEqual(case["artifact_score"]["score"], 90)

    def test_event_log_has_required_ordered_stages(self) -> None:
        report = run_replay(load_artifact(SAMPLE))
        expected = [
            "route",
            "execute",
            "runtime_verify",
            "adoption_gate",
            "decision_lock",
            "post_lock_score",
            "artifact_score",
            "log",
        ]
        for case in report["cases"]:
            self.assertEqual([event["stage"] for event in case["event_log"]], expected)
            self.assertEqual([event["step"] for event in case["event_log"]], list(range(1, 9)))
            self.assertIn("artifact_score", case)
            self.assertFalse(case["artifact_score"]["benchmark_metric"])

    def test_artifact_score_policy_includes_retained_and_harmful_cases(self) -> None:
        retained = score_artifact(
            baseline_passed=True,
            final_passed=True,
            adoption_gate_result={"decision": "candidate_adopted"},
        )
        harmful = score_artifact(
            baseline_passed=True,
            final_passed=False,
            adoption_gate_result={"decision": "candidate_adopted"},
        )
        unresolved = score_artifact(
            baseline_passed=False,
            final_passed=False,
            adoption_gate_result={"decision": "baseline_preserved"},
        )
        self.assertEqual(retained["score"], 70)
        self.assertEqual(harmful["score"], 0)
        self.assertFalse(harmful["floor_preserved"])
        self.assertEqual(unresolved["score"], 40)

    def test_outcome_classifier_includes_harmful_flip(self) -> None:
        self.assertEqual(classify_outcome(False, True), "beneficial_flip")
        self.assertEqual(classify_outcome(True, False), "harmful_flip")
        self.assertEqual(classify_outcome(True, True), "unchanged_correct")
        self.assertEqual(classify_outcome(False, False), "unchanged_incorrect")

    def test_reports_export_visible_pipeline(self) -> None:
        report = run_replay(load_artifact(SAMPLE))
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = export_reports(report, temp_dir)
            self.assertTrue(paths["json"].is_file())
            self.assertTrue(paths["html"].is_file())
            self.assertTrue(paths["summary"].is_file())
            parsed = json.loads(paths["json"].read_text(encoding="utf-8"))
            html = paths["html"].read_text(encoding="utf-8")
            summary = paths["summary"].read_text(encoding="utf-8")
            self.assertEqual(parsed["policy_label"], PUBLIC_POLICY_LABEL)
            self.assertIn(PUBLIC_POLICY_LABEL, html)
            self.assertIn(PUBLIC_POLICY_LABEL, summary)
            self.assertIn("Download JSON", html)
            self.assertIn("Download summary", html)
            self.assertIn("Open live BYOK", html)
            self.assertIn("Inspect live diagnostic", html)
            self.assertIn("https://omaragi.com/run", html)
            self.assertIn("Reliability BYOK Replay", html)
            self.assertIn("Live BYOK product · omaragi.com", html)
            self.assertIn("Public demo mode", html)
            self.assertIn("Real model execution with a user-supplied API key", html)
            self.assertIn("Sanitized deterministic replay", html)
            self.assertIn("Baseline</span><span>Router</span><span>Executor</span>", html)
            self.assertIn("<span>Runtime Verifier", html)
            self.assertIn("<span>Adoption Gate</span>", html)
            self.assertIn("<span>Decision Lock</span>", html)
            self.assertIn("<span>Post-lock Scorer</span>", html)
            self.assertIn("<span>Artifact Score</span>", html)
            self.assertIn("Skipped by route", html)
            self.assertIn("baseline preserved", html.lower())
            self.assertIn("Ordered decision trace", html)
            self.assertIn("8 recorded stages", html)
            self.assertIn("public demonstration score, not a benchmark metric", html)
            self.assertIn(
                "Baseline → Router → Executor → Runtime Verifier → Adoption Gate → "
                "Decision Lock → Post-lock Scorer → Scored Artifact",
                summary,
            )
            self.assertIn("## Runtime boundary", summary)
            self.assertIn("actual model execution", summary)
            self.assertIn("not benchmark evidence", summary)
            self.assertIn("Harmful flips: 0", summary)
            self.assertIn("Mean: 84.0/100", summary)
            self.assertIn("Sample delta: +40.0 percentage points", summary)

    def test_runtime_projection_excludes_post_lock_scoring(self) -> None:
        artifact = load_artifact(SAMPLE)
        runtime_case = build_runtime_case(artifact["cases"][0])
        self.assertNotIn("post_lock_scoring", runtime_case)
        self.assertNotIn("expected", runtime_case["runtime_verification"])

    def test_scoring_target_cannot_change_locked_decision(self) -> None:
        artifact = load_artifact(SAMPLE)
        original = run_replay(artifact)
        changed = json.loads(json.dumps(artifact))
        changed["cases"][0]["post_lock_scoring"]["expected"] = "999"
        rescored = run_replay(changed)

        original_case = original["cases"][0]
        rescored_case = rescored["cases"][0]
        self.assertEqual(original_case["final_answer"], rescored_case["final_answer"])
        self.assertEqual(
            original_case["adoption_gate_result"], rescored_case["adoption_gate_result"]
        )
        self.assertEqual(
            original_case["decision_lock"]["decision_sha256"],
            rescored_case["decision_lock"]["decision_sha256"],
        )
        self.assertNotEqual(
            original_case["post_lock_scorer_result"]["final"]["passed"],
            rescored_case["post_lock_scorer_result"]["final"]["passed"],
        )

    def test_non_synthetic_artifact_is_rejected(self) -> None:
        payload = json.loads(SAMPLE.read_text(encoding="utf-8"))
        payload["synthetic"] = False
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "unsafe.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ReplayArtifactError, "explicitly synthetic"):
                load_artifact(path)


if __name__ == "__main__":
    unittest.main()

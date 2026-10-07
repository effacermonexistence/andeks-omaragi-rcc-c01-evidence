from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app
import benchmark_replay_harness as replay
import reconstructed_matched_live_harness as reconstructed
import reports
import run_hallucination_hint_v8_heldout100 as factuality_runner


class ByokZeroDownliftGlobalGateTests(unittest.TestCase):
    def test_zero_downlift_adoption_receipt_is_publicly_allowlisted(self) -> None:
        self.assertIn(
            "zero_downlift_adoption.json",
            app.PUBLIC_RESULT_ARTIFACT_CONTENT_TYPES,
        )

    def test_control_report_and_manifest_never_publish_private_or_broken_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "run_request.json").write_text('{"private": true}\n')
            (run_dir / "skipped_cases.md").write_text("internal\n")
            (run_dir / "strongest_honest_claim.md").write_text("internal\n")
            app.write_control_layer_zero_downlift_adoption(
                lane_key="HaluEval_BYOK",
                spec=app.CONTROL_LAYER_BYOK_LANES["HaluEval_BYOK"],
                run_dir=run_dir,
                summary_payload={},
                executed_case_count=1,
            )
            app.generate_control_layer_byok_report(
                run_id="run_public_artifact_contract",
                spec=app.CONTROL_LAYER_BYOK_LANES["HaluEval_BYOK"],
                sample_status={
                    "selected_provider": "openai",
                    "selected_model": "gpt-5-nano",
                    "executed_sample_count": 1,
                    "actual_executed_sample_count": 1,
                },
                run_dir=run_dir,
                command_display="test",
                returncode=0,
                duration_seconds=0.1,
            )

            results = json.loads((run_dir / "results.json").read_text())
            manifest = json.loads((run_dir / "repro_manifest.json").read_text())
            report = (run_dir / "report.html").read_text()

        public_names = set(app.PUBLIC_RESULT_ARTIFACT_CONTENT_TYPES)
        self.assertLessEqual(set(results["artifacts"]), public_names)
        self.assertLessEqual(set(manifest["files"]), public_names)
        self.assertEqual(
            manifest["report_url"],
            "/results/run_public_artifact_contract",
        )
        for private_name in (
            "run_request.json",
            "skipped_cases.md",
            "strongest_honest_claim.md",
            "report.html",
        ):
            self.assertNotIn(private_name, results["artifacts"])
            self.assertNotIn(private_name, manifest["files"])
            self.assertNotIn(f"/{private_name}\"", report)

    def test_all_control_lanes_emit_the_six_file_evidence_contract_without_fabrication(self) -> None:
        for lane_key, spec in app.CONTROL_LAYER_BYOK_LANES.items():
            with self.subTest(lane_key=lane_key), tempfile.TemporaryDirectory() as tmp:
                run_dir = Path(tmp)
                app.write_control_layer_zero_downlift_adoption(
                    lane_key=lane_key,
                    spec=spec,
                    run_dir=run_dir,
                    summary_payload={},
                    executed_case_count=1,
                )
                app.generate_control_layer_byok_report(
                    run_id=f"run_evidence_{lane_key}",
                    spec=spec,
                    sample_status={
                        "lane_key": lane_key,
                        "selected_provider": "openai",
                        "selected_model": "gpt-5-nano",
                        "executed_sample_count": 1,
                        "actual_executed_sample_count": 1,
                    },
                    run_dir=run_dir,
                    command_display="test",
                    returncode=0,
                    duration_seconds=0.1,
                )

                for name in app.CONTROL_LAYER_STANDARD_EVIDENCE_FILES:
                    self.assertTrue((run_dir / name).is_file(), f"{lane_key}:{name}")
                manifest = json.loads((run_dir / "repro_manifest.json").read_text())
                self.assertEqual(
                    manifest["standard_evidence_files"],
                    list(app.CONTROL_LAYER_STANDARD_EVIDENCE_FILES),
                )
                self.assertEqual(
                    manifest["standard_evidence_schema"],
                    app.CONTROL_LAYER_STANDARD_EVIDENCE_SCHEMA_VERSION,
                )
                self.assertTrue(manifest["raw_output_fabrication_forbidden"])
                self.assertTrue(manifest["derived_artifacts_labelled"])
                provenance = manifest["standard_artifact_provenance"]
                self.assertEqual(set(provenance), set(app.CONTROL_LAYER_STANDARD_EVIDENCE_FILES))
                for name in app.CONTROL_LAYER_STANDARD_EVIDENCE_FILES:
                    self.assertIn(name, provenance)
                raw_rows = [
                    json.loads(line)
                    for line in (run_dir / "raw_outputs.jsonl").read_text().splitlines()
                    if line.strip()
                ]
                if provenance["raw_outputs.jsonl"].get("status") == "derived_availability_record":
                    self.assertFalse(raw_rows[0]["raw_model_output_fabricated"])

                csv_rows = (run_dir / "results.csv").read_text().splitlines()
                self.assertEqual(len(csv_rows), 2)
                self.assertIn("run_summary_not_case_level", csv_rows[1])
                cost_text = (run_dir / "cost_summary.txt").read_text()
                self.assertIn("cost_usd=unavailable", cost_text)
                self.assertIn("api_keys_stored=false", cost_text)

    def test_security_and_utility_metrics_remain_separate(self) -> None:
        metrics = app.control_layer_auxiliary_metrics(
            "AgentDojo_Tool_Knowledge_BYOK",
            {
                "conditions": {
                    "baseline_heldout100": {
                        "attack_success_rate": 0.04,
                        "utility_rate": 0.48,
                    },
                    "hint_v2_heldout100": {
                        "attack_success_rate": 0.03,
                        "utility_rate": 0.46,
                    },
                }
            },
        )

        self.assertAlmostEqual(metrics["security"]["attack_success_rate_delta"], -0.01)
        self.assertAlmostEqual(metrics["utility"]["utility_rate_delta"], -0.02)
        self.assertEqual(metrics["primary_metric"], "attack_success_rate")
        self.assertEqual(metrics["comparison_condition_source"], "hint_v2_heldout100")
        self.assertEqual(metrics["comparison_condition_stage"], "raw_routed_condition")
        self.assertIn("separate", metrics["claim_boundary"].lower())

    def test_bipia_auxiliary_metrics_do_not_mislabel_gold_blind_gate_as_raw(self) -> None:
        metrics = app.control_layer_auxiliary_metrics(
            "BIPIA_BYOK",
            {
                "baseline": {"attack_success_rate": 0.8, "utility_rate": 0.6},
                "omar_hint_v16_gold_blind_gate": {
                    "attack_success_rate": 0.2,
                    "utility_rate": 0.6,
                },
            },
        )
        self.assertEqual(
            metrics["comparison_condition_source"],
            "omar_hint_v16_gold_blind_gate",
        )
        self.assertEqual(
            metrics["comparison_condition_stage"],
            "gold_blind_gate_condition",
        )
        self.assertEqual(metrics["security"]["comparison_attack_success_rate"], 0.2)
        self.assertNotIn("raw_routed_attack_success_rate", metrics["security"])

    def test_http_success_blank_normalization_fails_completed_pair_gate(self) -> None:
        pair = {
            "baseline": {
                "ok": False,
                "status": 200,
                "text": "",
                "error": "reasoning_budget_exhausted_without_visible_output",
            },
            "omar_rcc": {"ok": True, "status": 200, "text": "A"},
            "baseline_grade": {"ok": True, "score": 0},
            "omar_rcc_grade": {"ok": True, "score": 1},
        }
        self.assertTrue(app.matched_live_pair_execution_failed(pair))
        self.assertFalse(app.provider_policy_refusal_pair_is_scored(pair))

    def test_uncertified_candidate_cannot_replace_baseline_even_when_candidate_scores_higher(self) -> None:
        route = {"short_reason": "test"}
        harness: dict[str, object] = {}
        baseline = {"ok": True, "text": "baseline"}
        candidate = {"ok": True, "text": "candidate"}
        final, grade = replay.apply_model_substitute_baseline_safe_adoption(
            baseline=baseline,
            routed_candidate=candidate,
            baseline_grade={"ok": True, "score": 0, "grade": "incorrect"},
            routed_candidate_grade={"ok": True, "score": 1, "grade": "correct"},
            route_record=route,
            harness=harness,
            selected_model="same-model",
            historical_model="same-model",
            routed_call_path="test-routed-call",
        )

        self.assertEqual(final["text"], "baseline")
        self.assertEqual(grade["score"], 0)
        self.assertEqual(final["adoption_decision"], "baseline_fallback")
        self.assertEqual(route["adoption_signal_used"], "no_pre_score_verifier_certificate")
        self.assertTrue(route["candidate_grade_diagnostic_only"])
        self.assertFalse(route["scorer_visible_to_adoption"])

    def test_pre_score_certificate_can_adopt_without_using_candidate_grade(self) -> None:
        route = {"short_reason": "test"}
        harness: dict[str, object] = {}
        certificate = {
            "verifier_id": "shape_dominance_test_v1",
            "certified_safe_adoption": True,
            "gold_accessed": False,
            "scorer_visible": False,
            "row_id_visible": False,
            "decision_frozen_before_scoring": True,
        }
        final, grade = replay.apply_model_substitute_baseline_safe_adoption(
            baseline={"ok": True, "text": "ungradable baseline"},
            routed_candidate={"ok": True, "text": "structurally valid candidate"},
            baseline_grade={"ok": True, "score": 0, "grade": "incorrect"},
            # Deliberately keep the post-score candidate grade at zero.  The
            # adoption decision must depend only on the pre-score certificate.
            routed_candidate_grade={"ok": True, "score": 0, "grade": "incorrect"},
            route_record=route,
            harness=harness,
            selected_model="same-model",
            historical_model="same-model",
            routed_call_path="test-routed-call",
            pre_score_verifier_certificate=certificate,
        )

        self.assertEqual(final["text"], "structurally valid candidate")
        self.assertEqual(grade["score"], 0)
        self.assertEqual(route["adoption_decision"], "routed_candidate")
        self.assertEqual(route["adoption_signal_used"], "shape_dominance_test_v1")
        self.assertTrue(route["adoption_gold_blind"])
        self.assertFalse(route["scorer_visible_to_adoption"])

    def test_every_reconstructed_lane_has_global_delivery_floor(self) -> None:
        drift_guarded = {
            lane
            for lane, spec in reconstructed.RECONSTRUCTED_MATCHED_LIVE_SPECS.items()
            if spec.get("baseline_preserving_adoption_gate")
        }
        self.assertEqual(drift_guarded, set(reconstructed.RECONSTRUCTED_MATCHED_LIVE_SPECS))
        for lane, spec in reconstructed.RECONSTRUCTED_MATCHED_LIVE_SPECS.items():
            with self.subTest(lane=lane):
                self.assertEqual(
                    spec["adoption_policy"],
                    "strict_gold_blind_baseline_floor_no_uncertified_override",
                )

    def test_row_accounting_detects_accepted_b_even_when_net_uplift_is_positive(self) -> None:
        outputs = [
            {
                "baseline_grade": {"score": 0},
                "routed_candidate_grade": {"score": 1},
                "omar_rcc_grade": {"score": 1},
                "route": {"adoption_gate_active": False},
            },
            {
                "baseline_grade": {"score": 0},
                "routed_candidate_grade": {"score": 1},
                "omar_rcc_grade": {"score": 1},
                "route": {"adoption_gate_active": False},
            },
            {
                "baseline_grade": {"score": 1},
                "routed_candidate_grade": {"score": 0},
                "omar_rcc_grade": {"score": 0},
                "route": {"adoption_gate_active": False},
            },
        ]
        summary = app.routed_candidate_score_summary("UNLOCKED_TEST", outputs)

        self.assertGreater(summary["final_adopted_absolute_gain"], 0)
        self.assertEqual(summary["accepted_C"], 2)
        self.assertEqual(summary["accepted_B"], 1)
        self.assertEqual(summary["candidate_accepted_C"], 2)
        self.assertEqual(summary["candidate_accepted_B"], 1)
        self.assertFalse(summary["zero_downlift_invariant_pass"])
        guard = app.byok_zero_downlift_invariant_guard(summary)
        self.assertIsNotNone(guard)
        self.assertEqual(guard["error"], "BYOK_ACCEPTED_B_NONZERO")

    def test_strict_baseline_floor_has_zero_accepted_b(self) -> None:
        outputs = [
            {
                "baseline_grade": {"score": 1},
                "routed_candidate_grade": {"score": 0},
                "omar_rcc_grade": {"score": 1},
                "route": {
                    "adoption_gate_active": True,
                    "adoption_decision": "baseline_fallback",
                    "final_omar_rcc_source": "baseline_fallback",
                },
            }
        ]
        summary = app.routed_candidate_score_summary("GPQA_MatchedLive", outputs)

        self.assertEqual(summary["accepted_B"], 0)
        self.assertEqual(summary["candidate_accepted_B"], 1)
        self.assertFalse(summary["candidate_zero_downlift_invariant_pass"])
        self.assertEqual(summary["neutral_vs_baseline"], 1)
        self.assertTrue(summary["zero_downlift_invariant_pass"])
        self.assertIsNone(app.byok_zero_downlift_invariant_guard(summary))

    def test_uncertified_control_lane_keeps_raw_runner_output_diagnostic_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            payload = app.write_control_layer_zero_downlift_adoption(
                lane_key="HaluEval_BYOK",
                spec=app.CONTROL_LAYER_BYOK_LANES["HaluEval_BYOK"],
                run_dir=run_dir,
                summary_payload={
                    "conditions": {
                        "halueval_baseline": {"accuracy": 0.5},
                        "halueval_omar_hint_v9": {"accuracy": 1.0},
                    }
                },
                executed_case_count=100,
            )
            persisted = json.loads((run_dir / "zero_downlift_adoption.json").read_text())

        self.assertEqual(payload, persisted)
        self.assertEqual(payload["routed_candidate_metric"], 1.0)
        self.assertEqual(payload["raw_routed_candidate_metric"], 1.0)
        self.assertEqual(payload["pre_score_floor_candidate_metric"], 0.5)
        self.assertEqual(
            payload["unverified_model_draft_metric_diagnostic_only"],
            1.0,
        )
        self.assertEqual(payload["routed_candidate_metric_diagnostic_only"], 1.0)
        self.assertEqual(payload["canonical_final_metric"], 0.5)
        self.assertEqual(payload["accepted_B"], 0)
        self.assertEqual(payload["security_B"], 0)
        self.assertEqual(payload["canonical_final_accepted_B"], 0)
        self.assertIsNone(payload["certified_final_accepted_C"])
        self.assertIsNone(payload["certified_final_accepted_B"])
        self.assertEqual(
            payload[
                "runner_reported_canonical_candidate_accepted_B_diagnostic_only"
            ],
            None,
        )
        self.assertTrue(payload["zero_downlift_invariant_pass"])
        self.assertEqual(
            payload["zero_downlift_claim_status"],
            "canonical_floor_verified_by_fixed_pre_score_fallback",
        )
        self.assertEqual(payload["canonical_final_source"], "baseline_fallback")

    def test_headline_metrics_ignore_inactive_null_benchmark_conditions(self) -> None:
        summary = {
            "conditions": {
                "halueval_baseline": {"accuracy": None},
                "halueval_omar_hint_v8": {"accuracy": None},
                "truthfulqa_baseline": {"accuracy": 1.0},
                "truthfulqa_omar_hint_v8": {"accuracy": 1.0},
            }
        }

        self.assertEqual(
            app.control_layer_run_headline_metrics(summary),
            (1.0, 1.0, "+0.0% relative / +0.0pp (this run)", False),
        )

    def test_certified_control_lane_fails_closed_if_accepted_b_is_missing_or_nonzero(self) -> None:
        spec = app.CONTROL_LAYER_BYOK_LANES["ZebraLogic_BYOK"]
        for label, summary in (
            (
                "missing",
                {"n": 10, "baseline_correct": 2, "REVAS_final_correct": 8},
            ),
            (
                "nonzero",
                {"n": 10, "baseline_correct": 2, "REVAS_final_correct": 8, "accepted_B": 1},
            ),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                payload = app.write_control_layer_zero_downlift_adoption(
                    lane_key="ZebraLogic_BYOK",
                    spec=spec,
                    run_dir=Path(tmp),
                    summary_payload=summary,
                    executed_case_count=10,
                )
                self.assertFalse(payload["zero_downlift_invariant_pass"])

    def test_certified_control_lane_can_complete_only_with_explicit_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = app.write_control_layer_zero_downlift_adoption(
                lane_key="ZebraLogic_BYOK",
                spec=app.CONTROL_LAYER_BYOK_LANES["ZebraLogic_BYOK"],
                run_dir=Path(tmp),
                summary_payload={
                    "n": 10,
                    "baseline_correct": 2,
                    "REVAS_final_correct": 8,
                    "accepted_B": 0,
                },
                executed_case_count=10,
            )

        self.assertTrue(payload["certified_invariant_evidence_complete"])
        self.assertEqual(payload["certified_final_accepted_B"], 0)
        self.assertEqual(payload["accepted_B"], 0)
        self.assertTrue(payload["zero_downlift_invariant_pass"])

    def test_uncertified_runner_canonical_counts_are_not_relabelled_certified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = app.write_control_layer_zero_downlift_adoption(
                lane_key="HaluEval_BYOK",
                spec=app.CONTROL_LAYER_BYOK_LANES["HaluEval_BYOK"],
                run_dir=Path(tmp),
                summary_payload={
                    "conditions": {
                        "halueval_baseline": {"accuracy": 0.8},
                        "halueval_omar_hint_v9": {"accuracy": 0.8},
                    },
                    "raw_candidate_accepted_C": 1,
                    "raw_candidate_accepted_B": 1,
                    "canonical_final_accepted_C": 1,
                    "canonical_final_accepted_B": 1,
                },
                executed_case_count=5,
            )

        self.assertFalse(payload["certified_pre_score_adoption"])
        self.assertIsNone(payload["certified_final_accepted_C"])
        self.assertIsNone(payload["certified_final_accepted_B"])
        self.assertEqual(
            payload[
                "runner_reported_canonical_candidate_accepted_C_diagnostic_only"
            ],
            1,
        )
        self.assertEqual(
            payload[
                "runner_reported_canonical_candidate_accepted_B_diagnostic_only"
            ],
            1,
        )
        self.assertEqual(payload["canonical_final_accepted_B"], 0)
        self.assertEqual(payload["accepted_B"], 0)

    def test_uncertified_report_separates_operative_candidate_from_diagnostic_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            summary = {
                "conditions": {
                    "halueval_baseline": {"accuracy": 0.5},
                    "halueval_omar_hint_v9": {"accuracy": 1.0},
                },
                "accepted_C": 5,
                "accepted_B": 0,
            }
            (run_dir / "results_summary.json").write_text(json.dumps(summary))
            app.write_control_layer_zero_downlift_adoption(
                lane_key="HaluEval_BYOK",
                spec=app.CONTROL_LAYER_BYOK_LANES["HaluEval_BYOK"],
                run_dir=run_dir,
                summary_payload=summary,
                executed_case_count=10,
            )
            app.generate_control_layer_byok_report(
                run_id="run_1784366117429_5c09440d014d",
                spec=app.CONTROL_LAYER_BYOK_LANES["HaluEval_BYOK"],
                sample_status={
                    "selected_provider": "mistral",
                    "selected_model": "ministral-3b-2512",
                    "executed_sample_count": 10,
                    "actual_executed_sample_count": 10,
                },
                run_dir=run_dir,
                command_display="test",
                returncode=0,
                duration_seconds=1.0,
            )
            report = (run_dir / "report.html").read_text()
            results = json.loads((run_dir / "results.json").read_text())
            lane_receipt = json.loads(
                (run_dir / "lane_execution_receipt.json").read_text()
            )
            repro_manifest = json.loads(
                (run_dir / "repro_manifest.json").read_text()
            )

        self.assertIn("Raw routed candidate", report)
        self.assertIn("lane_execution_receipt.json", report)
        self.assertIn("Raw uplift; baseline preserved — verifier required", report)
        self.assertIn("Pre-score floor", report)
        self.assertIn("Raw candidate change", report)
        self.assertIn("+100.0% relative / +50.0pp (this run)", report)
        self.assertIn("Canonical delivered final", report)
        self.assertIn("baseline_fallback", report)
        self.assertIn("canonical floor verified", report)
        self.assertEqual(
            results["canonical_delivery_classification"],
            "BASELINE_PRESERVED_VERIFIER_REQUIRED",
        )
        self.assertEqual(
            results["verification_state"],
            "BASELINE_PRESERVED_VERIFIER_REQUIRED",
        )
        self.assertEqual(results["raw_routed_candidate_metric"], 1.0)
        self.assertEqual(results["pre_score_floor_candidate_metric"], 0.5)
        self.assertEqual(lane_receipt["lane_key"], "HaluEval_BYOK")
        self.assertTrue(lane_receipt["executed_path_verified"])
        self.assertEqual(
            repro_manifest["lane_execution_receipt_sha256"],
            lane_receipt["receipt_sha256"],
        )

    def test_zebra_report_keeps_numeric_uplift_and_verified_accepted_b(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            summary = {
                "n": 10,
                "baseline_correct": 2,
                "REVAS_final_correct": 8,
                "accepted_C": 6,
                "accepted_B": 0,
            }
            (run_dir / "summary.json").write_text(json.dumps(summary))
            app.write_control_layer_zero_downlift_adoption(
                lane_key="ZebraLogic_BYOK",
                spec=app.CONTROL_LAYER_BYOK_LANES["ZebraLogic_BYOK"],
                run_dir=run_dir,
                summary_payload=summary,
                executed_case_count=10,
            )
            app.generate_control_layer_byok_report(
                run_id="run_1784366117429_5c09440d014d",
                spec=app.CONTROL_LAYER_BYOK_LANES["ZebraLogic_BYOK"],
                sample_status={
                    "selected_provider": "anthropic",
                    "selected_model": "claude-haiku-4-5-20251001",
                    "executed_sample_count": 10,
                    "actual_executed_sample_count": 10,
                },
                run_dir=run_dir,
                command_display="test",
                returncode=0,
                duration_seconds=1.0,
            )
            report = (run_dir / "report.html").read_text()

        self.assertIn("+300.0% relative / +60.0pp (this run)", report)
        self.assertIn("verified; candidate accepted_B=0", report)
        self.assertIn("certified_pre_score_verifier_candidate", report)

    def test_control_report_refuses_to_invent_provider_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "explicit selected provider"):
                app.generate_control_layer_byok_report(
                    run_id="run_provider_missing",
                    spec=app.CONTROL_LAYER_BYOK_LANES["HaluEval_BYOK"],
                    sample_status={
                        "executed_sample_count": 1,
                        "actual_executed_sample_count": 1,
                    },
                    run_dir=Path(tmp),
                    command_display="test",
                    returncode=0,
                    duration_seconds=0.1,
                )

    def test_generic_report_keeps_unverified_draft_diagnostic_only(self) -> None:
        samples = [
            {"id": "row-1", "benchmark": "AIME", "family": "math", "gold": "x"},
            {"id": "row-2", "benchmark": "AIME", "family": "math", "gold": "y"},
        ]
        outputs = []
        for sample_id, baseline_score, candidate_score in (("row-1", 1, 1), ("row-2", 0, 1)):
            baseline = {"ok": True, "status": 200, "text": "baseline", "usage": {}}
            draft = {"ok": True, "status": 200, "text": "candidate", "usage": {}}
            outputs.append(
                {
                    "sample_id": sample_id,
                    "family": "math",
                    "baseline": baseline,
                    "routed_candidate": baseline,
                    "unverified_model_draft": draft,
                    "omar_rcc": baseline,
                    "baseline_grade": {"score": baseline_score, "grade": "CORRECT" if baseline_score else "INCORRECT"},
                    "routed_candidate_grade": {"score": baseline_score, "grade": "CORRECT" if baseline_score else "INCORRECT"},
                    "unverified_model_draft_grade": {"score": candidate_score, "grade": "CORRECT"},
                    "omar_rcc_grade": {"score": baseline_score, "grade": "CORRECT" if baseline_score else "INCORRECT"},
                    "route": {
                        "source_locked": True,
                        "chosen_strategy": "aime_test",
                        "adoption_gate_active": True,
                        "adoption_decision": "baseline_fallback",
                        "final_omar_rcc_source": "baseline_fallback",
                    },
                    "harness": {
                        "inputs_identical": False,
                        "baseline_call_path": "reconstructed_matched_live_baseline_call",
                        "omar_rcc_call_path": "strict_gold_blind_baseline_floor_final",
                    },
                }
            )
        score_meta = app.routed_candidate_score_summary("AIME_MatchedLive", outputs)
        sample_meta = {
            **score_meta,
            "requested_sample_count": 2,
            "available_sample_count": 2,
            "executed_sample_count": 2,
            "actual_executed_sample_count": 2,
            "capped_by": "none",
            "score_metric": "mean_score",
            "proof_status": "RECONSTRUCTED MATCHED LIVE ATTEMPT",
            "exactness_status": "RECONSTRUCTED_ONLY",
            "reconstructed_live_sample_count": 120,
            "claim_allowed_for_run": False,
            "selected_provider": "openai",
        }
        with tempfile.TemporaryDirectory() as tmp:
            prior = reports.RUNS_DIR
            reports.RUNS_DIR = Path(tmp)
            try:
                run_dir = reports.generate_run_report(
                    run_id="run_candidate_surface_test",
                    mode="BYOK_MODE",
                    model="gpt-4o",
                    subset="AIME_MatchedLive",
                    samples=samples,
                    run_outputs=outputs,
                    estimated_cost={},
                    sample_meta=sample_meta,
                )
            finally:
                reports.RUNS_DIR = prior
            report = (run_dir / "report.html").read_text()
            result = json.loads((run_dir / "results.json").read_text())
            lane_receipt = json.loads(
                (run_dir / "lane_execution_receipt.json").read_text()
            )
            repro_manifest = json.loads(
                (run_dir / "repro_manifest.json").read_text()
            )

        self.assertIn("Raw routed candidate", report)
        self.assertIn("lane_execution_receipt.json", report)
        self.assertIn("Benchmark result", report)
        self.assertIn("Raw candidate relative uplift", report)
        self.assertIn("Pre-score floor", report)
        self.assertIn("100.00%", report)
        self.assertIn("baseline_fallback", report)
        self.assertEqual(result["summary"]["benchmark_result_score"], 0.5)
        self.assertEqual(
            result["summary"]["unverified_model_draft_score_diagnostic_only"],
            1.0,
        )
        self.assertEqual(result["summary"]["omar_rcc_score"], 0.5)
        self.assertEqual(
            result["lane_taxonomy"]["matched_live_range_check"]["observed_relative_uplift"],
            0.0,
        )
        self.assertEqual(lane_receipt["lane_key"], "AIME_MatchedLive")
        self.assertTrue(lane_receipt["executed_path_verified"])
        self.assertEqual(
            repro_manifest["lane_execution_receipt_sha256"],
            lane_receipt["receipt_sha256"],
        )

    def test_retryable_provider_error_reaches_next_attempt_without_exc_scope_crash(self) -> None:
        payload = {
            "text": "No",
            "provider": "mistral",
            "id": "retry-success",
            "model": "mistral-small-latest",
            "usage": {},
        }
        with (
            patch.object(
                factuality_runner,
                "call_control_layer_text",
                side_effect=[RuntimeError("temporary provider reset"), payload],
            ) as provider_call,
            patch.object(factuality_runner, "is_retryable_provider_error", return_value=True),
            patch.object(factuality_runner, "provider_retry_delay_seconds", return_value=0),
            patch.object(factuality_runner.time, "sleep") as sleep_call,
        ):
            result = factuality_runner.call_openai(
                "system",
                "user",
                lambda text: text,
                "case-1",
                "halueval_baseline",
            )

        self.assertEqual(result["status"], "executed")
        self.assertEqual(result["parsed_answer"], "No")
        self.assertEqual(provider_call.call_count, 2)
        sleep_call.assert_called_once_with(0)


if __name__ == "__main__":
    unittest.main()

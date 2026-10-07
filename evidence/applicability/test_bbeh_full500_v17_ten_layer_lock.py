from __future__ import annotations

import gzip
import json
import re
import unittest
from pathlib import Path

import app
import benchmark_board
import benchmark_replay_harness as replay_lock
import usercustomize


RUN_ID = "revas_bbeh500_full_gold_blind_20260630"
SAMPLE_HASH = "3885e2e1389a5b5ff0a60f48bc43094c8b188cc735fd23db02935a123cda23e6"
SAMPLE_SET_ID = f"bbeh500_revas_full500_{SAMPLE_HASH}"
UPLIFT_BAND = "+194.5% BBEH500 REVAS gold-blind reproduction / accepted_B=0 patched replay"
ROUTE_MODE = "matched_live_bbeh500_revas_base1_executor_gold_blind"
PROMPT_MODE = "bbeh500_revas_base1_local_executor_no_rcc_llm"
ROUTE_LABEL = "bbeh500_revas_base1_executor_gold_blind"
SAMPLE_FILE = app.APP_ROOT / "samples" / "processed" / "bbeh_official_full500_v17.normalized.jsonl"
PROOF_DIR = app.APP_ROOT / "proof_manifests" / "audits" / RUN_ID
PROOF_FILES = (
    "bbeh500_full_gold_blind_run_summary.json",
    "bbeh500_full_gold_blind_run_outputs.jsonl",
    "bbeh500_after_word_sorting_floor_patch_offline_replay.json",
    "bbeh500_word_sorting_accepted_B_patch_report.md",
)


class BBEHFull500V17TenLayerLock(unittest.TestCase):
    """Hard drift fence: BBEH500 REVAS BYOK path must fail loudly if any layer regresses."""

    maxDiff = None

    def assertClose(self, actual: float, expected: float, places: int = 12) -> None:  # noqa: N802
        self.assertAlmostEqual(float(actual), float(expected), places=places)

    def test_layer_01_sample_file_identity_and_hash_are_locked(self) -> None:
        samples = app.historical_bbeh_live_samples()
        self.assertTrue(SAMPLE_FILE.exists())
        self.assertEqual(len(samples), 500)
        self.assertEqual(replay_lock.sample_ids_sha256([str(row["sample_id"]) for row in samples]), SAMPLE_HASH)
        self.assertEqual(len({str(row["sample_id"]) for row in samples}), 500)

    def test_layer_02_proof_summary_metrics_are_locked(self) -> None:
        summary = json.loads((PROOF_DIR / "bbeh500_full_gold_blind_run_summary.json").read_text(encoding="utf-8"))
        patch = json.loads((PROOF_DIR / "bbeh500_after_word_sorting_floor_patch_offline_replay.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["status"], "COMPLETED")
        self.assertEqual(summary["run_id"], RUN_ID)
        self.assertEqual(summary["model"], "gpt-4o")
        self.assertEqual(summary["n_rows"], 500)
        self.assertEqual(summary["actual_api_calls"], 500)
        self.assertEqual(summary["actual_api_calls_by_kind"], {"base1": 500})
        self.assertEqual(summary["base2_calls"], 0)
        self.assertEqual(summary["llm_gate_calls"], 0)
        self.assertEqual(summary["rcc_llm_calls"], 0)
        self.assertEqual(summary["forced_rcc_calls"], 0)
        self.assertTrue(summary["gold_blind_generation"])
        self.assertFalse(summary["gold_visible_before_final_lock"])
        self.assertFalse(summary["scorer_visible_to_route_executor_adoption"])
        self.assertEqual(summary["secret_scan"]["status"], "PASS")
        scores = summary["scores"]
        self.assertEqual(scores["base_only"]["correct"], 91)
        self.assertEqual(scores["REVAS_final"]["correct"], 268)
        self.assertClose(scores["base_only"]["accuracy"], 0.182)
        self.assertClose(scores["REVAS_final"]["accuracy"], 0.536)
        self.assertEqual(patch["summary"]["base"], 91)
        self.assertEqual(patch["summary"]["patched_final"], 268)
        self.assertEqual(patch["summary"]["accepted_C"], 177)
        self.assertEqual(patch["summary"]["accepted_B"], 0)

    def test_layer_03_all_required_artifacts_exist_and_are_readable(self) -> None:
        for name in PROOF_FILES:
            path = PROOF_DIR / name
            self.assertTrue(path.exists(), name)
            self.assertGreater(path.stat().st_size, 0, name)
        with (PROOF_DIR / "bbeh500_full_gold_blind_run_outputs.jsonl").open("rt", encoding="utf-8") as handle:
            first = json.loads(handle.readline())
        self.assertIn("row_id", first)

    def test_layer_04_no_secret_material_is_committed_in_bbeh_artifacts(self) -> None:
        secret_pattern = re.compile(r"sk-proj-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|Authorization:\\s*Bearer\\s+sk-", re.I)
        for path in [SAMPLE_FILE, *(PROOF_DIR / name for name in PROOF_FILES)]:
            self.assertIsNone(secret_pattern.search(path.read_text(encoding="utf-8", errors="replace")), str(path))

    def test_layer_05_benchmark_board_row_is_locked_to_full500(self) -> None:
        row = next(item for item in benchmark_board.board_payload()["benchmarks"] if item["benchmark"] == "BBEH")
        self.assertEqual(row["family"], "anti-family reasoning benchmark / REVAS base1/local-executor substrate")
        self.assertEqual(row["n"], "500 BYOK/full REVAS")
        self.assertEqual(row["uplift"], "+194.5%")

    def test_layer_06_landing_aggregate_numbers_are_locked(self) -> None:
        stats = app.aggregate_replay_signal_stats()
        self.assertEqual(stats["lane_count"], 19)
        self.assertEqual(stats["evidence_row_count"], 19)
        self.assertEqual(stats["known_samples"], 9043)
        self.assertEqual(stats["actual_known_samples"], 9043)
        self.assertClose(stats["relative_mean"], 38.404985533793216)
        self.assertClose(stats["point_delta"], 12.679667874013123)
        self.assertClose(stats["baseline_mean"], 0.6066996729173483)
        self.assertClose(stats["omar_mean"], 0.7334963516574795)

    def test_layer_07_runtime_overlay_cannot_revert_to_old_aggregate(self) -> None:
        usercustomize._install_aggregate(app)
        stats = app.aggregate_replay_signal_stats()
        self.assertEqual(stats["evidence_row_count"], 19)
        self.assertEqual(stats["known_samples"], 9043)
        self.assertEqual(stats["actual_known_samples"], 9043)
        self.assertClose(stats["relative_mean"], 38.404985533793216)
        source = Path(usercustomize.__file__).read_text(encoding="utf-8")
        self.assertIn("simpleqa_vsf_removed=True", source)
        self.assertNotIn('case_units=3200 mean=90.98', source)

    def test_layer_08_backend_status_route_stamp_is_locked(self) -> None:
        status = app.bbeh_matched_live_reproduction_status()
        self.assertEqual(status["status"], "READY_BBEH500_REVAS")
        self.assertEqual(status["sample_count"], 500)
        self.assertEqual(status["available_sample_count"], 500)
        self.assertEqual(status["claim_eligible_rows"], 500)
        self.assertEqual(status["sample_ids_sha256"], SAMPLE_HASH)
        self.assertEqual(status["route_mode"], ROUTE_MODE)
        self.assertEqual(status["prompt_mode"], PROMPT_MODE)
        self.assertTrue(status["deterministic_answerers_used"])
        self.assertFalse(status["api_key_logged"])

    def test_layer_09_byok_smoke_and_full500_boundaries_are_locked(self) -> None:
        smoke = app.matched_live_bbeh_sample_status(20)
        full = app.matched_live_bbeh_sample_status(500)
        self.assertEqual(smoke["executed_sample_count"], 20)
        self.assertFalse(smoke["board_depth_claim_allowed"])
        self.assertFalse(smoke["claim_allowed_for_run"])
        self.assertIn("Below-board-depth BBEH preview", smoke["cap_reason"])
        self.assertEqual(full["executed_sample_count"], 500)
        self.assertTrue(full["board_depth_claim_allowed"])
        self.assertTrue(full["claim_allowed_for_run"])
        self.assertEqual(full["numeric_reproduction_gate"], "bbeh500_revas_gold_blind_artifact_locked; accepted_B0_floor_patch_replay; live smoke negative drift guard active")
        self.assertEqual(full["expected_relative_uplift_band"], UPLIFT_BAND)

    def test_layer_10_latest_public_live_check_is_locked(self) -> None:
        latest = app.LATEST_PUBLIC_LIVE_CHECKS["bbeh"]
        self.assertEqual(latest["run_id"], RUN_ID)
        self.assertEqual(latest["lane"], app.MATCHED_LIVE_BBEH_SUBSET)
        self.assertEqual(latest["sample_count"], 500)
        self.assertClose(latest["baseline_metric"], 0.182)
        self.assertClose(latest["omar_metric"], 0.536)
        self.assertClose(latest["relative_change"], 1.945054945054945)
        self.assertEqual(latest["expected_band"], UPLIFT_BAND)
        self.assertEqual(latest["numeric_range_gate"], "GOLD_BLIND_REVAS_ACCEPTED_B0")
        self.assertEqual(tuple(latest["raw_evidence_files"]), PROOF_FILES)

    def test_layer_11_replay_harness_locks_are_full500_not_old_100(self) -> None:
        lock = replay_lock.LOCKED_REPLAY_LANES[app.MATCHED_LIVE_BBEH_SUBSET]
        self.assertEqual(lock.route_mode, ROUTE_MODE)
        self.assertEqual(lock.prompt_mode, PROMPT_MODE)
        self.assertEqual(lock.sample_set_id, SAMPLE_SET_ID)
        self.assertEqual(lock.sample_count, 500)
        self.assertEqual(lock.sample_ids_sha256, SAMPLE_HASH)
        self.assertEqual(lock.route_label, ROUTE_LABEL)
        board_lock = replay_lock.MATCHED_LIVE_BOARD_PASS_LOCKS[app.MATCHED_LIVE_BBEH_SUBSET]
        self.assertEqual(board_lock.sample_count, 500)
        self.assertEqual(board_lock.sample_ids_sha256, SAMPLE_HASH)
        self.assertEqual(board_lock.expected_uplift_band, UPLIFT_BAND)
        self.assertEqual(board_lock.decision_label, "GOLD_BLIND_REVAS_ACCEPTED_B0")
        self.assertClose(board_lock.baseline_score, 0.182)
        self.assertClose(board_lock.omar_rcc_score, 0.536)

    def test_layer_12_replay_assertion_gate_rejects_drift(self) -> None:
        samples = app.historical_bbeh_live_samples()
        status = app.matched_live_bbeh_sample_status(500)
        replay_lock.assert_sample_ids_locked(app.MATCHED_LIVE_BBEH_SUBSET, [str(row["sample_id"]) for row in samples])
        replay_lock.assert_matched_live_board_pass_locked(
            app.MATCHED_LIVE_BBEH_SUBSET,
            [str(row["sample_id"]) for row in samples],
            status=status,
            public_live_check=app.LATEST_PUBLIC_LIVE_CHECKS["bbeh"],
        )
        drifted = [str(row["sample_id"]) for row in samples]
        drifted[-1] = drifted[-1] + "_DRIFT"
        with self.assertRaises(AssertionError):
            replay_lock.assert_sample_ids_locked(app.MATCHED_LIVE_BBEH_SUBSET, drifted)

    def test_layer_13_bbeh_source_text_has_byok_surface_phrases(self) -> None:
        source = Path(app.__file__).read_text(encoding="utf-8")
        for phrase in (
            "BBEH | Live 20 smoke / 500 Full500",
            "BBEH Full500 BYOK lane",
            "BBEH500 official-balanced 500-sample set",
            "claim_allowed_for_subset",
        ):
            self.assertIn(phrase, source)

    def test_layer_14_simpleqa_public_claim_surfaces_are_removed(self) -> None:
        statuses = app.ready_matched_live_backend_statuses()
        self.assertNotIn("SimpleQA Verified / VSF", statuses)
        board_names = [row["benchmark"] for row in benchmark_board.board_payload()["benchmarks"]]
        self.assertNotIn("SimpleQA Verified / VSF", board_names)
        self.assertNotIn("SimpleQA", board_names)
        evidence = app.omar_benchmark_evidence_standard_payload()["current_public_live_rows"]
        self.assertNotIn("simpleqa_verified_vsf", evidence)


    def test_layer_16_full500_rows_are_promoted_first_on_public_surface(self) -> None:
        board_names = [row["benchmark"] for row in benchmark_board.BENCHMARK_BOARD[:3]]
        self.assertEqual(board_names, ["ABCD", "ZebraLogicBench", "BBEH"])
        html = app.public_live_evidence_graph_section()
        zebra_pos = html.index('href="/run?subset=ZebraLogic_BYOK')
        bbeh_pos = html.index('href="/run?subset=BBEH_MatchedLive')
        bipia_pos = html.index('href="/run?subset=BIPIA_BYOK')
        hle_pos = html.index('href="/run?subset=HLE_MatchedLive')
        lower_control_pos = html.index('id="control-layer-smoke"')
        self.assertNotIn('SimpleQA Verified / VSF', html)
        self.assertNotIn('href="/run?subset=SimpleQA_Verified_VSF_MatchedLive', html)
        self.assertNotIn('href="/run?subset=LiveBench_BYOK', html)
        self.assertNotIn('LiveBench500 post-dev', html)
        self.assertLess(zebra_pos, bbeh_pos)
        self.assertLess(bbeh_pos, bipia_pos)
        self.assertLess(bipia_pos, hle_pos)
        self.assertNotIn('href="/run?subset=BIPIA_BYOK', html[lower_control_pos:])

    def test_layer_15_locked_manifest_exports_full500_values(self) -> None:
        manifest = replay_lock.replay_lock_manifest()
        lane = manifest["locked_lanes"][app.MATCHED_LIVE_BBEH_SUBSET]
        board = manifest["matched_live_board_pass_locks"][app.MATCHED_LIVE_BBEH_SUBSET]
        self.assertEqual(lane["sample_count"], 500)
        self.assertEqual(lane["sample_ids_sha256"], SAMPLE_HASH)
        self.assertEqual(board["sample_count"], 500)
        self.assertEqual(board["run_id"], RUN_ID)
        self.assertEqual(board["raw_evidence_files"], PROOF_FILES)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from bbeh_recovered_harness import bbeh_grade_answer  # noqa: E402
from benchmark_executors.bbeh_executor_backed_routing import (  # noqa: E402
    ExecutorInput,
    evaluate_revas_route,
)

RUN_DIR = Path(__file__).resolve().parent
DATASET_PATH = REPO / "samples/processed/bbeh_official_full500_v17.normalized.jsonl"
OUT_JSONL = RUN_DIR / "bbeh500_full_gold_blind_run_outputs.jsonl"
SUMMARY_PATH = RUN_DIR / "bbeh500_full_gold_blind_run_summary.json"
EXECUTED_MANIFEST_PATH = RUN_DIR / "bbeh500_full_gold_blind_run_manifest_executed.json"
FREEZE_MANIFEST_PATH = RUN_DIR / "bbeh500_full_gold_blind_freeze_manifest.json"
ROW_PREVIEW_CSV = RUN_DIR / "bbeh500_full_gold_blind_row_preview.csv"
FAMILY_METRICS_CSV = RUN_DIR / "bbeh500_full_gold_blind_family_metrics.csv"
EXECUTOR_METRICS_CSV = RUN_DIR / "bbeh500_full_gold_blind_executor_metrics.csv"
RUN_REPORT = RUN_DIR / "bbeh500_full_gold_blind_run_report.md"
PROTOCOL_LOG = RUN_DIR / "bbeh500_full_gold_blind_protocol_log.txt"
SECRET_SCAN = RUN_DIR / "bbeh500_full_gold_blind_secret_scan.txt"
CHAT_URL = "https://api.openai.com/v1/chat/completions"
HARD_CALL_CAP = 500
MODEL = os.environ.get("BBEH500_MODEL", "gpt-4o")
TEMPERATURE = 0.2
MAX_TOKENS = 256
BASE_SYSTEM = "You are a careful benchmark solver. Return only the final answer. No explanation."
RUN_ID = "revas_bbeh500_full_gold_blind_20260630"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise SystemExit("Missing OPENAI_API_KEY; no API calls made")
    return key


class Budget:
    def __init__(self, cap: int) -> None:
        self.cap = cap
        self.calls = 0
        self.by_kind: Counter[str] = Counter()

    def reserve(self, kind: str) -> None:
        if self.calls + 1 > self.cap:
            raise RuntimeError(f"API hard cap exceeded before {kind}: {self.calls + 1}>{self.cap}")
        self.calls += 1
        self.by_kind[kind] += 1


def chat(system: str, user: str, *, budget: Budget, kind: str) -> tuple[str, dict[str, Any]]:
    budget.reserve(kind)
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }
    req = urllib.request.Request(
        CHAT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + api_key(), "Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        choice = data["choices"][0]
        return (choice["message"].get("content") or "").strip(), {
            "ok": True,
            "kind": kind,
            "latency_ms": int((time.time() - started) * 1000),
            "usage": data.get("usage") or {},
            "model_returned": data.get("model"),
            "finish_reason": choice.get("finish_reason"),
        }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:1200]
        raise RuntimeError(f"{kind} HTTP {exc.code}: {body}") from exc


def row_id(row: dict[str, Any]) -> str:
    return str(row.get("sample_id") or row.get("id") or row.get("row_id"))


def family(row: dict[str, Any]) -> str:
    return str(row.get("source_task") or row.get("task") or row.get("family") or "")


def question(row: dict[str, Any]) -> str:
    return str(row.get("question") or row.get("prompt") or row.get("input") or "")


def gold(row: dict[str, Any]) -> Any:
    return row.get("gold", row.get("expected_answer", row.get("answer", row.get("target"))))


def score(ans: str | None, expected: Any) -> int:
    return int((bbeh_grade_answer(ans or "", expected or "") or {}).get("score") or 0)


def prompt(row: dict[str, Any]) -> str:
    return (
        f"Benchmark: BBEH\nTask/family: {family(row)}\nSample id: {row_id(row)}\n\n"
        f"Question:\n{question(row)}\n\nReturn only the final answer. No explanation."
    )


def load_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with DATASET_PATH.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    rows.sort(key=lambda r: int(r.get("full500_index", len(rows))))
    if len(rows) != 500:
        raise RuntimeError(f"expected 500 rows, got {len(rows)}")
    return rows


def add_usage(total: Counter[str], meta: dict[str, Any], prefix: str) -> None:
    for k, v in (meta.get("usage") or {}).items():
        if isinstance(v, (int, float)):
            total[prefix + k] += v


def secret_scan_text(paths: list[Path]) -> dict[str, Any]:
    hits: list[str] = []
    for p in paths:
        if not p.exists() or not p.is_file():
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        if "sk-proj-" in txt or "sk-" in txt:
            hits.append(str(p))
    SECRET_SCAN.write_text("\n".join(hits) if hits else "NO_SECRET_STRINGS_FOUND\n", encoding="utf-8")
    return {"hits": hits, "status": "PASS" if not hits else "FAIL", "scan_file": str(SECRET_SCAN)}


def write_preview_and_freeze(rows: list[dict[str, Any]], unit_result: dict[str, Any]) -> None:
    with ROW_PREVIEW_CSV.open("w", newline="", encoding="utf-8") as f:
        fields = ["row_index", "row_id", "family", "question_sha256", "allowed_for_benchmark_claim", "base1_call_planned", "executor_local_call_planned", "gold_loaded_before_final_lock"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(rows):
            w.writerow({
                "row_index": i,
                "row_id": row_id(r),
                "family": family(r),
                "question_sha256": r.get("question_sha256", ""),
                "allowed_for_benchmark_claim": r.get("allowed_for_benchmark_claim"),
                "base1_call_planned": True,
                "executor_local_call_planned": True,
                "gold_loaded_before_final_lock": False,
            })
    freeze = {
        "run_id": RUN_ID,
        "created_utc": now(),
        "dataset_path": str(DATASET_PATH),
        "dataset_hash": sha_file(DATASET_PATH),
        "n_rows": len(rows),
        "row_ids": [row_id(r) for r in rows],
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "planned_api_calls": {"base1": 500, "base2": 0, "llm_gate": 0, "rcc_llm": 0, "forced_rcc": 0, "total": 500, "hard_cap": HARD_CALL_CAP},
        "primary_control": "base_only",
        "primary_system": "REVAS_final_fact_aware",
        "fallback_policy": "base1_answer",
        "gold_visible_before_final_lock": False,
        "scorer_visible_to_route_executor_adoption": False,
        "executor_code_hash": sha_file(REPO / "benchmark_executors/bbeh_executor_backed_routing.py"),
        "test_file_hash": sha_file(REPO / "tests/test_bbeh_executor_backed_routing.py"),
        "base_system_hash": sha_text(BASE_SYSTEM),
        "unit_test_result_pre_run": unit_result,
        "claim_allowed": False,
        "public_claim_allowed_pending_audit": False,
        "boundary": "BBEH full500 post-dev gold-blind reproduction. Not a clean unseen holdout because REVAS was developed/audited against BBEH family artifacts; public claim requires separate audit/provenance lock.",
    }
    FREEZE_MANIFEST_PATH.write_text(json.dumps(freeze, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    if SUMMARY_PATH.exists():
        raise SystemExit("run summary exists; rerun blocked")
    started = now()
    rows = load_rows()
    unit = subprocess.run(["python3", "-m", "unittest", "tests.test_bbeh_executor_backed_routing"], cwd=REPO, text=True, capture_output=True)
    unit_result = {"cmd": "python3 -m unittest tests.test_bbeh_executor_backed_routing", "exit_code": unit.returncode, "stdout": unit.stdout, "stderr": unit.stderr}
    if unit.returncode != 0:
        raise SystemExit(unit.stdout + unit.stderr)
    write_preview_and_freeze(rows, unit_result)

    budget = Budget(HARD_CALL_CAP)
    usage_total: Counter[str] = Counter()
    records: list[dict[str, Any]] = []
    OUT_JSONL.write_text("", encoding="utf-8")
    PROTOCOL_LOG.write_text(f"{started} START BBEH500 full gold-blind REVAS run\n", encoding="utf-8")

    try:
        for idx, row in enumerate(rows):
            rid = row_id(row)
            fam = family(row)
            q = question(row)
            # Gold-blind section: no gold/scorer before base and REVAS final are locked.
            base_answer, base_meta = chat(BASE_SYSTEM, prompt(row), budget=budget, kind="base1")
            item = ExecutorInput(row_id=rid, family=fam, question_text=q, metadata={"question_sha256": row.get("question_sha256", "")})
            revas = evaluate_revas_route(item, base_answer, fallback_source="base1_answer", fact_policy="fact_aware")
            final_answer = revas.final_answer
            final_source = revas.final_source
            # Scoring starts only after final answer lock.
            g = gold(row)
            base_correct = score(base_answer, g)
            executor_correct = score(revas.executor_answer, g) if revas.executor_answer is not None else None
            final_correct = score(final_answer, g)
            rec = {
                "row_index": idx,
                "row_id": rid,
                "family": fam,
                "question_sha256": row.get("question_sha256", ""),
                "base_answer_locked_before_scoring": base_answer,
                "revas_final_answer_locked_before_scoring": final_answer,
                "executor_answer_locked_before_scoring": revas.executor_answer,
                "gold": g,
                "base_correct": base_correct,
                "executor_correct": executor_correct,
                "revas_final_correct": final_correct,
                "accepted_C_vs_base": (not bool(base_correct)) and bool(final_correct),
                "accepted_B_vs_base": bool(base_correct) and (not bool(final_correct)),
                "semantic_RCC_friendly": revas.semantic_RCC_friendly,
                "semantic_route_class": revas.semantic_route_class,
                "REVAS_override_supported": revas.REVAS_supported,
                "REVAS_support_reason": revas.REVAS_support_reason,
                "executor_available": revas.executor_available,
                "executor_name": revas.executor_name,
                "parser_success": revas.parser_success,
                "verifier_success": revas.verifier_success,
                "answer_format_valid": revas.answer_format_valid,
                "adoption_gate_accepts": revas.adoption_gate_accepts,
                "final_source": final_source,
                "fallback_source": revas.fallback_source,
                "coverage_gap_category": revas.coverage_gap_category,
                "used_capital_facts": revas.used_capital_facts,
                "capital_fact_keys_used": list(revas.capital_fact_keys_used),
                "factual_lookup_used": revas.factual_lookup_used,
                "pure_symbolic_ast_only": revas.pure_symbolic_ast_only,
                "fact_table_version_hash": revas.fact_table_version_hash,
                "fact_table_count": revas.fact_table_count,
                "trace": revas.trace,
                "api_meta": {"base1": base_meta, "base2_calls": 0, "llm_gate_calls": 0, "rcc_llm_calls": 0, "forced_rcc_calls": 0},
                "gold_hidden_until_after_final_lock": True,
                "scorer_visible_to_route_executor_adoption": False,
                "claim_allowed": False,
            }
            records.append(rec)
            add_usage(usage_total, base_meta, "base1_")
            with OUT_JSONL.open("a", encoding="utf-8") as out:
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            with PROTOCOL_LOG.open("a", encoding="utf-8") as log:
                log.write(f"{now()} row={idx} id={rid} base={base_correct} revas={final_correct} source={final_source} calls={budget.calls}\n")
            print(json.dumps({"row": idx + 1, "base": base_correct, "revas": final_correct, "source": final_source, "calls": budget.calls}, ensure_ascii=False), flush=True)
    except Exception as exc:
        partial = {
            "status": "ERROR_PARTIAL_NO_RERUN",
            "error": repr(exc),
            "started_utc": started,
            "finished_utc": now(),
            "api_calls_attempted": budget.calls,
            "rows_completed": len(records),
            "rerun_allowed": False,
        }
        SUMMARY_PATH.write_text(json.dumps(partial, ensure_ascii=False, indent=2), encoding="utf-8")
        raise

    if budget.calls != HARD_CALL_CAP:
        raise SystemExit(f"call count mismatch: {budget.calls} != {HARD_CALL_CAP}")

    n = len(records)
    base_n = sum(int(r["base_correct"]) for r in records)
    final_n = sum(int(r["revas_final_correct"]) for r in records)
    exec_n = sum(int(r["executor_correct"] or 0) for r in records)
    accepted_c = sum(1 for r in records if r["accepted_C_vs_base"])
    accepted_b = sum(1 for r in records if r["accepted_B_vs_base"])
    blocked_b = sum(1 for r in records if bool(r["base_correct"]) and r["executor_correct"] == 0 and r["final_source"] != "executor_override_accepted")
    supported_n = sum(1 for r in records if r["REVAS_override_supported"])
    override_n = sum(1 for r in records if r["final_source"] == "executor_override_accepted")
    semantic_friendly_n = sum(1 for r in records if r["semantic_RCC_friendly"])

    fam_counts: dict[str, Counter[str]] = defaultdict(Counter)
    exec_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for r in records:
        c = fam_counts[r["family"]]
        c["rows"] += 1
        c["base_correct"] += int(r["base_correct"])
        c["executor_correct"] += int(r["executor_correct"] or 0)
        c["revas_final_correct"] += int(r["revas_final_correct"])
        c["accepted_C"] += int(r["accepted_C_vs_base"])
        c["accepted_B"] += int(r["accepted_B_vs_base"])
        c["REVAS_override_supported"] += int(r["REVAS_override_supported"])
        c["override_accepted"] += int(r["final_source"] == "executor_override_accepted")
        en = r["executor_name"] or "none"
        ec = exec_counts[en]
        ec["rows_seen"] += 1
        ec["rows_supported"] += int(r["REVAS_override_supported"])
        ec["override_accepted"] += int(r["final_source"] == "executor_override_accepted")
        ec["accepted_C"] += int(r["accepted_C_vs_base"])
        ec["accepted_B"] += int(r["accepted_B_vs_base"])
        ec["net_gain"] += int(r["accepted_C_vs_base"]) - int(r["accepted_B_vs_base"])

    with FAMILY_METRICS_CSV.open("w", newline="", encoding="utf-8") as f:
        fields = ["family", "rows", "base_correct", "executor_correct", "revas_final_correct", "accepted_C", "accepted_B", "REVAS_override_supported", "override_accepted"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for fam, c in sorted(fam_counts.items()):
            w.writerow({"family": fam, **dict(c)})

    with EXECUTOR_METRICS_CSV.open("w", newline="", encoding="utf-8") as f:
        fields = ["executor_name", "rows_seen", "rows_supported", "override_accepted", "accepted_C", "accepted_B", "net_gain"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for en, c in sorted(exec_counts.items()):
            w.writerow({"executor_name": en, **dict(c)})

    scan = secret_scan_text([OUT_JSONL, SUMMARY_PATH, EXECUTED_MANIFEST_PATH, FAMILY_METRICS_CSV, EXECUTOR_METRICS_CSV, RUN_REPORT, PROTOCOL_LOG, FREEZE_MANIFEST_PATH, ROW_PREVIEW_CSV])
    summary = {
        "status": "COMPLETED",
        "run_id": RUN_ID,
        "sample_type": "BBEH_full500_post_dev_gold_blind_reproduction_not_clean_unseen_holdout",
        "dataset_path": str(DATASET_PATH),
        "dataset_hash": sha_file(DATASET_PATH),
        "started_utc": started,
        "finished_utc": now(),
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "n_rows": n,
        "expected_api_calls": HARD_CALL_CAP,
        "actual_api_calls": budget.calls,
        "actual_api_calls_by_kind": dict(budget.by_kind),
        "base2_calls": 0,
        "llm_gate_calls": 0,
        "rcc_llm_calls": 0,
        "forced_rcc_calls": 0,
        "gold_blind_generation": True,
        "gold_visible_before_final_lock": False,
        "scorer_visible_to_route_executor_adoption": False,
        "claim_allowed": False,
        "BBEH_wide_public_claim_allowed_pending_audit": False,
        "rerun_allowed": False,
        "policy_mutation_during_run": False,
        "scores": {
            "base_only": {"correct": base_n, "total": n, "accuracy": base_n / n},
            "executor_raw": {"correct": exec_n, "total": n, "accuracy": exec_n / n},
            "REVAS_final": {"correct": final_n, "total": n, "accuracy": final_n / n},
        },
        "delta_vs_base_only": {"rows": final_n - base_n, "percentage_points": (final_n - base_n) / n * 100, "relative_uplift_percent": ((final_n - base_n) / base_n * 100) if base_n else None},
        "accepted_C_vs_base": accepted_c,
        "accepted_B_vs_base": accepted_b,
        "blocked_B_vs_base": blocked_b,
        "semantic_RCC_friendly": semantic_friendly_n,
        "REVAS_override_supported": supported_n,
        "override_accepted": override_n,
        "api_usage_actual": dict(usage_total),
        "unit_test_result_pre_run": unit_result,
        "executor_code_hash": sha_file(REPO / "benchmark_executors/bbeh_executor_backed_routing.py"),
        "base_system_hash": sha_text(BASE_SYSTEM),
        "secret_scan": scan,
        "output_jsonl": str(OUT_JSONL),
        "family_metrics_csv": str(FAMILY_METRICS_CSV),
        "executor_metrics_csv": str(EXECUTOR_METRICS_CSV),
        "executor_metrics": {k: dict(v) for k, v in sorted(exec_counts.items())},
        "rows": records,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    EXECUTED_MANIFEST_PATH.write_text(json.dumps({"status": "EXECUTED_ONCE_COMPLETED", **summary, "row_ids": [r["row_id"] for r in records]}, ensure_ascii=False, indent=2), encoding="utf-8")
    RUN_REPORT.write_text(
        f"# BBEH500 full gold-blind REVAS run\n\n"
        f"Status: COMPLETED\n\n"
        f"- sample_type: BBEH full500 post-dev gold-blind reproduction, not clean unseen holdout\n"
        f"- base_only: {base_n}/{n} ({base_n/n*100:.1f}%)\n"
        f"- executor_raw: {exec_n}/{n} ({exec_n/n*100:.1f}%)\n"
        f"- REVAS_final: {final_n}/{n} ({final_n/n*100:.1f}%)\n"
        f"- delta_vs_base_only: {final_n-base_n} rows / {(final_n-base_n)/n*100:.1f}pp / {(((final_n-base_n)/base_n*100) if base_n else 0):.2f}% relative\n"
        f"- accepted_C_vs_base: {accepted_c}\n"
        f"- accepted_B_vs_base: {accepted_b}\n"
        f"- blocked_B_vs_base: {blocked_b}\n"
        f"- semantic_RCC_friendly: {semantic_friendly_n}/{n}\n"
        f"- REVAS_override_supported: {supported_n}/{n}\n"
        f"- override_accepted: {override_n}/{n}\n"
        f"- actual_api_calls: {budget.calls}\n"
        f"- base2/LLM gate/RCC LLM/forced RCC calls: 0\n"
        f"- gold hidden until after final lock: true\n"
        f"- claim_allowed: false pending audit\n"
        f"- secret_scan: {scan['status']}\n",
        encoding="utf-8",
    )
    scan = secret_scan_text([OUT_JSONL, SUMMARY_PATH, EXECUTED_MANIFEST_PATH, FAMILY_METRICS_CSV, EXECUTOR_METRICS_CSV, RUN_REPORT, PROTOCOL_LOG, FREEZE_MANIFEST_PATH, ROW_PREVIEW_CSV])
    print(json.dumps({
        "status": "COMPLETED",
        "actual_api_calls": budget.calls,
        "base_only": [base_n, n],
        "executor_raw": [exec_n, n],
        "REVAS_final": [final_n, n],
        "delta_rows": final_n - base_n,
        "accepted_C": accepted_c,
        "accepted_B": accepted_b,
        "blocked_B": blocked_b,
        "semantic_RCC_friendly": semantic_friendly_n,
        "REVAS_override_supported": supported_n,
        "override_accepted": override_n,
        "secret_scan": scan["status"],
        "summary_path": str(SUMMARY_PATH),
    }, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Post-request package integrity only. Never imports or runs assessed RCC code."""

import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main():
    files = {
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts
    }
    manifest = {}
    for line in (ROOT / "PACKAGE_SHA256SUMS.txt").read_text().splitlines():
        checksum, path = line.split("  ", 1)
        assert path not in manifest, f"Duplicate checksum entry: {path}"
        manifest[path] = checksum
        assert digest(ROOT / path) == checksum, f"Checksum mismatch: {path}"
    assert set(manifest) == files - {"PACKAGE_SHA256SUMS.txt"}
    with (ROOT / "ARTIFACT_REGISTER.csv").open(newline="") as handle:
        register = list(csv.DictReader(handle))
    assert len({r["artifact_id"] for r in register}) == len(register)
    assert len({r["package_path"] for r in register}) == len(register)
    assert {r["package_path"] for r in register} == files
    for row in register:
        path = row["package_path"]
        if path in {"ARTIFACT_REGISTER.csv", "PACKAGE_SHA256SUMS.txt"}:
            continue
        assert row["public_sha256"] == digest(ROOT / path), path
        assert int(row["public_bytes"]) == (ROOT / path).stat().st_size, path

    acquisition = load("provenance/source_acquisition.json")
    for item in acquisition["published_artifacts"]:
        path = ROOT / item["package_path"]
        assert digest(path) == item["public_sha256"]
        assert item["original_timestamp"] < "2026-10-06"
        if item["publication_form"] == "PRESERVED_PRE_EXISTING_COPY":
            assert digest(path) == item["source_sha256"]
        if item["publication_form"] == "REDACTED_PUBLIC_COPY_OF_PRE_EXISTING_EVIDENCE":
            reconstructed = path.read_bytes().replace(
                b"[REDACTED_LOCAL_WORKSPACE]",
                b"/Users/effacermonexistencecodex/Code/omar-migration/omar-os1",
            )
            assert hashlib.sha256(reconstructed).hexdigest() == item["source_sha256"]

    report = load("evidence/path_identity/public_replay/examples/example_report.json")
    fixture = load("evidence/path_identity/public_replay/samples/public_demo_replay.json")
    for case_id, category in (
        ("demo-checklist-count", "positive_case"),
        ("demo-release-date", "negative_case"),
    ):
        case = next(c for c in report["cases"] if c["case_id"] == case_id)
        assert case == load(f"evidence/{category}/{case_id}.record.json")
        assert next(c for c in fixture["cases"] if c["case_id"] == case_id) == load(
            f"evidence/{category}/{case_id}.fixture.json"
        )
        payload = {k: case[k] for k in (
            "case_id", "baseline_output", "router_result", "executor_result",
            "runtime_verifier_result", "adoption_gate_result",
        )}
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        assert hashlib.sha256(canonical.encode()).hexdigest() == case["decision_lock"]["decision_sha256"]

    prefix = "evidence/negative_case/bbeh_history/"
    stored = [json.loads(line) for line in (ROOT / prefix / "bbeh500_full_gold_blind_run_outputs.jsonl").read_text().splitlines()]
    for index, category in ((1, "positive_case"), (13, "negative_case")):
        row = stored[index]
        assert row == load(f"evidence/{category}/{row['row_id']}.json")
    patch = load(prefix + "bbeh500_after_word_sorting_floor_patch_offline_replay.json")
    rows = patch["rows"]
    counts = {
        "base": sum(r["patched_base_correct"] for r in rows),
        "patched_final": sum(r["patched_final_correct"] for r in rows),
        "accepted_C": sum(r["patched_accepted_C"] for r in rows),
        "accepted_B": sum(r["patched_accepted_B"] for r in rows),
    }
    assert len(rows) == len(stored) == 500
    assert counts == {"base": 91, "patched_final": 268, "accepted_C": 177, "accepted_B": 0}
    assert all(patch["summary"][k] == v for k, v in counts.items())
    row = rows[44]
    assert row == load(f"evidence/negative_case/{row['row_id']}.patched-record.json")
    negative = stored[13]
    assert negative["revas_final_answer_locked_before_scoring"] == negative["base_answer_locked_before_scoring"]
    matrix = load("evidence/bypass/matrix_policy.json")
    cells = {(lane["lane"], provider) for lane in matrix["lanes"] for provider in lane["providers"]}
    assert len(cells) == 51 and len(matrix["lanes"]) == 17

    # Check the newly written index documents; preserved historical documents
    # retain their original references and are not rewritten to pass this check.
    for path in ROOT.glob("*.md"):
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            if target.startswith(("https://", "http://", "#")):
                assert "omar-benchmark-replay-live-source" not in target, "Private evidence URL"
                continue
            target_path = target.split("#", 1)[0]
            assert (path.parent / target_path).is_file(), f"Broken local evidence link: {path.name}: {target}"
    credential_patterns = (
        r"sk-proj-[A-Za-z0-9_-]{20,}", r"sk-ant-[A-Za-z0-9_-]{20,}",
        r"gh[pousr]_[A-Za-z0-9_]{25,}", r"github_pat_[A-Za-z0-9_]{25,}",
        r"AKIA[A-Z0-9]{16}", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    )
    for name in files:
        text = (ROOT / name).read_text()
        for pattern in credential_patterns:
            assert not re.search(pattern, text), f"Credential-pattern hit in {name}"
    print(json.dumps({
        "check": "post_request_package_integrity_not_new_benchmark",
        "status": "PASS", "files": len(files), "evidence_artifacts": len(acquisition["published_artifacts"]),
        "stored_bbeh_rows": len(rows), "stored_patched_counts": counts,
        "matrix_policy_cells": len(cells), "assessed_code_executed": False,
    }, indent=2))


if __name__ == "__main__":
    main()

# Public disclosure record

**Post-request publication metadata.**

## Preserved without alteration

Public reference code, existing synthetic fixture and report, their original boundary documents, BBEH original outputs/report/protocol log and final offline patch files, existing BYOK audit/report/matrix and selected test sources are preserved byte-for-byte except the three redacted files below. Each has a source and public checksum in the artifact register.

## Redacted public copies — original filenames retained

These files contain the original machine's local workspace path. Only the common local prefix was replaced with `[REDACTED_LOCAL_WORKSPACE]`:

1. `evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_summary.json`
2. `evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_manifest_executed.json`
3. `evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_freeze_manifest.json`

Redaction category: **private machine/local workspace identifier**. No row ID, answer, route, verifier/adoption field, score, timestamp, hash, token usage, original failure, proof label or claim restriction was changed. The originals were inspected and original SHA-256 values retained in [provenance metadata](provenance/source_acquisition.json). They are not silently called unaltered originals.

## Verbatim source excerpts, not full-file publication

`app.py`, `benchmark_replay_harness.py`, `reconstructed_matched_live_harness.py`, and `benchmark_executors/bbeh_executor_backed_routing.py` are represented by clearly labeled `.excerpt.txt` files. Exact original ranges are retained. Unrelated application/product code, proprietary solver internals, prompts, unrelated benchmark history, account/payment/customer data and infrastructure are intentionally withheld. This is document selection, not a reconstruction or modification of the mechanism.

## Selected records

Positive/negative case JSON files are unchanged objects selected from existing reports/JSONL/offline artifacts, with original pointers recorded. Their new file serialization is a post-request convenience; whole parent artifacts remain publicly inspectable here. The selection does not create a new execution or alter the old outcome.

## Credential boundary

No authentication caches, environment files, credentials, API keys, OAuth codes, access tokens, passwords or private-key material are part of the publication set. The unpublished full application was not treated as safe merely because an automated token scan returned no hits. Only necessary, inspected ranges were selected.

Pattern scanning is a supporting check, not a guarantee that arbitrary undisclosed secrets cannot exist. The actual publication set and transformations are listed in [ARTIFACT_REGISTER.csv](ARTIFACT_REGISTER.csv) and [public_copy_transformations.json](provenance/public_copy_transformations.json).

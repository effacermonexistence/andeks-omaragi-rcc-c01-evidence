# C: negative case and state preservation

Post-request mapping of existing records. The request permits existing or reproducible cases from the same implemented path; it does not impose an additional production-only or non-empty-only rule. Applicability to the agreed object is handled in [00_OBJECT_BINDING.md](00_OBJECT_BINDING.md).

## C1-C8: R case `demo-release-date`

| ID | Requested relation | Existing response |
|---|---|---|
| C1 | Candidate identity | Case `demo-release-date`; candidate `2026-08-16` |
| C2 | Route identity | Same R `_run_case` as the positive case; route allowed, executor executed |
| C3 | Applicable adoption condition | Allowed route and passed `source_contains`, using the supplied release-note source |
| C4 | Condition failure | `passed=false`; candidate is absent from supplied source evidence |
| C5 | Rejection/non-promotion | `baseline_preserved`, `source=baseline_output` |
| C6 | Immediately prior baseline | `2026-08-15` |
| C7 | Corresponding after-state | `final_answer=2026-08-15`, `preserved_baseline=true`; differs from the rejected candidate |
| C8 | Replayable artifacts where necessary | Original fixture/report, existing engine/policy and failed-verification test |

[Selected fixture](evidence/negative_case/demo-release-date.fixture.json), [selected recorded case](evidence/negative_case/demo-release-date.record.json), [complete report](evidence/path_identity/public_replay/examples/example_report.json), [existing tests](evidence/path_identity/public_replay/tests/test_replay.py).

The condition source is `Sanitized release note: release date 2026-08-15.` The stored decision hash is `ead95e882a69abce3b8f3cc77a591df0134fc148b33124588f6f454e851d2eb8`. The existing test checks `final_answer == baseline_output`; the separate denied-route test covers skipped execution. These are pre-existing synthetic reference records/test definitions, not production logs or newly run tests.

## Separate H operational abstention/fallback

[Historical row](evidence/negative_case/bbeh_full_object_properties_0019_ac96f0e25b.json), row index 13 / JSONL line 14, records baseline `12`, attempted `object_collection_state_simulator`, executor answer `null`, failed parser/verifier/shape, `friendly_but_parse_failed`, adoption false, and final/fallback source `base1_answer`. Final answer remains `12`. The source trace explains that a concrete color was not uniquely inferred. Post-lock gold is `13`: preservation is not a claim of correctness.

[Original outputs](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_outputs.jsonl) and [final patched artifact](evidence/negative_case/bbeh_history/bbeh500_after_word_sorting_floor_patch_offline_replay.json) preserve these records. This is real abstention/fallback evidence, not an emitted non-empty candidate being rejected. Whether that object satisfies C1/C4 for the agreed path is a bounded identity/applicability question, not resolved by mixing it with R.

## Historical repair and final result

[Initial report](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_report.md) retains accepted_C=178 and accepted_B=1. The [pre-request patch report](evidence/negative_case/bbeh_history/bbeh500_word_sorting_accepted_B_patch_report.md) and final offline artifact retain 500 rows, baseline 91, final 268, accepted_C=177 and accepted_B=0.

The [word-sorting patched record](evidence/negative_case/bbeh_full_word_sorting_0132_4195006c6a.patched-record.json) preserves initial candidate `4` and patched final `No`. The patched executor answer is `null`; the record does not show the patched executor generating `4` and subsequently rejecting it.

A complete operational record of non-empty-candidate verification failure with same-attempt before/after state was not located in the acquired package. This is G04 / `NOT AVAILABLE` for that particular evidence shape, not an extra mandatory criterion or a finding against C-01. Exact historical replay/version linkage, where necessary, is G02.

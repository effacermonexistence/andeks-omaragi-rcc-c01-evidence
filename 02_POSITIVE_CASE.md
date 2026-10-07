# B: positive case

Post-request selection of pre-existing records. No new candidate or execution was created. R and H remain separate paths under [object binding](00_OBJECT_BINDING.md).

## B1-B7: R case `demo-checklist-count`

| ID | Requested relation | Existing response |
|---|---|---|
| B1 | Candidate identity | `governed_candidate=3`, case `demo-checklist-count` |
| B2 | Route identity | R's pinned `_run_case`; `route_allowed`, bounded arithmetic verification |
| B3 | Applicable adoption condition | Allowed route and passed `arithmetic_expression`; configured expression `1 + 1 + 1` |
| B4 | Verifier result | `passed=true`, `target_accessed=false` |
| B5 | Adopted decision | `candidate_adopted`, `source=executor_output` |
| B6 | Resulting state | Baseline `4` -> final `3`, the selected candidate |
| B7 | Replayable artifacts where necessary | Existing fixture, complete report, policy/engine and test source; not a newly run test receipt |

[Selected fixture](evidence/positive_case/demo-checklist-count.fixture.json), [selected record](evidence/positive_case/demo-checklist-count.record.json), [complete parent fixture](evidence/path_identity/public_replay/samples/public_demo_replay.json), [complete parent report](evidence/path_identity/public_replay/examples/example_report.json), [engine](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py), [policy](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py).

The stored decision hash is `bf33ee98ea374e8497e1df47700c211381ed9fc9b0fa3973a2325ba2ad831aad`. The record binds baseline, candidate, verifier, adoption and final answer, rather than supplying only an isolated successful verifier result. The fixture explicitly labels these cases synthetic; that classification is retained.

## Separate historical operational corroboration H

[BBEH row](evidence/positive_case/bbeh_full_boolean_expressions_0035_2ed600e2a1.json), row index 1 / JSONL line 2, records baseline `(A)`, executor `(E)`, `boolean_expression_parser`, parser/verifier/shape success, `adoption_gate_accepts=true`, final source `executor_override_accepted` and final answer `(E)`. Its parent is [the historical outputs file](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_outputs.jsonl). Its trace records A-D false and E true.

This supports that historical recorded chain. It is not the R execution, a new clean holdout, or a universal verifier-correctness result. The later patched offline artifact retains this row's adopted answer. B7's exact historical replay, if needed for the agreed object, additionally requires the matching historical executor version; that link remains G02, not silently replaced by the September excerpt.

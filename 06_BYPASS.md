# F · Bypass within the bounded canonical path

**Status: post-request mapping of existing structural evidence.**

OmarAGI has multiple routes and lanes. This package does not claim one global route. The assessed question is whether an alternative route **within the identified canonical path** can skip the applicable adoption requirement and replace the same baseline state.

## P1 — one public replay attempt

[`_run_case`](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py#L77-L147) has one gate call, followed by one decision receipt and post-lock scoring. Failure returns the baseline branch; later scoring is not another candidate-selection stage. A separate `run_replay` invocation is another attempt. This is the ordinary defined control flow, not an adversarial capability-isolation or tamper-resistance proof.

## P3 — existing multi-lane guard evidence

[audit_report.md](evidence/bypass/audit_report.md), [audit_summary.json](evidence/bypass/audit_summary.json), and [matrix_policy.json](evidence/bypass/matrix_policy.json) preserve:

- `17` lanes × `3` providers = `51` route cells;
- `all_51_cells_structurally_guarded=true` in audit summary;
- `all_cells_structurally_guarded=true` in matrix policy;
- `canonical_accepted_B_required=0`;
- `missing_evidence=fail_closed`, `nonzero_evidence=fail_closed` as audited policy;
- `scorer_visible_to_adoption=false`;
- `uncertified_candidate=diagnostic_only_baseline_canonical`;
- `fresh_external_provider_matrix_executed=false`.

The [certificate/fallback excerpt](evidence/bypass/benchmark_replay_harness.py.excerpt.txt) shows candidate admission predicates and baseline copying without using grade to select a row winner. The [reconstructed-lane excerpt](evidence/bypass/reconstructed_matched_live_harness.py.excerpt.txt) applies the common baseline-preserving policy to its lane registry. The [control-layer excerpt](evidence/bypass/app.py.excerpt.txt) distinguishes raw candidates, canonical fallback, certification and completion status.

[Existing tests](evidence/bypass/test_byok_zero_downlift_global_gate.py) include uncertified candidates scoring higher, certified zero evidence, certified missing/nonzero evidence, diagnostic-only canonical runner claims and row-accounting detection despite positive aggregate uplift. These are pre-request tests, not a new 51-cell live run.

## Exact status boundary

When certification is absent, canonical delivery is baseline and the candidate remains diagnostic. When canonical regression accounting is missing or positive, the completion guard marks the run failed closed rather than publishing a verified zero-downlift outcome. A completion rejection is **not** proof that all internal candidate objects were erased or that a past adoption never happened.

The audit reports 113 focused tests passing, while also disclosing 77 failures and 50 errors in a broader 1,005-test run. Those broader failures are not hidden and are not claimed resolved by this package. Audit source hashes refer to its own earlier repair snapshot; current preserved excerpts have separately registered hashes at the September source pin.

## Terminality and scope

For the defined public replay attempt, the failed adoption branch ends with baseline output; scorer execution does not retry promotion. A new run or distinct lane is a new attempt subject to its own applicable rules. The 51-cell audit is bounded structural evidence, **not coverage of every private, future or unrelated OmarAGI surface**, hostile forged certificates, or independent live-provider execution.

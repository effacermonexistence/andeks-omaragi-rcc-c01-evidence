# D: applicability and candidate-condition binding

Post-request mapping; no threshold or assessed mechanism is changed.

| ID | R: existing relation | H/D scope |
|---|---|---|
| D1 | `runtime_verification.method` identifies the condition; arithmetic expression and source text identify its parameters | H excerpt identifies verifier and adoption thresholds; D identifies certificate predicates and lane policy |
| D2 | Existing fixture supplies route/config; validation admits supported methods | H family/type mapping selects executor or baseline-only behavior; D receives its certificate/config from callers |
| D3 | Same case supplies candidate and config to the same verification call | Historical H row/source linkage and D certificate-to-candidate binding are not inferred from R |
| D4 | Fixture -> runtime projection -> route -> verification -> adoption | Historical runner shows ordering; current excerpt is not asserted identical to its historical executor |

R sources: [fixture](evidence/path_identity/public_replay/samples/public_demo_replay.json), [engine](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py), [policy](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py). The positive case uses `arithmetic_expression` with `1 + 1 + 1`; the negative uses `source_contains` with the release-note source. These existing bindings are not newly selected to improve the assessment result.

[H executor excerpt](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt) defines `ExecutorInput`, family selection, `ExecutorVerifier.verify` and `base_default_adoption` with default confidence threshold `0.9`. The verifier rejects unparsed/empty answers, low confidence, missing trace or errors. `evaluate_revas_route` requires semantic support, executor availability, parser/verifier/shape success and adoption acceptance; otherwise it selects baseline.

The later source's family-level hardening is not the June execution source. [Historical runner](evidence/upstream_influence/run_bbeh500_full_gold_blind.py) and [freeze manifest](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_freeze_manifest.json) preserve historical ordering/identity; matching historical executor code remains a separate G02 linkage.

[D certificate excerpt](evidence/bypass/benchmark_replay_harness.py.excerpt.txt) and [control/completion excerpt](evidence/bypass/app.py.excerpt.txt) describe different conditions: admission predicates versus downstream completion accounting. Existing [tests](evidence/bypass/test_byok_zero_downlift_global_gate.py) and [BBEH lock source](evidence/applicability/test_bbeh_full500_v17_ten_layer_lock.py) are preserved test definitions, not new result receipts.

Showing the selection mechanism does not pre-judge whether the condition was correctly applicable. The Evidence Request expressly leaves that assessment open. Configuration influence is detailed in [E1-E6](05_UPSTREAM_INFLUENCE.md).

# D · Applicable condition and candidate binding

**Status: post-request mapping. All conditions cited below predate the request.**

## Public reference condition

The [original fixture](evidence/path_identity/public_replay/samples/public_demo_replay.json) binds each `case_id`, prompt, baseline, candidate, route request and runtime-verification object before `_run_case` begins.

- [Validation](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L45-L75) requires the case fields and supported method identity.
- [Runtime projection](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L79-L93) includes the same case's baseline, candidate, route and verifier configuration, excluding `post_lock_scoring`.
- [Router](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L96-L125) checks enabled route, supported method and non-empty candidate.
- [Executor](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L128-L151) loads that case's candidate.
- [Verifier](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L275-L288) receives the executed output, same route result and preselected verification configuration.
- [Adoption](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L291-L311) depends on allowed route and passed verifier, not on post-lock correctness.

For B1, identity is `arithmetic_expression` with `1 + 1 + 1`. For C1, identity is `source_contains` with the release-note text. The fixture supplies these conditions; this package did not choose new thresholds to produce a favorable outcome.

## Existing BBEH condition

The [verbatim source excerpt](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt) exposes:

1. `ExecutorInput` identifies family/question, with no gold field in its declared schema.
2. Family rules choose supported executors or baseline-only fallback.
3. `ExecutorVerifier.verify` rejects unparsed/empty outputs, low confidence, missing trace or error.
4. `base_default_adoption` additionally applies its existing default confidence threshold `0.9`.
5. `evaluate_revas_route` requires semantic support, executor availability, parser success, verifier success, valid answer format and adoption acceptance; otherwise `final_answer=base_answer` and `final_source=fallback_source`.

The input schema itself does not prove every possible caller excludes gold; the [historical runner call site](evidence/upstream_influence/run_bbeh500_full_gold_blind.py#L238-L247) and stored flags supply the bounded execution evidence. The source-pin's family hardening is later than the June run. No source hash equivalence between those revisions is asserted.

## BYOK certification and completion are different conditions

[Certificate predicates](evidence/bypass/benchmark_replay_harness.py.excerpt.txt) check pre-score certification and gold/scorer/row-id visibility flags. [Control-layer source](evidence/bypass/app.py.excerpt.txt) distinguishes fixed lane certification from the subsequent zero-regression completion check. [Existing tests](evidence/bypass/test_byok_zero_downlift_global_gate.py) cover uncertified fallback, explicit zero, missing and nonzero evidence.

[Existing ten-layer BBEH lock](evidence/applicability/test_bbeh_full500_v17_ten_layer_lock.py) preserves row identities and both original-run and patched-final metrics. It is pre-existing test source, not a new test receipt.

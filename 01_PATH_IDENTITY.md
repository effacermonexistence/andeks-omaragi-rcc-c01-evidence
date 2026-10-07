# A: operational path identity

Read [00_OBJECT_BINDING.md](00_OBJECT_BINDING.md). All source identities are fixed; no assessed mechanism was edited.

| Item | Identified existing location |
|---|---|
| A1 | One row's `ExecutorOutput` enters `ExecutorVerifier.verify` and then `base_default_adoption` within `evaluate_revas_route` |
| A2 | Candidate object carries family, executor name, parsed flag, optional answer, confidence, trace/error; run/row identity is supplied by `ExecutorInput` and recorded `row_id` |
| A3 | Existing family policy, `ExecutorVerifier.verify` predicates, `base_default_adoption` default threshold, and the enclosing six-condition support conjunction |
| A4 | `ExecutorVerifier.verify`; verification result is `VerifierOutput` |
| A5 | `base_default_adoption` produces an intermediate decision; `evaluate_revas_route` makes the final supported-candidate versus baseline selection |
| A6 | `RevasRouteRecord.final_answer` / `final_source` for this invocation; `base_answer` is the prior baseline |
| A7 | Returned record, linked by the existing recorder to its row's stored final answer/source; later scoring is not a second answer selector |

[Existing operational declarations and complete adoption functions](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt), [historical recorder](evidence/upstream_influence/run_bbeh500_full_gold_blind.py), [mechanical control-flow analysis](reproduction/bounded_control_flow.json).

The new controlled cases execute the verifier/adoption components, not the complete solver or live product. Their connection to the enclosing output is separately checked from the unmodified source. The [proof note](10_OPERATIONAL_C01_PROOF.md) states the exact conditional argument.

The original [public reference engine](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py) remains available as a different, explicitly synthetic reference implementation. It is no longer used to fill an operational source gap by analogy.

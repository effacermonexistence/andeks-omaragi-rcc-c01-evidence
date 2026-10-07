# A: path identity

Post-request mapping. Read [00_OBJECT_BINDING.md](00_OBJECT_BINDING.md) before treating an evidence path as the constituted object.

## A1-A7: primary reference read-through R

Source: `omaragi-reliability-replay @ f141fd09217279ca48f2cfbecc532fed8ecaa6e9`. The primary case pair is `demo-checklist-count` and `demo-release-date`, selected from the same existing fixture/report and same `_run_case` implementation.

| ID | Identified element | Preserved evidence |
|---|---|---|
| A1 | One validated case enters `_run_case`; runtime fields are projected before routing | [engine.py](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py) |
| A2 | `governed_candidate` -> `execute_candidate.output`; case ID plus source pin and parent record identify the attempt | [fixture](evidence/path_identity/public_replay/samples/public_demo_replay.json), [policy.py](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py) |
| A3 | `route_request`, `runtime_verification` and the policy's `allowed AND passed` condition | Same fixture and policy |
| A4 | `verify_execution` -> `verify_runtime_output` | Same policy |
| A5 | `apply_adoption_gate` selects executor output or baseline | Same policy |
| A6 | In R, `adoption_gate_result.final_answer`, subsequently copied to the returned case's `final_answer`; not a whole-machine state | Same engine/policy and [complete report](evidence/path_identity/public_replay/examples/example_report.json) |
| A7 | Adoption result and decision payload receipt; subsequent scoring does not reselect the answer in this invocation | Same engine and policy |

A6 identifies R exactly; it does **not** establish the historical binding between R and the already confirmed C-01 object. That binding is G01 in the [gap register](07_COUNTERPARTY_EXPLANATIONS.md).

The ordinary sequence is baseline -> route -> executor -> runtime verifier -> adoption gate -> decision receipt -> post-lock scorer. The receipt hashes a payload; it is not an independently authenticated immutable ledger. Baseline preservation does not imply baseline correctness.

## H and D are supporting paths, not interchangeable stages of R

H's [original runner](evidence/upstream_influence/run_bbeh500_full_gold_blind.py) assigns baseline and evaluates the route before final answer/source assignment and scoring. Its [stored rows](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_outputs.jsonl) identify historical outcomes. The [executor excerpt](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt) is from the later source pin; no equality with the historical executor hash is asserted.

D's [certificate/fallback excerpt](evidence/bypass/benchmark_replay_harness.py.excerpt.txt) returns row-level `final_omar`; the [control/completion excerpt](evidence/bypass/app.py.excerpt.txt) also writes a summary receipt and evaluates completion/publication status. These states are not R's case output or a retroactive replacement of H's recorded adoption.

For all three, a complete inventory of writers to an independently persisted shared canonical state is not supplied merely by identifying a local return value. See [F1-F4](06_BYPASS.md).

# F: mandatory scope and bypass

Post-request mapping of existing structural evidence. The unit is the **same relevant adopted state**, not a count of agents, lanes or provider routes. Read [object binding](00_OBJECT_BINDING.md).

## F1-F4

| ID | R: observed ordinary flow | H/D: bounded remaining question |
|---|---|---|
| F1 | `_run_case` contains one adoption call that selects this invocation's returned answer. No alternate answer-selection branch was identified within that shown flow | Existing lane plurality does not enumerate all writers to a shared operational state. G05: `NOT AVAILABLE` for a complete same-state entrypoint/writer map in the provided evidence. |
| F2 | Failed routing/verification selects baseline; engine copies the gate's answer and scores it without another selection | The completion guard returns a failed status; the excerpts alone do not show that it necessarily precedes every relevant operational state write. G05: `NOT OBSERVABLE` from the current bounded excerpts. |
| F3 | Within this `_run_case` invocation, failure ends with baseline result/receipt and post-lock scoring, not re-promotion | Operational terminality must refer to the actual identified attempt and writer path. A completion failure cannot erase an earlier adoption. |
| F4 | No second promotion route within the shown R invocation; a different invocation produces its own result object | A new run/lane is **not automatically outside C-01**. If it reaches the same relevant canonical state, its entrypoint, applicable condition and relation to the rejected attempt must be examined. That operational linkage is G05, `NOT AVAILABLE`. |

R sources: [engine](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py), [policy](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py), [negative record](evidence/negative_case/demo-release-date.record.json). These identify ordinary return-value control flow, not universal capability isolation or an independently persisted canonical store.

## Distinct states must not be conflated

| State | Existing selector/writer | What the evidence does not automatically prove |
|---|---|---|
| R case answer | `apply_adoption_gate` -> `_run_case` return | Every external caller or shared persistence destination |
| H row answer/source | `evaluate_revas_route` -> historical runner record | Equality of June executor and later source snapshot |
| D row output | Certificate/fallback helper returns `final_omar` | Certificate issuer/binding and all callers writing the same operational state |
| D summary receipt | `write_control_layer_zero_downlift_adoption` writes `zero_downlift_adoption.json` | That a summary metric is the original candidate state |
| D completion/publication status | `byok_zero_downlift_invariant_guard` returns diagnostic failure | Physical blocking of all writes or retroactive non-adoption |

Sources: [H excerpt](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt), [H runner](evidence/upstream_influence/run_bbeh500_full_gold_blind.py), [D helper](evidence/bypass/benchmark_replay_harness.py.excerpt.txt), [D receipt/guard](evidence/bypass/app.py.excerpt.txt).

## Existing 51-cell audit: evidence, not an automatic closure of F

[audit_report.md](evidence/bypass/audit_report.md), [audit_summary.json](evidence/bypass/audit_summary.json), [matrix_policy.json](evidence/bypass/matrix_policy.json) record 17 lanes x 3 providers, all 51 structurally guarded, uncertified diagnostic-only candidates with baseline canonical, and missing/nonzero accounting failing completion. They expressly record `fresh_external_provider_matrix_executed=false`.

The audit reports 113 focused passing tests and discloses 77 failures and 50 errors in a broader 1,005-test run. The [existing test source](evidence/bypass/test_byok_zero_downlift_global_gate.py) and [reconstructed-lane excerpt](evidence/bypass/reconstructed_matched_live_harness.py.excerpt.txt) provide additional policy/control-flow evidence. None is promoted into an exhaustive same-state writer proof.

No bypass event is asserted to have occurred. No universal/private/future-system security audit is demanded. G03/G05 identify only the caller, state and scope relations needed if D/H are part of the already agreed C-01 object.

# E · Candidate, route, verifier, adoption and scorer separation

**Status: post-request source mapping, not a fresh experimental validation.**

## Public reference path

| Property | Pre-existing source/record |
|---|---|
| `post_lock_scoring` excluded from runtime projection | [policy.py L79–93](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L79-L93) |
| `target_accessed=false` in verifier result | [verification source](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L209-L288), [positive](evidence/positive_case/demo-checklist-count.record.json), [negative](evidence/negative_case/demo-release-date.record.json) |
| Route/execute/verify/adopt occur before lock/scoring | [engine.py](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py#L77-L116) |
| `locked_before_scoring=true`, `scorer_accessed=false`, `gold_accessed=false` | [lock implementation](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L314-L345) and preserved records |
| Changed target cannot change final answer, adoption result or decision hash | [existing target-mutation test](evidence/path_identity/public_replay/tests/test_replay.py#L197-L223) |

The last item is an existing test definition and the committed example is an existing record. Neither is presented as a newly run test. The receipt is a deterministic hash of an in-memory decision payload, **not authenticated immutable storage or proof against arbitrary mutation by an outside caller**.

## Historical BBEH sequence

[Original runner L238–247](evidence/upstream_influence/run_bbeh500_full_gold_blind.py#L238-L247): baseline model call → executor/route evaluation → assignment of final answer/source → first access to `gold(row)` → post-lock score calculation.

[Freeze manifest](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_freeze_manifest.json), [executed manifest](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_manifest_executed.json) and [row records](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_outputs.jsonl) preserve `gold_visible_before_final_lock=false` / `gold_hidden_until_after_final_lock=true` and `scorer_visible_to_route_executor_adoption=false` as recorded fields. They are corroborated by the code ordering, not claimed to be independent observation of hidden execution state.

The initial generation and final offline patch have different proof labels. Development access to BBEH and the post-run repair remain visible. `accepted_B=0` in the final replay is not relabeled as a clean unseen live result.

## Uncertified BYOK candidates

The [preserved gate excerpt](evidence/bypass/benchmark_replay_harness.py.excerpt.txt) accepts a qualifying pre-score certificate or copies the baseline into canonical output. Candidate grades remain diagnostic fields. The [existing test](evidence/bypass/test_byok_zero_downlift_global_gate.py#L192-L247) explicitly checks that a higher candidate grade without a certificate cannot promote it, and that a qualifying certificate can adopt even with a zero candidate grade.

The [historical adoption-lock document](evidence/upstream_influence/benchmark_gold_blind_adoption_lock.md) prohibits scorer-visible row selection. Its [existing test](evidence/upstream_influence/test_benchmark_gold_blind_adoption_lock.py) checks policy text; it is not sufficient on its own to prove all runtimes complied.

## Completion audit is not row-selection evidence

The [BYOK audit](evidence/bypass/audit_report.md) uses final-vs-baseline accounting to block completion/publication when evidence is missing or regression is positive. That downstream audit does **not** use correctness to choose the better answer row-by-row. Keep this status gate separate from the pre-score adoption gate.

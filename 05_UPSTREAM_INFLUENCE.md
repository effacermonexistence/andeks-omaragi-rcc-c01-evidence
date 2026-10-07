# E: upstream influence, item by item

Post-request mapping of existing code/records. Influence is described, not presumed absent and not characterized as an independent positive or negative finding. Gold/scorer separation answers only part of E.

## E1-E6

| ID | Existing influence and separation | Evidence and remaining limit |
|---|---|---|
| E1 | R's upstream fixture supplies `runtime_verification.method`; the candidate string does not assign that field in the shown flow | [fixture](evidence/path_identity/public_replay/samples/public_demo_replay.json), [policy](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py). No claim that every production config producer is LLM-independent. |
| E2 | The fixture supplies `expression`, `source_text` or `required_terms`; these determine the condition's content | Same fixture/policy. `post_lock_scoring` is excluded from the runtime projection, but that does not remove configuration-supplier influence. |
| E3 | `route_request.enabled`, supported method and candidate emptiness affect routing. Candidate content therefore has a bounded influence through the non-empty check | `decide_route` in the same policy. H's family/config input also affects executor selection. |
| E4 | R chooses verifier behavior by the configured method; H chooses executors through family mapping and uses `ExecutorVerifier` | Same policy and [H excerpt](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt). Historical version and production caller linkage remain separate. |
| E5 | Candidate is verification data; configured method/evidence controls the operation. H's parser, confidence, trace and error fields affect verification/adoption | Same sources. Data influencing a result is not the same claim as candidate text rewriting verifier code. No universal absence-of-influence assertion. |
| E6 | D's helper accepts a caller-supplied certificate dictionary and checks admission flags; that input can change its branch | [D gate excerpt](evidence/bypass/benchmark_replay_harness.py.excerpt.txt). Issuer/caller chain and binding of the certificate to this exact candidate/attempt: G03, `NOT AVAILABLE` in the provided excerpts. |

G03 is not an allegation that a certificate was forged or a demand to add signatures. It records a missing relation where D is part of the agreed assessment path. For R, no live LLM is invoked in the reference executor; this fact is not projected onto H or D.

## What the scorer-separation artifacts actually show

R's [engine](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py) calls route, execution, verification and adoption before constructing a decision receipt and invoking scoring. The runtime projection omits `post_lock_scoring`. Stored [positive](evidence/positive_case/demo-checklist-count.record.json) and [negative](evidence/negative_case/demo-release-date.record.json) records include the corresponding visibility fields.

The existing [target-mutation test](evidence/path_identity/public_replay/tests/test_replay.py) changes the post-lock target while requiring the same answer, adoption result and decision hash. It is an existing test definition, not a newly executed experiment.

The receipt is SHA-256 of an in-memory decision payload. In the preserved code, `score_after_decision_lock` checks `status == locked`; its returned `lock_verified=true` does not itself mean a cryptographic hash recomputation or authenticated persistence occurred. Package integrity tooling can separately recompute stored receipt hashes.

H's [runner](evidence/upstream_influence/run_bbeh500_full_gold_blind.py) assigns final answer/source before accessing `gold(row)` and scoring. Recorded flags and manifests are source evidence, not independent observation of all inaccessible execution state. The historical execution, pre-request repair and later source snapshot remain separate.

D's existing [tests](evidence/bypass/test_byok_zero_downlift_global_gate.py) cover higher post-score candidate grades without a certificate and qualifying certificates without a positive grade. The [adoption-lock text](evidence/upstream_influence/benchmark_gold_blind_adoption_lock.md) and [text-presence test](evidence/upstream_influence/test_benchmark_gold_blind_adoption_lock.py) are policy evidence, not proof that every runtime complies.

A post-run zero-downlift completion check may reject publication based on outcome accounting without choosing a row winner. That downstream status is not evidence that a prior candidate was never adopted. See [F](06_BYPASS.md).

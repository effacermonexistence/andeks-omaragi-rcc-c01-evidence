# A · Path identity

**Status: post-request evidence mapping, not newly generated runtime evidence.**

## P1 — identified public reference replay

Source pin: `effacermonexistence/omaragi-reliability-replay @ f141fd09217279ca48f2cfbecc532fed8ecaa6e9`.

Start: one validated case passed to [`_run_case`](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py#L77-L116). End: that case's `adoption_gate_result.final_answer` and `decision_lock`, subsequently reported/scored without a second adoption choice.

| State/component | Existing identity | Evidence |
|---|---|---|
| Prior baseline | `runtime_case.baseline_output` | [Runtime projection](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L79-L93) |
| Candidate entry | `governed_candidate` from validated fixture → `execute_candidate.output` | [Executor](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L128-L151) |
| Applicability | `route_request.enabled`, supported verifier method, non-empty candidate | [Route](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L96-L125) |
| Verification | `verify_execution` → `verify_runtime_output`, using task evidence | [Verifier](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L209-L288) |
| Adoption condition | `router_result.allowed AND runtime_verifier_result.passed` | [Gate](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L291-L311) |
| Adopted output | Passing branch: executor output; failing branch: string baseline output | Same gate |
| Decision receipt | Serialized baseline/route/executor/verifier/adoption payload → SHA-256 | [Lock](evidence/path_identity/public_replay/omaragi_reliability_replay/policy.py#L314-L345) |
| Downstream scorer | Called only after lock construction | [Engine ordering](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py#L77-L116) |

The preserved call order is:

```text
Baseline → Router → Executor → Runtime Verifier → Adoption Gate
→ Decision Lock → Post-lock Scorer → Scored Artifact
```

P1's state boundary is the **canonical answer for one replay case**, not the whole machine, account, model memory, database or all OmarAGI deployments. Baseline preservation does not imply that the baseline is correct. The loader explicitly requires `synthetic: true`; see [engine](evidence/path_identity/public_replay/omaragi_reliability_replay/engine.py#L41-L47) and [original public boundary](evidence/path_identity/public_replay/PUBLIC_LOGIC_BOUNDARY.md).

## P2 — historical BBEH adoption records

The [preserved runner](evidence/upstream_influence/run_bbeh500_full_gold_blind.py#L238-L247) assigns `base_answer`, evaluates the route, and assigns `final_answer/final_source` before loading gold and scoring. Stored rows include baseline/candidate/final, parser/verifier/shape/route fields and fallback source.

[Existing implementation excerpt](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt) preserves the input types, verifier, family applicability and `base_default_adoption` / `evaluate_revas_route` source at the source-2 pin. The latter source includes later family-level hardening; it is **not claimed to be byte-identical to the June execution's recorded executor hash**.

## P3 — bounded canonical BYOK completion/delivery

[Certificate/fallback source excerpt](evidence/bypass/benchmark_replay_harness.py.excerpt.txt), [control completion excerpt](evidence/bypass/app.py.excerpt.txt), and [existing matrix audit](evidence/bypass/audit_report.md) identify the separate baseline/candidate/canonical-output and completion-status layers. A failed publication/completion audit is not retroactively called a pre-score row-verifier decision. See [F](06_BYPASS.md).

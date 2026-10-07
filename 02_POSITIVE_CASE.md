# B · Positive case

**Status: post-request selection and explanation of existing records. No case was generated now.**

## B1 — original public replay record

Case `demo-checklist-count` is already in the [original fixture](evidence/path_identity/public_replay/samples/public_demo_replay.json) and [committed original report](evidence/path_identity/public_replay/examples/example_report.json). It is explicitly synthetic.

| Required element | Preserved value |
|---|---|
| Pre-decision baseline | `4` |
| Candidate | `3` |
| Route | enabled; `route_allowed`; bounded arithmetic verifier |
| Applicable condition | route allowed and verifier passes |
| Condition evidence | `runtime_verification.method=arithmetic_expression`; expression `1 + 1 + 1` |
| Verifier result | `passed=true`; `target_accessed=false` |
| Adoption | `candidate_adopted`; `source=executor_output` |
| Resulting adopted answer | `3` |
| Receipt | `locked_before_scoring=true`; `scorer_accessed=false`; decision hash below |

Decision hash: `bf33ee98ea374e8497e1df47700c211381ed9fc9b0fa3973a2325ba2ad831aad`.

[Selected fixture object](evidence/positive_case/demo-checklist-count.fixture.json) · [Selected recorded case, including ordered event log](evidence/positive_case/demo-checklist-count.record.json).

## B2 — existing executed BBEH row

Historical row `bbeh_full_boolean_expressions_0035_2ed600e2a1`, zero-based index `1`, JSONL line `2`:

| Required element | Stored value |
|---|---|
| Baseline locked before scoring | `(A)` |
| Executor candidate | `(E)` |
| Route / executor | `solver_friendly` / `boolean_expression_parser` |
| Applicability/support | `REVAS_override_supported=true` |
| Parser / verifier / answer shape | all `true` |
| Adoption gate | `adoption_gate_accepts=true` |
| Adopted source | `executor_override_accepted` |
| Adopted answer | `(E)` |
| Upstream separation flags | `gold_hidden_until_after_final_lock=true`; `scorer_visible_to_route_executor_adoption=false` |

[Selected unchanged historical row](evidence/positive_case/bbeh_full_boolean_expressions_0035_2ed600e2a1.json) and [complete original outputs](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_outputs.jsonl). The trace records `A: False` through `E: True`. In the final patched offline artifact this row still has `patched_final_answer=(E)` and `patched_final_source=executor_override_accepted`.

This is operational historical corroboration, not a fresh ANDEKS experiment or independent proof that the verifier is correct for all inputs. Source records describe the run as post-development reproduction and keep `claim_allowed=false`.

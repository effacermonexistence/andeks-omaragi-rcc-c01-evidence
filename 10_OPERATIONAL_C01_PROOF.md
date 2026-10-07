# Source-linked conditional proof of non-promotion and preservation

This is a post-request technical argument grounded in the existing operational source, not an ANDEKS determination. It concerns the ordinary completed invocation and typed per-attempt answer state identified in [00](00_OBJECT_BINDING.md).

## Symbols tied to actual fields

`B0 = base_answer`, the prior baseline string. `E = ExecutorOutput`, the candidate object. `V = ExecutorVerifier().verify(E)`. `A = base_default_adoption(B0, E, V)`.

The operational wrapper computes:

```text
supported = all(semantic_friendly, executor_available, parser_success,
                verifier_success, format_valid, adoption_accepts)
final_answer = A.final_answer if supported else B0
final_source = A.final_source if supported else fallback_source
```

These are explanatory transcriptions of the actual expressions in [the source excerpt](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt); the machine check parses the original expressions rather than trusting this transcription.

## Inner boundary

The original gate's first failing branch returns `AdoptionDecision(B0, ..., override_accepted=False, ...)` when parsing or verification fails. Its next failing branch returns the same baseline/non-promotion relation when candidate confidence is below its applicable threshold. Neither branch writes the candidate into the returned final answer.

The successful branch returns the verifier-normalized candidate and `override_accepted=True`. This claim does not equate successful verification with universal answer correctness. It states enforcement of the selected condition; suitability of the selected condition remains independently assessable.

## Enclosing state

If inner admission fails, `adoption_accepts=False`, so the support conjunction is false. The only final-answer assignment therefore selects `B0`, and the single `RevasRouteRecord` return exposes that selected value. The same implication holds when any other required support flag is false.

[bounded_control_flow.json](reproduction/bounded_control_flow.json) records all 64 finite Boolean combinations of the six source support flags. The 63 false conjunctions select the baseline and fallback source. This is an exhaustive analysis of these finite expressions, not exhaustive testing of the whole program, all floating-point values, caller behavior or arbitrary external effects.

The existing [historical runner](evidence/upstream_influence/run_bbeh500_full_gold_blind.py) assigns its row final answer from `revas.final_answer` before `gold(row)` is consulted, and places that local value into the recorded final-answer field. The AST check records the selection location and field expression. No post-score answer reselection is used as proof of pre-score preservation.

## Independent evidence forms supporting the same relation

1. [Source equivalence](reproduction/source_equivalence.json) compares the recovered committed June declarations with the current declared source components. Whole-file/solver/policy identity is not asserted.
2. [New component execution](reproduction/unchanged_component_cases.json) records one positive and six negative controlled cases using those unchanged original components, including a nonempty candidate rejected by the actual verifier. No verifier result is fabricated and no operational log is reconstructed.
3. [Stored-corpus analysis](reproduction/whole_corpus_preservation.json) checks all existing original failed-admission rows and separately the patched fallback records, preserving original and patched histories.

## Limits that are not silently promoted

The component reproduction is not full solver, full wrapper, live model or full deployment execution. The enclosing relation is a separately identified source argument. Normal typed baseline strings are treated as input values, not as proof of crash-safe authenticated storage. Arbitrary source mutation, malicious interpreter-level mutation, external shared-store writers and universal action prevention are not established. A certificate from the separate D helper is not an input in the shown H wrapper and is not used to discharge this proof.

These limits do not erase the proved conditional in its stated source/value domain. Conversely, the conditional must not be marketed as a proof of every broader system state.

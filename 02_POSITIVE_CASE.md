# B: positive case in the original operational adoption component

## New, dated reproduction of unchanged existing code

The `component-reproduction-positive` case in [unchanged_component_cases.json](reproduction/unchanged_component_cases.json) executes the original `ExecutorVerifier.verify` and `base_default_adoption` declarations. Inputs are explicitly new controlled test inputs, not historical model outputs or existing unit-test records.

| Required item | Observable relation |
|---|---|
| B1 | Serialized `ExecutorOutput` with answer `(B)`, case/attempt ID and source pin |
| B2 | Existing operational `ExecutorVerifier.verify -> base_default_adoption` component relation |
| B3 | Parsed, nonempty answer, confidence 0.99, present trace, no error; original verification and adoption predicates unchanged |
| B4 | The executed verifier returns `verified=true` |
| B5 | The executed gate returns `override_accepted=true` |
| B6 | Baseline `(A)` -> `AdoptionDecision.final_answer=(B)`; enclosing canonical-output linkage is shown separately in the original source |
| B7 | Original source excerpts, source-equivalence record, executable reproduction script and dated structured output |

Source: [current operational excerpt](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt). Reproduction: [script](scripts/reproduce_bounded_adoption.py). The reproduction is a new component execution under request P8, not a new benchmark or proof of solver correctness. The [outer control-flow check](reproduction/bounded_control_flow.json) and [proof](10_OPERATIONAL_C01_PROOF.md) link admitted candidates to the enclosing state without calling the component test a full route execution.

## Separate historical operational corroboration

[Existing BBEH positive row](evidence/positive_case/bbeh_full_boolean_expressions_0035_2ed600e2a1.json) records baseline `(A)`, executor/final `(E)`, successful parser/verifier/adoption and `executor_override_accepted`. Its parent raw file, row index and original identity remain in the register. That historical result is not replaced by the new controlled case.

[Existing synthetic reference case](evidence/positive_case/demo-checklist-count.record.json) remains a reference illustration, not the primary operational evidence.

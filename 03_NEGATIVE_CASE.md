# C: failed condition, non-promotion and baseline preservation

## Same original components as the positive reproduction

The [new unchanged-component record](reproduction/unchanged_component_cases.json) includes `component-reproduction-failed_parse_nonempty`. Candidate answer is `(B)`, its parsed flag is false, the existing verifier returns failure, the existing gate returns `override_accepted=false`, and its final answer remains baseline `(A)`. No verifier result is mocked; the original verifier is executed on the disclosed input.

| Required item | Evidence |
|---|---|
| C1 | Serialized candidate object and new attempt ID; nonempty answer `(B)` |
| C2 | Same source declarations and verifier/adoption route as B |
| C3 | Existing parsed/verified admission condition; no threshold or policy change |
| C4 | Actual `VerifierOutput.verified=false` and reason |
| C5 | Actual non-promotion decision, `override_accepted=false` |
| C6 | `baseline_before=(A)` |
| C7 | `state_after=(A)`, different from rejected candidate `(B)` |
| C8 | Original source, runner, timestamps, input/output record and content digest |

Additional controlled cases exercise low verifier confidence, low adoption confidence, empty candidate, missing trace and executor error. These are **new test inputs executing unchanged component behavior**, not previously recorded production incidents. In particular, the low-adoption-confidence case separates verifier success from adoption-condition failure.

The [source proof and outer-expression analysis](10_OPERATIONAL_C01_PROOF.md) show why a failed inner adoption cannot become a different enclosing final answer: the outer conjunction includes adoption acceptance; a false conjunction selects the same `base_answer`.

## Existing operational records, fully retained

[Original BBEH fallback row](evidence/negative_case/bbeh_full_object_properties_0019_ac96f0e25b.json) records a named executor's abstention, verifier/adoption failure and baseline `12` preserved as final `12`. Its missing executor answer is not invented. [Whole-corpus preservation analysis](reproduction/whole_corpus_preservation.json) checks every original stored failed-admission row, and separately every patched record explicitly marked with the fallback source. The patched file does not contain a patched gate flag, so none is inferred or fabricated.

The [final patched offline record](evidence/negative_case/bbeh_history/bbeh500_after_word_sorting_floor_patch_offline_replay.json) remains 500 rows, baseline 91, final 268, accepted_C 177 and accepted_B 0. The initial stored accepted_B=1 is preserved as a different historical state. Correctness of accepted candidates and preservation after failed admission are different propositions.

The prior absence of a historical nonempty rejected candidate in these 500 rows remains a fact. It is no longer substituted for the broader question of whether the unchanged operational components can reproduce that relation. The request permits reproducible cases; a new dated component execution is not disguised as an old full-production trace.

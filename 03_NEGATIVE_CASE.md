# C · Negative case / state preservation

**Status: post-request mapping of preserved records.**

## C1 — explicit non-empty candidate rejected by runtime verification

Existing synthetic replay case `demo-release-date`:

| State | Preserved value |
|---|---|
| Before decision | baseline `2026-08-15` |
| Candidate presented to executor | `2026-08-16` |
| Route | enabled, allowed; executor status `executed` |
| Applicable verifier | `source_contains` against `Sanitized release note: release date 2026-08-15.` |
| Verification result | `passed=false`; candidate absent from supplied evidence; `target_accessed=false` |
| Non-promotion | `decision=baseline_preserved`; `source=baseline_output` |
| After decision | `final_answer=2026-08-15`; `preserved_baseline=true` |

Thus **post-decision final answer equals pre-decision baseline and differs from the rejected candidate**. This is a state relationship, not just a rejection label.

[Selected original fixture](evidence/negative_case/demo-release-date.fixture.json) · [Selected original report record](evidence/negative_case/demo-release-date.record.json) · [complete source report](evidence/path_identity/public_replay/examples/example_report.json).

The record's lock hash is `ead95e882a69abce3b8f3cc77a591df0134fc148b33124588f6f454e851d2eb8`. The [existing failed-verification test](evidence/path_identity/public_replay/tests/test_replay.py#L85-L94) expressly checks `final_answer == baseline_output`. The [denied-route test](evidence/path_identity/public_replay/tests/test_replay.py#L96-L104) separately covers non-execution and baseline preservation. These test definitions were not newly run or authored for ANDEKS.

## C2 — real historical abstention / failed applicability, not an invented rejected output

Row `bbeh_full_object_properties_0019_ac96f0e25b`, zero-based index `13`, JSONL line `14`:

- baseline before decision: `12`;
- executor exists: `object_collection_state_simulator`;
- attempted executor output: `null`, with trace `object-properties sister concrete color not uniquely inferred`;
- parser, verifier and shape: `false`;
- support reason: `friendly_but_parse_failed`;
- adoption: `false`; final source and fallback source both `base1_answer`;
- final answer: `12`, unchanged from baseline;
- the final patched artifact also records `patched_final_answer=12`, `patched_final_source=base1_answer`.

[Unchanged historical row](evidence/negative_case/bbeh_full_object_properties_0019_ac96f0e25b.json) · [original outputs](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_outputs.jsonl) · [final patched rows](evidence/negative_case/bbeh_history/bbeh500_after_word_sorting_floor_patch_offline_replay.json).

This shows baseline fallback following failed parsing/verification in an actual historical run. **It does not supply a non-empty rejected executor candidate.** The baseline was also wrong under post-lock scoring (`gold=13`); preserving baseline does not guarantee truth.

## C3 — preserve the failure history and the final floor repair

[Initial run report](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_report.md) and [initial summary](evidence/negative_case/bbeh_history/bbeh500_full_gold_blind_run_summary.json) retain `accepted_C=178`, `accepted_B=1`.

The [pre-request patch report](evidence/negative_case/bbeh_history/bbeh500_word_sorting_accepted_B_patch_report.md) and [final offline artifact](evidence/negative_case/bbeh_history/bbeh500_after_word_sorting_floor_patch_offline_replay.json) record **500 rows; baseline 91; final 268; accepted_C 177; accepted_B 0**. The repaired row's [preserved full record](evidence/negative_case/bbeh_full_word_sorting_0132_4195006c6a.patched-record.json) keeps both initial candidate `4` and patched final `No`. Patched executor output is `null`; do not claim that the patched run generated `4` and then rejected it.

This repair existed before the assessment request and was not performed by this publication task. It is development-informed offline replay, not new clean holdout evidence. The historical failure prevents interpreting the source as proof that every parsed or verified candidate was intrinsically safe.

## Unfilled production evidence question

Within the acquired records, a complete production trace of **a non-empty candidate failing its runtime verifier and leaving the same canonical state unchanged** is absent. C1 is the explicit synthetic case; C2 is the operational abstention/fallback case. They remain separate evidence classes rather than being blended into a stronger claim.

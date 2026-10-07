# C-01 object, path and state binding

Post-request clarification of the existing evidence package. This document does not constitute a new assessment object or record assessor acceptance.

## Governing object

The 5 October 2026 Assessment Object Confirmation Record, sections 4, 5 and 11, identifies a specific implemented reliability/replay adoption path. The 6 October 2026 Bounded Evidence Request, sections 3, 4 and 6, carries that object forward. The Evidence Package cannot replace that object merely by choosing an easier example.

C-01 concerns the relation: identifiable candidate -> applicable condition -> verifier result -> adoption decision -> corresponding adopted state; on failure, non-promotion and preservation of the prior baseline.

## Exact evidence identities

| Evidence path | Fixed source/version | Candidate and attempt identity | Output state and end boundary | Role in this package |
|---|---|---|---|---|
| R: public reference replay | `omaragi-reliability-replay @ f141fd09217279ca48f2cfbecc532fed8ecaa6e9`; preserved `engine.py` and `policy.py` | `case_id` plus the pinned fixture/report and one `_run_case` invocation; `governed_candidate` becomes `executor_result.output` | `adoption_gate_result.final_answer`, copied to the case's `final_answer`; decision payload receipt is recorded before scoring | Primary read-through for the explicitly linked positive and negative case mechanics. Existing synthetic reference implementation, not a production execution record. |
| H: historical BBEH | `omar-benchmark-replay-live-source @ 8976dc12c2d398dd59e4e193c41fa36749dee996`; June run and later pre-request patched offline artifact are separate recorded states | Run identity, parent artifact, `row_id`, row position, question hash and recorded candidate | Historical `revas_final_answer_locked_before_scoring` / `final_source`; patched `patched_final_answer` / `patched_final_source` belong to the later offline replay | Separate operational historical evidence. Not the same execution or implementation as R. |
| D: BYOK delivery/completion | Same source-2 pin; certificate/fallback, control-layer and completion excerpts; July audit is its own older snapshot | Lane/run/row/candidate/certificate inputs where recorded | Row-level `final_omar` is distinct from `zero_downlift_adoption.json` metrics and completion/publication status | Supplementary structural evidence. A publication failure is not retroactive non-adoption. |

The R state is one returned answer, not all machine, account, database or downstream state. A receipt hash identifies content; it does not by itself create authenticated immutable storage. H and D are not aliases of that R state.

## Binding status

**A6 / G01: NOT AVAILABLE in the reviewed source chain:** an explicit historical binding of the already confirmed C-01 object to exactly one of these repository/function/version/state identities was not established by this package review. R is the primary *reference read-through*, not a newly declared substitute for the agreed operational object. H and D cannot silently fill a missing R relation, or vice versa.

The existing object must be linked to its actual path before sufficiency is claimed. If that path is R, its pre-existing synthetic cases are evaluated on that basis. If it is H or D, their own versions, callers and states must supply the relation. No new production-only, non-empty-candidate-only or fresh-live-run requirement is introduced here.

## Version boundary

The September source-2 excerpt includes later family-level baseline-only restrictions. It is not asserted to match the June execution's recorded executor hash. The July 51-cell audit has its own recorded source hashes. See [PROVENANCE.md](PROVENANCE.md) and [09_CHANGE_RECORD.md](09_CHANGE_RECORD.md).

The full item response is [08_REQUIREMENT_CROSSWALK.md](08_REQUIREMENT_CROSSWALK.md). Open relations are mapped there and in [07_COUNTERPARTY_EXPLANATIONS.md](07_COUNTERPARTY_EXPLANATIONS.md), not concealed by a package-level completion percentage.

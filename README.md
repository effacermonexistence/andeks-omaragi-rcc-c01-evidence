# ANDEKS · OmarAGI / RCC · C-01 evidence package

**Claim C-01:** within the identified reliability/replay adoption attempt, a candidate that fails the applicable adoption condition is not promoted into the adopted output; the prior baseline output is preserved.

This repository provides publicly readable copies of **pre-existing evidence**, plus an index prepared after ANDEKS's **2026-10-06** request. It does not change RCC, run a new benchmark, or generate a new demonstration.

## Assessment route A–F

| Request | Evidence map | Principal evidence |
|---|---|---|
| A · Path identity | [01_PATH_IDENTITY.md](01_PATH_IDENTITY.md) | Preserved engine/policy, original fixture/report, existing runtime/adoption source excerpts |
| B · Positive case | [02_POSITIVE_CASE.md](02_POSITIVE_CASE.md) | Existing synthetic replay record and an existing executed BBEH row |
| C · Negative case / state preservation | [03_NEGATIVE_CASE.md](03_NEGATIVE_CASE.md) | Explicit verifier-failure replay record; historical BBEH abstention/fallback records; final patched floor accounting |
| D · Applicability | [04_APPLICABILITY.md](04_APPLICABILITY.md) | Verifier identity in fixture; route-family and fixed-threshold source; existing lock tests |
| E · Upstream influence | [05_UPSTREAM_INFLUENCE.md](05_UPSTREAM_INFLUENCE.md) | Runtime projection, pre-score decision receipt, scorer-target mutation test, historical runner ordering |
| F · Bypass | [06_BYPASS.md](06_BYPASS.md) | Existing 17-lane × 3-provider structural audit, certificate/fallback code and existing tests |

[07_COUNTERPARTY_EXPLANATIONS.md](07_COUNTERPARTY_EXPLANATIONS.md) separates the explanations supported by those artifacts from unresolved assessment questions.

## Evidence classes — read before interpreting the numbers

1. **Public reference replay:** source `effacermonexistence/omaragi-reliability-replay`, pinned at `f141fd09217279ca48f2cfbecc532fed8ecaa6e9` (Git committer time `2026-08-30T01:13:34Z`). Its five cases are explicitly **synthetic**, and its executor loads pre-generated fixture candidates. The preserved report proves what that recorded reference replay contains; it is not a production execution record.
2. **Historical BBEH operational records:** source `effacermonexistence/omar-benchmark-replay-live-source`, pinned at `8976dc12c2d398dd59e4e193c41fa36749dee996` (`2026-09-01T19:09:24Z`). Relevant files are copied here so private-source access is unnecessary. The initial run is a **post-development gold-blind reproduction**. Its later, pre-request repair is an **offline replay against locked baseline outputs**, not a fresh run or clean unseen holdout.
3. **BYOK audit:** the preserved audit records **17 lanes, 3 providers, 51 structurally guarded route cells**. It explicitly reports that a fresh external-provider matrix was **not executed**. Existing test source is preserved, not presented as a newly executed test result.

### Final BBEH state and historical intermediate state

| Artifact state | Rows | Baseline correct | Final correct | Positive flips / accepted_C | Regressions / accepted_B |
|---|---:|---:|---:|---:|---:|
| Initial run, preserved without rewriting | 500 | 91 | 268 | 178 | 1 |
| **Final recorded patched offline replay** | **500** | **91** | **268** | **177** | **0** |

The final patched artifact supports **177 positive flips, zero regressions, baseline floor preserved on those 500 stored rows**. The initial `accepted_B=1` remains visible as history; it is not the final patched regression state. The sources retain `claim_allowed=false` and their post-development/offline proof boundaries. Publishing copies does not promote that score into clean public benchmark proof.

## Start with the actual states

- [Recorded positive case](evidence/positive_case/demo-checklist-count.record.json): baseline `4`, candidate `3`, verifier passed, adopted answer `3`.
- [Recorded failed-verification case](evidence/negative_case/demo-release-date.record.json): baseline `2026-08-15`, candidate `2026-08-16`, verifier failed, adopted answer remains `2026-08-15`.
- [Historical executed positive BBEH row](evidence/positive_case/bbeh_full_boolean_expressions_0035_2ed600e2a1.json).
- [Historical BBEH parse/verification failure and baseline fallback](evidence/negative_case/bbeh_full_object_properties_0019_ac96f0e25b.json).
- [Complete final patched offline artifact](evidence/negative_case/bbeh_history/bbeh500_after_word_sorting_floor_patch_offline_replay.json).

The BBEH negative row has **no emitted executor answer** because it abstained. It is not misrepresented as a non-empty candidate failing a separately recorded verifier. The explicit non-empty candidate/verifier-failure relationship is in the pre-existing synthetic replay record.

## Provenance and integrity

- [ARTIFACT_REGISTER.csv](ARTIFACT_REGISTER.csv): source, path, pin, timestamp, evidence class, public form and hashes for every package file.
- [PROVENANCE.md](PROVENANCE.md): source acquisition, publication transformations and timestamp limits.
- [Source acquisition record](provenance/source_acquisition.json): pinned Git blob identity and source-file hashes.
- [Public-copy transformations](provenance/public_copy_transformations.json): redactions, verbatim excerpts and selected-record provenance.
- [PACKAGE_SHA256SUMS.txt](PACKAGE_SHA256SUMS.txt): public-file checksums. The checksum manifest excludes itself; register self-reference is explicitly excluded from its own hash cell.

No private GitHub URL is required to inspect A–F. All principal links resolve to files in this public repository. Historical links retained inside unchanged source documents are background references, not substitutes for the local evidence.

## Remaining evidence boundary

A–F are mapped and populated for the declared paths. **A logged production rejection of a non-empty candidate with the complete same-attempt before/after state is not present in the acquired artifacts.** The package supplies the existing synthetic explicit rejection and real historical abstention/fallback evidence without filling that gap with a new demonstration. The complete ANDEKS request document, independent assessor acceptance, universal/private-system bypass coverage and a fresh live-provider matrix are not asserted.

See [DISCLOSURE.md](DISCLOSURE.md) and [NOTICE.md](NOTICE.md) for private-source omissions and licensing scope. This is an evidence package, not an assessment verdict or a deployable RCC replacement.

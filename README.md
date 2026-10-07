# OmarAGI / RCC C-01 evidence package

**Status: request-aligned evidence submission, not an independent determination.** This repository preserves existing source and execution artifacts and supplies post-request explanations. No assessed mechanism is changed by this documentation revision.

C-01 concerns non-promotion of a candidate that fails its applicable adoption condition and preservation of the prior baseline in the identified reliability/replay path. It does not claim universal prevention of external side effects.

## Read in this order

1. [Object, path and state binding](00_OBJECT_BINDING.md): R, H and D are separate evidence paths; the original agreed object is not silently replaced.
2. [All 45 request items](08_REQUIREMENT_CROSSWALK.md): A1 through F4 and P1 through P9, with evidence, responses and explicit limits.
3. [Open relations](07_COUNTERPARTY_EXPLANATIONS.md) and [change record](09_CHANGE_RECORD.md): unavailable evidence is not presumed to exist.

| Request | Evidence map |
|---|---|
| A: path identity | [01_PATH_IDENTITY.md](01_PATH_IDENTITY.md) |
| B: positive case | [02_POSITIVE_CASE.md](02_POSITIVE_CASE.md) |
| C: negative case and preservation | [03_NEGATIVE_CASE.md](03_NEGATIVE_CASE.md) |
| D: applicability | [04_APPLICABILITY.md](04_APPLICABILITY.md) |
| E: upstream influence | [05_UPSTREAM_INFLUENCE.md](05_UPSTREAM_INFLUENCE.md) |
| F: bypass | [06_BYPASS.md](06_BYPASS.md) |
| P: identity, provenance and change | [PROVENANCE.md](PROVENANCE.md) |

## Evidence classes

**R:** pre-existing, explicitly synthetic public reference replay at `f141fd09217279ca48f2cfbecc532fed8ecaa6e9`. The executor loads stored candidates. The [positive record](evidence/positive_case/demo-checklist-count.record.json) adopts `3` instead of baseline `4`. The [negative record](evidence/negative_case/demo-release-date.record.json) rejects `2026-08-16` and preserves `2026-08-15`. These are linked cases of the same reference implementation, not production logs.

**H:** historical BBEH records copied from private source pin `8976dc12c2d398dd59e4e193c41fa36749dee996`. Original run, pre-request offline repair and later source hardening remain distinguishable.

| Recorded artifact state | Rows | Baseline correct | Final correct | accepted_C | accepted_B |
|---|---:|---:|---:|---:|---:|
| Initial historical run | 500 | 91 | 268 | 178 | 1 |
| Final recorded patched offline replay | 500 | 91 | 268 | 177 | 0 |

The **final patched result remains 177 positive flips and zero regressions on the stored 500 rows**. The initial result is history, not the final patched state. Source claim restrictions, post-development exposure and the offline-replay classification are retained. This revision neither reverses the final result nor upgrades it into a fresh unseen benchmark.

[Historical positive BBEH row](evidence/positive_case/bbeh_full_boolean_expressions_0035_2ed600e2a1.json) and [historical fallback row](evidence/negative_case/bbeh_full_object_properties_0019_ac96f0e25b.json) are operational records. The latter has no emitted executor answer. That is abstention/fallback evidence, not a fabricated non-empty rejected answer. [Complete final patched artifact](evidence/negative_case/bbeh_history/bbeh500_after_word_sorting_floor_patch_offline_replay.json).

**D:** the existing BYOK audit records 17 lanes, 3 providers and 51 structurally guarded route cells, but explicitly reports no fresh external-provider matrix execution. Its 113 focused passing tests and broader 1,005-test run with 77 failures and 50 errors remain disclosed. Route-matrix coverage does not alone establish every writer to the same adopted state.

## What has and has not been established

The full request is now used for the mapping. It does not impose a production-only or non-empty-only case rule. R supplies explicit linked case mechanics; applicability to the agreed C-01 object remains a separate binding question. H's historical source linkage and D's caller/certificate/state-writer coverage are not silently inferred from R.

A-F are populated, but **presence is not sufficiency and sufficiency is not a positive determination**. Remaining relations are labeled `NOT AVAILABLE` or `NOT OBSERVABLE` for the reviewed package, not declared nonexistent system-wide. See the [gap register](07_COUNTERPARTY_EXPLANATIONS.md).

## Identity, access and checks

[ARTIFACT_REGISTER.csv](ARTIFACT_REGISTER.csv) identifies every tracked file. [PROVENANCE.md](PROVENANCE.md), [source acquisition](provenance/source_acquisition.json), and [copy transformations](provenance/public_copy_transformations.json) preserve source identity. [PACKAGE_SHA256SUMS.txt](PACKAGE_SHA256SUMS.txt) identifies the current publication bytes.

All principal evidence links are local public copies. Historical private-source links inside unchanged source documents remain background references, not the access path for this submission. [DISCLOSURE.md](DISCLOSURE.md) and [NOTICE.md](NOTICE.md) retain redaction and licensing boundaries.

`scripts/verify_package.py` checks stored artifacts, hashes, selected records and stored counts without importing or executing assessed RCC code. Publication metadata refresh is separate from that check. Neither is an ANDEKS assessment, a new benchmark, or a fresh execution of the preserved source tests.

Sending a package permits administrative intake only. Independent review and determination remain subject to ANDEKS's separate process and commercial commencement. This repository does not record receipt, payment, acceptance or endorsement.

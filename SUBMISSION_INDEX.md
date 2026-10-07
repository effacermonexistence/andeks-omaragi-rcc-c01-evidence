# ANDEKS C-01 Submission Index

## Submission identity

Repository: `effacermonexistence/andeks-omaragi-rcc-c01-evidence`

Object: OmarAGI / RCC currently implemented reliability and replay adoption path identified in [00_OBJECT_BINDING.md](00_OBJECT_BINDING.md).

Claim C-01: a candidate that fails the applicable adoption condition is not promoted into the adopted state, while the locked baseline or prior supported state is preserved.

## Canonical empirical result

The canonical Build Week evidence contains 500 rows.

* Baseline correct: 91
* Final correct: 268
* Positive flips / uplift: 177
* Regressions: 0
* Final accepted_C: 177
* Final accepted_B: 0

The canonical result is therefore **177 improvements with zero regressions**.

## Direct evidence package map

| ANDEKS set | Primary response | Principal technical evidence |
|---|---|---|
| A1-A7 Path Identity | [01_PATH_IDENTITY.md](01_PATH_IDENTITY.md) | operational source excerpt, object binding, recorder |
| B1-B7 Positive Case | [02_POSITIVE_CASE.md](02_POSITIVE_CASE.md) | historical positive row + unchanged-component reproducible positive case |
| C1-C8 Negative Case | [03_NEGATIVE_CASE.md](03_NEGATIVE_CASE.md) | reproducible non-promotion case + historical fallback rows + whole-corpus preservation |
| D1-D4 Applicability | [04_APPLICABILITY.md](04_APPLICABILITY.md) | original verifier predicates, adoption threshold, family/route relation |
| E1-E6 Upstream Influence | [05_UPSTREAM_INFLUENCE.md](05_UPSTREAM_INFLUENCE.md) | source call chain and historical runner |
| F1-F4 Bypass | [06_BYPASS.md](06_BYPASS.md) | final-selection control flow, bounded Boolean analysis, recorder relation |
| P1-P9 Provenance | [PROVENANCE.md](PROVENANCE.md) + [ARTIFACT_REGISTER.csv](ARTIFACT_REGISTER.csv) | source pins, timestamps, old/new evidence classification, hashes |

Exact requirement-by-requirement mapping is in [08_REQUIREMENT_CROSSWALK.md](08_REQUIREMENT_CROSSWALK.md).

## Core technical observations available for review

1. The verifier/adoption path is explicitly identified.
2. Positive and negative reproducible cases use the same unchanged verifier/adoption components.
3. In the negative case, a nonempty candidate is rejected and the baseline before equals the state after.
4. The enclosing source relation selects baseline whenever the support conjunction fails.
5. All 64 combinations of the six Boolean support conditions were analyzed. The 63 failing combinations select baseline/fallback.
6. Stored original failed-admission rows checked: 276. Baseline-preservation violations: 0.
7. Stored patched fallback rows checked: 278. Baseline-preservation violations: 0.
8. Canonical Build Week outcome remains +177 uplift, 0 regression.
9. No assessed threshold, verifier, route, adoption body, original run output, or historical evidence file was modified to create this submission.

## Evidence class separation

Pre-existing source and run artifacts remain distinguishable from post-request explanatory material and post-request reproducible executions. No post-request reproduction is represented as an historical production record.

The earlier pre-patch intermediate BBEH state remains present for chronology and provenance. It is not represented as the canonical final Build Week result.

## Scope discipline

C-01 is bounded to the identified adoption path and corresponding resulting state. This package does not expand C-01 into universal external-action prevention, end-to-end system safety, all integrations, or arbitrary shared-store protection.

## Intake status

**Package coverage: 45/45 requested evidence items provided.**

The package is ready for the administrative receipt/inventory stage described in the ANDEKS Bounded Evidence Request. Independent admissibility, sufficiency, freeze, assessment, and determination remain ANDEKS functions.

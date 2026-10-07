# OmarAGI / RCC C-01 Public Evidence Package

**Submission status: READY FOR ANDEKS ADMINISTRATIVE INTAKE**

This public repository is the evidence package for the constituted ANDEKS™ × OmarAGI / RCC Claim C-01.

**C-01:** when a candidate output fails the applicable adoption condition in the identified reliability/replay path, that candidate is not promoted and the locked baseline or prior supported state is preserved.

## Canonical Build Week evidence

| Measure | Result |
|---|---:|
| Evaluated rows | **500** |
| Baseline correct | **91** |
| Final correct | **268** |
| Positive flips / uplift | **177** |
| Regressions | **0** |
| Final accepted_C | **177** |
| Final accepted_B | **0** |

**Canonical outcome: +177 uplift with zero regressions.**

The preserved earlier pre-patch artifact remains in the repository only as historical chronology. It is not the canonical final Build Week result.

## ANDEKS request coverage

| Evidence set | Requested items | Package status |
|---|---:|---|
| A. Path Identity | A1-A7 | **7/7 PROVIDED** |
| B. Positive Case | B1-B7 | **7/7 PROVIDED** |
| C. Negative Case | C1-C8 | **8/8 PROVIDED** |
| D. Applicability | D1-D4 | **4/4 PROVIDED** |
| E. Upstream Influence | E1-E6 | **6/6 PROVIDED** |
| F. Bypass | F1-F4 | **4/4 PROVIDED** |
| P. Identity & Provenance | P1-P9 | **9/9 PROVIDED** |
| **Total** | **45** | **45/45 PROVIDED** |

“PROVIDED” means the requested evidence relation is mapped to an identified artifact or source relation in this package. It does not pre-judge ANDEKS admissibility, sufficiency, or final determination.

## Reviewer path

1. [Submission index](SUBMISSION_INDEX.md)
2. [Object and adopted-state binding](00_OBJECT_BINDING.md)
3. [45-item request crosswalk](08_REQUIREMENT_CROSSWALK.md)
4. [Operational C-01 proof](10_OPERATIONAL_C01_PROOF.md)
5. [Canonical machine-readable summary](CANONICAL_EVIDENCE_SUMMARY.json)
6. [Artifact register](ARTIFACT_REGISTER.csv)
7. [Provenance](PROVENANCE.md)

## C-01 evidence chain

```text
candidate identity
→ applicable condition
→ verifier result
→ adoption decision
→ resulting adopted state

negative case:
condition fails
→ candidate not promoted
→ baseline before == state after
```

The same existing verifier/adoption components are used for the reproducible positive and negative cases. The negative case is an expected rejection-path test, not a regression. Stored-corpus analysis also found **zero baseline-preservation violations** across the selected failed-admission/fallback records.

## Evidence integrity

The assessed mechanism was not modified for this package. Original thresholds, verifier behavior, routing rules, adoption logic, source repositories, benchmark outputs, and historical evidence are unchanged.

Post-request material is explicitly separated into:
* selection/excerpts of pre-existing source,
* explanatory mapping,
* static or stored-data analysis,
* reproducible execution of unchanged existing components.

No new BBEH benchmark run or model-provider call was used to manufacture a passing result.

The package validator passes with all 45 request IDs represented, original evidence preserved, and the canonical Build Week result unchanged.

## Evidence sections

[A: Path](01_PATH_IDENTITY.md) · [B: Positive](02_POSITIVE_CASE.md) · [C: Negative](03_NEGATIVE_CASE.md) · [D: Applicability](04_APPLICABILITY.md) · [E: Upstream influence](05_UPSTREAM_INFLUENCE.md) · [F: Bypass](06_BYPASS.md) · [Counterparty explanations](07_COUNTERPARTY_EXPLANATIONS.md)

[Change record](09_CHANGE_RECORD.md) · [Disclosure](DISCLOSURE.md) · [Checksums](PACKAGE_SHA256SUMS.txt) · [Notice](NOTICE.md)

This repository presents evidence for independent review. It does not itself claim an ANDEKS determination, certification, or endorsement.

# OmarAGI / RCC C-01: source-linked evidence and reproduction

This package preserves and maps the existing OmarAGI / RCC evidence for ANDEKS C-01. It identifies the operational adoption path, preserves the canonical Build Week outcome, links the original verifier/adoption components to reproducible positive and negative cases, and records provenance for every evidence class.

C-01 is the bounded relation: failed applicable adoption condition -> candidate not promoted -> prior baseline preserved. A verifier rejection is an expected negative-case branch, not a benchmark regression or system failure.

## Canonical Build Week result

| Rows | Baseline correct | Final correct | Positive flips | Regressions |
|---:|---:|---:|---:|---:|
| 500 | 91 | 268 | 177 | 0 |

The canonical final Build Week evidence is **177 positive flips and zero regressions**. The preserved pre-patch intermediate artifact is retained only as chronology and is not the canonical final result. The final recorded patched offline replay has `accepted_C=177` and `accepted_B=0`.

## Main evidence

| Evidence | What it establishes |
|---|---|
| [Implementation and state identity](00_OBJECT_BINDING.md) | Existing operational functions, source pin, candidate, attempt and per-row returned state |
| [Conditional proof](10_OPERATIONAL_C01_PROOF.md) | Original failed-admission branch implies baseline at the enclosing final-answer return |
| [Source equivalence](reproduction/source_equivalence.json) | Mechanical comparison of recovered June and current selected declarations, without claiming whole-file equality |
| [Unchanged-component reproduction](reproduction/unchanged_component_cases.json) | Dated reproducible positive and negative cases using unchanged original verifier/adoption components |
| [Bounded control flow](reproduction/bounded_control_flow.json) | Original final selection, return and recorder field; all combinations of the six Boolean support conditions |
| [Whole stored-corpus analysis](reproduction/whole_corpus_preservation.json) | Stored failed-admission/fallback preservation relationships |
| [All 45 request items](08_REQUIREMENT_CROSSWALK.md) | One-to-one response to A1-F4 and P1-P9 |

## Request navigation

[A: Path](01_PATH_IDENTITY.md) · [B: Positive](02_POSITIVE_CASE.md) · [C: Negative](03_NEGATIVE_CASE.md) · [D: Applicability](04_APPLICABILITY.md) · [E: Upstream influence](05_UPSTREAM_INFLUENCE.md) · [F: Bypass](06_BYPASS.md) · [Counterparty explanations](07_COUNTERPARTY_EXPLANATIONS.md).

## Evidence integrity

The original source repositories, original benchmark outputs, original historical evidence files, thresholds, verifier behavior, routing rules and gate bodies were not modified for this package. Post-request material is separately labeled as source selection, explanatory mapping, static analysis, stored-data analysis, or a reproducible execution of unchanged existing components.

A tooling error in an earlier post-request analysis script was not a Build Week result, benchmark result, C-01 result, regression, or assessed-system failure. It is not part of the evidentiary outcome. The corrected analysis reads the actual stored schema and the final validation passes.

[Provenance](PROVENANCE.md), [artifact register](ARTIFACT_REGISTER.csv), [checksums](PACKAGE_SHA256SUMS.txt), [source recovery](provenance/source_recovery_20261007.json), [change record](09_CHANGE_RECORD.md), [disclosure](DISCLOSURE.md), [notice](NOTICE.md).

Technical evidence is distinct from ANDEKS admission, sufficiency and independent determination. No third-party finding is claimed here.

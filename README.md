# OmarAGI / RCC C-01: source-linked evidence and reproduction

**This revision fills missing evidence links, not just missing-field labels.** It identifies the existing operational adoption path, recovers its committed June components, compares them with the current components, executes the unchanged original verifier/adoption functions on disclosed controlled inputs, and checks preservation across the stored BBEH records.

C-01 is the bounded relation: failed applicable adoption condition -> candidate not promoted -> prior baseline preserved. Enforcement of that condition is not a claim that every accepted answer is true, nor universal prevention of external actions.

## Main evidence

| Evidence | What it establishes |
|---|---|
| [Implementation and state identity](00_OBJECT_BINDING.md) | Exact existing operational functions, source pin, candidate, attempt and per-row returned state |
| [Conditional proof](10_OPERATIONAL_C01_PROOF.md) | Original failed-admission branch implies baseline at the enclosing final-answer return |
| [Source equivalence](reproduction/source_equivalence.json) | Mechanical comparison of recovered June and current selected declarations, without pretending whole-file equality |
| [Unchanged-component reproduction](reproduction/unchanged_component_cases.json) | New dated positive and failure/non-promotion/baseline-preservation cases, including a nonempty rejected candidate |
| [Bounded control flow](reproduction/bounded_control_flow.json) | Original final selection, return and recorder field; all combinations of the six Boolean support conditions |
| [Whole stored-corpus analysis](reproduction/whole_corpus_preservation.json) | Actual stored failed-admission/fallback preservation relationships, with original and patched records separated |
| [All 45 request items](08_REQUIREMENT_CROSSWALK.md) | One-to-one source/result responses, rather than a blanket completion percentage |

## Request navigation

[A: Path](01_PATH_IDENTITY.md) · [B: Positive](02_POSITIVE_CASE.md) · [C: Negative](03_NEGATIVE_CASE.md) · [D: Applicability](04_APPLICABILITY.md) · [E: Upstream influence](05_UPSTREAM_INFLUENCE.md) · [F: Bypass](06_BYPASS.md) · [Resolution and limits](07_COUNTERPARTY_EXPLANATIONS.md).

## Original evidence is unchanged

| Recorded BBEH artifact | Rows | Baseline correct | Final correct | accepted_C | accepted_B |
|---|---:|---:|---:|---:|---:|
| Initial historical run | 500 | 91 | 268 | 178 | 1 |
| Final recorded patched offline replay | 500 | 91 | 268 | 177 | 0 |

The final patched result remains **177 positive flips and zero regressions on those 500 stored rows**. Its post-development/offline classification and `claim_allowed=false` remain intact. No original result was rewritten to pass a check. The new reproduction is not a new benchmark, a historical production trace, a fresh unseen evaluation, or the R synthetic demo disguised as operational code.

New controlled cases execute only the unchanged original operational verifier/adoption components. The outer canonical-output connection is a separately stated source argument, not falsely called an executed complete solver or application. The older R public reference demo and D broader BYOK audit remain inspectable as separate supplementary evidence.

## Evidence classes and integrity

[Provenance](PROVENANCE.md), [artifact register](ARTIFACT_REGISTER.csv), [checksums](PACKAGE_SHA256SUMS.txt), [new source recovery](provenance/source_recovery_20261007.json), [change record](09_CHANGE_RECORD.md), [disclosure](DISCLOSURE.md), [notice](NOTICE.md).

Reproduction is permitted as a new record of unchanged components and is labeled as such. No assessed threshold, route, verifier or implementation was modified. New inputs, dates, component scope and source fingerprints are supplied. No model API call is required.

Technical source/value evidence is distinct from ANDEKS admission, sufficiency and independent determination. No such third-party finding is claimed here. Claims about external shared stores, all deployments, interpreter tampering or universal safety are not silently added to the bounded argument.

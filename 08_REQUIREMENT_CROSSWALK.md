# Exact request crosswalk: 45 items

Post-request response mapping to the 6 October 2026 Evidence Request, sections 6-12. Original item wording is kept below. The response is evidence-scoped, not an assessor finding.

R = public reference replay; H = historical BBEH; D = BYOK delivery/completion. Read [object binding](00_OBJECT_BINDING.md). R observations do not establish G01 or silently substitute for H/D. `NOT AVAILABLE` / `NOT OBSERVABLE` refer to the reviewed package, not all possible source material.

The request allows existing or reproducible cases. No production-only, non-empty-only, new-test, cryptographic-signature or universal-security requirement is added. [Open relations G01-G06](07_COUNTERPARTY_EXPLANATIONS.md) remain explicit.

## A

Detailed evidence: [01_PATH_IDENTITY.md](01_PATH_IDENTITY.md).

| ID | Original request item | Response / boundary |
|---|---|---|
| A1 | Where the assessed adoption path begins. | R: one validated case enters `_run_case`; runtime projection precedes routing. |
| A2 | What candidate object enters it. | R: `governed_candidate` -> executor output, identified by case/pin/parent record. |
| A3 | Where the applicable adoption condition is defined or retrieved. | R: fixture route/verifier config plus policy admission condition. H historical source linkage is G02. |
| A4 | Which component performs verification. | R: `verify_execution` -> `verify_runtime_output`. H excerpt: `ExecutorVerifier.verify`. |
| A5 | Where the adoption decision occurs. | R: `apply_adoption_gate`; H/D are separate selectors, not aliases. |
| A6 | What state is treated as the adopted-system state for C-01. | R answer field is precisely identified, but its historical binding to the confirmed object is G01 / NOT AVAILABLE. |
| A7 | Where the assessed boundary ends. | R: recorded adoption answer and decision receipt, before post-lock scoring. |

## B

Detailed evidence: [02_POSITIVE_CASE.md](02_POSITIVE_CASE.md).

| ID | Original request item | Response / boundary |
|---|---|---|
| B1 | Candidate identity. | R case `demo-checklist-count`, candidate `3`; separate H row has candidate `(E)`. |
| B2 | Route identity. | R same pinned `_run_case` implementation and allowed route; H has its own run/row identity. |
| B3 | Applicable adoption condition. | R: allowed route and passed arithmetic verification of `1 + 1 + 1`. |
| B4 | Verifier result. | R recorded `passed=true`; H separately records verifier success. |
| B5 | Adoption decision = adopted. | R `candidate_adopted`; source executor output. |
| B6 | Resulting adopted-system state. | R baseline `4` -> final `3`, linked to the candidate/decision. |
| B7 | Replayable run artifacts, where necessary to establish the B1-B6 relation. | Existing R fixture/report/source/tests. Exact H historical replay source, where necessary, is G02. |

## C

Detailed evidence: [03_NEGATIVE_CASE.md](03_NEGATIVE_CASE.md).

| ID | Original request item | Response / boundary |
|---|---|---|
| C1 | Candidate identity. | R non-empty candidate `2026-08-16`; H operational fallback record has null executor answer. Different evidence shapes. |
| C2 | Route identity. | R same `_run_case` as B, allowed route and executed fixture candidate. |
| C3 | Applicable adoption condition. | R allowed route and source-evidence verifier. H version linkage remains G02. |
| C4 | Verifier result showing failure of the condition. | R `passed=false`, candidate absent from source. H records parse/verifier failure with abstention. |
| C5 | Adoption decision = rejected / not promoted. | R `baseline_preserved`, source baseline output. |
| C6 | Locked baseline / prior supported state immediately before the decision. | R immediately prior baseline `2026-08-15`. |
| C7 | Corresponding system state after the decision. | R after-state remains `2026-08-15`, distinct from rejected candidate. |
| C8 | Replayable run artifacts, where necessary to establish the C1-C7 relation. | R original fixture/report and source. H matching historical source, where necessary, is G02. |

## D

Detailed evidence: [04_APPLICABILITY.md](04_APPLICABILITY.md).

| ID | Original request item | Response / boundary |
|---|---|---|
| D1 | Identity of the condition. | R method identity and parameters in the same fixture. |
| D2 | Source or mechanism of its applicability. | R upstream fixture/config supplies applicability; supported-method validation is visible. |
| D3 | Relation between the candidate and the selected condition. | R same case binds candidate and verification config; selection correctness is not pre-judged. |
| D4 | Point at which applicability is fixed or determined relative to verification and the adoption decision. | R config exists before routing, verification and adoption. |

## E

Detailed evidence: [05_UPSTREAM_INFLUENCE.md](05_UPSTREAM_INFLUENCE.md).

| ID | Original request item | Response / boundary |
|---|---|---|
| E1 | Selection of the applicable adoption condition. | Configuration-supplier influence exists: fixture method selects condition. No candidate-only field reassignment in shown R flow. |
| E2 | Content of the condition. | Fixture supplies expression/source/terms. Gold separation does not imply absence of condition-supplier influence. |
| E3 | Route selection. | Route enabled flag, method support and candidate emptiness affect routing; bounded candidate influence is explicit. |
| E4 | Verifier selection. | R configured method selects verifier behavior; H family mapping is separate. Production callers are not inferred. |
| E5 | Verifier behavior. | Candidate is inspected data; config controls the operation; H confidence/trace/error affect result. Data/control influence distinguished. |
| E6 | Any other element capable of changing the adoption decision outside the stated bounded relation. | D caller-supplied certificate can change adoption. Issuer/candidate/attempt binding is G03 / NOT AVAILABLE in provided excerpts. |

## F

Detailed evidence: [06_BYPASS.md](06_BYPASS.md).

| ID | Original request item | Response / boundary |
|---|---|---|
| F1 | Whether an alternative route exists to the same relevant adopted-system state. | R local selector identified; complete operational same-state entrypoint/writer map is G05 / NOT AVAILABLE. |
| F2 | Whether the relevant state can change without passing through the assessed boundary. | R failure returns baseline; mandatory placement before all operational state writes is G05 / NOT OBSERVABLE from excerpts. |
| F3 | Whether rejection is terminal for the identified adoption attempt. | R rejection is terminal within the identified invocation; no retry in its scorer. Operational attempt linkage is separate. |
| F4 | Whether the same candidate, or a functionally equivalent candidate, can be promoted through another route within the scope of C-01. | No second R promotion path in shown invocation. New run/lane not automatically out of scope; same-state re-entry linkage is G05. |

## P

Detailed evidence: [PROVENANCE.md](PROVENANCE.md).

| ID | Original request item | Response / boundary |
|---|---|---|
| P1 | Short name / identifier. | Per-file artifact identifier and package path in register. |
| P2 | Artifact type. | Artifact type and publication form in register. |
| P3 | Source or originating system. | Original repository/path/pin/selector and acquisition record. |
| P4 | Date or time interval of creation. | Recorded source/publication timestamps with explicit timestamp-kind limits. |
| P5 | Relation to the positive case, negative case, or architecture/path evidence. | Request section, inclusion reason and case/source cross-references. |
| P6 | Whether it is system-generated, an existing technical record, or a counterparty explanation. | Source code, stored run, synthetic fixture/report, existing test/audit and post-request explanation are distinguished. |
| P7 | Whether it existed before this Evidence Request. | Pre-request source pins and historical timestamps remain source records, not independent timestamp attestation. |
| P8 | If created after this request, whether it is a new run artifact of the unchanged existing mechanism or newly prepared explanatory material. | New publication index/tooling and selections are not new executions; original source evidence unchanged. |
| P9 | Whether any change was made after object confirmation that could affect C-01 or the evidence surface. | This publication-only change is disclosed. Deployment/config changes beyond inspected sources are G06 / NOT OBSERVABLE. |

## Transfer and process conditions

The current index follows sections 13-18 through separate raw artifacts, cross-references, identified excerpts/redactions and per-artifact provenance. Unavailable relations are disclosed rather than reconstructed. Source filenames/fields remain intact in the preserved evidence set.

Sections 19-22 distinguish administrative intake, commercial commencement, admissibility/sufficiency review, freeze and independent determination. No such later step is asserted completed by publishing this repository. Missing observability may limit the permissible determination; it is not automatically a negative finding.

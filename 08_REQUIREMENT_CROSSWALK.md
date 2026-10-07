# C-01 request crosswalk: all 45 items

**Coverage status: 45/45 REQUESTED ITEMS PROVIDED.**

No requested A1-F4 or P1-P9 item is left unanswered in this package. “Provided” means mapped to an identified evidence artifact, source relation, reproducible unchanged-component record, or provenance record. ANDEKS independently determines admissibility, sufficiency, and the final C-01 determination.

Post-request response to the exact 6 October request. Primary identification: [00_OBJECT_BINDING.md](00_OBJECT_BINDING.md). Technical argument: [10_OPERATIONAL_C01_PROOF.md](10_OPERATIONAL_C01_PROOF.md). No assessor verdict is asserted.

Evidence abbreviations: O = [operational source](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt); J = [June recovered component](evidence/source_recovery/bbeh_adoption_core_20260630.py.excerpt.txt); N = [new unchanged-component execution](reproduction/unchanged_component_cases.json); T = [control-flow/boolean analysis](reproduction/bounded_control_flow.json); H = [whole stored-corpus analysis](reproduction/whole_corpus_preservation.json); V = [version comparison](reproduction/source_equivalence.json). These are distinct evidence classes, not one invented execution.

## A

| ID | Original request item | Response and evidence |
|---|---|---|
| A1 | Where the assessed adoption path begins. | Identified row candidate enters the original verifier/adoption segment inside evaluate_revas_route; O, N |
| A2 | What candidate object enters it. | ExecutorOutput identified by row/attempt and its fields, including optional answer; O, N, historical rows |
| A3 | Where the applicable adoption condition is defined or retrieved. | O family policy, ExecutorVerifier, default gate threshold and final six-condition conjunction; J/V establish selected component version relation |
| A4 | Which component performs verification. | ExecutorVerifier.verify; actual execution in N |
| A5 | Where the adoption decision occurs. | base_default_adoption followed by enclosing supported-state selection; O/T |
| A6 | What state is treated as the adopted-system state for C-01. | Per-attempt RevasRouteRecord.final_answer/final_source, linked to recorded row output; 00 and T. No shared global store substituted |
| A7 | Where the assessed boundary ends. | Recorded/returned selected answer/source; T and existing recorder |

## B

| ID | Original request item | Response and evidence |
|---|---|---|
| B1 | Candidate identity. | N positive serializes candidate (B), metadata and new attempt ID; historical positive separately identified |
| B2 | Route identity. | Same operational verifier/adoption functions for positive and negative N cases; O |
| B3 | Applicable adoption condition. | Original parsed/verified/confidence checks; no new threshold; O/N |
| B4 | Verifier result. | N executes verifier and records verified=true |
| B5 | Adoption decision = adopted. | N records override_accepted=true from original gate |
| B6 | Resulting adopted-system state. | N intermediate final (B) linked to enclosing output by O/T; historical row also stores adopted (E) |
| B7 | Replayable run artifacts, where necessary to establish the B1-B6 relation. | N plus source excerpts, reproduction script, V and T; full solver/live product not claimed rerun |

## C

| ID | Original request item | Response and evidence |
|---|---|---|
| C1 | Candidate identity. | N failed_parse_nonempty retains candidate (B); historical abstention separately retains row/executor identity |
| C2 | Route identity. | N positive and negative use the same original operational verifier/adoption declarations |
| C3 | Applicable adoption condition. | O parsed/verified/default-confidence predicates; same conditions in N |
| C4 | Verifier result showing failure of the condition. | N actual verifier failure and reason; additional verifier and adoption failure cases distinguish the two |
| C5 | Adoption decision = rejected / not promoted. | N override_accepted=false; T links failure to outer fallback |
| C6 | Locked baseline / prior supported state immediately before the decision. | N baseline_before=(A), plus actual stored baseline in H rows |
| C7 | Corresponding system state after the decision. | N state_after=(A), not rejected (B); O/T extend relation to returned row; H checks stored equality |
| C8 | Replayable run artifacts, where necessary to establish the C1-C7 relation. | N, original source, executable reproduction, T/H; new controlled input is not called old production evidence |

## D

| ID | Original request item | Response and evidence |
|---|---|---|
| D1 | Identity of the condition. | Named verifier/gate predicates and enclosing conjunction; O, 04 |
| D2 | Source or mechanism of its applicability. | Source family policy, local verifier construction and gate parameter/default; O |
| D3 | Relation between the candidate and the selected condition. | Same ExecutorOutput goes to verification and adoption; N/O; no unrelated certificate substituted |
| D4 | Point at which applicability is fixed or determined relative to verification and the adoption decision. | Family/config before executor; verifier before gate; final selection before recorder gold/scoring; O/T |

## E

| ID | Original request item | Response and evidence |
|---|---|---|
| E1 | Selection of the applicable adoption condition. | Family/source policy influence disclosed; wrapper constructs verifier locally; 05/O |
| E2 | Content of the condition. | Source defaults and helper parameter influence disclosed, including direct caller threshold possibility; 05/O |
| E3 | Route selection. | Family/fact policy and parsed/verified/support predicates affect routing and final support; O |
| E4 | Verifier selection. | Explicit ExecutorVerifier construction in identified wrapper, family-mapped executor selection; O |
| E5 | Verifier behavior. | Candidate answer/parsed/confidence/trace/error materially affect result; source behavior versus input influence distinguished; O/N |
| E6 | Any other element capable of changing the adoption decision outside the stated bounded relation. | Caller baseline/config effects disclosed. Separate D certificate helper not used by identified H call chain; broader issuer binding not asserted; 05 |

## F

| ID | Original request item | Response and evidence |
|---|---|---|
| F1 | Whether an alternative route exists to the same relevant adopted-system state. | O/T identify single final selection/return for this invocation, with baseline fallback as alternative; 06 |
| F2 | Whether the relevant state can change without passing through the assessed boundary. | Candidate promotion into returned value requires the conjunction; all failing Boolean combinations preserve baseline; T. External shared-store claim remains distinct |
| F3 | Whether rejection is terminal for the identified adoption attempt. | Original normal-flow invocation returns baseline after failed admission without retry; O/N/T |
| F4 | Whether the same candidate, or a functionally equivalent candidate, can be promoted through another route within the scope of C-01. | No second promotion branch to the same returned record in shown wrapper/recorder. New invocation obeys same checks; external shared writers not dismissed by different run IDs; 06 |

## P

| ID | Original request item | Response and evidence |
|---|---|---|
| P1 | Short name / identifier. | Per-file artifact IDs and paths in ARTIFACT_REGISTER.csv |
| P2 | Artifact type. | Register separates source, excerpt, old record, new analysis and new component execution |
| P3 | Source or originating system. | Source repository/path/pins/blob identity, original acquisition and new source_recovery_20261007.json |
| P4 | Date or time interval of creation. | Source commit timestamps, new execution created_at and publication times explicitly distinguished |
| P5 | Relation to the positive case, negative case, or architecture/path evidence. | This crosswalk, per-section maps and inclusion reasons |
| P6 | Whether it is system-generated, an existing technical record, or a counterparty explanation. | Register/reproduction classifications distinguish these categories |
| P7 | Whether it existed before this Evidence Request. | Original evidence and June source predate request; new selections/analysis/reproduction explicitly dated afterward |
| P8 | If created after this request, whether it is a new run artifact of the unchanged existing mechanism or newly prepared explanatory material. | N is NEW_POST_REQUEST_EXECUTION_OF_UNCHANGED_EXISTING_COMPONENTS with new controlled inputs; V/T/H are analysis; documents are explanations |
| P9 | Whether any change was made after object confirmation that could affect C-01 or the evidence surface. | 09 discloses source recovery, new component execution and evidence-surface changes; original implementation/records not edited; outside deployment history not asserted |

Request sections 13-18: separate artifacts, identified excerpts, truthful new/old labels and preserved source fields. Sections 19-22: independent sufficiency/admission/assessment remain separate; this is not their outcome. Scope qualifications identify what the proof does and does not establish rather than forcing blanket PASS or blanket NOT AVAILABLE.

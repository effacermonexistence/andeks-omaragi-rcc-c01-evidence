# Provenance and evidence classes

## Pre-existing originals

Source 1: `effacermonexistence/omaragi-reliability-replay @ f141fd09217279ca48f2cfbecc532fed8ecaa6e9`, recorded commit time `2026-08-30T01:13:34Z`.

Source 2: `effacermonexistence/omar-benchmark-replay-live-source @ 8976dc12c2d398dd59e4e193c41fa36749dee996`, recorded commit time `2026-09-01T19:09:24Z`.

[Original acquisition record](provenance/source_acquisition.json) and [original public-copy transformations](provenance/public_copy_transformations.json) are unchanged. They describe the initial 48 evidence artifacts, not every later added artifact. Source/public hashes and private-prefix redactions remain as recorded.

## Recovered historical source

[Additional recovery metadata](provenance/source_recovery_20261007.json) records excerpts from source-2 commit `b38e6757673173df19216877368e020eb4b51fc5`, recorded time `2026-06-30T23:41:59Z`, full original Git blob `2eb56b207971ac569865d256633c4b2d62f6ef23`.

The original full-file SHA-256 was not computed in this recovery and is not fabricated. Excerpt public SHA-256, source path, commit, Git blob and selector are supplied. [Component AST comparison](reproduction/source_equivalence.json) verifies the exact selected declaration relationship. It is not a claim that the whole initial pre-run frozen file or all solver/family logic is identical.

## Newly created records, explicitly after the request

| New material | Classification |
|---|---|
| source_equivalence.json | New source analysis of old components |
| unchanged_component_cases.json | New execution of unchanged original verifier/adoption components, with new controlled test inputs |
| bounded_control_flow.json | New source/control-flow and finite-Boolean expression analysis |
| whole_corpus_preservation.json | New analysis of already stored records; no new benchmark |
| source_recovery_20261007.json | New provenance metadata identifying recovered old source |
| README, A-F/P maps, proof and scripts | New explanatory or verification tooling, not historical behavior |

[Change record](09_CHANGE_RECORD.md) discloses the distinction between the earlier static-only package checks and the new controlled execution. No original assessed source or historical record was edited. Git times are source-record times, not independent timestamp attestation.

## Integrity

[ARTIFACT_REGISTER.csv](ARTIFACT_REGISTER.csv) covers all publication files, including newly recovered excerpts and newly executed component records. Old historical rows retain their original provenance fields. [PACKAGE_SHA256SUMS.txt](PACKAGE_SHA256SUMS.txt) covers final bytes except itself; register self-reference exclusions remain explicit.

The original `scripts/verify_package.py` still performs static package checks only. The new `scripts/finalize_evidence_repair.py` separately runs the explicitly labeled reproduction, protects every previously acquired evidence file byte-for-byte, refreshes all new provenance classes, and then calls that original static checker. A static check reporting that it did not execute RCC is not misread as a claim that the separate reproduction did not execute components.

No private source URL is needed to inspect the submitted principal evidence. Full private source, unrelated product code, credentials and private correspondence are not newly published.

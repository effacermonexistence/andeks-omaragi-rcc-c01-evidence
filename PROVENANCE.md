# Provenance and P1-P9

## Original source identities remain unchanged

| Source | Pinned commit | Git author/committer timestamp | Access at initial acquisition |
|---|---|---|---|
| `effacermonexistence/omaragi-reliability-replay` | `f141fd09217279ca48f2cfbecc532fed8ecaa6e9` | `2026-08-30T01:13:34Z` | Public |
| `effacermonexistence/omar-benchmark-replay-live-source` | `8976dc12c2d398dd59e4e193c41fa36749dee996` | `2026-09-01T19:09:24Z` | Private |

The original [source acquisition record](provenance/source_acquisition.json) records authenticated pinned source acquisition, Git blob identity, byte counts, SHA-256 values and source-path timestamps. It and [copy transformations](provenance/public_copy_transformations.json) are preserved unchanged by this revision. The two source repositories are not edited.

## P1-P9 response

| ID | Where supplied / boundary |
|---|---|
| P1 | `artifact_id`, `package_path` in [ARTIFACT_REGISTER.csv](ARTIFACT_REGISTER.csv) |
| P2 | `artifact_type`, `publication_form` distinguish copy, excerpt, selected record and index |
| P3 | `original_repository`, `original_path`, `pinned_source_commit`, source selector and acquisition record |
| P4 | `original_timestamp` and `timestamp_kind`. Git source-record times are not authenticated historical event times; embedded run timestamps remain separate |
| P5 | `andeks_section`, `reason_for_inclusion`, selected record pointers and [45-item crosswalk](08_REQUIREMENT_CROSSWALK.md) |
| P6 | Technical source, stored operational record, synthetic reference fixture/report, audit/test definition and counterparty index are expressly distinguished. Existing test source is not a new passing test receipt |
| P7 | Historical evidence is fixed at the recorded pre-request pins; this is source-record provenance, not independent timestamp attestation |
| P8 | New documents, excerpts/selections and publication tooling are post-request representations of existing evidence, not new runs. No assessed mechanism is executed by metadata refresh |
| P9 | [09_CHANGE_RECORD.md](09_CHANGE_RECORD.md) identifies this publication-only change and earlier snapshot distinctions. Deployed changes outside inspected sources are G06 / NOT OBSERVABLE, not presumed absent |

## Historical versions

The original BBEH run records accepted_B=1 and its executor hash. The later pre-request offline repair records accepted_B=0. The September executor excerpt has additional family-level hardening and is not asserted byte-identical to the June executor. The July BYOK audit's source hashes belong to its own repair snapshot, not automatically to the September excerpts.

## Publication forms

Preserved source copies remain byte-identical. Selected JSON objects retain their original parent pointers but have post-request file serialization. Verbatim excerpts retain source ranges and are not standalone executable substitutes. Three original JSON files have only the private workspace prefix redacted, as documented in [DISCLOSURE.md](DISCLOSURE.md); original/public hashes remain distinct.

## Current register and checksum rules

The artifact register covers every tracked publication file. Pre-existing E rows and their source metadata are preserved. Changed/new index rows receive current publication timestamps and hashes; no historical source pin or execution time is invented for them. The register's own hash/byte cells use `SELF_REFERENCE_EXCLUDED`; the checksum manifest's register hash is `MANIFEST_SELF_EXCLUDED`. The checksum manifest hashes the final register but excludes itself.

`scripts/refresh_publication_metadata.py` only refreshes post-request index rows and checksum metadata and refuses altered pre-existing evidence. `scripts/verify_package.py` separately checks existing stored artifacts, hashes, linked selected records, receipt hashes and stored BBEH counts. Such checks do not run RCC, call model providers, rerun the original tests or constitute an independent assessment.

The initial publication remains identifiable at `329b46add38a1770b484bdf90e9db458407a15e1`. Git history, current manifest and the change record distinguish its index from this revision; source artifacts are not rewritten to fit the revised explanation.

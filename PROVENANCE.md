# Provenance

## Source pins

| Source | Pinned commit | Git author and committer timestamp | Access during acquisition |
|---|---|---|---|
| `effacermonexistence/omaragi-reliability-replay` | `f141fd09217279ca48f2cfbecc532fed8ecaa6e9` | `2026-08-30T01:13:34Z` | Public |
| `effacermonexistence/omar-benchmark-replay-live-source` | `8976dc12c2d398dd59e4e193c41fa36749dee996` | `2026-09-01T19:09:24Z` | Private |

Acquisition used authenticated GitHub API reads of pinned commits, trees and blobs. Every acquired blob was checked against its Git blob SHA-1 and byte count; SHA-256 was computed for the source and public copy. Neither source repository was edited. Source-2 private checkout contents outside the authorized evidence set are not published.

The [acquisition record](provenance/source_acquisition.json) maps every evidence file to the pin, original path, last path-changing commit before that pin, date, original blob hash and SHA-256. **Git commit timestamps are source-record timestamps, not independently authenticated event times.** Embedded run times are separate recorded fields. Acquiring a file today does not change its historical event time.

## Pre-existing versus post-request

- Original code, fixtures, report records, audit files and tests are **pre-existing source evidence** at the named pins, both earlier than the request date `2026-10-06`.
- README, A–F mappings, counterparty explanations, this provenance page, disclosure record, artifact register, hash manifest and integrity tooling are **post-request publication/index material**.
- Selected JSON objects are post-request selections of unchanged pre-existing objects; they are not newly run cases. Their exact parent pointer/JSONL line is in the register.
- Source excerpts are post-request documentary selections of verbatim source lines. They are labeled excerpts, not whole originals or deployable replacement code.
- Redacted JSON copies retain original filenames but are explicitly labeled in the register and [disclosure record](DISCLOSURE.md). The only redaction is a private local workspace prefix; original/public hashes differ and both are recorded.

## Historical source-version distinctions

The initial BBEH run files record their executor hash and original accepted_B=1. The later pre-request offline repair file records final accepted_B=0. The implementation at the September pin includes additional family-level hardening. Its file hash is not assumed identical to the June run's executor hash.

The July BYOK audit's `hashes` object records its own earlier repair snapshot, while this package's source excerpts come from the September pin. Register hashes establish those identities separately; no false one-to-one hash match is claimed.

## Register and manifest rules

[ARTIFACT_REGISTER.csv](ARTIFACT_REGISTER.csv) covers all tracked files, including index material. Original source path, pinned commit and source hash apply only where a historical source exists. Index-only files have no fabricated source pin. `ARTIFACT_REGISTER.csv` uses `SELF_REFERENCE_EXCLUDED` for its own hash cell; [PACKAGE_SHA256SUMS.txt](PACKAGE_SHA256SUMS.txt) includes its final actual hash and excludes only itself. The manifest's register hash cell is `MANIFEST_SELF_EXCLUDED` to avoid circular hashing.

The acquisition transcript, full private source API responses and unpublished source originals remain outside this public repository. Hashes prove byte identity of the published package, not historical authenticity, full corpus completeness or RCC efficacy.

## No new mechanism or experiment

No assessed source code was edited or executed. No benchmark was rerun; no provider call was spent; no new runtime case was constructed. Package integrity checks only parse existing stored records, match selected objects, count stored row outcomes, verify hashes and check publication links. They are publication checks, not new assessment evidence or newly executed source tests.

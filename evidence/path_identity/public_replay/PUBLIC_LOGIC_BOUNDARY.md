# Public Logic Boundary

This repository contains a simplified public reliability policy created for the OmarAGI Reliability BYOK Replay Build Week demonstration.

The live OmarAGI website accepts a user-supplied API key and runs actual model calls through the BYOK reliability workflow. This repository is not that live runtime. It is a sanitized, deterministic, offline representation of the public decision shape around a BYOK run.

## Included

The public workflow is intentionally small and inspectable:

```text
baseline
→ router
→ offline deterministic public executor
→ target-blind runtime verifier
→ adoption gate
→ decision lock
→ post-lock scorer
→ scored artifact
```

The default fixture is synthetic, the public executor only replays sanitized pre-generated candidates, and the available runtime verifiers are transparent. Runtime stages receive no post-lock scoring target. The decision is hashed before the scorer runs, and the artifact score is deterministic and documented. The code makes no network call and has no hidden runtime dependency.

## Excluded

This repository does not contain, reconstruct, or document:

- OmarAGI production decision logic;
- internal routing thresholds or production governance rules;
- confidential prompts or private datasets;
- private benchmark, customer, or partner material;
- unpublished evaluation results;
- credentials or production infrastructure configuration.

It also does not accept, transmit, or store a user's BYOK credential.

## Claim boundary

The included five-case fixture is synthetic, benchmark-shaped demonstration data. Its 0–100 artifact score explains the visible public outcome and is explicitly not a benchmark metric. The fixture is not benchmark evidence, independent validation, a production-readiness claim, or a universal reliability claim. The routing and adoption design aims to make candidate replacement safer and more inspectable; it does not guarantee that every answer improves.

The separate [`EVIDENCE.md`](EVIDENCE.md) page links to a committed live BYOK diagnostic. That external artifact retains its own diagnostic-only claim status and is not imported as proof for the synthetic fixture.

## Input boundary

The loader accepts only artifacts that explicitly declare the public demo schema and `synthetic: true`. Unsupported or malformed artifacts fail closed before replay.

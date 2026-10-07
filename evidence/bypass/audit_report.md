# BYOK Global Zero-Downlift Gate — Repair Audit

UTC run: 2026-07-18T20:17:59Z
Source parent: `c5945656cbcce8164c5f84a399d72b9d25f4c732`
Scope: 17 public BYOK lanes × OpenAI/Mistral/Anthropic = 51 route cells.

## Locked result

A completed, publishable canonical BYOK run now has one of two outcomes:

1. a routed candidate is adopted only through an audited pre-score verifier/certificate and row-level `accepted_B=0` evidence; or
2. the paired baseline remains canonical.

If canonical final-vs-baseline row evidence is missing, or any row has `accepted_B>0`, the run fails closed and is retained only as diagnostic evidence. Benchmark score/gold is never used to choose between baseline and routed output.

Security regression follows the same control-layer floor: uncertified control candidates remain diagnostic and canonical `security_B=0` is baseline-preserved; certified control lanes must emit explicit zero-regression evidence.

## Failure family removed

The prior model-substitute/reconstructed gate compared benchmark grades after generation and used that comparison for adoption while labeling the decision gold-blind. That was a scorer-visible best-of gate. It has been replaced by `strict_gold_blind_baseline_floor_v1`.

## Verification

- Focused changed-scope suite: **113/113 PASS**.
- Python compile: **PASS**.
- Matrix preflight: **17 lanes / 3 providers / 51 unique route cells**.
- All 51 cells structurally guarded: **true**.
- Row accounting detects downlift even when aggregate net uplift remains positive.
- Missing row evidence fails closed.
- Certified zero evidence passes; certified missing/nonzero evidence fails.
- Uncertified candidate uplift remains visible only as diagnostic evidence.

## Repository-wide suite disclosure

A broad repository-wide discovery run completed 1,005 tests with 77 failures and 50 errors. The failures include landing/Lua/R2/network/integration surfaces outside this benchmark repair and are not used as the changed-scope release gate. This patch did not edit those surfaces. The exact changed-scope suite above is green.

## Claim boundary

This audit proves the **code path and adoption invariant**, not a fresh external-provider outcome matrix. No OpenAI, Mistral, or Anthropic credential was available in the execution environment, so the 51 live provider cells were not freshly spent/replayed in this repair. The honest claim is:

> Publishable canonical BYOK runs cannot complete with accepted_B above zero; uncertified candidates fall back to baseline, and missing/nonzero evidence fails closed.

It is not valid to claim that every routed candidate is intrinsically regression-free or that all 51 external cells were freshly executed.

## Source hashes

- patch diff: `5900b4cb7e8fe2649fc88fc5798ab6e8e251d236f2a95dd490306b62f16fce05`
- `app.py`: `03f75ed8f6f2269ab1b3eb79360106291ffe3b779326e60e821afc64a7937c82`
- `benchmark_replay_harness.py`: `1ed1a8e302063ce2f3d32dab2b08350b094e23e74409ea9923f4919e4754a3c6`
- `reconstructed_matched_live_harness.py`: `a7981e283765148bfa603ca90676438005a3da091f9c08d3dbd56d68e7214dba`
- `runners.py`: `74990770815843e7c3fe1b4cedba5b4836810c755b0275a69076df4e3dff5e96`
- `tests/test_byok_zero_downlift_global_gate.py`: `6baf8cfca9640de058a13d556c3dd997c052e0279dc4ed2d4c962a38e1f3f6e4`

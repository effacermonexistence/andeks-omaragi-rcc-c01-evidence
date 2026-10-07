# Evidence index

This page separates the repository's **synthetic architecture demonstration**
from a **committed live BYOK diagnostic run** that can be inspected on
omaragi.com.

## Evidence lanes

| Lane | What it establishes | What it does not establish |
|---|---|---|
| Public repository fixture | The offline Router → Executor → Runtime Verifier → Adoption Gate → Decision Lock → Post-lock Scorer → Scored Artifact path is deterministic and testable without credentials. | Benchmark uplift, production validation, or the private production implementation. |
| Committed live diagnostic | A 100-case BYOK run produced inspectable raw outputs, route logs, results, costs, and a reproduction manifest. | Historical-board reproduction, independent validation, clean public benchmark proof, or universal uplift. |

## Committed live BYOK diagnostic

- **Run ID:** `run_1779840603_8c2cfeec9d`
- **Lane:** SimpleQA Verified / VSF — matched-live reproduction attempt
- **Executed cases:** 100
- **Selected model:** `gpt-4.1`
- **Historical reference model:** `gpt-5.2`
- **Model comparison status:** `MODEL_SUBSTITUTE`
- **Metric reported by the run:** baseline F1 `0.400000`; governed final F1
  `0.484848`; absolute change `+0.084848`; relative change `+21.21%`
- **Artifact claim gate:** `claim_allowed_for_run=false`
- **Evidence label in the artifact:** `diagnostic live replay`

Those numbers describe this committed diagnostic artifact only. The run itself
states that the selected model does not match the historical model and that the
historical numeric reproduction gate was not applied. They are therefore not
presented here as benchmark proof or a reproduction of the historical board.

### Inspect the run

- [Human-readable report](https://omaragi.com/results/run_1779840603_8c2cfeec9d)
- [Raw model outputs — JSONL](https://omaragi.com/results/run_1779840603_8c2cfeec9d/raw_outputs.jsonl)
- [Route log — JSONL](https://omaragi.com/results/run_1779840603_8c2cfeec9d/route_log.jsonl)
- [Full results — JSON](https://omaragi.com/results/run_1779840603_8c2cfeec9d/results.json)
- [Tabular results — CSV](https://omaragi.com/results/run_1779840603_8c2cfeec9d/results.csv)
- [Reproduction manifest — JSON](https://omaragi.com/results/run_1779840603_8c2cfeec9d/repro_manifest.json)
- [Cost summary](https://omaragi.com/results/run_1779840603_8c2cfeec9d/cost_summary.txt)
- [Run a fresh BYOK check](https://omaragi.com/run#byok-run)

### Download integrity

The public files were downloaded and hashed on 2026-07-21 PT.

| File | Rows | SHA-256 |
|---|---:|---|
| `raw_outputs.jsonl` | 100 | `ddb936ca8c3b44309395ea8a9df05494397def40be85b5aeb68fabceab9e7142` |
| `route_log.jsonl` | 100 | `101114c93e5dbe6165d02f8628b87d09a231a1a087f4a7e49bd127d6555952ad` |
| `results.json` | — | `cae1ab23f93ecaa5720cbd5dc5baed6b1d99b52948ca8b883605cbca08bddd33` |
| `results.csv` | 100 | `95fed6173002d155320ae01f64f2f52a9cac169cb8339218371dafefb63ee28c` |
| `repro_manifest.json` | — | `45c88933951198e0726f186edb96d30706624e29c610055267adc326ad2059be` |
| `cost_summary.txt` | — | `b02112f4b7d1a9dfb9fb4cfde8f5036b40904cac86ddd8a325658d8717c7875c` |

The repository links to these committed artifacts rather than duplicating the
100-case payload. Live, non-committed run logs may be ephemeral across service
restarts; the linked committed example is the stable inspection surface.

## Decision-lock evidence in this repository

The synthetic public runner demonstrates a stronger causal boundary than the
previous version:

1. Runtime routing, execution, verification, and adoption receive no
   `post_lock_scoring` object.
2. The chosen final answer and its upstream decision objects are serialized and
   hashed into a `decision_lock` receipt.
3. Only after that receipt exists does the post-lock scorer read the scoring
   target.
4. Tests mutate the scoring target and verify that the route, adopted answer,
   and decision-lock hash do not change.

This is public reference architecture, not a claim that the synthetic fixture is
a clean benchmark run or that it exposes private OmarAGI production logic.

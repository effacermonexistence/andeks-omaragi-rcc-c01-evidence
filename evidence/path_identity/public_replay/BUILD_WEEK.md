# OmarAGI Reliability BYOK Replay — Build Week

## Project summary

OmarAGI Reliability BYOK Replay is the public demonstration surface for a live BYOK reliability workflow. The live OmarAGI website lets users supply their own API key and run actual model calls; this repository replays the sanitized public decision shape through explicit runtime and evaluation stages: Baseline → Router → Executor → Runtime Verifier → Adoption Gate → Decision Lock → Post-lock Scorer → Scored Artifact. It emits structured JSON, Markdown, and a local visual report for every decision without calling the private production executor.

## Inspiration

AI systems can generate alternative answers cheaply. The harder engineering problem is deciding whether a new answer has earned the right to replace the previous one. This project turns that hidden adoption decision into an explicit, replayable workflow.

The connected live product is where that workflow operates around real BYOK model output: a routed and verified candidate may replace the baseline, while a candidate that does not earn adoption leaves the fallback floor intact. The repository is deliberately offline and synthetic so reviewers can inspect that architecture safely; its five cases are a benchmark-shaped demonstration, not benchmark evidence or a universal performance claim.

## What it does

1. Loads a clearly labeled synthetic replay fixture.
2. Records the baseline and sanitized candidate inputs.
3. Applies a small public router.
4. Runs an explicit deterministic offline public executor.
5. Runs one transparent deterministic runtime verifier without access to the scoring target.
6. Applies an adoption gate that replaces the baseline only after runtime verification passes.
7. Hashes and locks the decision before any target-based scoring occurs.
8. Runs a separate post-lock scorer that cannot alter the locked answer.
9. Preserves the baseline on route denial, unsupported verification, an empty candidate, or verifier failure.
10. Creates a transparent public demonstration artifact score.
11. Exports the ordered eight-stage event trail to JSON, Markdown, and a local web UI.

The committed fixture includes candidate-adoption and baseline-preservation cases. It makes no network calls and requires no secrets.

## How it was built

The implementation is a Python package with:

- a deterministic replay engine;
- a deliberately limited public policy;
- a CLI entry point;
- a standard-library local HTTP server;
- JSON, Markdown, and HTML report exporters;
- synthetic fixtures;
- unit, smoke, clean-copy, and public-safety checks.

The release repository was created as a clean standalone history rather than publishing a legacy monorepo.

## Challenges

- Making the adoption decision inspectable without exposing private production logic.
- Preserving the baseline as an explicit fallback rather than treating every generated candidate as an upgrade.
- Separating a compelling demonstration from unsupported benchmark or production claims.
- Making score-target non-interference structural and testable rather than relying on a prose promise.
- Producing a default experience that is deterministic and requires no API key.

## What was learned

- Candidate generation and candidate adoption are different engineering objects.
- A compact event trail can make router, executor, verifier, adoption-gate, score, and final-source decisions easy to audit.
- A public demo is stronger when its evidence boundary is machine-readable and test-enforced.
- A verifier and a scorer are different authorities: adoption must be locked before target-based scoring.
- An offline synthetic path is useful for judges because it removes credential and provider variability.

## Inspectable evidence bridge

The public repository stays synthetic, but [`EVIDENCE.md`](EVIDENCE.md) links to a committed 100-case live BYOK diagnostic with raw outputs, route logs, results, costs, and a reproduction manifest. That run is intentionally labeled `diagnostic live replay`, `MODEL_SUBSTITUTE`, and `claim_allowed_for_run=false`; it is evidence that the live path produced inspectable artifacts, not a historical-board reproduction or universal uplift claim.

## Exact role of GPT-5.6

GPT-5.6 was used during the Build Week workflow for reasoning, specification refinement, architecture review, public explanation, and checking whether the demo matched the intended reliability behavior. It is not required to run this repository, and the public demo does not make a GPT-5.6 API call.

## Exact role of Codex

Codex was used for repository analysis, implementation, debugging, test generation, documentation, clean-repository extraction, security review, and release preparation. It is not required to run the finished demo.

## What is next

- Add optional model adapters while keeping the deterministic offline replay as the default path.
- Add more transparent verifier plugins for bounded public task families.
- Extend the current SHA-256 decision receipt toward signed replay artifacts and richer report comparison.
- Keep the public demonstration boundary separate from private production logic.

## Local testing instructions

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
python -m unittest discover -s tests -v
./scripts/smoke_test.sh
./scripts/clean_install_test.sh
```

Start the web UI:

```bash
omaragi-replay serve \
  --input samples/public_demo_replay.json \
  --output-dir output/demo
```

Then open <http://127.0.0.1:8765/>.

## Suggested Devpost repository link title

**Try OmarAGI Reliability BYOK Replay on GitHub**

Repository: <https://github.com/effacermonexistence/omaragi-reliability-replay>

Website: <https://omaragi.com>

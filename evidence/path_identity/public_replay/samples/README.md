# Public Demonstration Sample

`public_demo_replay.json` contains five invented examples created only to exercise
the public demo's router, executor, target-blind runtime verifier, adoption gate,
decision lock, post-lock scorer, artifact score, logging, and flip-accounting
paths.

The fixture is intentionally synthetic. That constraint remains machine-readable
in the artifact even though the judge-facing UI uses the shorter “public
demonstration sample” label.

It is a benchmark-shaped demonstration of the public decision architecture around
a live BYOK workflow. It is not benchmark evidence, and it does not execute or
store a user-supplied API key.

It contains no production record, customer input, benchmark row, private prompt,
credential, or proprietary RCC rule.

Each case supplies:

- a unique `case_id`
- an invented prompt
- a baseline output
- a pre-generated sanitized candidate
- an explicit public route request
- one transparent runtime-verification specification containing task evidence or constraints
- one separate post-lock scoring specification used only after the decision receipt exists

The engine projects those inputs into a runtime-only view and creates explicit
`router_result`, `executor_result`, `runtime_verifier_result`,
`adoption_gate_result`, `decision_lock`, `post_lock_scorer_result`, and
`artifact_score` objects. The executor is deterministic and offline; the scorer
cannot change the locked answer; the artifact score is a public demonstration
explanation aid, not a benchmark metric.

The loader rejects an artifact unless its `artifact_kind` matches the public
schema, `synthetic` is `true`, and every case passes structural validation.

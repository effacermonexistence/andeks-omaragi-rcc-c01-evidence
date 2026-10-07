# E: upstream influence in the identified operational relation

Influence is disclosed, not assumed absent. Sources are the [operational excerpt](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt), [historical runner](evidence/upstream_influence/run_bbeh500_full_gold_blind.py) and [source/control-flow records](reproduction/bounded_control_flow.json).

| ID | Actual influence and boundary |
|---|---|
| E1 | Caller-supplied family and source family policy affect executor/route selection. The shown `evaluate_revas_route` selects `ExecutorVerifier` in code, rather than reading a condition instruction from candidate text |
| E2 | Existing source defaults and comparisons supply verifier/adoption thresholds. A direct helper caller can supply `confidence_threshold`; the shown enclosing call uses the default. This parameter influence is not described as impossible |
| E3 | Family and fact policy influence selection; parsing, verifier result, shape and support predicates affect final route support |
| E4 | Family mapping selects the executor; the shown function explicitly constructs `ExecutorVerifier()`; no D certificate issuer is used by this H call chain |
| E5 | Candidate answer, parsed flag, confidence, trace and error are inspection inputs and materially affect verifier results. Source selection/configuration affects the operation; candidate data influence is not equivalent to rewriting source |
| E6 | Baseline supplied by the caller, candidate metadata and any explicit helper threshold affect the decision relation. In the shown operational wrapper the verifier is computed from that same candidate, not accepted as a separate caller certificate. External reconfiguration or arbitrary mutation of Python source is not tested by these normal-flow records |

The historical base-model answer is used as baseline, not as the condition definition. The recorded candidate comes from the local executor. Gold is loaded by the shown recorder only after final answer/source selection. The statement is supported by call ordering and recorded fields, not by visibility flags alone.

The new component reproduction supplies controlled candidate metadata and executes the actual verifier before the actual adoption function. It does not forge a passing verifier result or patch either component. Its finite cases do not prove correctness of all possible verifier inputs.

The broader [D certificate helper](evidence/bypass/benchmark_replay_harness.py.excerpt.txt) is a different route whose caller-supplied certificate can change its decision. Its issuer binding remains outside the evidence established here. It is retained as context, not relied upon to prove that the identified operational H path has no upstream influence or no bypass.

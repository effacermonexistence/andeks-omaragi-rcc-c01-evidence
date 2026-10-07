# D: applicability in the operational path

| Item | Existing relation and source |
|---|---|
| D1 | `ExecutorVerifier.verify`, the gate's existing `confidence_threshold=0.9`, and `evaluate_revas_route`'s six-condition support conjunction identify the conditions |
| D2 | Family/type policy selects the executor; the operational function constructs its verifier locally; gate parameters/defaults and source policy supply applicability |
| D3 | The same `ExecutorOutput` is passed to verification and adoption. Its parsed/confidence/trace/error and returned verifier result are used by those exact calls |
| D4 | Family/configuration is supplied before candidate processing; verification precedes adoption; outer supported-state selection precedes recorder scoring |

[Current operational source](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt), [recording call site](evidence/upstream_influence/run_bbeh500_full_gold_blind.py), [new component cases](reproduction/unchanged_component_cases.json).

The verifier rejects unparsed, empty, low-confidence, trace-less or error-bearing results by its existing comparisons. The adoption component separately rejects confidence below its threshold. This documents the actual program predicates; it does not assert that these predicates prove answer truth for all tasks, or add finite-number or other requirements absent from the source.

[Recovered June declarations](evidence/source_recovery/bbeh_types_verifier_20260630.py.excerpt.txt) and [adoption functions](evidence/source_recovery/bbeh_adoption_core_20260630.py.excerpt.txt) are compared with current selected declarations in [source_equivalence.json](reproduction/source_equivalence.json). Whole-module family policies changed; the exact initial pre-run freeze file is not claimed recovered merely because the committed adoption components match.

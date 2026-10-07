# F: mandatory scope for the identified per-attempt output

The relevant state is identified in [00_OBJECT_BINDING.md](00_OBJECT_BINDING.md). It is the answer/source returned for this adoption attempt, not an unspecified shared production store. [Original source](evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt), [recording call site](evidence/upstream_influence/run_bbeh500_full_gold_blind.py), [mechanical control-flow record](reproduction/bounded_control_flow.json) and [conditional proof](10_OPERATIONAL_C01_PROOF.md) are the primary evidence.

| Item | Source-derived answer |
|---|---|
| F1 | Inside the shown operational wrapper, there is one final-answer assignment and one returned `RevasRouteRecord`. Its alternative branch is baseline preservation, not unguarded candidate promotion |
| F2 | For this returned value, the support conjunction controls the single candidate-versus-baseline assignment. Any false conjunct selects `base_answer`. The shown recorder copies that final value and does not select a new answer after scoring |
| F3 | Failure in the identified normal invocation reaches the baseline return, with no retry/re-promotion loop in that function. The reproduction demonstrates failure/non-promotion; the source links it to the outer return |
| F4 | The same candidate can be evaluated in a distinct invocation, but the shown function applies the same checks and returns that invocation's own record. No second promotion route to the first returned record is present in the shown flow. Whether a separate caller overwrites a shared external store is a different, explicitly unestablished state claim, not dismissed merely because a run ID changed |

The finite source-expression analysis enumerates all 64 combinations of the six support booleans. Its 63 failing combinations select baseline and fallback source. This is exhaustive for those boolean expressions, not 64 live product runs or proof against arbitrary mutation of interpreter state.

The existing broader [51-cell BYOK audit](evidence/bypass/audit_report.md) is retained with its declared limitations. It is not the justification for F1-F4 above. A downstream completion rejection is not retroactive non-adoption. D's certificate/helper and summary files are not aliases of this H return value.

If C-01 is intended to include a particular persistent shared state beyond the identified recorded per-attempt output, its writers and authorization paths still require evidence. This package neither fabricates that proof nor calls an arbitrary new run automatically outside scope. The narrower value-level argument is explicit so its applicability can be assessed without a silent object substitution.

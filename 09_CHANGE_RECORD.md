# Change and execution disclosure: 7 October 2026

Prior reviewed package: `b61e2159a7c10a7ce3a604f4c972a671cc9025f6`. Initial package: `329b46add38a1770b484bdf90e9db458407a15e1`.

## Original request identity

| Privately reviewed original | SHA-256 |
|---|---|
| 06.10.2026_ANDEKS_OmarAGI_RCC_Bounded_Evidence_Request_v1.0_EN_EXTERNAL.pdf | 9ff401dd93c9ee952575be1664cb8fa7637574c133d002b0b385dad3aa944b3a |
| 05.10.2026_ANDEKS_OmarAGI_RCC_Assessment_Object_Confirmation_Record_v1.0_EN_EXTERNAL.pdf | 219f95a6d377e9f6d9b938a08f0a31c1cc925b5abf70aa51666db27c6b8c78df |

## This revision

Recovered two necessary excerpts from the June committed operational source, compared selected declarations to the existing current-source excerpt, and added a source-derived conditional proof/control-flow argument. The entire initial frozen source file is not claimed recovered.

Added **new execution of unchanged existing verifier/adoption components**, with newly disclosed controlled inputs. This is a P8 new run artifact at component scope, not an old production trace, not a fresh BBEH run, and not a newly created implementation. Source declarations and predicates are compiled unchanged; the separate runner supplies standard-library imports and test inputs. Candidate generation and the full solver/product are not executed.

Added new analysis of all stored original failed-admission rows and patched fallback rows. These are data checks, not new model calls. Patched fallback selection is read from its actual final-source field; an absent patched gate flag is not invented. The first analysis-reader attempt failed on that absent field; the reader was corrected, not the stored artifact.

Updated A-F/P mappings to the actual operational component and enclosing returned state. The R synthetic demo and D completion helpers remain separately labeled supplementary evidence rather than silently filling another path's gaps.

## P9: mechanism versus evidence surface

Changed evidence surface: added source selections, source comparison, controlled component-execution records, static/stored-data analysis, explanatory mapping and integrity metadata. Effective times and executing revision/run IDs are in the generated records and Git history.

**Unchanged by this task:** original source repositories, every previously published historical evidence file, original acquisition and redaction metadata, thresholds, verifiers, routing rules, gate bodies and original run outcomes. Finalization compares all previously protected files with the prior package and stops on a mismatch.

Prior wording that no assessed code was executed described earlier packaging checks. It does not describe this new, explicitly labeled component reproduction. No mechanism change is hidden behind that old wording.

No claim is made about uninspected deployments or shared stores outside the identified source/value boundary. Whether a scope clarification matches the already constituted object remains independently assessable; no historical agreement or assessor acceptance is fabricated.

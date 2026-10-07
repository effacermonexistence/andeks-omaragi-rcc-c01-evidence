# Benchmark Gold-Blind Adoption Lock

Status: SYSTEM-PROMPT-GRADE REPO LOCAL LOCK
Created: 2026-06-30 / 2026-07-01 UTC

## Conclusion
Any benchmark final-answer adoption that chooses between base and candidate after seeing scorer/gold-derived grades is oracle diagnostic only.

## Forbidden pattern

```text
base answer
candidate answer
-> score/grade base with gold/scorer/correctness
-> score/grade candidate with gold/scorer/correctness
-> choose row-level winner
```

This is forbidden even if the raw gold answer is not directly placed in the generation prompt. A grade, score, correctness flag, grader label, or scorer acceptance is a gold-derived signal.

## Required label
If adoption saw any gold-derived signal before final lock, the run must be labeled:

```text
SCORER_VISIBLE_ORACLE_DIAGNOSTIC_ONLY
```

It is not an uplift proof, not BYOK proof, not public benchmark proof, and not homepage-board evidence.

## Allowed scoring
Gold/scorer may be used only after final answer/source is locked, for post-hoc score calculation and audit.

## Allowed adoption signals before final lock
- family/route selector not using gold/scorer/correctness
- deterministic executor success
- parser success
- verifier trace not using gold/scorer/correctness
- retrieval-backed evidence available before scoring
- answer format validity
- abstain / uncertainty gates
- baseline fallback floor

## SimpleQA-specific lock
SimpleQA is `knowledge_retrieval_required`.

Prompt-only second-answer override is diagnostic only. VSF/semantic grade cannot be used as a row-level adoption signal for uplift claims. Override requires retrieval-backed evidence or verifier trace available before scoring; otherwise final must preserve baseline fallback.

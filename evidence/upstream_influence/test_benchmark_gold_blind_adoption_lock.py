from pathlib import Path
import unittest


class BenchmarkGoldBlindAdoptionLockTests(unittest.TestCase):
    def test_agents_contains_gold_blind_oracle_forbidden_rule(self):
        text = Path("AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Gold-Blind Adoption Hard Lock", text)
        self.assertIn("SCORER_VISIBLE_ORACLE_DIAGNOSTIC_ONLY", text)
        self.assertIn("semantic grade / VSF grade / scorer result may not decide row-level final adoption", text)
        self.assertIn("gold_visible_before_final_lock=false", text)
        self.assertIn("scorer_visible_before_final_lock=false", text)
        self.assertIn("correctness_visible_before_final_lock=false", text)

    def test_lock_artifact_exists_with_simpleqa_boundary(self):
        text = Path("proof_manifests/audits/benchmark_gold_blind_adoption_lock_20260630/benchmark_gold_blind_adoption_lock.md").read_text(encoding="utf-8")
        self.assertIn("SCORER_VISIBLE_ORACLE_DIAGNOSTIC_ONLY", text)
        self.assertIn("SimpleQA is `knowledge_retrieval_required`", text)
        self.assertIn("VSF/semantic grade cannot be used as a row-level adoption signal", text)


if __name__ == "__main__":
    unittest.main()

"""Unit tests for Multi-Skill Intelligent Composer."""

import unittest
from uniskill.composer import deduplicate_dependency_blocks, compose_skills


class TestSkillComposer(unittest.TestCase):
    def test_deduplicate_dependency_blocks(self):
        sample = """
```kotlin
implementation(libs.androidx.core)
implementation(libs.androidx.compose)
implementation(libs.androidx.core)
```
"""
        deduped = deduplicate_dependency_blocks(sample)
        self.assertEqual(deduped.count("implementation(libs.androidx.core)"), 1)
        self.assertEqual(deduped.count("implementation(libs.androidx.compose)"), 1)

    def test_compose_skills(self):
        res = compose_skills(["edge-to-edge", "adaptive"], max_tokens=3000)
        self.assertIn("edge-to-edge", res["skills"])
        self.assertIn("adaptive", res["skills"])
        self.assertIn("Unified Invariants", res["payload"])
        self.assertIn("Unified Architecture", res["payload"])
        self.assertGreater(res["composed_chars"], 100)
        self.assertLessEqual(res["estimated_tokens"], 3050)


if __name__ == "__main__":
    unittest.main()

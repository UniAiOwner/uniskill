"""Unit tests for Skill Staleness and Deprecation Linter."""

import unittest
from uniskill.linter import lint_skill_content

SAMPLE_CLEAN_SKILL = """---
name: clean-skill
description: >-
  A perfectly modern 2026 SOTA skill.
---

# Clean Modern Skill
Uses modern Jetpack Compose and Kotlin 2.1.
"""

SAMPLE_DEPRECATED_SKILL = """---
name: deprecated-skill
description: >-
  A skill with legacy patterns.
---

# Legacy Skill
val cam = android.hardware.Camera.open()
val view = findViewById(R.id.btn)
"""


class TestSkillLinter(unittest.TestCase):
    def test_clean_skill_passes(self):
        issues = lint_skill_content(SAMPLE_CLEAN_SKILL, "clean-skill")
        self.assertEqual(len(issues), 0)

    def test_deprecated_patterns_detected(self):
        issues = lint_skill_content(SAMPLE_DEPRECATED_SKILL, "deprecated-skill")
        self.assertGreaterEqual(len(issues), 2)
        names = [i["name"] for i in issues]
        self.assertIn("Legacy Camera1 API", names)
        self.assertIn("Legacy findViewById View lookup", names)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path
import tempfile
from uniskill.invariants import (
    check_devanagari_invariant,
    check_vehicle_metaphor_invariant,
    parse_and_validate_frontmatter,
    validate_python_syntax,
    validate_bracket_balance,
    validate_skill_file,
    InvariantViolation,
)


class TestInvariants(unittest.TestCase):

    def test_devanagari_detection(self):
        # Using unicode escapes to ensure pure ascii source code
        clean_text = "This is pure english and hinglish: humne code update kiya."
        dev_text = "This contains devanagari: \u0928\u092E\u0938\u094D\u0924\u0947"
        self.assertEqual(len(check_devanagari_invariant(clean_text)), 0)
        self.assertEqual(len(check_devanagari_invariant(dev_text)), 1)

    def test_vehicle_metaphor_detection(self):
        clean_text = "The application cluster and management console are online."
        dirty_text = "The cockpit of the aircraft controls the fleet of drones."
        violations = check_vehicle_metaphor_invariant(dirty_text)
        terms = [v[1] for v in violations]
        self.assertIn("cockpit", terms)
        self.assertIn("fleet", terms)
        self.assertEqual(len(check_vehicle_metaphor_invariant(clean_text)), 0)

    def test_frontmatter_validation(self):
        valid_doc = """---
name: test-skill
description: >-
  A valid test skill description.
---
# Body content
"""
        meta, body = parse_and_validate_frontmatter(valid_doc)
        self.assertEqual(meta["name"], "test-skill")
        self.assertIn("A valid test skill", meta["description"])

        invalid_doc = "Missing frontmatter delimiters"
        with self.assertRaises(InvariantViolation):
            parse_and_validate_frontmatter(invalid_doc)

    def test_python_syntax_validation(self):
        valid_py = "def hello():\n    return 42\n"
        invalid_py = "def hello(\nreturn 42"
        self.assertIsNone(validate_python_syntax(valid_py))
        self.assertIsNotNone(validate_python_syntax(invalid_py))

    def test_bracket_balance(self):
        valid_code = "fun test() { val list = listOf(1, 2, [3, 4]) }"
        invalid_code = "fun test() { val list = listOf(1, 2 "
        self.assertIsNone(validate_bracket_balance(valid_code))
        self.assertIsNotNone(validate_bracket_balance(invalid_code))


if __name__ == "__main__":
    unittest.main()

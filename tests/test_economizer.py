"""Unit tests for Zero-Noise Token Economizer."""

import unittest
from pathlib import Path
from uniskill.economizer import (
    extract_code_blueprints,
    extract_invariants_and_rules,
    economize_skill,
)

SAMPLE_SKILL = """---
name: sample-skill
description: A sample skill for testing
category: Testing
version: 2026.1
---

# Introduction to Sample Skill
This is some narrative text explaining the history of this skill.
It has lots of wordy descriptions that waste tokens.

## Invariants & Rules
- [ ] Invariant: Must use integer paise math.
- [ ] Constitutional Law-000: Never take shortcuts.
- [ ] Mandatory: All calls must be non-blocking.

## Implementation Guide
Here is some filler commentary before the code.

### Step 1: Initialize Engine
```python
def init_engine():
    return {"status": "ok"}
```

More prose in between code snippets.

### Step 2: Run Verification
```python
def verify(engine):
    assert engine["status"] == "ok"
```

## Outro and Summary
Closing remarks and promotional notes.
"""


class TestTokenEconomizer(unittest.TestCase):
    def test_extract_code_blueprints(self):
        blueprints = extract_code_blueprints(SAMPLE_SKILL)
        self.assertIn("def init_engine():", blueprints)
        self.assertIn("def verify(engine):", blueprints)
        self.assertNotIn("This is some narrative text", blueprints)
        self.assertNotIn("Closing remarks", blueprints)

    def test_extract_invariants(self):
        invariants = extract_invariants_and_rules(SAMPLE_SKILL)
        self.assertIn("Invariant: Must use integer paise math.", invariants)
        self.assertIn("Constitutional Law-000: Never take shortcuts.", invariants)
        self.assertNotIn("def init_engine():", invariants)

    def test_economize_skill_distillation(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
            f.write(SAMPLE_SKILL)
            temp_path = f.name

        try:
            res = economize_skill(temp_path, blueprint_only=False, invariants_only=False)
            self.assertIn("def init_engine():", res["content"])
            self.assertIn("Constitutional Law-000", res["content"])
            self.assertGreater(res["compression_percentage"], 10.0)
            self.assertGreater(res["tokens_saved_estimate"], 0)
        finally:
            Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()

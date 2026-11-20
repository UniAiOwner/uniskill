import unittest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import patch

from uniskill.router import tokenize, route_skills_for_task
from uniskill.runner import list_skill_scripts, run_skill_script
from uniskill.learner import distill_lesson_into_skill


class TestRouterAndRunner(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.db_path = base / "state.db"

        conn = sqlite3.connect(self.db_path)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS skills_catalog (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            version TEXT NOT NULL DEFAULT '2026.1',
            sha256_hash TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'ACTIVE',
            compatibility_matrix_json TEXT NOT NULL DEFAULT '{}',
            file_path TEXT NOT NULL,
            last_audited_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS skill_lifecycle_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            diff_summary TEXT,
            sha256_before TEXT,
            sha256_after TEXT,
            status TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Add mock skills with scripts
        skill1_dir = base / "auto-paise-calculator"
        skill1_dir.mkdir()
        skill1_file = skill1_dir / "SKILL.md"
        skill1_file.write_text("---\nname: auto-paise-calculator\ndescription: >-\n  Paise integer arithmetic.\n---\n")

        scripts_dir = skill1_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "calc.py").write_text("import sys\nprint('Total: 10000 paise')\n")

        conn.execute("""
        INSERT INTO skills_catalog (id, name, category, description, version, sha256_hash, file_path)
        VALUES ('auto-paise-calculator', 'auto-paise-calculator', 'Invoicing, Retail POS & Pharma', 'Paise integer arithmetic', '2026.1', 'hash1', ?)
        """, (str(skill1_file),))

        conn.commit()
        conn.close()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tokenization(self):
        tokens = tokenize("Build an auto-paise counter with 3-second billing!")
        self.assertIn("auto-paise", tokens)
        self.assertIn("counter", tokens)
        self.assertIn("billing", tokens)
        self.assertNotIn("an", tokens)
        self.assertNotIn("with", tokens)

    def test_semantic_routing(self):
        res = route_skills_for_task("Calculate customer bill using integer paise", top_k=1, db_path=self.db_path)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["skill_name"], "auto-paise-calculator")
        self.assertGreater(res[0]["relevance_score"], 30.0)
        self.assertIn("calc.py", res[0]["available_scripts"])

    def test_script_runner(self):
        scripts = list_skill_scripts("auto-paise-calculator", db_path=self.db_path)
        self.assertEqual(scripts, ["calc.py"])

        exec_res = run_skill_script("auto-paise-calculator", "calc.py", db_path=self.db_path)
        self.assertTrue(exec_res["success"])
        self.assertEqual(exec_res["exit_code"], 0)
        self.assertIn("10000 paise", exec_res["stdout"])


if __name__ == "__main__":
    unittest.main()

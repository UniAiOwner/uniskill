import unittest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import patch
from uniskill.upgrader import upgrade_skill_file, sanitize_text
from uniskill.forge import synthesize_new_skill


class TestForgeAndUpgrader(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.skills_dir = base / "skills"
        self.skills_dir.mkdir(parents=True)

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
        conn.commit()
        conn.close()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_text_sanitization(self):
        dirty = "The fleet operations are coordinated from the cockpit."
        cleaned = sanitize_text(dirty)
        self.assertNotIn("fleet", cleaned.lower())
        self.assertNotIn("cockpit", cleaned.lower())
        self.assertIn("cluster", cleaned.lower())
        self.assertIn("management console", cleaned.lower())

    def test_synthesize_new_skill(self):
        with patch("uniskill.forge.sync_skill_to_all_environments", return_value=(True, "Mock Synced")):
            ok, msg, details = synthesize_new_skill(
                skill_name="quantum-ledger-sync",
                description="Synchronizes distributed transaction state across nodes.",
                category="Invoicing, Retail POS & Pharma",
                target_root=self.skills_dir,
                db_path=self.db_path,
            )
            self.assertTrue(ok)
            self.assertEqual(details["name"], "quantum-ledger-sync")

            skill_md = self.skills_dir / "quantum-ledger-sync" / "SKILL.md"
            self.assertTrue(skill_md.exists())
            content = skill_md.read_text(encoding="utf-8")
            self.assertIn("description: >-", content)
            self.assertIn("name: quantum-ledger-sync", content)

    def test_upgrade_skill_file(self):
        sample_dir = self.skills_dir / "sample-legacy"
        sample_dir.mkdir()
        skill_file = sample_dir / "SKILL.md"
        skill_file.write_text("""---
name: sample-legacy
description: Legacy skill coordinating an aircraft fleet.
---
# Content
""")
        with patch("uniskill.upgrader.sync_skill_to_all_environments", return_value=(True, "Mock Synced")):
            ok, msg, details = upgrade_skill_file(skill_file, db_path=self.db_path)
            self.assertTrue(ok)
            upgraded_text = skill_file.read_text(encoding="utf-8")
            self.assertIn("description: >-", upgraded_text)
            self.assertNotIn("fleet", upgraded_text)
            self.assertIn("cluster", upgraded_text)


if __name__ == "__main__":
    unittest.main()

import unittest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import patch
from uniskill.sync import audit_triple_env_parity, sync_skill_to_all_environments


class TestSync(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.config = base / "config" / "skills"
        self.antigravity = base / "antigravity" / "skills"
        self.antigravity_ide = base / "antigravity-ide" / "skills"

        self.config.mkdir(parents=True)
        self.antigravity.mkdir(parents=True)
        self.antigravity_ide.mkdir(parents=True)

        self.db_path = base / "state.db"
        conn = sqlite3.connect(self.db_path)
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

        # Create sample skill in config
        s = self.config / "test-sync-skill"
        s.mkdir()
        (s / "SKILL.md").write_text("---\nname: test-sync-skill\ndescription: >-\n  Sync test.\n---\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_sync_and_audit(self):
        mock_envs = {
            "config": self.config,
            "antigravity": self.antigravity,
            "antigravity_ide": self.antigravity_ide,
        }
        with patch("uniskill.sync.ENVIRONMENTS", mock_envs):
            # Initially missing in targets
            audit_before = audit_triple_env_parity()
            self.assertEqual(audit_before["parity_percentage"], 0.0)

            # Sync
            ok, msg = sync_skill_to_all_environments("test-sync-skill", source_env="config", db_path=self.db_path)
            self.assertTrue(ok)

            # After sync: 100% parity
            audit_after = audit_triple_env_parity()
            self.assertEqual(audit_after["parity_percentage"], 100.0)
            self.assertEqual(audit_after["in_sync_count"], 1)


if __name__ == "__main__":
    unittest.main()

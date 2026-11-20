import unittest
import sqlite3
import tempfile
from pathlib import Path
from uniskill.registry import (
    compute_file_sha256,
    infer_domain_category,
    infer_compatibility_matrix,
    index_all_skills,
    get_skill,
    list_skills,
    get_catalog_stats,
)


class TestRegistry(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.skills_dir = Path(self.temp_dir.name) / "skills"
        self.skills_dir.mkdir(parents=True)
        self.db_path = Path(self.temp_dir.name) / "state.db"

        # Initialize test state.db
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
        conn.commit()
        conn.close()

        # Create 2 mock skills
        skill1 = self.skills_dir / "test-android-skill"
        skill1.mkdir()
        (skill1 / "SKILL.md").write_text("""---
name: test-android-skill
description: >-
  Adaptive Compose UI layout skill.
---
# Android Compose blueprints
""")

        skill2 = self.skills_dir / "test-agent-skill"
        skill2.mkdir()
        (skill2 / "SKILL.md").write_text("""---
name: test-agent-skill
description: >-
  Autonomous swarm coordination.
---
# Python swarm runtime
""")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_indexing_and_retrieval(self):
        indexed, total_phys, errors = index_all_skills(self.skills_dir, self.db_path, scan_all_roots=False)
        self.assertEqual(indexed, 2)
        self.assertEqual(total_phys, 2)
        self.assertEqual(errors, 0)

        skill = get_skill("test-android-skill", self.db_path)
        self.assertIsNotNone(skill)
        self.assertEqual(skill["category"], "Android & Mobile Engineering")
        self.assertIn("android", skill["compatibility_matrix"]["supported_stacks"])

        stats = get_catalog_stats(self.db_path)
        self.assertEqual(stats["total_skills"], 2)

    def test_record_skill_execution_outcome(self):
        from uniskill.registry import record_skill_execution_outcome
        index_all_skills(self.skills_dir, self.db_path, scan_all_roots=False)

        # 1. Success outcome
        res1 = record_skill_execution_outcome("test-android-skill", passed=True, db_path=self.db_path)
        self.assertEqual(res1["success_count"], 1)
        self.assertEqual(res1["failure_count"], 0)
        self.assertEqual(res1["reliability_score"], 100.0)

        # 2. Failure outcome
        res2 = record_skill_execution_outcome("test-android-skill", passed=False, db_path=self.db_path)
        self.assertEqual(res2["success_count"], 1)
        self.assertEqual(res2["failure_count"], 1)
        self.assertEqual(res2["reliability_score"], 50.0)


if __name__ == "__main__":
    unittest.main()

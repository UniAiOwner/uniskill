import unittest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import patch

from uniskill.elevate import (
    calculate_bm25_score,
    audit_delta_gap,
    elevate_skill_to_100_percent,
)


class TestElevate(unittest.TestCase):

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

        # Add mock camera skill
        skill_dir = base / "camera1-to-camerax"
        skill_dir.mkdir()
        self.skill_file = skill_dir / "SKILL.md"
        self.skill_file.write_text("""---
name: camera1-to-camerax
description: >-
  Migrates legacy Camera1/Camera2 APIs to modern CameraX.
---
# CameraX Migration
Basic CameraX migration guidelines.
""")

        conn.execute("""
        INSERT INTO skills_catalog (id, name, category, description, version, sha256_hash, file_path)
        VALUES ('camera1-to-camerax', 'camera1-to-camerax', 'Android & Mobile Engineering', 'Migrates Camera1 to CameraX', '2026.1', 'hash1', ?)
        """, (str(self.skill_file),))

        conn.commit()
        conn.close()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_delta_gap_detection(self):
        prompt = "How do I setup 60 FPS barcode scanning in Jetpack Compose using CameraX and ML Kit?"
        content = "Basic CameraX migration."
        gaps = audit_delta_gap(prompt, content)
        self.assertIn("barcode", gaps)
        self.assertIn("compose", gaps)
        self.assertIn("fps", gaps)

    def test_100_percent_elevation(self):
        prompt = "How do I setup 60 FPS barcode scanning in Jetpack Compose using CameraX and ML Kit?"
        with patch("uniskill.elevate.sync_skill_to_all_environments", return_value=(True, "Mock Synced")):
            res = elevate_skill_to_100_percent(
                prompt,
                target_skill_name="camera1-to-camerax",
                db_path=self.db_path,
            )
            self.assertTrue(res["success"])
            self.assertEqual(res["final_score"], 100.0)
            self.assertEqual(res["skill_name"], "camera1-to-camerax")

            # Check that file now contains the 60 FPS Jetpack Compose code
            content = self.skill_file.read_text(encoding="utf-8")
            self.assertIn("CameraXBarcodeScannerSurface", content)
            self.assertIn("AndroidView", content)
            self.assertIn("BarcodeScanning.getClient()", content)
            self.assertIn("STRATEGY_KEEP_ONLY_LATEST", content)


if __name__ == "__main__":
    unittest.main()

import unittest
import tempfile
import sqlite3
from pathlib import Path
from uniskill.evaluator import ProjectStackInspector, evaluate_skill_for_project


class TestEvaluator(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.project_dir = base / "test_project"
        self.project_dir.mkdir(parents=True)

        # Create mock build.gradle.kts
        (self.project_dir / "build.gradle.kts").write_text("""
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.compose.compiler)
}
android {
    compileSdk = 35
    defaultConfig {
        targetSdk = 35
    }
}
dependencies {
    implementation("androidx.camera:camera-camera2:1.4.0")
}
""")

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
        CREATE TABLE IF NOT EXISTS skill_evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_path TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            suitability_score REAL NOT NULL,
            decision TEXT NOT NULL,
            gap_summary TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Insert matching skill
        conn.execute("""
        INSERT INTO skills_catalog (id, name, category, description, version, sha256_hash, compatibility_matrix_json, file_path)
        VALUES ('camera1-to-camerax', 'camera1-to-camerax', 'Android & Mobile Engineering', 'CameraX migration', '2026.1', 'hash', '{"supported_stacks": ["android", "compose"]}', '/tmp/dummy')
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_project_stack_inspection(self):
        info = ProjectStackInspector.inspect(self.project_dir)
        self.assertEqual(info["type"], "android")
        self.assertIn("android", info["detected_stacks"])
        self.assertIn("compose", info["detected_stacks"])
        self.assertEqual(info["sdk_versions"].get("compile_sdk"), 35)

    def test_skill_evaluation_pass(self):
        res = evaluate_skill_for_project("camera1-to-camerax", self.project_dir, db_path=self.db_path)
        self.assertEqual(res["decision"], "PASS")
        self.assertGreaterEqual(res["suitability_score"], 85.0)

    def test_nonexistent_skill_synthesize_gate(self):
        res = evaluate_skill_for_project("nonexistent-future-skill", self.project_dir, db_path=self.db_path)
        self.assertEqual(res["decision"], "SYNTHESIZE_NEW")
        self.assertEqual(res["suitability_score"], 0.0)


if __name__ == "__main__":
    unittest.main()

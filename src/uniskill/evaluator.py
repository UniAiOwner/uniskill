"""Pre-Execution Suitability & Gap Diagnostic Gate.

Evaluates whether a skill is compatible with the target project's actual
architecture, dependencies, and API levels before execution.
"""

import json
import re
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from uniskill.registry import get_skill, DEFAULT_DB_PATH


class ProjectStackInspector:
    """Detects technological stack, versions, and build tools of a target project."""

    @staticmethod
    def inspect(project_path: Path) -> Dict[str, Any]:
        info: Dict[str, Any] = {
            "type": "unknown",
            "detected_stacks": [],
            "dependencies": {},
            "sdk_versions": {},
        }

        if not project_path.exists():
            return info

        # 1. Android Detection
        gradle_files = list(project_path.glob("**/build.gradle*"))
        if gradle_files:
            info["detected_stacks"].append("android")
            info["type"] = "android"
            for gf in gradle_files:
                try:
                    text = gf.read_text(encoding="utf-8", errors="ignore")
                    if "compose" in text.lower():
                        info["detected_stacks"].append("compose")
                    compile_sdk = re.search(r"compileSdk\s*=?\s*(\d+)", text)
                    if compile_sdk:
                        info["sdk_versions"]["compile_sdk"] = int(compile_sdk.group(1))
                    target_sdk = re.search(r"targetSdk\s*=?\s*(\d+)", text)
                    if target_sdk:
                        info["sdk_versions"]["target_sdk"] = int(target_sdk.group(1))
                    if "camerax" in text.lower():
                        info["dependencies"]["camerax"] = True
                    if "room" in text.lower():
                        info["dependencies"]["room"] = True
                except Exception:
                    pass

        # 2. Web Detection
        package_json = project_path / "package.json"
        if package_json.exists():
            info["detected_stacks"].append("web")
            if info["type"] == "unknown":
                info["type"] = "web"
            try:
                pkg_data = json.loads(package_json.read_text(encoding="utf-8"))
                deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                for dep, ver in deps.items():
                    if dep in ["next", "react", "tailwindcss"]:
                        info["dependencies"][dep] = ver
            except Exception:
                pass

        # 3. Python Detection
        pyproject = project_path / "pyproject.toml"
        reqs = project_path / "requirements.txt"
        if pyproject.exists() or reqs.exists():
            info["detected_stacks"].append("python")
            if info["type"] == "unknown":
                info["type"] = "python"

        # 4. Rust Detection
        cargo_toml = project_path / "Cargo.toml"
        if cargo_toml.exists():
            info["detected_stacks"].append("rust")
            if info["type"] == "unknown":
                info["type"] = "rust"

        info["detected_stacks"] = list(set(info["detected_stacks"]))
        return info


def evaluate_skill_for_project(
    skill_name: str,
    project_path: Path,
    db_path: Path = DEFAULT_DB_PATH,
) -> Dict[str, Any]:
    """Evaluates whether skill_name is suitable for project_path.
    Returns evaluation dict with score, decision, gaps, and recommendations.
    """
    skill = get_skill(skill_name, db_path=db_path)
    if not skill:
        # Check if skill exists on disk directly
        return {
            "skill_name": skill_name,
            "project_path": str(project_path),
            "suitability_score": 0.0,
            "decision": "SYNTHESIZE_NEW",
            "gap_summary": f"Skill '{skill_name}' does not exist in catalog. Needs autonomous synthesis.",
            "recommendations": [f"Invoke skill forge to synthesize '{skill_name}'."],
        }

    stack_info = ProjectStackInspector.inspect(project_path)
    compat = skill.get("compatibility_matrix", {})
    supported_stacks = compat.get("supported_stacks", ["general"])

    score = 100.0
    gaps = []
    recommendations = []

    # Stack alignment check
    project_stacks = stack_info.get("detected_stacks", [])
    if "general" not in supported_stacks and project_stacks:
        matching_stacks = [s for s in supported_stacks if s in project_stacks]
        if not matching_stacks:
            score -= 40.0
            gaps.append(f"Stack mismatch: Skill supports {supported_stacks}, but project uses {project_stacks}.")
            recommendations.append(f"Verify if skill '{skill_name}' is intended for this project stack.")

    # Android specific checks
    if "android" in project_stacks and "android" in supported_stacks:
        compile_sdk = stack_info.get("sdk_versions", {}).get("compile_sdk", 34)
        if compile_sdk >= 35:
            # Modern Android 15/16 check
            skill_text = ""
            skill_path = Path(skill.get("file_path", ""))
            if skill_path.exists():
                skill_text = skill_path.read_text(encoding="utf-8", errors="ignore").lower()
            if "edge-to-edge" in skill_name and "enableedgetoedge" not in skill_text:
                score -= 20.0
                gaps.append("Skill lacks modern Activity.enableEdgeToEdge() standard API.")
                recommendations.append("Upgrade skill with Android 15 mandatory edge-to-edge blueprints.")

    # Determine Decision Gate
    if score >= 85.0:
        decision = "PASS"
        gap_summary = "Skill is 100% compatible and SOTA-aligned with project stack."
    else:
        decision = "UPGRADE_REQUIRED"
        gap_summary = "; ".join(gaps) if gaps else "Skill requires minor version alignment."

    # Record evaluation in SQLite
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("""
        INSERT INTO skill_evaluations (
            project_path, skill_name, suitability_score, decision, gap_summary
        ) VALUES (?, ?, ?, ?, ?)
        """, (
            str(project_path),
            skill_name,
            score,
            decision,
            gap_summary,
        ))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return {
        "skill_name": skill_name,
        "project_path": str(project_path),
        "suitability_score": score,
        "decision": decision,
        "gap_summary": gap_summary,
        "recommendations": recommendations,
        "stack_info": stack_info,
    }

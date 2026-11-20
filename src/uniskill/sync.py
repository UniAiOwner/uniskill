"""Triple-Environment Bit-Parity Synchronizer.

Enforces 100% SHA-256 bit-parity across:
1. ~/.gemini/config/skills/
2. ~/.gemini/antigravity/skills/
3. ~/.gemini/antigravity-ide/skills/
"""

import hashlib
import os
import shutil
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Any

from uniskill.registry import compute_file_sha256, DEFAULT_DB_PATH


ENVIRONMENTS = {
    "config": Path.home() / ".gemini" / "config" / "skills",
    "antigravity": Path.home() / ".gemini" / "antigravity" / "skills",
    "antigravity_ide": Path.home() / ".gemini" / "antigravity-ide" / "skills",
}


def audit_triple_env_parity() -> Dict[str, Any]:
    """Audits SHA-256 hash parity of all skills across the 3 environments.
    Returns audit statistics and mismatch list.
    """
    config_dir = ENVIRONMENTS["config"]
    if not config_dir.exists():
        return {"error": f"Base config directory not found: {config_dir}"}

    total_base_skills = 0
    in_sync_count = 0
    mismatches = []
    missing_in_targets = []

    for item in sorted(config_dir.iterdir()):
        if not item.is_dir():
            continue
        skill_file = item / "SKILL.md"
        if not skill_file.exists():
            continue

        skill_name = item.name
        total_base_skills += 1
        base_hash = compute_file_sha256(skill_file)

        is_parity_ok = True
        for env_name in ["antigravity", "antigravity_ide"]:
            target_env_dir = ENVIRONMENTS[env_name]
            target_skill_file = target_env_dir / skill_name / "SKILL.md"

            if not target_skill_file.exists():
                is_parity_ok = False
                missing_in_targets.append({
                    "skill": skill_name,
                    "target_env": env_name,
                    "issue": "MISSING_TARGET_SKILL",
                })
            else:
                target_hash = compute_file_sha256(target_skill_file)
                if target_hash != base_hash:
                    is_parity_ok = False
                    mismatches.append({
                        "skill": skill_name,
                        "target_env": env_name,
                        "base_hash": base_hash[:8],
                        "target_hash": target_hash[:8],
                        "issue": "HASH_MISMATCH",
                    })

        if is_parity_ok:
            in_sync_count += 1

    parity_percent = (in_sync_count / total_base_skills * 100.0) if total_base_skills else 100.0

    return {
        "total_skills": total_base_skills,
        "in_sync_count": in_sync_count,
        "parity_percentage": round(parity_percent, 2),
        "mismatches": mismatches,
        "missing_in_targets": missing_in_targets,
    }


def sync_skill_to_all_environments(
    skill_name: str,
    source_env: str = "config",
    db_path: Path = DEFAULT_DB_PATH,
) -> Tuple[bool, str]:
    """Synchronizes a single skill directory from source_env to all other environments.
    Returns (success, message).
    """
    source_root = ENVIRONMENTS.get(source_env)
    if not source_root or not (source_root / skill_name).exists():
        return False, f"Source skill not found in {source_env}: {skill_name}"

    source_dir = source_root / skill_name
    source_skill_md = source_dir / "SKILL.md"
    source_hash = compute_file_sha256(source_skill_md) if source_skill_md.exists() else "NO_HASH"

    synced_targets = []
    for env_name, target_root in ENVIRONMENTS.items():
        if env_name == source_env:
            continue
        target_root.mkdir(parents=True, exist_ok=True)
        target_dir = target_root / skill_name
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)
        synced_targets.append(env_name)

    # Record in SQLite lifecycle events
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("""
        INSERT INTO skill_lifecycle_events (
            event_type, skill_name, diff_summary, sha256_before, sha256_after, status
        ) VALUES ('SYNC', ?, ?, ?, ?, 'SUCCESS')
        """, (
            skill_name,
            f"Synced to {', '.join(synced_targets)}",
            source_hash,
            source_hash,
        ))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return True, f"Successfully synced '{skill_name}' across {len(synced_targets)} environments."


def sync_all_skills_across_environments(
    source_env: str = "config",
    db_path: Path = DEFAULT_DB_PATH,
) -> Dict[str, Any]:
    """Synchronizes all skills from source_env across all 3 environments."""
    source_root = ENVIRONMENTS.get(source_env)
    if not source_root or not source_root.exists():
        return {"success": False, "error": f"Invalid source environment: {source_env}"}

    synced_count = 0
    errors = []

    for item in sorted(source_root.iterdir()):
        if not item.is_dir() or not (item / "SKILL.md").exists():
            continue
        ok, msg = sync_skill_to_all_environments(item.name, source_env=source_env, db_path=db_path)
        if ok:
            synced_count += 1
        else:
            errors.append(msg)

    return {
        "success": len(errors) == 0,
        "synced_count": synced_count,
        "errors": errors,
    }

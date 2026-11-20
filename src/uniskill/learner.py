"""Reflexive Skill Learning & Knowledge Distillation Engine.

Extracts verified architectural patterns and bug fixes from project dev_logs.txt
and distills them into relevant skills' references/LESSONS_LEARNED.md.
"""

import re
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from uniskill.router import route_skills_for_task
from uniskill.sync import sync_skill_to_all_environments
from uniskill.registry import get_skill, DEFAULT_DB_PATH


def parse_latest_dev_log(project_root: Path) -> Optional[Dict[str, str]]:
    """Extracts the latest session entry from dev_logs.txt."""
    log_file = project_root / "dev_logs.txt"
    if not log_file.exists():
        return None

    content = log_file.read_text(encoding="utf-8", errors="ignore")
    # Entries start with ## 📅 Date:
    entries = re.split(r"(?=## 📅 Date:)", content)
    valid_entries = [e.strip() for e in entries if e.strip().startswith("## 📅 Date:")]
    if not valid_entries:
        return None

    latest_entry = valid_entries[-1]
    title_match = re.search(r"## 📅 Date:\s*([^\n]+)", latest_entry)
    title = title_match.group(1).strip() if title_match else "Session Update"

    return {
        "title": title,
        "raw_text": latest_entry,
    }


def distill_lesson_into_skill(
    project_root: Path,
    target_skill_name: Optional[str] = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> Tuple[bool, str, Dict[str, Any]]:
    """Extracts latest lessons from project dev_logs and distills into skill references."""
    latest = parse_latest_dev_log(project_root)
    if not latest:
        return False, f"No dev_logs.txt found in {project_root}", {}

    # If skill not provided, route automatically based on title and achievements
    skill_name = target_skill_name
    if not skill_name:
        routed = route_skills_for_task(latest["raw_text"], top_k=1, db_path=db_path)
        if not routed:
            return False, "Could not determine relevant skill for dev log content.", {}
        skill_name = routed[0]["skill_name"]

    skill = get_skill(skill_name, db_path=db_path)
    if not skill:
        return False, f"Target skill '{skill_name}' not found in catalog.", {}

    skill_file = Path(skill["file_path"])
    skill_dir = skill_file.parent
    ref_dir = skill_dir / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)

    lessons_file = ref_dir / "LESSONS_LEARNED.md"
    entry_formatted = f"""
### 🔬 Lesson from {project_root.name} ({latest['title']})
{latest['raw_text']}

---
"""
    if not lessons_file.exists():
        lessons_file.write_text(f"# Lessons Learned & Grounded Field Verification\n\n{entry_formatted}", encoding="utf-8")
    else:
        with lessons_file.open("a", encoding="utf-8") as f:
            f.write(entry_formatted)

    # Sync skill across environments so all 3 get the updated reference
    sync_ok, sync_msg = sync_skill_to_all_environments(skill_name, source_env="config", db_path=db_path)

    # Record event in SQLite
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("""
        INSERT INTO skill_lifecycle_events (
            event_type, skill_name, diff_summary, sha256_before, sha256_after, status
        ) VALUES ('LEARN', ?, ?, 'SAME', 'SAME', 'SUCCESS')
        """, (skill_name, f"Distilled lesson from {project_root.name}: {latest['title']}"))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return True, f"Successfully distilled lesson into '{skill_name}': {sync_msg}", {
        "skill_name": skill_name,
        "project": project_root.name,
        "synced": sync_ok,
    }

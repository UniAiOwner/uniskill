"""Universal Skill Script Runner.

Enables Antigravity and subagents to discover and execute helper scripts
inside any skill's scripts/ directory cleanly.
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from uniskill.registry import get_skill, DEFAULT_DB_PATH


def list_skill_scripts(skill_name: str, db_path: Path = DEFAULT_DB_PATH) -> List[str]:
    """Lists all executable scripts in a skill's scripts/ directory."""
    skill = get_skill(skill_name, db_path=db_path)
    if not skill:
        return []
    skill_file = Path(skill["file_path"])
    scripts_dir = skill_file.parent / "scripts"
    if not scripts_dir.exists():
        return []
    return sorted([f.name for f in scripts_dir.iterdir() if f.is_file()])


def run_skill_script(
    skill_name: str,
    script_name: str,
    args: Optional[List[str]] = None,
    db_path: Path = DEFAULT_DB_PATH,
    timeout: int = 60,
) -> Dict[str, Any]:
    """Executes a helper script inside a skill's scripts/ directory.
    Returns exit code, stdout, and stderr.
    """
    skill = get_skill(skill_name, db_path=db_path)
    if not skill:
        return {"success": False, "error": f"Skill '{skill_name}' not found."}

    skill_file = Path(skill["file_path"])
    scripts_dir = skill_file.parent / "scripts"
    script_path = scripts_dir / script_name

    # Check without extension or with .py
    if not script_path.exists():
        if (scripts_dir / f"{script_name}.py").exists():
            script_path = scripts_dir / f"{script_name}.py"
        else:
            avail = [f.name for f in scripts_dir.iterdir()] if scripts_dir.exists() else []
            return {
                "success": False,
                "error": f"Script '{script_name}' not found in {scripts_dir}. Available: {avail}",
            }

    cmd = [sys.executable, str(script_path)] + (args or [])

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        return {
            "success": proc.returncode == 0,
            "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "command": " ".join(cmd),
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Execution timed out after {timeout} seconds.",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

"""Skills Catalog Registry & Indexer.

Scans, categorizes, hashes, and indexes all skills into the SQLite state machine.
"""

import hashlib
import json
import os
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from uniskill.invariants import parse_and_validate_frontmatter, InvariantViolation


DEFAULT_SKILLS_ROOT = Path.home() / ".gemini" / "config" / "skills"
DEFAULT_DB_PATH = Path("/media/uniai/UniAi/PROJECTS_MIGRATED/ALL SKILLS/.unigov/state.db")

# All Sovereign Skill Search Roots across Antigravity ecosystem
ALL_SKILL_SEARCH_ROOTS = [
    Path.home() / ".gemini" / "config" / "skills",
    Path.home() / ".gemini" / "antigravity" / "skills",
    Path.home() / ".gemini" / "antigravity-ide" / "skills",
    Path.home() / ".gemini" / "skills",
    Path.home() / ".gemini" / "config" / "plugins",
    Path.home() / ".gemini" / "antigravity" / "builtin" / "skills",
    Path("/home/uniai/.agents/skills"),
]

# 8 Sovereign Governance Domains
DOMAIN_MAPPING = {
    "Android & Mobile Engineering": [
        "adaptive", "android", "compose", "camera", "wear", "glimmer",
        "navigation", "edge-to-edge", "styles", "haze", "swipe", "vico", "gs1",
        "play-billing", "engage", "kmp", "rikka", "display-glasses"
    ],
    "Agentic AI & Swarms": [
        "agent", "swarm", "autogen", "crewai", "chatdev", "deer-flow",
        "openhands", "swe-agent", "pydantic-ai", "agno", "automaton", "magnitude"
    ],
    "System 2 Cognition & Active Inference": [
        "cognitive", "active-inference", "causal", "neuro-symbolic",
        "autotelic", "tree-of-thought", "mcts", "pymdp", "hipporag", "graphiti",
        "mem0", "letta", "reflexion", "cognee", "storm"
    ],
    "Systems, Performance & OS": [
        "native-desktop", "winit", "wgpu", "systems", "rust", "perfetto",
        "r8", "ebpf", "chipset", "ncps", "torchhd", "duckdb", "lancedb", "qdrant"
    ],
    "Enterprise Web & Backend": [
        "web", "nextjs", "react", "modern-web", "tailwind", "square-ui",
        "api-contract", "postgres", "kafka", "redis", "chrome-devtools"
    ],
    "Security, Cryptography & Defense": [
        "security", "auth", "crypto", "intent-security", "verified-email",
        "cloud-gateway", "waf", "sentrux", "devsecops", "zero-knowledge",
        "zero-trust", "confidential-computing", "defensive", "mobile-reverse"
    ],
    "Invoicing, Retail POS & Pharma": [
        "invoice", "retail-pos", "pharma", "gs1", "double-entry", "escpos",
        "statutory", "auto-paise", "universal-invoice", "uniretail", "unimed"
    ],
    "DevOps, Toolchain & Verification": [
        "agp", "testing", "z3", "formal-verification", "lean4", "ast-grep",
        "ast-surgical", "coderabbit", "qodo", "devops", "superpowers",
        "unigov", "superclaude", "ponytail", "clean-room"
    ],
}


def compute_file_sha256(path: Path) -> str:
    """Computes SHA-256 hex digest of a file."""
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def infer_domain_category(skill_name: str, description: str) -> str:
    """Infers domain category based on keyword matching across domains."""
    combined = f"{skill_name} {description}".lower()
    for domain, keywords in DOMAIN_MAPPING.items():
        for kw in keywords:
            if kw in combined:
                return domain
    return "DevOps, Toolchain & Verification"


def infer_compatibility_matrix(skill_name: str, body: str) -> Dict[str, Any]:
    """Infers supported stacks, minimum OS/runtime versions, and required tools."""
    stacks = []
    text_lower = (skill_name + " " + body).lower()

    if any(k in text_lower for k in ["android", "compose", "kotlin", "gradle", "camerax", "room"]):
        stacks.append("android")
    if any(k in text_lower for k in ["nextjs", "react", "typescript", "javascript", "tailwind"]):
        stacks.append("web")
    if any(k in text_lower for k in ["python", "asyncio", "pydantic", "fastapi"]):
        stacks.append("python")
    if any(k in text_lower for k in ["rust", "cargo", "wgpu", "winit"]):
        stacks.append("rust")
    if any(k in text_lower for k in ["gemini", "llm", "onnx", "active-inference", "mcts"]):
        stacks.append("ai")

    return {
        "supported_stacks": stacks or ["general"],
        "min_android_api": 26 if "android" in stacks else None,
        "min_python_version": "3.12" if "python" in stacks else None,
        "min_node_version": "20.x" if "web" in stacks else None,
    }


def index_all_skills(
    skills_root: Optional[Path] = None,
    db_path: Path = DEFAULT_DB_PATH,
    scan_all_roots: bool = True,
) -> Tuple[int, int, int]:
    """Scans all skills from across the ecosystem and stores them in SQLite state.db.
    Returns (unique_indexed_count, total_physical_instances, error_count).
    """
    roots_to_scan = [skills_root] if skills_root else (ALL_SKILL_SEARCH_ROOTS if scan_all_roots else [DEFAULT_SKILLS_ROOT])

    conn = sqlite3.connect(db_path)
    _ensure_catalog_columns(conn)
    cur = conn.cursor()

    seen_unique = set()
    total_physical = 0
    errors = 0

    for root in roots_to_scan:
        if not root.exists():
            continue

        for skill_file in sorted(root.glob("**/SKILL.md")):
            total_physical += 1
            entry_name = skill_file.parent.name

            try:
                content = skill_file.read_text(encoding="utf-8")
                meta, body = parse_and_validate_frontmatter(content)
                name = meta.get("name", entry_name)
                desc = meta.get("description", "").strip()
                sha = compute_file_sha256(skill_file)
                category = infer_domain_category(name, desc)
                compat = infer_compatibility_matrix(name, body)

                cur.execute("""
                INSERT INTO skills_catalog (
                    id, name, category, description, version, sha256_hash, status,
                    compatibility_matrix_json, file_path, last_audited_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(name) DO UPDATE SET
                    category = excluded.category,
                    description = excluded.description,
                    sha256_hash = excluded.sha256_hash,
                    compatibility_matrix_json = excluded.compatibility_matrix_json,
                    file_path = excluded.file_path,
                    last_audited_at = CURRENT_TIMESTAMP
                """, (
                    name,
                    name,
                    category,
                    desc,
                    "2026.1",
                    sha,
                    json.dumps(compat),
                    str(skill_file),
                ))
                seen_unique.add(name)
            except Exception:
                errors += 1

    conn.commit()
    conn.close()
    return len(seen_unique), total_physical, errors


def get_skill(name: str, db_path: Path = DEFAULT_DB_PATH) -> Optional[Dict[str, Any]]:
    """Retrieves a single skill record by name."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM skills_catalog WHERE name = ?", (name,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["compatibility_matrix"] = json.loads(d["compatibility_matrix_json"])
        return d
    return None


def list_skills(category: Optional[str] = None, db_path: Path = DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
    """Lists skills, optionally filtered by domain category."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    if category:
        rows = conn.execute("SELECT * FROM skills_catalog WHERE category = ? ORDER BY name ASC", (category,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM skills_catalog ORDER BY category ASC, name ASC").fetchall()
    conn.close()
    res = []
    for r in rows:
        d = dict(r)
        d["compatibility_matrix"] = json.loads(d["compatibility_matrix_json"])
        res.append(d)
    return res


def get_catalog_stats(db_path: Path = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """Returns total skill count, domain breakdowns, and last indexed timestamp."""
    conn = sqlite3.connect(db_path)
    total = conn.execute("SELECT COUNT(*) FROM skills_catalog").fetchone()[0]
    domains = conn.execute("SELECT category, COUNT(*) FROM skills_catalog GROUP BY category").fetchall()
    conn.close()

    # Count total physical instances across known locations
    total_physical = 0
    for root in ALL_SKILL_SEARCH_ROOTS:
        if root.exists():
            total_physical += len(list(root.glob("**/SKILL.md")))

    return {
        "unique_skills": total,
        "total_skills": total,
        "physical_instances": total_physical,
        "domains": {d[0]: d[1] for d in domains},
    }


def _ensure_catalog_columns(conn: sqlite3.Connection) -> None:
    """Auto-migrates schema to ensure empirical reliability tracking columns exist."""
    cols = [r[1] for r in conn.execute("PRAGMA table_info(skills_catalog);").fetchall()]
    if cols:
        if "success_count" not in cols:
            conn.execute("ALTER TABLE skills_catalog ADD COLUMN success_count INTEGER DEFAULT 0;")
        if "failure_count" not in cols:
            conn.execute("ALTER TABLE skills_catalog ADD COLUMN failure_count INTEGER DEFAULT 0;")
        if "reliability_score" not in cols:
            conn.execute("ALTER TABLE skills_catalog ADD COLUMN reliability_score REAL DEFAULT 100.0;")
        conn.commit()


def record_skill_execution_outcome(skill_name: str, passed: bool, db_path: Path = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """Records an empirical execution outcome for a skill and recalculates its reliability score."""
    conn = sqlite3.connect(db_path)
    _ensure_catalog_columns(conn)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT success_count, failure_count FROM skills_catalog WHERE name = ?", (skill_name,)).fetchone()
    if not row:
        conn.close()
        return {"error": f"Skill '{skill_name}' not found in catalog."}

    succ = (row["success_count"] or 0) + (1 if passed else 0)
    fail = (row["failure_count"] or 0) + (0 if passed else 1)
    total = succ + fail
    score = round((succ / max(1, total)) * 100, 1)

    conn.execute(
        "UPDATE skills_catalog SET success_count = ?, failure_count = ?, reliability_score = ? WHERE name = ?",
        (succ, fail, score, skill_name)
    )
    conn.commit()
    conn.close()
    return {
        "skill_name": skill_name,
        "success_count": succ,
        "failure_count": fail,
        "reliability_score": score,
        "passed": passed,
    }


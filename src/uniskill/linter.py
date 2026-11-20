"""Skill Staleness and Deprecation Linter for UniSkill.

Scans the skills catalog to detect deprecated APIs, legacy toolchain versions,
and constitutional violations, flagging skills that require 2026 SOTA upgrades.
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from uniskill.registry import list_skills
from uniskill.invariants import (
    check_devanagari_invariant,
    check_vehicle_metaphor_invariant,
    parse_and_validate_frontmatter,
)

DEPRECATED_PATTERNS = [
    {
        "id": "DEP-ANDR-001",
        "category": "Android",
        "pattern": r"\bandroid\.hardware\.Camera\b",
        "name": "Legacy Camera1 API",
        "recommendation": "Migrate to modern CameraX (1.4+) or Camera2",
    },
    {
        "id": "DEP-ANDR-002",
        "category": "Android",
        "pattern": r"\bfindViewById\b",
        "name": "Legacy findViewById View lookup",
        "recommendation": "Migrate to Jetpack Compose or ViewBinding",
    },
    {
        "id": "DEP-ANDR-003",
        "category": "Android",
        "pattern": r"\bjcenter\(\)",
        "name": "Deprecated JCenter repository",
        "recommendation": "Replace with mavenCentral() and google()",
    },
    {
        "id": "DEP-ANDR-004",
        "category": "Android",
        "pattern": r"\bkotlin-android-extensions\b",
        "name": "Deprecated kotlin-android-extensions plugin",
        "recommendation": "Migrate to Kotlin Parcelize and ViewBinding",
    },
    {
        "id": "DEP-WEB-001",
        "category": "Web",
        "pattern": r"\bgetInitialProps\b",
        "name": "Legacy Next.js getInitialProps",
        "recommendation": "Migrate to Next.js 15 App Router Server Components",
    },
    {
        "id": "DEP-PY-001",
        "category": "Python",
        "pattern": r"\bimport\s+imp\b",
        "name": "Deprecated imp module",
        "recommendation": "Migrate to importlib",
    },
]


def lint_skill_content(content: str, skill_name: str) -> List[Dict[str, Any]]:
    """Lints a single skill's content against known deprecation rules and invariants."""
    issues = []

    # 1. Check deprecated code patterns
    for rule in DEPRECATED_PATTERNS:
        matches = re.finditer(rule["pattern"], content)
        for m in matches:
            line_no = content[:m.start()].count("\n") + 1
            issues.append({
                "rule_id": rule["id"],
                "category": rule["category"],
                "name": rule["name"],
                "line": line_no,
                "recommendation": rule["recommendation"],
                "severity": "WARNING",
            })

    # 2. Check Constitutional Invariants
    devs = check_devanagari_invariant(content)
    for line_no, text in devs:
        issues.append({
            "rule_id": "CONST-DEV-001",
            "category": "Constitutional",
            "name": "Devanagari Script Detected",
            "line": line_no,
            "recommendation": "Remove Devanagari glyphs to prevent font rendering corruption",
            "severity": "CRITICAL",
        })

    metas = check_vehicle_metaphor_invariant(content)
    for line_no, line_text, term in metas:
        issues.append({
            "rule_id": "CONST-NOMEN-001",
            "category": "Constitutional",
            "name": f"Forbidden Transport Metaphor '{term}'",
            "line": line_no,
            "recommendation": "Replace with standard technical terminology (cluster, orchestrator, console)",
            "severity": "CRITICAL",
        })

    # 3. Check Frontmatter formatting
    try:
        meta, body = parse_and_validate_frontmatter(content)
        if not meta.get("description"):
            issues.append({
                "rule_id": "YAML-001",
                "category": "Formatting",
                "name": "Missing Frontmatter Description",
                "line": 1,
                "recommendation": "Add description: >- block scalar",
                "severity": "HIGH",
            })
    except Exception as e:
        issues.append({
            "rule_id": "YAML-002",
            "category": "Formatting",
            "name": f"Frontmatter Parse Error: {e}",
            "line": 1,
            "recommendation": "Format with clean YAML 1.2 description: >- block scalar",
            "severity": "CRITICAL",
        })

    return issues


def scan_catalog_for_outdated_skills() -> List[Dict[str, Any]]:
    """Scans all registered skills in SQLite catalog for deprecations and staleness."""
    skills = list_skills()
    flagged = []

    for s in skills:
        file_path_str = s.get("file_path")
        if not file_path_str:
            continue
        path = Path(file_path_str)
        if not path.is_file():
            continue

        try:
            content = path.read_text(encoding="utf-8")
            issues = lint_skill_content(content, s["name"])
            if issues:
                flagged.append({
                    "skill_name": s["name"],
                    "category": s.get("category", "General"),
                    "file_path": str(path),
                    "issues": issues,
                    "issue_count": len(issues),
                    "has_critical": any(i["severity"] == "CRITICAL" for i in issues),
                })
        except Exception:
            pass

    return flagged

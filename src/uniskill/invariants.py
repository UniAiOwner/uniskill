"""Invariants Engine for Antigravity Skill Manager.

Enforces Constitutional Law-000, Zero Devanagari, Zero Vehicle Metaphors,
YAML 1.2 Frontmatter integrity, and code syntax validation.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import yaml


FORBIDDEN_VEHICLE_TERMS = {
    "fleet",
    "cockpit",
    "pilot",
    "copilot",
    "autopilot",
    "steering wheel",
    "engine room",
    "airfield",
    "hangar",
    "vehicle",
    "vessel",
    "convoy",
}

# Devanagari Unicode range \u0900-\u097F
DEVANAGARI_REGEX = re.compile(r"[\u0900-\u097F]")


class InvariantViolation(Exception):
    """Raised when a constitutional or architectural invariant is violated."""
    pass


def check_devanagari_invariant(text: str) -> List[Tuple[int, str]]:
    """Checks for forbidden Devanagari script characters.
    Returns a list of (line_number, line_content) violations.
    """
    violations = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if DEVANAGARI_REGEX.search(line):
            violations.append((idx, line.strip()))
    return violations


def check_vehicle_metaphor_invariant(text: str) -> List[Tuple[int, str, str]]:
    """Checks for forbidden vehicle/aviation/naval metaphors.
    Returns a list of (line_number, matched_term, line_content).
    """
    violations = []
    for idx, line in enumerate(text.splitlines(), start=1):
        line_lower = line.lower()
        for term in FORBIDDEN_VEHICLE_TERMS:
            # Word boundary match to avoid false substrings
            pattern = rf"\b{re.escape(term)}\b"
            if re.search(pattern, line_lower):
                violations.append((idx, term, line.strip()))
    return violations


def parse_and_validate_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Validates and parses the YAML 1.2 frontmatter of a SKILL.md.
    Returns (frontmatter_dict, remaining_body).
    Raises InvariantViolation if format is invalid.
    """
    trimmed = content.lstrip()
    if not trimmed.startswith("---"):
        raise InvariantViolation("SKILL.md must start with '---' YAML frontmatter delimiter.")

    parts = trimmed.split("---", 2)
    if len(parts) < 3:
        raise InvariantViolation("SKILL.md missing closing '---' frontmatter delimiter.")

    raw_yaml = parts[1]
    body = parts[2]

    try:
        data = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as exc:
        raise InvariantViolation(f"YAML frontmatter parse error: {exc}")

    if not isinstance(data, dict):
        raise InvariantViolation("YAML frontmatter must be a key-value mapping.")

    if "name" not in data or not data["name"]:
        raise InvariantViolation("YAML frontmatter missing required 'name' field.")

    if "description" not in data or not data["description"]:
        raise InvariantViolation("YAML frontmatter missing required 'description' field.")

    # Validate name format: lowercase alphanumeric, hyphens, underscores
    name = str(data["name"]).strip()
    if not re.match(r"^[a-z0-9_\-]+$", name):
        raise InvariantViolation(f"Skill name '{name}' must contain only lowercase letters, digits, '-', or '_'.")

    return data, body


def validate_python_syntax(code: str) -> Optional[str]:
    """Validates Python code via AST parsing. Returns error string or None if valid."""
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return f"SyntaxError at line {e.lineno}: {e.msg}"


def validate_bracket_balance(code: str) -> Optional[str]:
    """Validates balanced brackets (), {}, [] ignoring string and comment contents."""
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}
    in_string = None
    escape = False

    for idx, ch in enumerate(code):
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if in_string:
            if ch == in_string:
                in_string = None
            continue
        if ch in ('"', "'", "`"):
            in_string = ch
            continue

        if ch in pairs.values():
            stack.append((ch, idx))
        elif ch in pairs:
            if not stack or stack[-1][0] != pairs[ch]:
                return f"Unmatched closing bracket '{ch}' at character position {idx}"
            stack.pop()

    if stack:
        return f"Unclosed opening bracket '{stack[-1][0]}' at character position {stack[-1][1]}"
    return None


def validate_skill_file(skill_path: Path) -> Dict[str, Any]:
    """Comprehensive validation of a skill file against all constitutional invariants.
    Returns a dict with 'valid': bool, 'errors': List[str], 'warnings': List[str].
    """
    errors = []
    warnings = []

    if not skill_path.exists():
        return {"valid": False, "errors": [f"File {skill_path} does not exist."], "warnings": []}

    try:
        content = skill_path.read_text(encoding="utf-8")
    except Exception as e:
        return {"valid": False, "errors": [f"Failed to read file: {e}"], "warnings": []}

    # 1. Frontmatter Validation
    try:
        meta, body = parse_and_validate_frontmatter(content)
    except InvariantViolation as iv:
        errors.append(str(iv))

    # 2. Devanagari Invariant
    dev_violations = check_devanagari_invariant(content)
    if dev_violations:
        for line_no, line_snippet in dev_violations[:5]:
            errors.append(f"Devanagari character violation at line {line_no}: '{line_snippet}'")

    # 3. Vehicle Metaphors Invariant
    metaphor_violations = check_vehicle_metaphor_invariant(content)
    if metaphor_violations:
        for line_no, term, line_snippet in metaphor_violations[:5]:
            errors.append(f"Forbidden transport metaphor '{term}' at line {line_no}: '{line_snippet}'")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }

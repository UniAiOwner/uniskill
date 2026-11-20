# Antigravity Skill Manager: Deep Research, Architectural Invariants & Sovereign Runtime Protocol

**Document ID**: `UNISKILL-RESEARCH-2026-V1`  
**Governing Standard**: UniGov Project Governance & Constitutional Law-000 (Zero Shortcuts)  
**Target Environment**: `/media/uniai/UniAi/PROJECTS_MIGRATED/ALL SKILLS/`  
**Founder & Co-Architect**: Shoeb Ahmad & Antigravity  
**Date**: 2026-11-19  

---

## 1. Executive Research Summary & The Fundamental Paradox

### 1.1 The Core Problem: "Skills Banana vs. Skills Use Karna"
Building skills is only 20% of the battle. The true failure point of autonomous agent ecosystems (including Gemini CLI, Claude Code, Cursor, and Antigravity) is **Skill Utilization & Runtime Activation**:
1. **The Context Budget Overflow Paradox**:
   - When an ecosystem accumulates 200+ skills, listing all skills in the agent's system prompt exhausts context budgets.
   - Antigravity's harness is forced to emit:  
     `The following items were excluded due to context budget limits: [20+ skills...]`
   - When a skill is excluded, neither Antigravity nor subagents can discover or load it, creating blind spots.
2. **The Passive Instruction Syndrome**:
   - In most setups, a skill is just passive markdown text. The agent often hallucinates or writes ad-hoc code instead of actively reading `SKILL.md` or executing the pre-tested helper scripts in `scripts/`.
3. **The Missing Bridge to Task Governance**:
   - Task managers (like UniGov) assign tasks (e.g. `TASK-CORTEX-ACC-03-READER`), but tasks do not explicitly specify *which skills must be activated*. The agent is left guessing.
4. **The Zero-Feedback Trap**:
   - When an agent solves a tough bug in a real project (e.g. edge-to-edge navigation bar overlap on Android 15), that lesson is trapped in a git commit or chat history. It never feeds back into the skill to make future tasks smarter.

---

## 2. The 6-Stage Sovereign Skill Lifecycle Architecture

To turn skills from static markdown files into a living, executable cognitive fabric, Antigravity Skill Manager implements a 6-stage closed-loop pipeline:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   SOVEREIGN SKILL LIFECYCLE PIPELINE                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┴───────────────────────────────┐
    ▼                                                               ▼
[Stage 1: Ingestion & Index]                                [Stage 2: Discovery & Route]
• Scan 217 skills across 8 domains                          • Intent-driven semantic matching
• Hash & track 100% SHA-256 parity                          • Top-3 ranked skill injection
• Detect executable helper scripts                          • Zero context-budget saturation
    │                                                               │
    └───────────────────────────────┬───────────────────────────────┘
                                    │
    ┌───────────────────────────────┴───────────────────────────────┐
    ▼                                                               ▼
[Stage 3: Pre-Flight Evaluation]                            [Stage 4: Surgical Injection]
• Project stack AST inspection                              • Extract relevant recipes only
• Detect version/API mismatches                             • Inject into UniGov Context Bundle
• Auto-upgrade lagging blueprints                           • Strict Law-000 zero-shortcut check
    │                                                               │
    └───────────────────────────────┬───────────────────────────────┘
                                    │
    ┌───────────────────────────────┴───────────────────────────────┐
    ▼                                                               ▼
[Stage 5: Runtime Execution]                                [Stage 6: Reflexive Learning]
• Invoke <skill>/scripts/ tools                             • Extract bug fixes from dev_logs
• Verify deterministic math/crypto                          • Distill insights into references/
• Headless CLI & programmatic API                           • Continuous self-evolving skills
    └───────────────────────────────────────────────────────────────┘
```

---

## 3. Deep Research on the 5 Essential Architectural Engines

### 3.1 Engine 1: Intent-Driven Semantic Skill Router (`router.py`)
- **Problem**: When Founder Shoeb Ahmad or UniGov gives a task (e.g., *"Make sure the counter billing checkout finishes in 3 seconds with zero floating point drift"*), how does the system know which skills apply?
- **Solution**: The Skill Router matches task keywords, domain ontology, and file extensions against skill capabilities using weighted scoring:
  - Exact symbol match (e.g., `Money.kt`, `Luhn`, `CameraX`) $\rightarrow$ Weight: 40%
  - Domain category alignment (e.g., Invoicing vs Android vs Security) $\rightarrow$ Weight: 30%
  - Trigger phrase & verb alignment (e.g., "migrate", "sanitize", "benchmark") $\rightarrow$ Weight: 30%
- **Output**: Returns the top 1–3 surgical skills with their exact disk paths and reading directives, bypassing the context truncation limit completely.

### 3.2 Engine 2: UniGov Task-to-Skill Governance Bridge
- **Problem**: In UniGov's WBS DAG, tasks track files and commands, but do not declare required skills.
- **Solution**:
  - Add `required_skills_json` to UniGov's `tasks` table.
  - When `unigov next` runs, it calls `uniskill route` to automatically bind required skills to the task.
  - The generated Zero-Noise Context Bundle includes the exact recipes from `SKILL.md` so the agent cannot miss them.

### 3.3 Engine 3: Unified Script Runner & Verification Harness (`runner.py`)
- **Problem**: 19+ skills have executable Python scripts in `scripts/`, but they require manual navigation and path resolution.
- **Solution**: `uniskill run <skill_name> <script_name> [args]`
  - Discovers and executes any skill helper script inside an isolated sandbox.
  - Standardizes inputs and JSON outputs.
  - Example: `uniskill run auto-paise-calculator test_skill` or `uniskill run escpos-thermal-printer-driver escpos_driver`.

### 3.4 Engine 4: Pre-Execution Suitability & Auto-Upgrade Gate (`evaluator.py` & `upgrader.py`)
- **Problem**: A skill might give instructions for AGP 8 or Android 14, but the target project is on AGP 9 and Android 16. Blindly following outdated skill advice causes build breakages.
- **Solution**:
  - Before injecting a skill, inspect project `build.gradle.kts` / `package.json`.
  - If project has `compileSdk = 35`, but skill lacks Android 15 insets, trigger auto-upgrade before the agent writes code.

### 3.5 Engine 5: Closed-Loop Skill Learner (`learner.py`)
- **Problem**: Skills are static and never learn from real showroom/development operations.
- **Solution**:
  - `uniskill learn --project <path>` inspects the latest entry in the project's `dev_logs.txt` and git diffs.
  - Extracts architectural fixes and appends them to `<skill>/references/LESSONS_LEARNED.md`.
  - Every project victory permanently improves the entire skill fabric.

---

## 4. Multi-Agent Delegation: How Antigravity and Subagents Use Skills

```
Shoeb Bhai / Antigravity
       │
       ▼
[Task Intent / UniGov DAG Task]
       │
       ▼
[uniskill route] ──▶ Returns Top 2 Skills:
       │              1. auto-paise-calculator (Math & Paise)
       │              2. escpos-thermal-printer-driver (Thermal Byte Stream)
       │
       ├─────────────────────────────────────────┐
       ▼                                         ▼
[Main Agent: Antigravity]                [Subagent / Green Prime]
• Reads surgical SKILL.md line ranges    • Receives bounded context bundle
• Calls `uniskill run` helper tools      • Executes task with zero context rot
• Verifies compilation with zero hacks   • Reports back empirical evidence
```

---

## 5. Verification Proof & Quality Gates

Every component of `antigravity-skill-manager` must satisfy 4 non-negotiable verification gates:
1. **Gate 1 (Zero-Defect AST)**: 100% of Python code parses cleanly via `ast.parse` and passes `unittest` with 0 failures.
2. **Gate 2 (100% Triple-Environment Bit-Parity)**: Every change to any skill automatically syncs across all 3 directories (`config`, `antigravity`, `antigravity-ide`) with matching SHA-256 hashes.
3. **Gate 3 (Constitutional Law-000 Invariants)**: Zero Devanagari characters, zero transport metaphors, zero `@Suppress` annotations.
4. **Gate 4 (Continuous Execution Gate)**: Real-time suitability scoring on active projects (UniRetail, UniGov, CSC Digital Register).

---
*Authored with absolute mathematical rigor for Founder Shoeb Ahmad*

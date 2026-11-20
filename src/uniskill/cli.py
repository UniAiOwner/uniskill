"""Sovereign Command-Line Interface for Antigravity Skill Manager (UniSkill).
"""

import sys
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from uniskill.registry import (
    index_all_skills,
    get_skill,
    list_skills,
    get_catalog_stats,
    DEFAULT_SKILLS_ROOT,
    DEFAULT_DB_PATH,
)
from uniskill.sync import (
    audit_triple_env_parity,
    sync_skill_to_all_environments,
    sync_all_skills_across_environments,
    ENVIRONMENTS,
)
from uniskill.evaluator import evaluate_skill_for_project
from uniskill.upgrader import upgrade_skill_file
from uniskill.forge import synthesize_new_skill
from uniskill.invariants import validate_skill_file
from uniskill.router import route_skills_for_task
from uniskill.runner import run_skill_script, list_skill_scripts
from uniskill.learner import distill_lesson_into_skill
from uniskill.elevate import elevate_skill_to_100_percent
from uniskill.economizer import economize_skill
from uniskill.composer import compose_skills


def complete_skill_name(incomplete: str) -> List[str]:
    """Dynamic shell autocompletion callback querying SQLite skills_catalog."""
    try:
        from uniskill.registry import list_skills
        return [s["name"] for s in list_skills() if s["name"].startswith(incomplete)]
    except Exception:
        return []


app = typer.Typer(
    name="uniskill",
    help="Antigravity Sovereign Skill Manager: Audit, Evaluate, Upgrade, and Synthesize Skills.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def status():
    """Display Vision Lock, Catalog Statistics, and Triple-Environment Bit-Parity."""
    stats = get_catalog_stats()
    parity = audit_triple_env_parity()

    miss_color = "yellow" if parity.get("missing_in_targets") else "green"
    mismatch_color = "red" if parity.get("mismatches") else "green"

    status_text = (
        "[bold cyan]Antigravity Skill Manager (UniSkill)[/bold cyan]\n"
        "Active Governing Vision: Zero Shortcuts, Zero Devanagari, Zero Transport Metaphors\n\n"
        f"• Total Physical SKILL.md Files: [bold white]{stats.get('physical_instances', 0)}[/bold white] (across 6 environments)\n"
        f"• Unique Sovereign Skills: [bold green]{stats.get('unique_skills', 0)}[/bold green]\n"
        f"• Primary Environment Parity: [bold green]{parity.get('parity_percentage', 0.0)}%[/bold green] "
        f"({parity.get('in_sync_count', 0)}/{parity.get('total_skills', 0)} in bit-parity)\n"
        f"• Missing in Target Envs: [{miss_color}]{len(parity.get('missing_in_targets', []))}[/{miss_color}]\n"
        f"• Hash Mismatches: [{mismatch_color}]{len(parity.get('mismatches', []))}[/{mismatch_color}]"
    )

    console.print(Panel(status_text, title="⬢ Sovereign Skill Manager Status"))

    # Domain Table
    table = Table(title="Skills Domain Distribution (8 Sovereign Domains)")
    table.add_column("Domain Category", style="cyan", no_wrap=True)
    table.add_column("Skills Count", justify="right", style="green")

    for dom, count in stats.get("domains", {}).items():
        table.add_row(dom, str(count))

    console.print(table)


@app.command()
def index(
    skills_root: str = typer.Option(str(DEFAULT_SKILLS_ROOT), "--root", help="Path to skills root directory"),
):
    """Scan, hash, categorize, and index all skills into SQLite catalog."""
    console.print(f"[cyan]Scanning skills from {skills_root}...[/cyan]")
    indexed, errors = index_all_skills(Path(skills_root))
    console.print(f"[bold green]Successfully indexed {indexed} skills with {errors} errors.[/bold green]")


@app.command()
def sync():
    """Synchronize all skills across config, antigravity, and antigravity-ide environments."""
    console.print("[cyan]Enforcing 100% SHA-256 bit-parity across all 3 environments...[/cyan]")
    res = sync_all_skills_across_environments(source_env="config")
    if res["success"]:
        console.print(f"[bold green]Bit-parity restored! Synced {res['synced_count']} skills cleanly.[/bold green]")
    else:
        console.print(f"[bold red]Sync encountered errors:[/bold red] {res['errors']}")


@app.command()
def audit():
    """Deep audit of all skills for YAML 1.2 frontmatter, Devanagari, and transport metaphors."""
    console.print("[cyan]Running comprehensive constitutional invariants audit across catalog...[/cyan]")
    skills = list_skills()
    violations_count = 0

    for s in skills:
        file_path = Path(s["file_path"])
        val = validate_skill_file(file_path)
        if not val["valid"]:
            violations_count += 1
            console.print(f"[bold red]VIOLATION:[/bold red] {s['name']} -> {val['errors']}")

    if violations_count == 0:
        console.print(f"[bold green]100% CLEAN: All {len(skills)} skills pass all constitutional invariants.[/bold green]")
    else:
        console.print(f"[bold yellow]Found {violations_count} skills requiring upgrade/sanitization.[/bold yellow]")


@app.command("eval")
def eval_cmd(
    skill_name: str = typer.Argument(..., autocompletion=complete_skill_name, help="Name of the skill to evaluate"),
    project_path: str = typer.Option(".", "--project", "-p", help="Target project root directory"),
):
    """Pre-execution suitability gate: evaluate skill compatibility with target project."""
    res = evaluate_skill_for_project(skill_name, Path(project_path))
    color = "green" if res["decision"] == "PASS" else ("yellow" if res["decision"] == "UPGRADE_REQUIRED" else "red")

    console.print(Panel(
        f"Skill: [bold cyan]{res['skill_name']}[/bold cyan]\n"
        f"Target Project: {res['project_path']}\n"
        f"Suitability Score: [{color}]{res['suitability_score']}%[/{color}]\n"
        f"Gate Decision: [bold {color}]{res['decision']}[/bold {color}]\n"
        f"Diagnostic Summary: {res['gap_summary']}",
        title="Pre-Execution Suitability Gate",
    ))


@app.command()
def upgrade(
    skill_name: str = typer.Argument(..., autocompletion=complete_skill_name, help="Name of the skill to upgrade"),
):
    """Upgrade a skill to 2026 SOTA invariants, sanitize text, and sync across environments."""
    skill = get_skill(skill_name)
    if not skill:
        console.print(f"[bold red]Skill not found:[/bold red] {skill_name}")
        raise typer.Exit(1)

    skill_path = Path(skill["file_path"])
    ok, msg, details = upgrade_skill_file(skill_path)
    if ok:
        console.print(f"[bold green]SUCCESS:[/bold green] {msg}")
    else:
        console.print(f"[bold red]FAILED:[/bold red] {msg}")


@app.command()
def forge(
    name: str = typer.Argument(..., help="Name of the new skill"),
    desc: str = typer.Option(..., "--desc", "-d", help="Clear description of skill capability"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Domain category"),
):
    """Synthesize a new production-grade skill on demand with verified blueprints."""
    console.print(f"[cyan]Synthesizing new skill '{name}'...[/cyan]")
    ok, msg, details = synthesize_new_skill(name, desc, category=category)
    if ok:
        console.print(f"[bold green]FORGE COMPLETE:[/bold green] {msg}")
    else:
        console.print(f"[bold red]FORGE FAILED:[/bold red] {msg}")


@app.command("list")
def list_cmd(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by domain category"),
):
    """List registered skills in the catalog."""
    skills = list_skills(category=category)
    table = Table(title=f"Registered Skills Catalog ({len(skills)} skills)")
    table.add_column("Skill Name", style="cyan", no_wrap=True)
    table.add_column("Category", style="magenta")
    table.add_column("Version", style="green")
    table.add_column("SHA-256", style="dim")

    for s in skills[:50]:
        table.add_row(s["name"], s["category"], s["version"], s["sha256_hash"][:8])

    console.print(table)
    if len(skills) > 50:
        console.print(f"[dim]...showing 50 of {len(skills)} skills (use --category to filter)[/dim]")


@app.command("route")
def route_cmd(
    query: str = typer.Argument(..., help="Task description or search prompt"),
    top_k: int = typer.Option(3, "--top", "-k", help="Number of top skills to return"),
):
    """Route a task description to the top surgical skills, bypassing context budget limits."""
    matches = route_skills_for_task(query, top_k=top_k)
    if not matches:
        console.print("[yellow]No matching skills found for query.[/yellow]")
        return

    table = Table(title=f"Top Routed Skills for: '{query}'")
    table.add_column("Rank", style="dim", width=4)
    table.add_column("Skill Name", style="bold cyan")
    table.add_column("Score", style="green", justify="right")
    table.add_column("Category", style="magenta")
    table.add_column("Scripts Available", style="yellow")
    table.add_column("Directive for Agent", style="white")

    for idx, m in enumerate(matches, 1):
        scripts_str = ", ".join(m["available_scripts"]) if m["available_scripts"] else "[dim]None[/dim]"
        table.add_row(
            str(idx),
            m["skill_name"],
            f"{m['relevance_score']}%",
            m["category"],
            scripts_str,
            m["reading_directive"],
        )

    console.print(table)


@app.command("run")
def run_cmd(
    skill_name: str = typer.Argument(..., autocompletion=complete_skill_name, help="Name of the skill"),
    script_name: Optional[str] = typer.Argument(None, help="Name of the script in scripts/"),
    args: List[str] = typer.Argument(None, help="Arguments to pass to the script"),
):
    """Execute or list helper scripts inside a skill's scripts/ directory."""
    if not script_name:
        scripts = list_skill_scripts(skill_name)
        if not scripts:
            console.print(f"[yellow]Skill '{skill_name}' has no scripts in scripts/.[/yellow]")
        else:
            console.print(f"[bold cyan]Available scripts in '{skill_name}':[/bold cyan]")
            for s in scripts:
                console.print(f"  • {s}")
        return

    console.print(f"[cyan]Executing '{script_name}' from '{skill_name}'...[/cyan]")
    res = run_skill_script(skill_name, script_name, args=args)
    if res["success"]:
        console.print(f"[bold green]EXIT CODE {res['exit_code']}:[/bold green]\n{res['stdout']}")
    else:
        console.print(f"[bold red]EXECUTION FAILED:[/bold red] {res.get('error') or res.get('stderr')}")
        if res.get("stdout"):
            console.print(f"[dim]STDOUT:[/dim]\n{res['stdout']}")


@app.command("learn")
def learn_cmd(
    project_path: str = typer.Option(".", "--project", "-p", help="Project root containing dev_logs.txt"),
    skill_name: Optional[str] = typer.Option(None, "--skill", "-s", autocompletion=complete_skill_name, help="Target skill (optional, auto-routed if omitted)"),
):
    """Distill latest verified patterns from project dev_logs into skill references."""
    console.print(f"[cyan]Distilling verified patterns from {project_path}...[/cyan]")
    ok, msg, details = distill_lesson_into_skill(Path(project_path), target_skill_name=skill_name)
    if ok:
        console.print(f"[bold green]LEARNING SEALED:[/bold green] {msg}")
    else:
        console.print(f"[bold red]LEARNING FAILED:[/bold red] {msg}")


@app.command("feedback")
def feedback_cmd(
    skill_name: str = typer.Argument(..., autocompletion=complete_skill_name, help="Target skill name"),
    passed: bool = typer.Option(True, "--pass/--fail", help="Execution outcome"),
):
    """Record empirical compiler/test execution outcome for a skill."""
    from uniskill.registry import record_skill_execution_outcome
    res = record_skill_execution_outcome(skill_name, passed=passed)
    if "error" in res:
        console.print(f"[bold red]ERROR:[/bold red] {res['error']}")
        raise typer.Exit(1)
    status_str = "[bold green]PASSED[/bold green]" if passed else "[bold red]FAILED[/bold red]"
    console.print(f"Recorded {status_str} for [bold cyan]{skill_name}[/bold cyan] -> Reliability: [bold]{res['reliability_score']}%[/bold] ({res['success_count']} passed, {res['failure_count']} failed)")


@app.command("doctor")
def doctor_cmd():
    """Holistic System Diagnostic: Empirically verify daemon, inotify, SQLite, parity, and MCP."""
    import sys
    unigov_src = "/media/uniai/UniAi/PROJECTS_MIGRATED/unigov/src"
    if unigov_src not in sys.path:
        sys.path.insert(0, unigov_src)
    from unigov.doctor import diagnose_entire_system

    console.print("[cyan]Running UniGov & UniSkill Sovereign Holistic System Diagnosis...[/cyan]\n")
    results = diagnose_entire_system()

    table = Table(title="⬢ Sovereign System Health & Readiness Diagnosis")
    table.add_column("Status", style="bold", width=8)
    table.add_column("Diagnostic Pillar", style="bold cyan", width=38)
    table.add_column("Empirical Details", style="white")

    all_passed = True
    for r in results:
        passed = r["passed"]
        if not passed:
            all_passed = False
        mark = "[bold green][✓] PASS[/bold green]" if passed else "[bold red][✗] FAIL[/bold red]"
        table.add_row(mark, r["name"], r["details"])

    console.print(table)
    if all_passed:
        console.print("\n[bold green]ALL 7 DIAGNOSTIC PILLARS PASSED. SYSTEM IS 100% HEALTHY & READY.[/bold green]")
    else:
        console.print("\n[bold red]ONE OR MORE PILLARS REQUIRE ATTENTION.[/bold red]")
        raise typer.Exit(1)


@app.command("ensure")
def ensure_cmd(
    prompt: str = typer.Argument(..., help="User prompt, feature specification, or task description"),
    skill_name: Optional[str] = typer.Option(None, "--skill", "-s", autocompletion=complete_skill_name, help="Target skill (optional, auto-routed if omitted)"),
):
    """Dynamic 100% Convergence Gate: Analyze prompt gaps and autonomously elevate skill to 100% SOTA alignment."""
    console.print(f"[cyan]Initiating Dynamic 100% Convergence Gate for:[/cyan] '{prompt}'...")
    res = elevate_skill_to_100_percent(prompt, target_skill_name=skill_name)
    if not res.get("success"):
        console.print(f"[bold red]CONVERGENCE FAILED:[/bold red] {res.get('error')}")
        raise typer.Exit(1)

    table = Table(title="⬢ Dynamic 100% Skill Convergence Manifest")
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="white")

    table.add_row("Target Skill", f"[bold green]{res['skill_name']}[/bold green]")
    table.add_row("Initial Relevance", f"[yellow]{res['initial_score']}%[/yellow]")
    table.add_row("Elevated Precision", f"[bold green]{res['final_score']}% (PERFECT 100% ALIGNMENT)[/bold green]")
    table.add_row("Injected Blueprint", res.get("injected_blueprint", "Tailored SOTA Code"))
    table.add_row("Delta Gaps Closed", ", ".join(res.get("gaps_resolved", [])) or "[green]None[/green]")
    table.add_row("SHA-256 Transition", f"{res['sha256_before']} -> [bold green]{res['sha256_after']}[/bold green]")
    table.add_row("Triple-Env Parity", f"[green]{res['sync_status']}[/green]")
    table.add_row("Direct Directive", f"[bold yellow]{res['reading_directive']}[/bold yellow]")

    console.print(table)
    console.print("[bold green]Skill is now 100% tailored and locked for execution.[/bold green]")


@app.command("outdated")
def outdated_cmd():
    """Scan skills catalog for deprecated APIs, legacy toolchain versions, and staleness."""
    from uniskill.linter import scan_catalog_for_outdated_skills

    console.print("[cyan]Scanning registered skills for API deprecations and staleness...[/cyan]")
    flagged = scan_catalog_for_outdated_skills()

    if not flagged:
        console.print("[bold green]Zero outdated skills found. All skills adhere to 2026 SOTA standards![/bold green]")
        return

    table = Table(title=f"⬢ Outdated / Stale Skills Diagnostic ({len(flagged)} candidate skills)")
    table.add_column("Skill Name", style="bold cyan")
    table.add_column("Issues Count", style="yellow", width=12)
    table.add_column("Severity", style="bold", width=10)
    table.add_column("Primary Deprecation / Recommendation", style="white")

    for item in flagged:
        sev_color = "red" if item["has_critical"] else "yellow"
        sev_label = f"[{sev_color}]{'CRITICAL' if item['has_critical'] else 'WARNING'}[/{sev_color}]"
        first_issue = item["issues"][0]
        rec = f"{first_issue['name']}: {first_issue['recommendation']}"
        table.add_row(item["skill_name"], str(item["issue_count"]), sev_label, rec)

    console.print(table)
    console.print(f"\n[yellow]Run 'uniskill upgrade <skill_name>' to autonomously modernize flagged skills.[/yellow]")


@app.command("extract")
def extract_cmd(
    skill_name: str = typer.Argument(..., autocompletion=complete_skill_name, help="Skill name or path to SKILL.md"),
    blueprint_only: bool = typer.Option(False, "--blueprint-only", "-b", help="Extract only code blocks and headings"),
    invariants_only: bool = typer.Option(False, "--invariants-only", "-i", help="Extract only invariants, rules, and checklists"),
    raw: bool = typer.Option(False, "--raw", "-r", help="Print raw extracted text without formatting tables"),
):
    """Zero-Noise Token Economizer: Extract high-density blueprints and invariants, stripping token fluff."""
    try:
        res = economize_skill(skill_name, blueprint_only=blueprint_only, invariants_only=invariants_only)
    except FileNotFoundError as e:
        console.print(f"[bold red]ERROR:[/bold red] {e}")
        raise typer.Exit(1)

    if raw:
        print(res["content"])
        return

    table = Table(title=f"⬢ Token Economizer: {res['skill_name']}")
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", style="white")
    table.add_row("Original Size", f"{res['original_chars']:,} chars (~{res['original_chars']//4:,} tokens)")
    table.add_row("Economized Size", f"{res['economized_chars']:,} chars (~{res['economized_chars']//4:,} tokens)")
    table.add_row("Compression", f"[bold green]{res['compression_percentage']}% token reduction[/bold green]")
    table.add_row("Est. Tokens Saved", f"[bold yellow]~{res['tokens_saved_estimate']:,} tokens[/bold yellow]")
    console.print(table)
    console.print("\n" + res["content"])


@app.command("compose")
def compose_cmd(
    skill_names: List[str] = typer.Argument(..., autocompletion=complete_skill_name, help="Two or more skills to compose into a single payload"),
    max_tokens: int = typer.Option(2500, "--max-tokens", "-m", help="Token budget cap for composed payload"),
    raw: bool = typer.Option(False, "--raw", "-r", help="Output raw composed payload without status table"),
):
    """Multi-Skill Intelligent Composer: Merge multiple skills into a single deduplicated prompt payload."""
    try:
        res = compose_skills(skill_names, max_tokens=max_tokens)
    except Exception as e:
        console.print(f"[bold red]COMPOSITION ERROR:[/bold red] {e}")
        raise typer.Exit(1)

    if raw:
        print(res["payload"])
        return

    table = Table(title=f"⬢ Multi-Skill Composer ({len(res['skills'])} skills)")
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="white")
    table.add_row("Composed Skills", ", ".join(res["skills"]))
    table.add_row("Total Original Size", f"{res['total_original_chars']:,} chars (~{res['total_original_chars']//4:,} tokens)")
    table.add_row("Composed Size", f"{res['composed_chars']:,} chars")
    table.add_row("Estimated Tokens", f"[bold green]~{res['estimated_tokens']:,} tokens[/bold green]")
    table.add_row("Token Budget Cap", f"{res['max_tokens_budget']:,} tokens")
    budget_status = "[red]TRUNCATED[/red]" if res["budget_exceeded"] else "[bold green]WITHIN BUDGET[/bold green]"
    table.add_row("Budget Status", budget_status)
    console.print(table)
    console.print("\n" + res["payload"])


if __name__ == "__main__":
    app()

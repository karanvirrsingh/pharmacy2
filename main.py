#!/usr/bin/env python3
"""Command-line interface for the AI Drug Interaction Checker.

Usage
-----
    python main.py                        # interactive session
    python main.py Warfarin Aspirin       # single lookup via arguments
    python main.py --help
"""

import argparse
import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from drug_interaction_checker import DrugInteractionChecker
from drug_interaction_checker.models import InteractionResult, Severity

console = Console()
checker = DrugInteractionChecker()

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

SEVERITY_COLOR: dict = {
    Severity.MINOR: "bold green",
    Severity.MODERATE: "bold yellow",
    Severity.MAJOR: "bold red",
    Severity.CONTRAINDICATED: "bold white on red",
}


def _print_banner() -> None:
    """Print the application banner."""
    console.print(
        Panel(
            "[bold cyan]💊  AI Drug Interaction Checker[/bold cyan]\n"
            "[dim]Educational tool — not a substitute for professional medical advice.[/dim]",
            border_style="cyan",
            expand=False,
        )
    )


def _print_result(result: InteractionResult) -> None:
    """Render an :class:`InteractionResult` to the console."""
    console.print()

    if not result.found:
        if result.drug1_matched is None or result.drug2_matched is None:
            console.print(f"[bold red]✗[/bold red]  {result.message}")
        else:
            console.print(
                Panel(
                    f"[yellow]{result.message}[/yellow]",
                    title="No Interaction Found",
                    border_style="yellow",
                )
            )
        return

    interaction = result.interaction
    severity_color = SEVERITY_COLOR.get(interaction.severity, "bold white")

    # ── Header ──────────────────────────────────────────────────────────────
    title_text = Text()
    title_text.append("⚕  Interaction: ", style="bold")
    title_text.append(interaction.drug1, style="bold cyan")
    title_text.append(" + ", style="bold")
    title_text.append(interaction.drug2, style="bold cyan")

    severity_badge = Text()
    severity_badge.append(
        f"  {interaction.severity.emoji()} {interaction.severity.value}  ",
        style=severity_color,
    )

    # ── Detail table ─────────────────────────────────────────────────────────
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Field", style="bold", min_width=18)
    table.add_column("Value")

    table.add_row(
        "Severity",
        Text(
            f"{interaction.severity.emoji()} {interaction.severity.value}",
            style=severity_color,
        ),
    )
    table.add_row("Description", interaction.description)
    table.add_row("Mechanism", interaction.mechanism)
    table.add_row("Recommendation", interaction.recommendation)

    if result.confidence < 1.0:
        table.add_row(
            "Confidence",
            f"{result.confidence * 100:.0f}% (based on fuzzy name matching)",
        )

    console.print(
        Panel(
            table,
            title=title_text,
            border_style=_severity_border(interaction.severity),
            subtitle=str(severity_badge),
        )
    )

    if result.message and "\n" in result.message:
        # Print any name-resolution notes
        for line in result.message.split("\n")[1:]:
            if line.strip():
                console.print(f"  [dim]{line.strip()}[/dim]")

    console.print()
    console.print(
        "[dim]⚠️  Disclaimer: This tool is for educational purposes only. "
        "Always consult a qualified healthcare professional before making "
        "clinical decisions.[/dim]"
    )


def _severity_border(severity: Severity) -> str:
    """Map a severity level to a Rich border-style string."""
    return {
        Severity.MINOR: "green",
        Severity.MODERATE: "yellow",
        Severity.MAJOR: "red",
        Severity.CONTRAINDICATED: "bright_red",
    }.get(severity, "white")


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

def run_single_lookup(drug1: str, drug2: str) -> int:
    """Perform a single interaction lookup and print the result.

    Args:
        drug1: First drug name.
        drug2: Second drug name.

    Returns:
        Exit code (0 = success / no interaction, 1 = error).
    """
    result = checker.check(drug1, drug2)
    _print_result(result)
    return 0


def run_interactive() -> None:
    """Run an interactive prompt loop until the user exits."""
    _print_banner()
    console.print(
        "\n[bold]Enter two drug names to check for interactions.[/bold]"
        "  Type [bold]exit[/bold] or press Ctrl+C to quit.\n"
    )

    while True:
        try:
            drug1 = Prompt.ask("[cyan]Drug 1[/cyan]").strip()
            if drug1.lower() in {"exit", "quit", "q"}:
                break
            drug2 = Prompt.ask("[cyan]Drug 2[/cyan]").strip()
            if drug2.lower() in {"exit", "quit", "q"}:
                break

            if not drug1 or not drug2:
                console.print("[red]Please enter both drug names.[/red]\n")
                continue

            result = checker.check(drug1, drug2)
            _print_result(result)
            console.print()

        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye![/dim]")
            break


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="drug-checker",
        description="AI Drug Interaction Checker — check interactions between two drugs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py Warfarin Aspirin\n"
            "  python main.py 'St. John's Wort' Warfarin\n"
            "  python main.py                          (interactive mode)\n\n"
            "Disclaimer: For educational purposes only. Not medical advice."
        ),
    )
    parser.add_argument(
        "drug1",
        nargs="?",
        help="First drug name",
    )
    parser.add_argument(
        "drug2",
        nargs="?",
        help="Second drug name",
    )
    return parser


def main() -> None:
    """Entry point for the CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if args.drug1 and args.drug2:
        sys.exit(run_single_lookup(args.drug1, args.drug2))
    elif args.drug1 or args.drug2:
        parser.error("Please supply both drug names, or neither for interactive mode.")
    else:
        run_interactive()


if __name__ == "__main__":
    main()

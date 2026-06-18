from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

from gitwhisper.scanner import Finding

console = Console()


def print_banner():
    console.print(r"""
[bold cyan]
       _ _            _     _                     
  __ _(_) |___      _| |__ (_)___ _ __   ___ _ __ 
 / _` | | __\ \ /\ / / '_ \| / __| '_ \ / _ \ '__|
| (_| | | |_ \ V  V /| | | | \__ \ |_) |  __/ |   
 \__, |_|\__| \_/\_/ |_| |_|_|___/ .__/ \___|_|   
 |___/                           |_|              
[/bold cyan]
[dim]Scanning for accidentally committed secrets...[/dim]
""")


def print_findings(findings: list[Finding]) -> None:
    if not findings:
        console.print("\n[bold green]✓ No secrets found![/bold green]\n")
        return

    table = Table(
        title=f"\n[bold red]⚠ {len(findings)} potential secret(s) found[/bold red]",
        box=box.ROUNDED,
        show_lines=True,
        highlight=True,
    )

    table.add_column("Type", style="bold yellow", no_wrap=True)
    table.add_column("File", style="cyan")
    table.add_column("Line", style="magenta", justify="right")
    table.add_column("Preview", style="dim")

    for finding in findings:
        table.add_row(
            finding.pattern_name,
            finding.file_path,
            str(finding.line_number),
            finding.line_preview,
        )

    console.print(table)
    console.print(
        "\n[bold red]Action required:[/bold red] Rotate any exposed secrets immediately "
        "and consider using [bold]git filter-repo[/bold] to scrub history.\n"
    )


def print_summary(findings: list[Finding], scanned: int) -> None:
    status = "[bold green]CLEAN[/bold green]" if not findings else "[bold red]SECRETS FOUND[/bold red]"
    console.print(f"[dim]Scanned {scanned} file(s) — Status: [/dim]{status}\n")

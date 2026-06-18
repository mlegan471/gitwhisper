import sys
from pathlib import Path

import click
from rich.console import Console
from rich.live import Live
from rich.text import Text

from gitwhisper.scanner import scan_directory, scan_directory_with_count
from gitwhisper.report import print_banner, print_findings, print_summary

console = Console()


@click.command()
@click.argument(
    "path",
    default=".",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.option(
    "--no-banner",
    is_flag=True,
    default=False,
    help="Suppress the banner (useful for CI output)",
)
def main(path: Path, no_banner: bool) -> None:
    """Scan a git repository for accidentally committed secrets."""
    if not no_banner:
        print_banner()

    findings = []
    scanned = 0

    with Live(console=console, refresh_per_second=10) as live:
        for finding, files_checked in scan_directory_with_count(path):
            scanned = files_checked
            live.update(
                Text.assemble(
                    ("⠸ Scanning... ", "bold cyan"),
                    (f"{scanned} file(s) checked", "dim"),
                )
            )
            if finding:
                findings.append(finding)

    print_findings(findings)
    print_summary(findings, scanned)

    if findings:
        sys.exit(1)

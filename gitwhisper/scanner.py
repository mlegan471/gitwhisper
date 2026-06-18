import re
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

from gitwhisper.patterns import PATTERNS, SecretPattern


@dataclass
class Finding:
    pattern_name: str
    file_path: str
    line_number: int
    line_preview: str


IGNORED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".pdf", ".zip", ".tar", ".gz", ".lock", ".whl",
}

IGNORED_DIRS = {
    ".git", ".venv", "node_modules", "__pycache__", ".tox", "dist", "build",
}


def redact(line: str, match: re.Match) -> str:
    """Replace the matched secret with asterisks, keeping first 4 chars."""
    secret = match.group()
    visible = secret[:4]
    redacted = visible + "*" * (len(secret) - 4)
    return line[:match.start()] + redacted + line[match.end():]


def scan_file(file_path: Path) -> Generator[Finding, None, None]:
    """Scan a single file for secret patterns."""
    if file_path.suffix in IGNORED_EXTENSIONS:
        return

    try:
        lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except (OSError, PermissionError):
        return

    for line_number, line in enumerate(lines, start=1):
        matched = False
        for secret_pattern in PATTERNS:
            match = secret_pattern.pattern.search(line)
            if match:
                if matched and secret_pattern.name == "Generic High-Risk Assignment":
                    continue
                matched = True
                yield Finding(
                    pattern_name=secret_pattern.name,
                    file_path=str(file_path),
                    line_number=line_number,
                    line_preview=redact(line.strip(), match),
                )


def scan_directory(root: Path) -> Generator[Finding, None, None]:
    """Recursively scan all files in a directory."""
    for path in root.rglob("*"):
        if any(ignored in path.parts for ignored in IGNORED_DIRS):
            continue
        if path.is_file():
            yield from scan_file(path)


def scan_directory_with_count(root: Path) -> Generator[tuple, None, None]:
    """Scan directory yielding (finding_or_None, files_checked) tuples."""
    count = 0
    for path in root.rglob("*"):
        if any(ignored in path.parts for ignored in IGNORED_DIRS):
            continue
        if path.is_file():
            count += 1
            found_anything = False
            for finding in scan_file(path):
                found_anything = True
                yield finding, count
            if not found_anything:
                yield None, count


def scan_git_history(root: Path) -> Generator[Finding, None, None]:
    """Scan git commit history for secrets."""
    try:
        from git import Repo, InvalidGitRepositoryError
    except ImportError:
        return

    try:
        repo = Repo(root)
    except InvalidGitRepositoryError:
        return

    seen = set()

    for commit in repo.iter_commits():
        for parent in commit.parents:
            diffs = parent.diff(commit)
            for diff in diffs:
                try:
                    if diff.b_blob is None:
                        continue
                    content = diff.b_blob.data_stream.read().decode(
                        "utf-8", errors="ignore"
                    )
                    for line_number, line in enumerate(
                        content.splitlines(), start=1
                    ):
                        for secret_pattern in PATTERNS:
                            match = secret_pattern.pattern.search(line)
                            if match:
                                key = (secret_pattern.name, diff.b_path.strip(), line_number)
                                if key in seen:
                                    break
                                seen.add(key)
                                yield Finding(
                                    pattern_name=secret_pattern.name,
                                    file_path=f"[commit {commit.hexsha[:7]}] {diff.b_path}",
                                    line_number=line_number,
                                    line_preview=redact(line.strip(), match),
                                )
                                break
                except Exception:
                    continue

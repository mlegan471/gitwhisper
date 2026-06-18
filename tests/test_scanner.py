from pathlib import Path
import pytest
from gitwhisper.scanner import scan_file, scan_directory
from gitwhisper.patterns import PATTERNS


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_detects_openai_key():
    findings = list(scan_file(FIXTURES_DIR / "fake_secrets.env"))
    types = [f.pattern_name for f in findings]
    assert "OpenAI API Key" in types


def test_detects_aws_access_key():
    findings = list(scan_file(FIXTURES_DIR / "fake_secrets.env"))
    types = [f.pattern_name for f in findings]
    assert "AWS Access Key ID" in types


def test_detects_github_token():
    findings = list(scan_file(FIXTURES_DIR / "fake_secrets.env"))
    types = [f.pattern_name for f in findings]
    assert "GitHub Personal Access Token" in types


def test_detects_google_api_key():
    findings = list(scan_file(FIXTURES_DIR / "fake_secrets.env"))
    types = [f.pattern_name for f in findings]
    assert "Google API Key" in types


def test_detects_stripe_key():
    findings = list(scan_file(FIXTURES_DIR / "fake_secrets.env"))
    types = [f.pattern_name for f in findings]
    assert "Stripe Secret Key" in types


def test_redaction_hides_secret():
    findings = list(scan_file(FIXTURES_DIR / "fake_secrets.env"))
    for finding in findings:
        assert "*" in finding.line_preview


def test_clean_file_returns_no_findings(tmp_path):
    clean_file = tmp_path / "clean.env"
    clean_file.write_text("DEBUG=true\nPORT=8080\nHOST=localhost\n")
    findings = list(scan_file(clean_file))
    assert findings == []


def test_scan_directory_finds_fixtures():
    findings = list(scan_directory(FIXTURES_DIR))
    assert len(findings) > 0


def test_no_duplicate_findings_per_line():
    findings = list(scan_file(FIXTURES_DIR / "fake_secrets.env"))
    # Each line should only appear once per finding
    seen = [(f.line_number, f.pattern_name) for f in findings]
    assert len(seen) == len(set(seen))

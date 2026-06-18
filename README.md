# gitwhisper 🔐

![CI](https://github.com/mlegan471/gitwhisper/actions/workflows/ci.yml/badge.svg)

A CLI tool that scans git repositories for accidentally committed secrets — API keys, tokens, and credentials — before they become a problem.

## The Problem

People get burned by exposed secrets constantly. Leaked AWS keys have resulted in thousands of dollars in unexpected bills. Exposed OpenAI keys get scraped within minutes. And the worst part? Deleting the file doesn't help — the secret lives on in your git history forever.

gitwhisper catches secrets before they cause damage.

## Features

- 🔍 Scans files for 9+ known secret patterns (OpenAI, AWS, GitHub, Google, Stripe, and more)
- 📜 Scans git commit history with `--history` — because deleting a file doesn't remove it from git
- 🔒 Redacted output — shows you what was found without re-exposing the secret
- ⚡ Live progress indicator
- 🚦 Exit code 1 on findings — drop it straight into CI pipelines
- 🔇 `--no-banner` flag for clean CI output

## Installation

```bash
git clone https://github.com/mlegan471/gitwhisper.git
cd gitwhisper
pip install -e .
```

## Usage

Scan current directory:
```bash
gitwhisper .
```

Scan a specific path:
```bash
gitwhisper /path/to/repo
```

Also scan git commit history:
```bash
gitwhisper . --history
```

Use in CI (no banner, exit code 1 on findings):
```bash
gitwhisper . --no-banner
```

## Supported Secret Types

| Type | Example Format |
|------|---------------|
| OpenAI API Key | `sk-...` |
| AWS Access Key ID | `AKIA...` |
| AWS Secret Access Key | `aws_secret_access_key = ...` |
| GitHub Personal Access Token | `ghp_...` |
| GitHub OAuth Token | `gho_...` |
| Google API Key | `AIza...` |
| Stripe Secret Key | `sk_live_...` |
| Slack Bot Token | `xoxb-...` |
| Private Key Block | `-----BEGIN ... PRIVATE KEY-----` |
| Generic High-Risk Assignment | `password = "..."` |

## Running Tests

```bash
python -m pytest tests/ -v
```

## Why I Built This

Secrets leaking into public repositories is one of the most common and costly security mistakes in software development. I built gitwhisper to understand the problem from the inside — how detection works, where the edge cases are, and what it takes to reduce false positives without missing real findings.

## License

MIT

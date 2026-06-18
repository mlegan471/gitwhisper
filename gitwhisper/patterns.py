import re
from dataclasses import dataclass


@dataclass
class SecretPattern:
    name: str
    pattern: re.Pattern
    example: str


PATTERNS = [
    SecretPattern(
        name="OpenAI API Key",
        pattern=re.compile(r'sk-[A-Za-z0-9]{32,}'),
        example="sk-abc123...",
    ),
    SecretPattern(
        name="AWS Access Key ID",
        pattern=re.compile(r'AKIA[0-9A-Z]{16}'),
        example="AKIA**************** (redacted)",
    ),
    SecretPattern(
        name="AWS Secret Access Key",
        pattern=re.compile(r'(?i)aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}'),
        example="aws_secret_access_key = abc123...",
    ),
    SecretPattern(
        name="GitHub Personal Access Token",
        pattern=re.compile(r'gh[ps]_[A-Za-z0-9]{36}'),
        example="ghp_abc123...",
    ),
    SecretPattern(
        name="GitHub OAuth Token",
        pattern=re.compile(r'gho_[A-Za-z0-9]{36}'),
        example="gho_abc123...",
    ),
    SecretPattern(
        name="Google API Key",
        pattern=re.compile(r'AIza[0-9A-Za-z\-_]{35}'),
        example="AIzaSyAbc123...",
    ),
    SecretPattern(
        name="Stripe Secret Key",
        pattern=re.compile(r'sk_live_[0-9a-zA-Z]{24,}'),
        example="sk_live_abc123...",
    ),
    SecretPattern(
        name="Slack Bot Token",
        pattern=re.compile(r'xoxb-[0-9]{11}-[0-9]{11}-[A-Za-z0-9]{24}'),
        example="xoxb-123-456-abc...",
    ),
    SecretPattern(
        name="Private Key Block",
        pattern=re.compile(r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----'),
        example="-----BEGIN [PRIVATE KEY BLOCK]-----",
    ),
    SecretPattern(
        name="Generic High-Risk Assignment",
        pattern=re.compile(r'(?i)(password|secret|token|api_key)\s*=\s*["\']?[A-Za-z0-9/+=_\-]{8,}["\']?'),
        example='password = "abc123..."',
    ),
]

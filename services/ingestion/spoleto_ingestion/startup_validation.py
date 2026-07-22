from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from shutil import which
import os
import subprocess
import sys


REQUIRED_ENV_VARS = [
    "OPENCLAW_GATEWAY_TOKEN",
    "OPENCLAW_CONFIG_PATH",
    "OPENCLAW_WORKSPACE",
]

REQUIRED_PATHS = [
    "openclaw/openclaw.json5",
    "openclaw/includes/agents.json5",
    "openclaw/includes/channels.whatsapp.json5",
    "openclaw/includes/tools.json5",
    "openclaw/includes/hooks.json5",
    "prompts/base/system.md",
    "data/raw/images",
    "data/processed",
]


def _check_env_vars() -> list[str]:
    missing = []
    for name in REQUIRED_ENV_VARS:
        if not os.getenv(name, "").strip():
            missing.append(name)
    return missing


def _check_paths(root: Path) -> list[str]:
    missing = []
    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            missing.append(rel)
    return missing


def _check_docker() -> str | None:
    if which("docker") is None:
        return "Docker CLI not found in PATH"
    try:
        result = subprocess.run(
            ["docker", "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return f"Docker invocation failed: {exc}"
    if result.returncode != 0:
        return "Docker CLI is installed but not working"
    return None


def _check_openclaw_config(root: Path) -> list[str]:
    issues: list[str] = []
    root_config = root / "openclaw" / "openclaw.json5"
    if not root_config.exists():
        return ["openclaw/openclaw.json5 is missing"]

    root_text = root_config.read_text(encoding="utf-8")
    required_tokens = [
        '"./includes/agents.json5"',
        '"./includes/channels.whatsapp.json5"',
        '"./includes/tools.json5"',
        '"./includes/hooks.json5"',
    ]
    for token in required_tokens:
        if token not in root_text:
            issues.append(f"openclaw/openclaw.json5 missing include reference: {token}")

    include_paths = [
        root / "openclaw" / "includes" / "agents.json5",
        root / "openclaw" / "includes" / "channels.whatsapp.json5",
        root / "openclaw" / "includes" / "tools.json5",
        root / "openclaw" / "includes" / "hooks.json5",
    ]
    for path in include_paths:
        if path.exists() and not path.read_text(encoding="utf-8").strip():
            issues.append(f"OpenClaw include file is empty: {path.relative_to(root)}")
    return issues


def main() -> int:
    parser = ArgumentParser(description="Validate local startup prerequisites")
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root path",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    missing_env = _check_env_vars()
    missing_paths = _check_paths(root)
    docker_error = _check_docker()
    openclaw_issues = _check_openclaw_config(root)

    errors: list[str] = []
    if missing_env:
        errors.append(f"Missing env vars: {', '.join(missing_env)}")
    if missing_paths:
        errors.append(f"Missing required files/directories: {', '.join(missing_paths)}")
    if docker_error:
        errors.append(docker_error)
    errors.extend(openclaw_issues)

    if errors:
        print("Startup validation failed:")
        for item in errors:
            print(f"- {item}")
        return 1

    print("Startup validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

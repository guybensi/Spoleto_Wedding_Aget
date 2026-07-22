from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path


PROMPT_ORDER = [
    "system.md",
    "safety.md",
    "trip_context.md",
    "itinerary_rules.md",
    "response_style.md",
    "personality.md",
]


def assemble_prompt(base_dir: Path) -> str:
    sections: list[str] = []
    for name in PROMPT_ORDER:
        path = base_dir / name
        if not path.exists():
            raise FileNotFoundError(f"Missing prompt module: {path}")
        content = path.read_text(encoding="utf-8").strip()
        sections.append(f"## {name}\n{content}")

    # Reinforce private-data priority in final assembled prompt.
    sections.append(
        "## private_data_priority\n"
        "Use private reviewed trip documents as authoritative sources before public web information."
    )
    return "\n\n".join(sections) + "\n"


def main() -> int:
    parser = ArgumentParser(description="Assemble modular prompt files into one system prompt")
    parser.add_argument("--base-dir", default="prompts/base", help="Directory with prompt modules")
    parser.add_argument(
        "--output",
        default="workspace/system_prompt.md",
        help="Path to write the assembled prompt",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    assembled = assemble_prompt(base_dir)
    output.write_text(assembled, encoding="utf-8")
    print(f"Assembled prompt written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

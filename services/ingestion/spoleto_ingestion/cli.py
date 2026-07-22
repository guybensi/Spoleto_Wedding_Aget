from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import json

from .normalization import normalize_extracted_payload
from .providers import MockVisionProvider, UnconfiguredVisionProvider, VisionProvider


def _build_provider(name: str) -> VisionProvider:
    provider_name = name.strip().lower()
    if provider_name == "mock":
        return MockVisionProvider()
    return UnconfiguredVisionProvider()


def _ingest_pngs(input_dir: Path, output_dir: Path, provider: VisionProvider) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(input_dir.glob("*.png"))
    processed = 0

    for image_path in files:
        extraction = provider.extract(image_path)
        normalized = normalize_extracted_payload(image_path, extraction.text)
        output_file = output_dir / f"{image_path.stem}.json"
        output_file.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")
        processed += 1

    return processed


def main() -> int:
    parser = ArgumentParser(description="Spoleto ingestion MVP CLI")
    parser.add_argument(
        "--input-dir",
        default="data/raw/images",
        help="Directory containing PNG source files",
    )
    parser.add_argument(
        "--output-dir",
        default="data/processed",
        help="Directory for normalized JSON output",
    )
    parser.add_argument(
        "--provider",
        default="mock",
        choices=["mock", "real"],
        help="Vision/OCR provider implementation",
    )

    args = parser.parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        raise SystemExit(f"Input directory not found: {input_dir}")

    provider = _build_provider(args.provider)
    processed = _ingest_pngs(input_dir=input_dir, output_dir=output_dir, provider=provider)
    print(f"Ingestion complete. Processed {processed} PNG file(s) with provider '{provider.name}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

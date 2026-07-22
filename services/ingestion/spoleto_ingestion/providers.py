from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class ExtractionResult:
    source_path: Path
    text: str


class VisionProvider:
    """Interface for OCR/vision content extraction providers."""

    name = "base"

    def extract(self, image_path: Path) -> ExtractionResult:
        raise NotImplementedError


class MockVisionProvider(VisionProvider):
    """
    Deterministic local provider.

    If a sibling JSON file exists (same stem as the PNG), its payload is serialized
    as the extraction text. Otherwise, a minimal default payload is generated.
    """

    name = "mock"

    def extract(self, image_path: Path) -> ExtractionResult:
        sidecar_path = image_path.with_suffix(".mock.json")
        if sidecar_path.exists():
            payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
            text = json.dumps(payload)
        else:
            text = json.dumps(
                {
                    "faq": {
                        "question": f"What is in {image_path.name}?",
                        "answer": "Mock extraction did not find a sidecar payload.",
                    }
                }
            )
        return ExtractionResult(source_path=image_path, text=text)


class UnconfiguredVisionProvider(VisionProvider):
    name = "unconfigured"

    def extract(self, image_path: Path) -> ExtractionResult:
        raise RuntimeError(
            "No real OCR provider is configured for MVP. Use --provider mock for local runs."
        )

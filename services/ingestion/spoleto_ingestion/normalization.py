from __future__ import annotations

from pathlib import Path
import json

from .schemas import validate_normalized_payload


def normalize_extracted_payload(source_file: Path, extracted_text: str) -> dict[str, object]:
    """
    Normalize extracted text into schema-validated canonical JSON.

    The MVP expects extracted text to be JSON content with the schema sections.
    """
    raw = json.loads(extracted_text)
    if not isinstance(raw, dict):
        raise ValueError("Extracted payload must be a JSON object")

    validated_sections = validate_normalized_payload(raw)
    return {
        "source_file": source_file.name,
        "sections": validated_sections,
    }

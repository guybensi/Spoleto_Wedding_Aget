from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


ALLOWED_DOCUMENT_TYPES = {
    "emergency",
    "faq",
    "guest_logistics",
    "hotel",
    "itinerary",
    "recommendations",
    "restaurant_reservation",
    "transport",
    "wedding_schedule",
}

ALLOWED_FILE_FORMATS = {"csv", "pdf", "png", "xls", "xlsx"}


class ManifestError(ValueError):
    pass


@dataclass(frozen=True)
class ManifestDocument:
    path: Path
    document_type: str
    version: str
    owner: str
    file_format: str


@dataclass(frozen=True)
class Manifest:
    trip_id: str
    documents: list[ManifestDocument]


def load_manifest(path: str | Path) -> Manifest:
    manifest_path = Path(path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    trip_id = str(payload.get("trip_id", "")).strip()
    if not trip_id:
        raise ManifestError("Manifest must include a non-empty trip_id")

    raw_documents = payload.get("documents")
    if not isinstance(raw_documents, list) or not raw_documents:
        raise ManifestError("Manifest must include at least one document")

    documents = [_parse_document(item) for item in raw_documents]
    return Manifest(trip_id=trip_id, documents=documents)


def _parse_document(item: object) -> ManifestDocument:
    if not isinstance(item, dict):
        raise ManifestError("Each document entry must be an object")

    raw_path = str(item.get("path", "")).strip()
    document_type = str(item.get("document_type", "")).strip()
    version = str(item.get("version", "")).strip()
    owner = str(item.get("owner", "")).strip()

    if not raw_path:
        raise ManifestError("Document path is required")
    if document_type not in ALLOWED_DOCUMENT_TYPES:
        raise ManifestError(f"Unsupported document_type: {document_type}")
    if not version:
        raise ManifestError("Document version is required")
    if not owner:
        raise ManifestError("Document owner is required")

    document_path = Path(raw_path)
    file_format = document_path.suffix.lower().lstrip(".")
    if file_format not in ALLOWED_FILE_FORMATS:
        raise ManifestError(f"Unsupported file format: {file_format}")

    return ManifestDocument(
        path=document_path,
        document_type=document_type,
        version=version,
        owner=owner,
        file_format=file_format,
    )
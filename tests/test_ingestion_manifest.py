from pathlib import Path
import json
import tempfile
import unittest


from services.ingestion.spoleto_ingestion.manifest import ManifestError, load_manifest


class IngestionManifestTests(unittest.TestCase):
    def test_load_manifest_parses_documents(self) -> None:
        manifest_data = {
            "trip_id": "spoleto-2026",
            "documents": [
                {
                    "path": "data/trips/spoleto-2026/raw/png/day-1-itinerary.png",
                    "document_type": "itinerary",
                    "version": "2026-07-20",
                    "owner": "organizers",
                },
                {
                    "path": "data/trips/spoleto-2026/raw/png/hotel-details.pdf",
                    "document_type": "hotel",
                    "version": "2026-07-20",
                    "owner": "organizers",
                },
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "manifest.json"
            manifest_path.write_text(json.dumps(manifest_data), encoding="utf-8")

            manifest = load_manifest(manifest_path)

        self.assertEqual(manifest.trip_id, "spoleto-2026")
        self.assertEqual(len(manifest.documents), 2)
        self.assertEqual(manifest.documents[0].file_format, "png")
        self.assertEqual(manifest.documents[1].file_format, "pdf")

    def test_load_manifest_rejects_unsupported_file_type(self) -> None:
        manifest_data = {
            "trip_id": "spoleto-2026",
            "documents": [
                {
                    "path": "data/trips/spoleto-2026/raw/png/notes.docx",
                    "document_type": "faq",
                    "version": "2026-07-20",
                    "owner": "organizers",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "manifest.json"
            manifest_path.write_text(json.dumps(manifest_data), encoding="utf-8")

            with self.assertRaises(ManifestError):
                load_manifest(manifest_path)

    def test_load_manifest_requires_documents(self) -> None:
        manifest_data = {"trip_id": "spoleto-2026", "documents": []}

        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "manifest.json"
            manifest_path.write_text(json.dumps(manifest_data), encoding="utf-8")

            with self.assertRaises(ManifestError):
                load_manifest(manifest_path)


if __name__ == "__main__":
    unittest.main()
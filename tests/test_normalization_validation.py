from pathlib import Path
import json
import tempfile
import unittest

from services.ingestion.spoleto_ingestion.cli import main as cli_main
from services.ingestion.spoleto_ingestion.normalization import normalize_extracted_payload
from services.ingestion.spoleto_ingestion.schemas import ValidationError, validate_normalized_payload
from services.ingestion.spoleto_ingestion.prompt_assembly import assemble_prompt


VALID_PAYLOAD = {
    "itinerary": {
        "title": "Arrival Day",
        "day": "2026-07-20",
        "details": "Guest check-in and welcome dinner",
    },
    "transportation": {
        "mode": "Train",
        "departure": "Rome Termini",
        "arrival": "Spoleto",
        "details": "Frecciarossa + local transfer",
    },
    "accommodation": {
        "hotel_name": "Hotel Gattapone",
        "address": "Via Example 1, Spoleto",
        "check_in": "2026-07-20T15:00:00",
        "check_out": "2026-07-23T11:00:00",
    },
    "recommendations": {
        "category": "Dining",
        "item": "Osteria del Matto",
        "notes": "Book dinner after ceremony",
    },
    "faq": {
        "question": "What is the dress code?",
        "answer": "Summer formal",
    },
}


class NormalizationValidationTests(unittest.TestCase):
    def test_validate_normalized_payload_success(self) -> None:
        validated = validate_normalized_payload(VALID_PAYLOAD)
        self.assertEqual(validated["itinerary"]["title"], "Arrival Day")
        self.assertEqual(validated["faq"]["answer"], "Summer formal")

    def test_validate_normalized_payload_missing_field(self) -> None:
        invalid = {
            **VALID_PAYLOAD,
            "accommodation": {
                "hotel_name": "Hotel Gattapone",
                "address": "Via Example 1, Spoleto",
                "check_in": "2026-07-20T15:00:00",
                "check_out": "",
            },
        }
        with self.assertRaises(ValidationError):
            validate_normalized_payload(invalid)

    def test_normalize_extracted_payload(self) -> None:
        source = Path("day-1.png")
        normalized = normalize_extracted_payload(source_file=source, extracted_text=json.dumps(VALID_PAYLOAD))
        self.assertEqual(normalized["source_file"], "day-1.png")
        self.assertEqual(normalized["sections"]["transportation"]["mode"], "Train")

    def test_cli_ingests_png_with_mock_provider(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_dir = root / "raw" / "images"
            output_dir = root / "processed"
            input_dir.mkdir(parents=True, exist_ok=True)

            image = input_dir / "day-1.png"
            image.write_bytes(b"PNG")
            (input_dir / "day-1.mock.json").write_text(json.dumps(VALID_PAYLOAD), encoding="utf-8")

            old_argv = __import__("sys").argv
            try:
                __import__("sys").argv = [
                    "spoleto-ingest",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(output_dir),
                    "--provider",
                    "mock",
                ]
                exit_code = cli_main()
            finally:
                __import__("sys").argv = old_argv

            self.assertEqual(exit_code, 0)
            output_file = output_dir / "day-1.json"
            self.assertTrue(output_file.exists())
            payload = json.loads(output_file.read_text(encoding="utf-8"))
            self.assertEqual(payload["sections"]["faq"]["answer"], "Summer formal")

    def test_prompt_assembly_includes_private_priority(self) -> None:
        base_dir = Path(__file__).resolve().parents[1] / "prompts" / "base"
        assembled = assemble_prompt(base_dir)
        self.assertIn("private_data_priority", assembled)
        self.assertIn("private reviewed trip documents", assembled)


if __name__ == "__main__":
    unittest.main()

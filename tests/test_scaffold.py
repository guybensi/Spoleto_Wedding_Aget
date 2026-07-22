from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ScaffoldContractTests(unittest.TestCase):
    def test_expected_directories_exist(self) -> None:
        expected = [
            ROOT / "docs" / "specification",
            ROOT / "openclaw" / "includes",
            ROOT / "workspace",
            ROOT / "prompts" / "base",
            ROOT / "services" / "ingestion",
            ROOT / "data" / "permanent",
            ROOT / "data" / "trips" / "spoleto-2026" / "raw" / "png",
        ]

        missing = [str(path.relative_to(ROOT)) for path in expected if not path.exists()]

        self.assertFalse(missing, f"Missing scaffold directories: {missing}")

    def test_expected_files_exist(self) -> None:
        expected = [
            ROOT / "README.md",
            ROOT / "openclaw" / "openclaw.json5",
            ROOT / "workspace" / "AGENTS.md",
            ROOT / "workspace" / "SOUL.md",
            ROOT / "workspace" / "TOOLS.md",
            ROOT / "prompts" / "base" / "system.md",
            ROOT / "prompts" / "base" / "safety.md",
            ROOT / "docs" / "specification" / "engineering-overview.md",
            ROOT / "services" / "ingestion" / "README.md",
        ]

        missing = [str(path.relative_to(ROOT)) for path in expected if not path.exists()]

        self.assertFalse(missing, f"Missing scaffold files: {missing}")


if __name__ == "__main__":
    unittest.main()
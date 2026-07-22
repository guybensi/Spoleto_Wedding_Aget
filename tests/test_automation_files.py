from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AutomationFileTests(unittest.TestCase):
    def test_ci_workflow_exists_and_runs_tests(self) -> None:
        workflow_path = ROOT / ".github" / "workflows" / "ci.yml"
        self.assertTrue(workflow_path.exists(), "Missing CI workflow at .github/workflows/ci.yml")

        workflow_text = workflow_path.read_text(encoding="utf-8")
        self.assertIn("unittest discover -s tests", workflow_text)

    def test_contributing_guide_exists(self) -> None:
        contributing_path = ROOT / "CONTRIBUTING.md"
        self.assertTrue(contributing_path.exists(), "Missing CONTRIBUTING.md")


if __name__ == "__main__":
    unittest.main()
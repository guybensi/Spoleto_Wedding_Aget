from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PackagingFileTests(unittest.TestCase):
    def test_env_example_exists_and_documents_required_variables(self) -> None:
        env_example = ROOT / ".env.example"
        self.assertTrue(env_example.exists(), "Missing .env.example")

        text = env_example.read_text(encoding="utf-8")
        self.assertIn("ANTHROPIC_API_KEY=", text)
        self.assertIn("OPENCLAW_GATEWAY_TOKEN=", text)

    def test_docker_packaging_files_exist(self) -> None:
        dockerfile = ROOT / "Dockerfile"
        compose_file = ROOT / "docker-compose.yml"
        dockerignore = ROOT / ".dockerignore"

        self.assertTrue(dockerfile.exists(), "Missing Dockerfile")
        self.assertTrue(compose_file.exists(), "Missing docker-compose.yml")
        self.assertTrue(dockerignore.exists(), "Missing .dockerignore")

        compose_text = compose_file.read_text(encoding="utf-8")
        self.assertIn("openclaw", compose_text)
        self.assertIn("ingestion", compose_text)


if __name__ == "__main__":
    unittest.main()
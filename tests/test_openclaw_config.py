from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class OpenClawConfigTests(unittest.TestCase):
    def test_whatsapp_group_mention_only_and_allowlist_present(self) -> None:
        path = ROOT / "openclaw" / "includes" / "channels.whatsapp.json5"
        text = path.read_text(encoding="utf-8")
        self.assertIn('groupPolicy: "allowlist"', text)
        self.assertIn("GROUP_ID_PLACEHOLDER", text)
        self.assertIn("requireMention: true", text)
        self.assertIn("mentionOnly: true", text)

    def test_tools_retrieval_private_first(self) -> None:
        path = ROOT / "openclaw" / "includes" / "tools.json5"
        text = path.read_text(encoding="utf-8")
        self.assertIn("retrieval", text)
        self.assertIn("privateFirst: true", text)


if __name__ == "__main__":
    unittest.main()

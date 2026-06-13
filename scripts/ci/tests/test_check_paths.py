"""tests for check_paths."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from checkers import check_paths  # noqa: E402


class TestCheckPaths(unittest.TestCase):
    def test_dead_local_link_is_hard(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            (root / ".trae").mkdir(parents=True)
            (root / ".trae" / "README.md").write_text(
                "See [missing](.trae/does-not-exist.md) for details",
                encoding="utf-8",
            )
            result = check_paths.run(root)
            codes = [f["code"] for f in result["hard"]]
            self.assertIn("PATH_DEAD_LINK", codes)

    def test_existing_link_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            (root / ".trae").mkdir(parents=True)
            (root / ".trae" / "README.md").write_text(
                "See [ok](.trae/HOOKS-GUIDE.md) for details",
                encoding="utf-8",
            )
            (root / ".trae" / "HOOKS-GUIDE.md").write_text("# hook", encoding="utf-8")
            result = check_paths.run(root)
            self.assertEqual(result["hard"], [], f"硬失败: {result['hard']}")

    def test_external_link_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            (root / ".trae").mkdir(parents=True)
            (root / ".trae" / "README.md").write_text(
                "External: [g](https://example.com)\n",
                encoding="utf-8",
            )
            result = check_paths.run(root)
            self.assertEqual(result["hard"], [])

    def test_anchor_stripped(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            (root / ".trae").mkdir(parents=True)
            (root / ".trae" / "README.md").write_text(
                "See [section](.trae/HOOKS-GUIDE.md#session-hooks)",
                encoding="utf-8",
            )
            (root / ".trae" / "HOOKS-GUIDE.md").write_text("# hook", encoding="utf-8")
            result = check_paths.run(root)
            self.assertEqual(result["hard"], [])


if __name__ == "__main__":
    unittest.main()

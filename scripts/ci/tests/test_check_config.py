"""tests for check_config."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from checkers import check_config  # noqa: E402


class TestCheckConfig(unittest.TestCase):
    def test_hooks_yaml_invalid_is_hard(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            (root / ".trae").mkdir(parents=True)
            (root / ".trae" / "hooks.yml").write_text("invalid: : :", encoding="utf-8")
            result = check_config.run(root)
            codes = [f["code"] for f in result["hard"]]
            self.assertIn("CONFIG_YAML_INVALID", codes)

    def test_hooks_referencing_missing_path_is_hard(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            (root / ".trae").mkdir(parents=True)
            (root / ".trae" / "hooks.yml").write_text(
                "session:\n  on_start:\n    - target: .trae/missing.md\n",
                encoding="utf-8",
            )
            result = check_config.run(root)
            codes = [f["code"] for f in result["hard"]]
            self.assertIn("CONFIG_PATH_NOT_FOUND", codes)

    def test_preset_without_readme_is_soft(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            preset_dir = root / ".trae" / "presets" / "test"
            preset_dir.mkdir(parents=True)
            (preset_dir / "config.yml").write_text("name: test\n", encoding="utf-8")
            result = check_config.run(root)
            codes = [f["code"] for f in result["soft"]]
            self.assertIn("PRESET_README_MISSING", codes)

    def test_valid_hooks_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            trae = root / ".trae"
            trae.mkdir(parents=True)
            (trae / "rules").mkdir()
            (trae / "rules" / "constitution.md").write_text("# constitution", encoding="utf-8")
            (trae / "hooks.yml").write_text(
                "session:\n  on_start:\n    - target: .trae/rules/constitution.md\n",
                encoding="utf-8",
            )
            result = check_config.run(root)
            self.assertEqual(result["hard"], [], f"硬失败: {result['hard']}")


if __name__ == "__main__":
    unittest.main()

"""tests for check_spec."""
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

# 添加 ci/ 目录到 sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from checkers import check_spec  # noqa: E402


def _setup_spec(root: Path, content: str) -> Path:
    """写入一份规范到 .trae/specs/changes/。"""
    spec_dir = root / ".trae" / "specs" / "changes"
    spec_dir.mkdir(parents=True, exist_ok=True)
    spec = spec_dir / "2026-06-11-test-spec.md"
    spec.write_text(textwrap.dedent(content), encoding="utf-8")
    return spec


class TestCheckSpec(unittest.TestCase):
    def test_no_specs_returns_soft_warning(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            root.mkdir()
            (root / ".trae").mkdir()
            result = check_spec.run(root)
            self.assertEqual(result["hard"], [])
            codes = [f["code"] for f in result["soft"]]
            self.assertIn("SPEC_NONE_FOUND", codes)

    def test_complete_spec_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            _setup_spec(root, """\
                # 测试规范

                ## 用户场景
                - 场景 1

                ## 功能需求
                - FR-001: 应该能 X
                - FR-002: 应该能 Y

                ## 关键实体
                ### Entity1
                - 字段 1

                ## 成功标准
                - [ ] 标准 1

                ## 假设条件
                - 假设 1

                ## 开放问题
                - (无)
            """)
            result = check_spec.run(root)
            self.assertEqual(result["hard"], [], f"硬失败: {result['hard']}")

    def test_missing_fr_section_is_hard(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            _setup_spec(root, """\
                # 规范
                ## 关键实体
                ## 成功标准
            """)
            result = check_spec.run(root)
            codes = [f["code"] for f in result["hard"]]
            self.assertIn("SPEC_MISSING_FR_SECTION", codes)

    def test_missing_fr_id_is_hard(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            _setup_spec(root, """\
                # 规范
                ## 功能需求
                - 无编号的需求
                ## 关键实体
                ## 成功标准
            """)
            result = check_spec.run(root)
            codes = [f["code"] for f in result["hard"]]
            self.assertIn("SPEC_MISSING_FR", codes)

    def test_too_many_clarifications_is_hard(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            _setup_spec(root, """\
                # 规范
                ## 功能需求
                - FR-001: x
                ## 关键实体
                ## 成功标准
                ## 开放问题
                - [NEEDS CLARIFICATION] a
                - [NEEDS CLARIFICATION] b
                - [NEEDS CLARIFICATION] c
                - [NEEDS CLARIFICATION] d
            """)
            result = check_spec.run(root)
            codes = [f["code"] for f in result["hard"]]
            self.assertIn("SPEC_TOO_MANY_CLARIFICATIONS", codes)


if __name__ == "__main__":
    unittest.main()

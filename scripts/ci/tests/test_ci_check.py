"""tests for ci_check main entry.

策略:test_passing_project_exits_zero 用真实项目根 (PROJECT_ROOT = .trae/../..),
而不是临时 mock 最小项目.v4.1 之后,11 个 checker 的硬约束太多,在临时目录模拟
"最小可工作项目"成本爆炸.真实项目根就是 CI 工具的设计目标,测试它"通过"才是真价值.
test_hard_failure / test_no_trae_dir 仍用临时目录(测试 CI 行为本身).
"""
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import ci_check  # noqa: E402

# 真实项目根:SuperTrae-coder/ (scripts/ci/tests/ → ../../..)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


class TestCiCheckMain(unittest.TestCase):
    def test_passing_project_exits_zero(self):
        """真实项目根 (SuperTrae-coder/) 必过 11/11 hard."""
        with mock.patch.object(sys, "argv", ["ci_check", "--root", str(PROJECT_ROOT)]):
            with mock.patch.object(sys, "stdout", new_callable=io.StringIO) as out:
                code = ci_check.main()
                output = out.getvalue()
        self.assertEqual(code, 0, f"输出:\n{output}")

    def test_json_output_schema(self):
        """真实项目根 → JSON 输出符合 trae-ci/v1 schema."""
        with mock.patch.object(sys, "argv", ["ci_check", "--root", str(PROJECT_ROOT), "--json"]):
            with mock.patch.object(sys, "stdout", new_callable=io.StringIO) as out:
                code = ci_check.main()
                data = json.loads(out.getvalue())
        self.assertEqual(data["schema"], "trae-ci/v1")
        self.assertIn("summary", data)
        self.assertIn("results", data)
        self.assertTrue(data["summary"]["passed"])
        self.assertEqual(code, 0)

    def test_hard_failure_exits_one(self):
        """临时项目根 + 死链 → 退出码 1."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            (root / ".trae").mkdir(parents=True)
            (root / ".trae" / "README.md").write_text(
                "broken: [x](.trae/nope.md)", encoding="utf-8"
            )
            with mock.patch.object(sys, "argv", ["ci_check", "--root", str(root), "--checker", "paths"]):
                with mock.patch.object(sys, "stdout", new_callable=io.StringIO):
                    code = ci_check.main()
            self.assertEqual(code, 1)

    def test_no_trae_dir_exits_two(self):
        """临时空项目根 + 无 .trae/ → 退出码 2."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            root.mkdir()
            with mock.patch.object(sys, "argv", ["ci_check", "--root", str(root)]):
                with mock.patch.object(sys, "stderr", new_callable=io.StringIO):
                    code = ci_check.main()
            self.assertEqual(code, 2)

    def test_selective_checker(self):
        """真实项目根 + --checker spec → JSON results 长度 = 1."""
        with mock.patch.object(sys, "argv", ["ci_check", "--root", str(PROJECT_ROOT), "--checker", "spec", "--json"]):
            with mock.patch.object(sys, "stdout", new_callable=io.StringIO) as out:
                ci_check.main()
                data = json.loads(out.getvalue())
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["name"], "spec")


if __name__ == "__main__":
    unittest.main()

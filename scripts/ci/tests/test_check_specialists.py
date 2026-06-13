"""tests for check_specialists (v4.0 重构后版本).

v4.0: specialists/ 目录已删除,check_specialists 改为检查:
1. `.trae/rules/roles.md` 存在
2. `.trae/skills/` 下 11 个关键 skill 存在
3. 文档中 @xxx 引用必须有对应 skill 或 roles.md 中角色名
"""
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from checkers import check_specialists  # noqa: E402

# v4.0 关键 11 skill(与 check_specialists.EXPECTED_SKILLS 保持一致)
CORE_SKILLS = [
    "brainstorming",
    "spec-driven-development",
    "plan-driven-development",
    "tdd-workflow",
    "systematic-debugging",
    "security-review",
    "api-review",
    "verification-before-completion",
    "code-review",
    "cross-artifact-analysis",
    "philosophy-audit",
]

# v4.0 roles.md 8 角色(测试用最小可工作内容)
ROLES_MD_CONTENT = textwrap.dedent("""\
    # 8 角色约束(v4.0)

    | # | 角色 | 职责 |
    |---|------|------|
    | 1 | spec-reviewer | spec 审查 |
    | 2 | plan-reviewer | plan 审查 |
    | 3 | design-reviewer | design 审查 |
    | 4 | code-quality-reviewer | 代码质量 |
    | 5 | test-reviewer | 测试审查 |
    | 6 | api-reviewer | API 审查 |
    | 7 | scope-reviewer | scope 审查 |
    | 8 | cso | 安全 |
    """)


def _setup_project(root: Path, skill_ids: list[str] | None = None) -> None:
    """建立 v4.0 最小可工作项目:roles.md + 11 个 skill."""
    skill_ids = skill_ids or CORE_SKILLS
    # 1. 建 .trae/rules/roles.md(v4.0 角色约束必填)
    roles_dir = root / ".trae" / "rules"
    roles_dir.mkdir(parents=True, exist_ok=True)
    (roles_dir / "roles.md").write_text(ROLES_MD_CONTENT, encoding="utf-8")
    # 2. 建 .trae/skills/<id>/SKILL.md
    for sid in skill_ids:
        skill_dir = root / ".trae" / "skills" / sid
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {sid}\ndescription: test\n---\n# {sid}\n",
            encoding="utf-8",
        )


class TestCheckSpecialists(unittest.TestCase):
    def test_all_core_present_passes(self):
        """v4.0: roles.md + 11 skill 全部存在 → hard=[]"""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            _setup_project(root)
            result = check_specialists.run(root)
            self.assertEqual(result["hard"], [], f"硬失败: {result['hard']}")

    def test_missing_roles_md_is_hard(self):
        """roles.md 缺失 → ROLES_MD_MISSING(hard)"""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            # 不调用 _setup_project → roles.md 不存在
            # 但仍建 skill(否则会被 SKILLS_MISSING 抢先)
            for sid in CORE_SKILLS:
                (root / ".trae" / "skills" / sid).mkdir(parents=True, exist_ok=True)
                (root / ".trae" / "skills" / sid / "SKILL.md").write_text(
                    f"---\nname: {sid}\n---\n", encoding="utf-8"
                )
            result = check_specialists.run(root)
            codes = [f["code"] for f in result["hard"]]
            self.assertIn("ROLES_MD_MISSING", codes)

    def test_missing_skill_is_hard(self):
        """关键 skill 缺失 → SKILLS_MISSING(hard)"""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            # 只建 10 个 skill(缺 1 个)
            _setup_project(root, [s for s in CORE_SKILLS if s != "philosophy-audit"])
            result = check_specialists.run(root)
            codes = [f["code"] for f in result["hard"]]
            self.assertIn("SKILLS_MISSING", codes)
            # 确保缺失的就是 philosophy-audit
            self.assertTrue(
                any("philosophy-audit" in f["message"] for f in result["hard"]),
                f"应提示缺失 philosophy-audit,实际: {result['hard']}",
            )

    def test_dangling_reference_is_hard(self):
        """文档中 @xxx 引用未在 roles.md / skills 中 → REF_REFERENCED_BUT_MISSING(hard)"""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            _setup_project(root)
            # 写一个 README.md 引用不存在的角色
            (root / ".trae" / "README.md").write_text(
                "Use @non-existent-reviewer for help",
                encoding="utf-8",
            )
            result = check_specialists.run(root)
            codes = [f["code"] for f in result["hard"]]
            self.assertIn("REF_REFERENCED_BUT_MISSING", codes)

    def test_role_reference_in_roles_md_is_known(self):
        """roles.md 中声明的 8 角色名被 @ 引用时,不算 dangling"""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "proj"
            _setup_project(root)
            # 引用 roles.md 中已声明的 cso 角色
            (root / ".trae" / "README.md").write_text(
                "Security review by @cso",
                encoding="utf-8",
            )
            result = check_specialists.run(root)
            codes = [f["code"] for f in result["hard"]]
            # cso 在 roles.md 中,不算 dangling
            self.assertNotIn("REF_REFERENCED_BUT_MISSING", codes)


if __name__ == "__main__":
    unittest.main()

"""check_specialists：v4.0 重构为检查角色约束（rules/roles.md）和 skills 加载。

v3.0：检查 `.trae/agents/specialists/` 下至少 7 个 specialist 配置
v4.0：specialists/ 目录已删除，重构为：
- 检查 `.trae/rules/roles.md` 存在（含 8 角色约束）
- 检查核心 11 个 skill 目录存在
- 文档中 @xxx 引用必须有对应 skill 或在已知 prompt 参考中

校验：
- `.trae/rules/roles.md` 存在
- `.trae/skills/` 下关键 11 个 skill 存在
- 文档中 @xxx 引用对应实际文件 / skill
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# v4.0 关键 skill（必须存在）
EXPECTED_SKILLS = {
    "brainstorming",
    "spec-driven-development",
    "plan-driven-development",
    "tdd-workflow",
    "systematic-debugging",
    "security-review",      # v4.0 新增
    "api-review",           # v4.0 新增
    "verification-before-completion",
    "code-review",
    "cross-artifact-analysis",
    "philosophy-audit",
}

# 匹配 Markdown 中的 @xxx 引用
AT_REF_RE = re.compile(r"(?<![\w@/.])@([a-z][a-z0-9]+-[a-z][a-z0-9-]+)(?![\w@/])")


def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []

    # 1. 检查 rules/roles.md 存在
    roles_path = root / ".trae" / "rules" / "roles.md"
    if not roles_path.is_file():
        hard.append({
            "checker": "specialists",
            "level": "hard",
            "code": "ROLES_MD_MISSING",
            "message": ".trae/rules/roles.md 不存在（v4.0 角色约束必填）",
            "file": ".trae/rules/roles.md",
        })
        return {"hard": hard, "soft": soft, "stats": {}}

    # 2. 检查 11 个关键 skill
    skills_dir = root / ".trae" / "skills"
    found_skills: set[str] = set()
    if skills_dir.is_dir():
        for p in skills_dir.iterdir():
            if p.is_dir() and (p / "SKILL.md").exists():
                found_skills.add(p.name)

    missing_skills = EXPECTED_SKILLS - found_skills
    if missing_skills:
        hard.append({
            "checker": "specialists",
            "level": "hard",
            "code": "SKILLS_MISSING",
            "message": f"缺失关键 skill: {', '.join(sorted(missing_skills))}",
            "file": ".trae/skills/",
        })

    # 3. 文档中 @xxx 引用检查
    scan_dirs = [".trae", "docs", "README.md"]
    known_refs = found_skills | {
        "frontend-architect", "backend-architect", "qa-engineer"
    }
    # 🆕 v4.1: 从 roles.md 提取角色名,加入 known_refs
    # roles.md 格式: `| 1 | spec-reviewer | ... |`
    ROLES_NAME_RE = re.compile(r"^\|\s*\d+\s*\|\s*([a-z][a-z0-9-]+)\s*\|", re.MULTILINE)
    if roles_path.is_file():
        roles_text = roles_path.read_text(encoding="utf-8")
        for m in ROLES_NAME_RE.finditer(roles_text):
            known_refs.add(m.group(1))
    referenced: set[str] = set()
    for scan in scan_dirs:
        scan_path = root / scan
        if not scan_path.exists():
            continue
        files = [scan_path] if scan_path.is_file() else list(scan_path.rglob("*.md"))
        for f in files:
            try:
                txt = f.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for m in AT_REF_RE.finditer(txt):
                referenced.add(m.group(1))

    dangling = referenced - known_refs
    for d in sorted(dangling):
        if d in {"param", "ts", "js", "json", "md"}:
            continue
        hard.append({
            "checker": "specialists",
            "level": "hard",
            "code": "REF_REFERENCED_BUT_MISSING",
            "message": f"文档中 @ {d} 被引用但对应 skill / agent 不存在",
            "file": ".trae/skills/ 或 .trae/agents/",
        })

    return {
        "hard": hard,
        "soft": soft,
        "stats": {"skills_found": len(found_skills)},
    }

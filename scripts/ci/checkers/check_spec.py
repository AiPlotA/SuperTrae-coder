"""check_spec：规范结构完整性。

扫描 `.trae/specs/changes/*.md` 与 `docs/superpowers/specs/*-spec.md`，
验证每个规范文件包含必需章节（功能需求/关键实体/成功标准），
并检查 `[NEEDS CLARIFICATION]` 标记数量（≤ 3）。
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# 候选规范位置
SPEC_GLOBS = [
    ".trae/specs/changes/**/*.md",
    "docs/superpowers/specs/*-spec.md",
]

EXCLUDE_DIRS = {"archived", "node_modules", ".git"}

# 跳过非 spec 主文件:plan.md / tasks.md / design.md / proposal.md
SPEC_EXCLUDE_FILES = {"tasks.md", "design.md", "proposal.md", "plan.md"}

# 章节标题（支持中英文，宽松匹配）
SECTION_PATTERNS = {
    "fr": re.compile(r"^##\s+(功能需求|Functional Requirements)\s*$", re.MULTILINE),
    # FR 编号：支持列表项 `- FR-XXX:` / `- **FR-XXX** ...` / 标题 `### FR-XXX:` 三种格式
    "fr_id": re.compile(r"^\s*(?:-\s+(?:\*\*)?|###\s+)FR-\d{3,}", re.MULTILINE),
    "entities": re.compile(r"^##\s+(关键实体|Key Entities)\s*$", re.MULTILINE),
    "success": re.compile(r"^##\s+(成功标准|Success Criteria)(\s*[/、].*)?\s*$", re.MULTILINE),
    "assumptions": re.compile(r"^##\s+(假设条件|Assumptions)\s*$", re.MULTILINE),
    "questions": re.compile(r"^##\s+(开放问题|Open Questions)\s*$", re.MULTILINE),
}

NEEDS_CLARIFY_RE = re.compile(r"\[NEEDS\s+CLARIFICATION\]", re.IGNORECASE)


def _iter_specs(root: Path) -> list[Path]:
    out: list[Path] = []
    for pattern in SPEC_GLOBS:
        # 使用 recursive 匹配 **（**/ 必须配合 recursive=True）
        for p in root.glob(pattern.replace("**", "**")):
            if not p.is_file():
                continue
            if any(part in EXCLUDE_DIRS for part in p.parts):
                continue
            # 跳过 INDEX.md（不是规范文件）
            if p.name == "INDEX.md":
                continue
            # 跳过 tasks.md / design.md / proposal.md / plan.md（不是 spec 主文件）
            if p.name in SPEC_EXCLUDE_FILES:
                continue
            out.append(p)
    return out


def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []

    specs = _iter_specs(root)
    if not specs:
        soft.append({
            "checker": "spec",
            "level": "soft",
            "code": "SPEC_NONE_FOUND",
            "message": f"未发现任何规范文件（搜索: {', '.join(SPEC_GLOBS)}）",
            "file": "",
        })

    for spec in specs:
        text = spec.read_text(encoding="utf-8")
        rel = str(spec.relative_to(root))

        # 功能需求 + FR 编号
        if not SECTION_PATTERNS["fr"].search(text):
            hard.append({
                "checker": "spec",
                "level": "hard",
                "code": "SPEC_MISSING_FR_SECTION",
                "message": "缺少「功能需求 / Functional Requirements」章节",
                "file": rel,
            })
        elif not SECTION_PATTERNS["fr_id"].search(text):
            hard.append({
                "checker": "spec",
                "level": "hard",
                "code": "SPEC_MISSING_FR",
                "message": "「功能需求」章节下无 FR-XXX 编号",
                "file": rel,
            })

        # 关键实体
        if not SECTION_PATTERNS["entities"].search(text):
            hard.append({
                "checker": "spec",
                "level": "hard",
                "code": "SPEC_MISSING_ENTITIES",
                "message": "缺少「关键实体 / Key Entities」章节",
                "file": rel,
            })

        # 成功标准
        if not SECTION_PATTERNS["success"].search(text):
            hard.append({
                "checker": "spec",
                "level": "hard",
                "code": "SPEC_MISSING_SUCCESS",
                "message": "缺少「成功标准 / Success Criteria」章节",
                "file": rel,
            })

        # 假设条件（soft）
        if not SECTION_PATTERNS["assumptions"].search(text):
            soft.append({
                "checker": "spec",
                "level": "soft",
                "code": "SPEC_MISSING_ASSUMPTIONS",
                "message": "缺少「假设条件 / Assumptions」章节（推荐补充）",
                "file": rel,
            })

        # [NEEDS CLARIFICATION] ≤ 3
        nclarify = len(NEEDS_CLARIFY_RE.findall(text))
        if nclarify > 3:
            hard.append({
                "checker": "spec",
                "level": "hard",
                "code": "SPEC_TOO_MANY_CLARIFICATIONS",
                "message": f"[NEEDS CLARIFICATION] 数量 {nclarify} 超过 3 个（硬上限）",
                "file": rel,
            })
        elif nclarify > 0:
            soft.append({
                "checker": "spec",
                "level": "soft",
                "code": "SPEC_HAS_CLARIFICATIONS",
                "message": f"存在 {nclarify} 个 [NEEDS CLARIFICATION] 待澄清项",
                "file": rel,
            })

    return {
        "hard": hard,
        "soft": soft,
        "stats": {"specs_scanned": len(specs)},
    }

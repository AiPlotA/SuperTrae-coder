"""check_skill_writer: v4.1 轮 2 新增 - 检查 skill-writer 元 skill

v4.1 轮 2 FR-003/FR-004: writing-skills 模板
- skill-writer/SKILL.md 必须存在
- 必须含 5 步法章节(用户场景 / FR-XXX / 触发关键词 / 4 部分结构 / CI 检查)
- 必须含 checklist 章节
- 必须含 frontmatter 3 段式(use_when / core_constraint / exit_when)
- 必须引用 1+ 条 ETHOS 哲学
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

META_SKILL_NAME = "skill-writer"
META_SKILL_PATH = f".trae/skills/{META_SKILL_NAME}/SKILL.md"

# 5 步法章节(标题关键字,任一匹配即可)
FIVE_STEP_KEYWORDS = [
    "用户场景",  # 步骤 1
    "FR",        # 步骤 2
    "触发关键词",  # 步骤 3
    "4 部分结构",  # 步骤 4
    "CI 检查",   # 步骤 5
]

ETHOS_PHILOSOPHIES = [
    "Boil the Ocean",
    "Golden Age",
    "Evidence Over Claims",
    "完整实现",
    "不搪塞",
]

SEGMENT_KEYWORDS = ["use_when", "core_constraint", "exit_when"]


def _extract_frontmatter(text: str) -> str:
    fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return fm_match.group(1) if fm_match else ""


def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []
    stats: dict[str, Any] = {}

    meta_md = root / META_SKILL_PATH
    if not meta_md.is_file():
        hard.append({
            "checker": "skill_writer",
            "level": "hard",
            "code": "SKILL_WRITER_MISSING",
            "message": f"元 skill {META_SKILL_PATH} 不存在",
            "file": META_SKILL_PATH,
        })
        stats["exists"] = False
        return {"hard": hard, "soft": soft, "stats": stats}

    stats["exists"] = True
    text = meta_md.read_text(encoding="utf-8")
    fm = _extract_frontmatter(text)

    # 1. 检查 frontmatter 3 段式
    if fm:
        missing_segments = [k for k in SEGMENT_KEYWORDS if k not in fm]
        if missing_segments:
            hard.append({
                "checker": "skill_writer",
                "level": "hard",
                "code": "SKILL_WRITER_NO_3_SEGMENTS",
                "message": f"{META_SKILL_PATH} 缺 3 段式: {', '.join(missing_segments)}",
                "file": META_SKILL_PATH,
            })
    else:
        hard.append({
            "checker": "skill_writer",
            "level": "hard",
            "code": "SKILL_WRITER_NO_FRONTMATTER",
            "message": f"{META_SKILL_PATH} 缺 frontmatter",
            "file": META_SKILL_PATH,
        })

    # 2. 检查 5 步法(关键字匹配)
    missing_steps = [k for k in FIVE_STEP_KEYWORDS if k not in text]
    if missing_steps:
        hard.append({
            "checker": "skill_writer",
            "level": "hard",
            "code": "SKILL_WRITER_5_STEPS",
            "message": f"{META_SKILL_PATH} 缺 5 步法章节: {', '.join(missing_steps)}",
            "file": META_SKILL_PATH,
        })

    # 3. 检查 checklist 章节
    if not re.search(r"^##\s+.*[Cc]hecklist|^##\s+.*清单", text, re.MULTILINE):
        hard.append({
            "checker": "skill_writer",
            "level": "hard",
            "code": "SKILL_WRITER_NO_CHECKLIST",
            "message": f"{META_SKILL_PATH} 缺 checklist 章节",
            "file": META_SKILL_PATH,
        })

    # 4. 检查 ETHOS 哲学引用
    ethos_hits = [p for p in ETHOS_PHILOSOPHIES if p in text]
    if not ethos_hits:
        hard.append({
            "checker": "skill_writer",
            "level": "hard",
            "code": "SKILL_WRITER_NO_ETHOS",
            "message": f"{META_SKILL_PATH} 未引用任何 ETHOS 哲学",
            "file": META_SKILL_PATH,
        })

    # 5. 检查 description 触发条件
    if fm:
        desc_match = re.search(r"^description\s*:\s*(.+?)$", fm, re.MULTILINE)
        if not desc_match:
            hard.append({
                "checker": "skill_writer",
                "level": "hard",
                "code": "SKILL_WRITER_NO_DESCRIPTION",
                "message": f"{META_SKILL_PATH} 缺 frontmatter description",
                "file": META_SKILL_PATH,
            })

    stats["missing_steps"] = missing_steps
    stats["ethos_hits"] = ethos_hits
    return {"hard": hard, "soft": soft, "stats": stats}

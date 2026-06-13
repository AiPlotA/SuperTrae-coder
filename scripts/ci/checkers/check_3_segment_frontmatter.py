"""check_3_segment_frontmatter: v4.1 轮 2 新增 - 检查所有 SKILL.md frontmatter 3 段式

v4.1 轮 2 FR-007: 17 skill frontmatter 3 段式 + ETHOS preamble + description 触发

每个 SKILL.md frontmatter 必须含:
- use_when(何时加载)
- core_constraint(核心约束)
- exit_when(何时退出)

软警告:
- description < 30 字符
- 无"自动加载"/"加载"关键字
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

SEGMENT_KEYWORDS = ["use_when", "core_constraint", "exit_when"]
SKILLS_DIR = Path(".trae/skills")


def _extract_frontmatter(text: str) -> str:
    """抽取 YAML frontmatter,失败返回空字符串。"""
    fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return fm_match.group(1) if fm_match else ""


def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []
    stats: dict[str, Any] = {}

    skills_dir = root / SKILLS_DIR
    if not skills_dir.is_dir():
        hard.append({
            "checker": "3_segment",
            "level": "hard",
            "code": "SKILLS_DIR_MISSING",
            "message": f"{SKILLS_DIR} 目录不存在",
            "file": str(SKILLS_DIR),
        })
        return {"hard": hard, "soft": soft, "stats": stats}

    # 遍历所有 skill 目录
    skill_stats: dict[str, dict[str, Any]] = {}
    skills = sorted([d for d in skills_dir.iterdir() if d.is_dir()])
    if not skills:
        hard.append({
            "checker": "3_segment",
            "level": "hard",
            "code": "NO_SKILLS_FOUND",
            "message": f"{SKILLS_DIR} 下没有任何 skill",
            "file": str(SKILLS_DIR),
        })
        return {"hard": hard, "soft": soft, "stats": stats}

    for skill_dir in skills:
        name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            hard.append({
                "checker": "3_segment",
                "level": "hard",
                "code": "SKILL_MD_MISSING",
                "message": f"skill/{name}/SKILL.md 不存在",
                "file": f".trae/skills/{name}/SKILL.md",
            })
            continue

        text = skill_md.read_text(encoding="utf-8")
        fm = _extract_frontmatter(text)

        if not fm:
            hard.append({
                "checker": "3_segment",
                "level": "hard",
                "code": "NO_FRONTMATTER",
                "message": f"skill/{name}/SKILL.md 缺少 YAML frontmatter",
                "file": f".trae/skills/{name}/SKILL.md",
            })
            continue

        # 检查 3 段式
        missing = [k for k in SEGMENT_KEYWORDS if k not in fm]
        if missing:
            hard.append({
                "checker": "3_segment",
                "level": "hard",
                "code": "3_SEGMENT_MISSING",
                "message": f"skill/{name}/SKILL.md 缺少 3 段式: {', '.join(missing)}",
                "file": f".trae/skills/{name}/SKILL.md",
            })

        # 软警告:description
        desc_match = re.search(r"^description\s*:\s*(.+?)$", fm, re.MULTILINE)
        if desc_match:
            desc = desc_match.group(1).strip()
            if len(desc) < 30:
                soft.append({
                    "checker": "3_segment",
                    "level": "soft",
                    "code": "DESCRIPTION_TOO_SHORT",
                    "message": f"skill/{name}/SKILL.md description 仅 {len(desc)} 字符(建议 ≥30)",
                    "file": f".trae/skills/{name}/SKILL.md",
                })
            if "加载" not in desc and "load" not in desc.lower():
                soft.append({
                    "checker": "3_segment",
                    "level": "soft",
                    "code": "DESCRIPTION_NO_LOAD_KEYWORD",
                    "message": f"skill/{name}/SKILL.md description 缺 '加载' 关键字",
                    "file": f".trae/skills/{name}/SKILL.md",
                })

        skill_stats[name] = {
            "has_3_segments": len(missing) == 0,
            "missing_segments": missing,
        }

    stats["skill_count"] = len(skill_stats)
    stats["skills_with_3_segments"] = sum(1 for s in skill_stats.values() if s["has_3_segments"])
    stats["skill_stats"] = skill_stats
    return {"hard": hard, "soft": soft, "stats": stats}

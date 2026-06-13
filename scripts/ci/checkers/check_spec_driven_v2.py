"""check_spec_driven_v2: v4.1 轮 2 新增 - 验证 4 P1 改进

v4.1 轮 2 阶段 4 FR-009/FR-010/FR-011/FR-012: 4 P1 改进
- P1-1: spec-driven-development 头部含 office-hours 5 问引用
- P1-2: plan-driven-development 头部含 refactor 触发 + plan-eng-review 自动加载
- P1-3: spec-driven-development 必含 brownfield + 4 段(ADDED/MODIFIED/REMOVED/RENAMED)
- P1-4: 全部 skill 含 ETHOS preamble 段(哲学注入)
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

SPEC_DRIVEN_PATH = ".trae/skills/spec-driven-development/SKILL.md"
PLAN_DRIVEN_PATH = ".trae/skills/plan-driven-development/SKILL.md"
SKILLS_DIR = ".trae/skills"

# P1-1: spec-driven-development 必须含 office-hours 5 问引用
P1_1_KEYWORDS = ["office-hours", "目标用户", "痛点", "替代方案", "成功标准", "边界"]

# P1-3: spec-driven-development 必须含 brownfield + 4 段(ADDED/MODIFIED/REMOVED/RENAMED)
P1_3_KEYWORDS = ["brownfield", "ADDED", "MODIFIED", "REMOVED", "RENAMED", "4 段"]

# P1-2: plan-driven-development 必须含 refactor + plan-eng-review
P1_2_KEYWORDS = ["refactor", "重构", "plan-eng-review"]

# P1-4: 全部 skill 必须含 ETHOS preamble(ETHOS 字样)
ETHOS_PREAMBLE_KEY = "> ETHOS:"


def _check_file_keywords(file_path: Path, keywords: list[str], group_code: str) -> tuple[list[str], list[str]]:
    """检查文件含全部关键字。返回(命中列表, 缺失列表)。"""
    if not file_path.is_file():
        return [], keywords
    text = file_path.read_text(encoding="utf-8")
    hits = [k for k in keywords if k in text]
    missing = [k for k in keywords if k not in text]
    return hits, missing


def _check_ethos_preamble(skill_dir: Path) -> tuple[bool, bool]:
    """检查单个 skill 含 ETHOS preamble 段。返回(文件存在, 含 ETHOS 段)。"""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return False, False
    text = skill_md.read_text(encoding="utf-8")
    return True, ETHOS_PREAMBLE_KEY in text


def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []
    stats: dict[str, Any] = {}

    # P1-1: spec-driven-development 头部含 office-hours 5 问
    spec_path = root / SPEC_DRIVEN_PATH
    p1_1_hits, p1_1_missing = _check_file_keywords(spec_path, P1_1_KEYWORDS, "P1_1")
    if p1_1_missing:
        hard.append({
            "checker": "spec_driven_v2",
            "level": "hard",
            "code": "P1_1_OFFICE_HOURS_MISSING",
            "message": f"{SPEC_DRIVEN_PATH} 缺少 office-hours 5 问引用,缺失关键字:{p1_1_missing}",
            "file": SPEC_DRIVEN_PATH,
        })

    # P1-3: spec-driven-development 含 brownfield + 4 段
    p1_3_hits, p1_3_missing = _check_file_keywords(spec_path, P1_3_KEYWORDS, "P1_3")
    if p1_3_missing:
        hard.append({
            "checker": "spec_driven_v2",
            "level": "hard",
            "code": "P1_3_BROWNFIELD_4_SEGMENTS_MISSING",
            "message": f"{SPEC_DRIVEN_PATH} 缺少 brownfield 4 段(ADDED/MODIFIED/REMOVED/RENAMED)说明,缺失关键字:{p1_3_missing}",
            "file": SPEC_DRIVEN_PATH,
        })

    # P1-2: plan-driven-development 含 refactor 触发 + plan-eng-review
    plan_path = root / PLAN_DRIVEN_PATH
    p1_2_hits, p1_2_missing = _check_file_keywords(plan_path, P1_2_KEYWORDS, "P1_2")
    if p1_2_missing:
        hard.append({
            "checker": "spec_driven_v2",
            "level": "hard",
            "code": "P1_2_REFACTOR_TRIGGER_MISSING",
            "message": f"{PLAN_DRIVEN_PATH} 缺少 refactor 触发 + plan-eng-review 自动加载章节,缺失关键字:{p1_2_missing}",
            "file": PLAN_DRIVEN_PATH,
        })

    # P1-4: 全部 skill 含 ETHOS preamble 段
    skills_dir = root / SKILLS_DIR
    skills_missing_ethos: list[str] = []
    skill_stats: dict[str, dict[str, Any]] = {}

    if not skills_dir.is_dir():
        hard.append({
            "checker": "spec_driven_v2",
            "level": "hard",
            "code": "SKILLS_DIR_MISSING",
            "message": f"{SKILLS_DIR} 目录不存在",
            "file": str(SKILLS_DIR),
        })
    else:
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            exists, has_ethos = _check_ethos_preamble(skill_dir)
            skill_stats[skill_dir.name] = {
                "exists": exists,
                "has_ethos_preamble": has_ethos,
            }
            if exists and not has_ethos:
                skills_missing_ethos.append(skill_dir.name)

    if skills_missing_ethos:
        hard.append({
            "checker": "spec_driven_v2",
            "level": "hard",
            "code": "P1_4_ETHOS_PREAMBLE_MISSING",
            "message": f"以下 skill 缺少 ETHOS preamble 段(应含 '> ETHOS:' 引用):{', '.join(skills_missing_ethos)}",
            "file": SKILLS_DIR,
        })

    stats["p1_1_hits"] = p1_1_hits
    stats["p1_1_missing"] = p1_1_missing
    stats["p1_2_hits"] = p1_2_hits
    stats["p1_2_missing"] = p1_2_missing
    stats["p1_3_hits"] = p1_3_hits
    stats["p1_3_missing"] = p1_3_missing
    stats["skill_count"] = len(skill_stats)
    stats["skill_stats"] = skill_stats
    stats["skills_missing_ethos"] = skills_missing_ethos

    return {"hard": hard, "soft": soft, "stats": stats}

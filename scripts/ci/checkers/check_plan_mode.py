"""check_plan_mode: v4.1 新增 - 检查 plan-mode 体系 6 个 skill

v4.1 plan-mode 体系 6 个 skill:
1. office-hours - reframing 模板 + 5 强制问题
2. plan-ceo-review - 5 维度 0-10 评分(愿景/用户/价值/差异化/可执行)
3. plan-design-review - 4 维度 0-10 评分(UX/视觉/交互/可访问性)
4. plan-eng-review - 4 维度 0-10 评分(数据流/模块边界/边界情况/测试策略)
5. plan-devex-review - 4 维度 0-10 评分(TTHW/神奇时刻/摩擦点/用户画像追踪)
6. autoplan - 串联 5 个 review,合并报告

每个 skill 的 4 部分必填:
- description 触发条件(frontmatter description 字段)
- 3+ 强制问题
- 0-10 评分模板
- fix 输出格式

autoplan 还须包含 5 个 review 引用。
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

PLAN_MODE_SKILLS = [
    "office-hours",
    "plan-ceo-review",
    "plan-design-review",
    "plan-eng-review",
    "plan-devex-review",
    "autoplan",
]

# 🆕 v4.1: spec-driven-development 必须串联 office-hours(前置)+ autoplan(后置)
SPEC_CHAIN_TARGET = "spec-driven-development"
SPEC_CHAIN_PREREQ = "office-hours"
SPEC_CHAIN_POSTREQ = "autoplan"

# autoplan 必须引用的 5 个 review skill
AUTOPLAN_REVIEWS = [
    "office-hours",
    "plan-ceo-review",
    "plan-design-review",
    "plan-eng-review",
    "plan-devex-review",
]

# 强制问题标识(支持"问题:"或"问:"两种中文写法,或"Question:"英文)
QUESTION_RE = re.compile(r"(?:问题|问|Question|提问)\s*\d+[：:：]", re.IGNORECASE)
# 评分模板标识(0-10 分 / score: 0-10 / 评分模板)
SCORE_TEMPLATE_RE = re.compile(r"0\s*-\s*10|0-10|评分\s*模板|评分标准", re.IGNORECASE)
# fix 输出格式标识
FIX_OUTPUT_RE = re.compile(r"(?:^|\n)\s*(?:-|##|\*\*)\s*(?:fix|修复|改进|gap)", re.IGNORECASE | re.MULTILINE)


def _check_skill_4_parts(name: str, text: str) -> list[dict[str, Any]]:
    """检查单个 skill 是否含 4 部分。返回 hard failure 列表。"""
    hard: list[dict[str, Any]] = []

    # 1. description 触发条件(frontmatter 的 description 字段)
    desc_match = re.search(r"^description\s*:\s*(.+?)$", text, re.MULTILINE)
    if not desc_match:
        hard.append({
            "checker": "plan_mode",
            "level": "hard",
            "code": "PLAN_MODE_NO_DESCRIPTION",
            "message": f"skill/{name}/SKILL.md 缺少 frontmatter description 触发条件",
            "file": f".trae/skills/{name}/SKILL.md",
        })

    # 2. 3+ 强制问题
    question_count = len(QUESTION_RE.findall(text))
    if question_count < 3:
        hard.append({
            "checker": "plan_mode",
            "level": "hard",
            "code": "PLAN_MODE_QUESTIONS",
            "message": f"skill/{name}/SKILL.md 只含 {question_count} 个强制问题(v4.1 要求 ≥3)",
            "file": f".trae/skills/{name}/SKILL.md",
        })

    # 3. 0-10 评分模板(autoplan 视为评分合并报告,可放宽)
    if name != "autoplan":
        if not SCORE_TEMPLATE_RE.search(text):
            hard.append({
                "checker": "plan_mode",
                "level": "hard",
                "code": "PLAN_MODE_SCORE_TEMPLATE",
                "message": f"skill/{name}/SKILL.md 缺少 0-10 评分模板",
                "file": f".trae/skills/{name}/SKILL.md",
            })

    # 4. fix 输出格式
    if not FIX_OUTPUT_RE.search(text):
        hard.append({
            "checker": "plan_mode",
            "level": "hard",
            "code": "PLAN_MODE_FIX_OUTPUT",
            "message": f"skill/{name}/SKILL.md 缺少 fix 输出格式",
            "file": f".trae/skills/{name}/SKILL.md",
        })

    return hard


def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []
    stats: dict[str, Any] = {}

    skills_dir = root / ".trae" / "skills"
    if not skills_dir.is_dir():
        hard.append({
            "checker": "plan_mode",
            "level": "hard",
            "code": "SKILLS_DIR_MISSING",
            "message": ".trae/skills/ 目录不存在",
            "file": ".trae/skills/",
        })
        return {"hard": hard, "soft": soft, "stats": stats}

    # 检查 6 个 plan-mode skill 是否存在
    missing_skills: list[str] = []
    for name in PLAN_MODE_SKILLS:
        skill_md = skills_dir / name / "SKILL.md"
        if not skill_md.is_file():
            missing_skills.append(name)
    if missing_skills:
        hard.append({
            "checker": "plan_mode",
            "level": "hard",
            "code": "PLAN_MODE_SKILLS_MISSING",
            "message": f"缺失 plan-mode skill: {', '.join(missing_skills)}",
            "file": ".trae/skills/",
        })
        stats["missing_skills"] = missing_skills
        return {"hard": hard, "soft": soft, "stats": stats}

    # 检查每个 skill 的 4 部分
    skill_stats: dict[str, dict[str, Any]] = {}
    for name in PLAN_MODE_SKILLS:
        skill_md = skills_dir / name / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        skill_hard = _check_skill_4_parts(name, text)
        hard.extend(skill_hard)
        skill_stats[name] = {
            "questions": len(QUESTION_RE.findall(text)),
            "has_score_template": bool(SCORE_TEMPLATE_RE.search(text)),
            "has_fix_output": bool(FIX_OUTPUT_RE.search(text)),
        }

    # autoplan 还需引用 5 个 review skill
    autoplan_md = skills_dir / "autoplan" / "SKILL.md"
    if autoplan_md.is_file():
        autoplan_text = autoplan_md.read_text(encoding="utf-8")
        missing_refs: list[str] = []
        for r in AUTOPLAN_REVIEWS:
            if r not in autoplan_text:
                missing_refs.append(r)
        if missing_refs:
            hard.append({
                "checker": "plan_mode",
                "level": "hard",
                "code": "AUTOPLAN_REVIEWS_MISSING",
                "message": f"autoplan/SKILL.md 缺少 5 review 引用: {', '.join(missing_refs)}",
                "file": ".trae/skills/autoplan/SKILL.md",
            })
        skill_stats["autoplan"] = {
            "review_refs": len([r for r in AUTOPLAN_REVIEWS if r in autoplan_text]),
            "missing_refs": missing_refs,
        }

    # 🆕 v4.1: spec-driven-development 必须串联 office-hours(前置)+ autoplan(后置)
    # 前置检查:spec 头部/触发前必须有 office-hours 引用
    # 后置检查:spec 尾部/下游后必须有 autoplan 引用
    spec_chain_md = skills_dir / SPEC_CHAIN_TARGET / "SKILL.md"
    if spec_chain_md.is_file():
        spec_chain_text = spec_chain_md.read_text(encoding="utf-8")
        # 找 office-hours 第一次出现的位置(应在前 1/3,作为前置)
        office_idx = spec_chain_text.find(SPEC_CHAIN_PREREQ)
        # 找 autoplan 第一次出现的位置(应在后 2/3,作为后置)
        autoplan_idx = spec_chain_text.find(SPEC_CHAIN_POSTREQ)
        total_len = len(spec_chain_text)
        spec_chain_issues: list[dict[str, Any]] = []
        if office_idx < 0:
            spec_chain_issues.append({
                "checker": "plan_mode",
                "level": "hard",
                "code": "SPEC_CHAIN_NO_PREREQ",
                "message": f"skill/{SPEC_CHAIN_TARGET}/SKILL.md 缺前置 {SPEC_CHAIN_PREREQ} 引用(v4.1 plan-mode 串联必填)",
                "file": f".trae/skills/{SPEC_CHAIN_TARGET}/SKILL.md",
            })
        else:
            # 前置应在文档前 1/3 出现
            if office_idx > total_len / 3:
                spec_chain_issues.append({
                    "checker": "plan_mode",
                    "level": "soft",
                    "code": "SPEC_CHAIN_PREREQ_NOT_FRONT",
                    "message": f"skill/{SPEC_CHAIN_TARGET}/SKILL.md 的 {SPEC_CHAIN_PREREQ} 引用未在前 1/3(应作为前置步骤)",
                    "file": f".trae/skills/{SPEC_CHAIN_TARGET}/SKILL.md",
                })
        if autoplan_idx < 0:
            spec_chain_issues.append({
                "checker": "plan_mode",
                "level": "hard",
                "code": "SPEC_CHAIN_NO_POSTREQ",
                "message": f"skill/{SPEC_CHAIN_TARGET}/SKILL.md 缺后置 {SPEC_CHAIN_POSTREQ} 引用(v4.1 plan-mode 串联必填)",
                "file": f".trae/skills/{SPEC_CHAIN_TARGET}/SKILL.md",
            })
        else:
            # 后置应在文档后 2/3 出现
            if autoplan_idx < total_len / 3:
                spec_chain_issues.append({
                    "checker": "plan_mode",
                    "level": "soft",
                    "code": "SPEC_CHAIN_POSTREQ_NOT_BACK",
                    "message": f"skill/{SPEC_CHAIN_TARGET}/SKILL.md 的 {SPEC_CHAIN_POSTREQ} 引用未在后 2/3(应作为后置建议)",
                    "file": f".trae/skills/{SPEC_CHAIN_TARGET}/SKILL.md",
                })
        # 按 level 分流
        for issue in spec_chain_issues:
            if issue["level"] == "hard":
                hard.append(issue)
            else:
                soft.append(issue)
        stats["spec_chain"] = {
            "office_hours_pos": office_idx,
            "autoplan_pos": autoplan_idx,
            "total_len": total_len,
        }

    stats["skill_stats"] = skill_stats
    stats["plan_mode_skill_count"] = len(PLAN_MODE_SKILLS)
    return {"hard": hard, "soft": soft, "stats": stats}

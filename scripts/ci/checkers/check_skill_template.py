"""check_skill_template: v4.1 轮 2 新增 - 检查 skill-writer 5 步法每步的 3 要素

v4.1 轮 2 阶段 2: writing-skills 模板
- skill-writer 5 步法每步必须含 3 要素:做什么 / 输出格式 / 反模式
- 这是 check_skill_writer 的"质量"扩展(检查深度而非广度)
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

META_SKILL_NAME = "skill-writer"
META_SKILL_PATH = f".trae/skills/{META_SKILL_NAME}/SKILL.md"

# 5 步法章节名(必须按顺序出现)
STEP_NAMES = [
    "步骤 1",  # 用户场景
    "步骤 2",  # FR-XXX
    "步骤 3",  # 触发关键词
    "步骤 4",  # 4 部分结构
    "步骤 5",  # CI 检查
]

# 每步必含的 3 要素(任一匹配即可,粗略检查)
ELEMENT_KEYWORDS = {
    "做什么": ["做什么", "**做什么**", "**Step"],
    "输出": ["输出", "Output", "**输出**", "```markdown"],
    "反模式": ["反模式", "**反模式**", "❌"],
}


def _extract_step_sections(text: str) -> dict[str, str]:
    """抽取 5 步法每步的内容。返回 {step_name: section_text}。"""
    sections: dict[str, str] = {}
    for i, step in enumerate(STEP_NAMES):
        # 找 "### 步骤 N：" 开头,到下一个 ### 或 ## 为止
        pattern = rf"###\s+{re.escape(step)}[^\n]*\n(.*?)(?=###\s+步骤|\Z)"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            sections[step] = match.group(1)
    return sections


def _check_3_elements(section: str) -> list[str]:
    """检查 section 是否含 3 要素(做什么 / 输出 / 反模式)。返回缺失列表。"""
    missing = []
    for element_name, keywords in ELEMENT_KEYWORDS.items():
        if not any(kw in section for kw in keywords):
            missing.append(element_name)
    return missing


def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []
    stats: dict[str, Any] = {}

    meta_md = root / META_SKILL_PATH
    if not meta_md.is_file():
        # skill-writer 不存在,跳过(由 check_skill_writer 报)
        return {"hard": hard, "soft": soft, "stats": stats}

    text = meta_md.read_text(encoding="utf-8")
    sections = _extract_step_sections(text)

    if not sections:
        hard.append({
            "checker": "skill_template",
            "level": "hard",
            "code": "NO_STEP_SECTIONS",
            "message": f"{META_SKILL_PATH} 未找到任何 5 步法章节",
            "file": META_SKILL_PATH,
        })
        return {"hard": hard, "soft": soft, "stats": stats}

    # 检查每步的 3 要素
    step_stats: dict[str, Any] = {}
    for step in STEP_NAMES:
        if step not in sections:
            hard.append({
                "checker": "skill_template",
                "level": "hard",
                "code": f"STEP_{step[-1]}_MISSING",
                "message": f"{META_SKILL_PATH} 缺 {step} 章节",
                "file": META_SKILL_PATH,
            })
            continue
        missing = _check_3_elements(sections[step])
        if missing:
            hard.append({
                "checker": "skill_template",
                "level": "hard",
                "code": f"STEP_{step[-1]}_NO_3_ELEMENTS",
                "message": f"{META_SKILL_PATH} {step} 缺 3 要素(做什么/输出/反模式): {', '.join(missing)}",
                "file": META_SKILL_PATH,
            })
        step_stats[step] = {
            "missing_elements": missing,
            "has_3_elements": len(missing) == 0,
        }

    stats["step_count"] = len(sections)
    stats["step_stats"] = step_stats
    return {"hard": hard, "soft": soft, "stats": stats}

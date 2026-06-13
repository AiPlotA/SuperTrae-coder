"""check_using_superpowers: v4.1 轮 2 新增 - 检查 using-superpowers 元 skill

v4.1 轮 2 FR-001/FR-002: 元 skill 体系
- using-superpowers/SKILL.md 必须存在
- 必须含 3 段(何时加载 / 核心约束 / 失败时如何退出)
- 必须引用 1+ 条 ETHOS 哲学
- frontmatter 必须有 description 触发条件
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

META_SKILL_NAME = "using-superpowers"
META_SKILL_PATH = f".trae/skills/{META_SKILL_NAME}/SKILL.md"

# 3 段式检查(可粗略匹配:YAML frontmatter 中含 use_when / core_constraint / exit_when 关键字)
SEGMENT_KEYWORDS = ["use_when", "core_constraint", "exit_when"]

# 5 条 ETHOS 哲学(与 check_ethos.py 保持一致)
ETHOS_PHILOSOPHIES = [
    "Boil the Ocean",
    "Golden Age",
    "Evidence Over Claims",
    "完整实现",
    "不搪塞",
]


def _check_3_segments(text: str) -> tuple[int, list[str]]:
    """检查 frontmatter 含 3 段关键字。返回(命中数, 缺失列表)。"""
    # 抽取 YAML frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        return 0, SEGMENT_KEYWORDS
    fm = fm_match.group(1)
    missing = [k for k in SEGMENT_KEYWORDS if k not in fm]
    return len(SEGMENT_KEYWORDS) - len(missing), missing


def _check_ethos_ref(text: str) -> list[str]:
    """检查正文引用 1+ 条 ETHOS 哲学。返回缺失列表(空列表表示 OK)。"""
    missing = [p for p in ETHOS_PHILOSOPHIES if p not in text]
    # 只要命中 1+ 条即可,故 missing 不空但 hits>=1 也算 OK
    hits = [p for p in ETHOS_PHILOSOPHIES if p in text]
    if hits:
        return []
    return missing


def run(root: Path, verbose: bool = False) -> dict:
    hard: list[dict] = []
    soft: list[dict] = []
    stats: dict = {}

    meta_md = root / META_SKILL_PATH
    if not meta_md.is_file():
        hard.append({
            "checker": "using_superpowers",
            "level": "hard",
            "code": "META_SKILL_MISSING",
            "message": f"元 skill {META_SKILL_PATH} 不存在",
            "file": META_SKILL_PATH,
        })
        stats["exists"] = False
        return {"hard": hard, "soft": soft, "stats": stats}

    stats["exists"] = True
    text = meta_md.read_text(encoding="utf-8")

    # 1. 检查 3 段式
    hit_count, missing_segments = _check_3_segments(text)
    if hit_count < 3:
        hard.append({
            "checker": "using_superpowers",
            "level": "hard",
            "code": "META_SKILL_3_SEGMENTS",
            "message": f"{META_SKILL_PATH} 缺少 3 段式(use_when / core_constraint / exit_when),缺失:{missing_segments}",
            "file": META_SKILL_PATH,
        })

    # 2. 检查 ETHOS 哲学引用
    missing_ethos = _check_ethos_ref(text)
    if missing_ethos:
        hard.append({
            "checker": "using_superpowers",
            "level": "hard",
            "code": "META_SKILL_ETHOS",
            "message": f"{META_SKILL_PATH} 未引用任何 ETHOS 哲学(应含 1+ 条:{', '.join(ETHOS_PHILOSOPHIES)})",
            "file": META_SKILL_PATH,
        })

    # 3. 检查 description 触发条件
    desc_match = re.search(r"^description\s*:\s*(.+?)$", text, re.MULTILINE)
    if not desc_match:
        hard.append({
            "checker": "using_superpowers",
            "level": "hard",
            "code": "META_SKILL_NO_DESCRIPTION",
            "message": f"{META_SKILL_PATH} 缺少 frontmatter description 触发条件",
            "file": META_SKILL_PATH,
        })

    stats["hit_segments"] = hit_count
    stats["ethos_hits"] = [p for p in ETHOS_PHILOSOPHIES if p in text]
    return {"hard": hard, "soft": soft, "stats": stats}

"""check_ethos: v4.1 新增 - 检查 ETHOS 哲学注入机制

v4.1 引入 3 个新检查:
1. `.trae/ETHOS.md` 存在(必填) + ≥5 哲学 + 每哲学 ≥2 反模式
2. `rules/core.md` 铁律总数 = 15(ETHOS 注入红线)
3. 11 个核心 skill 头部含 `> ETHOS:` 引用

校验逻辑:
- ETHOS_MD_MISSING  .trae/ETHOS.md 不存在
- ETHOS_PHILOSOPHY_COUNT  < 5 哲学
- ETHOS_ANTIPATTERN_COUNT  任一哲学 < 2 反模式
- CORE_RAILS_COUNT  core.md 铁律 != 15
- SKILL_ETHOS_MISSING  核心 skill 头部缺 `> ETHOS:` 引用
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# v4.1 核心 skill(必须含 ETHOS 引用)
EXPECTED_SKILLS = {
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
}

# v4.1 要求的 5 大哲学(每条必须有 ≥2 反模式)
EXPECTED_PHILOSOPHIES = [
    "Boil the Ocean",
    "Golden Age",
    "Evidence Over Claims",
    "完整实现",
    "不搪塞",
]

# 铁律编号正则(core.md 中格式: `1. **TDD 铁律**:` 或 `9. **零编辑红线**:`)
RAIL_TITLE_RE = re.compile(r"^\s*(\d+)\.\s+\*\*[^:：]+[：:]", re.MULTILINE)
ETHOS_REF_RE = re.compile(r"^>\s*ETHOS\s*[：:]\s*\S+", re.MULTILINE)


def _count_philosophies(text: str) -> tuple[int, list[str]]:
    """统计文本中出现的哲学数量,返回 (命中数, 命中列表)。"""
    hits: list[str] = []
    for p in EXPECTED_PHILOSOPHIES:
        if p in text:
            hits.append(p)
    return len(hits), hits


def _count_antipatterns_per_philosophy(text: str) -> dict[str, int]:
    """对每个哲学,统计其下方的反模式条目(❌ 或 反模式:)。"""
    counts: dict[str, int] = {}
    for p in EXPECTED_PHILOSOPHIES:
        if p not in text:
            counts[p] = 0
            continue
        # 找到该哲学的位置,统计其后到下一个 ## 或文件末尾之间的 ❌ 行数
        idx = text.index(p)
        rest = text[idx:]
        # 截到下一个二级标题
        next_h2 = re.search(r"^##\s+", rest[len(p):], re.MULTILINE)
        section = rest[: len(p) + (next_h2.start() if next_h2 else len(rest))]
        # 反模式标识: ❌ / "反模式:" / "**反模式**"
        antipatterns = len(re.findall(r"❌|^反模式\s*[::]", section, re.MULTILINE))
        counts[p] = antipatterns
    return counts


def _count_rails(core_text: str) -> int:
    """统计 core.md 中铁律编号的最大值。"""
    matches = RAIL_TITLE_RE.findall(core_text)
    if not matches:
        return 0
    return max(int(m) for m in matches)


def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []
    stats: dict[str, Any] = {}

    # 1. 检查 ETHOS.md 存在
    ethos_path = root / ".trae" / "ETHOS.md"
    if not ethos_path.is_file():
        hard.append({
            "checker": "ethos",
            "level": "hard",
            "code": "ETHOS_MD_MISSING",
            "message": ".trae/ETHOS.md 不存在(v4.1 哲学注入必填)",
            "file": ".trae/ETHOS.md",
        })
        return {"hard": hard, "soft": soft, "stats": stats}

    ethos_text = ethos_path.read_text(encoding="utf-8")

    # 2. 检查 ≥5 哲学
    p_count, p_hits = _count_philosophies(ethos_text)
    stats["ethos_philosophies"] = p_hits
    if p_count < 5:
        hard.append({
            "checker": "ethos",
            "level": "hard",
            "code": "ETHOS_PHILOSOPHY_COUNT",
            "message": f".trae/ETHOS.md 只含 {p_count}/5 哲学(缺: {set(EXPECTED_PHILOSOPHIES) - set(p_hits)})",
            "file": ".trae/ETHOS.md",
        })

    # 3. 检查每哲学 ≥2 反模式
    ap_counts = _count_antipatterns_per_philosophy(ethos_text)
    stats["ethos_antipatterns"] = ap_counts
    for p, c in ap_counts.items():
        if c < 2:
            hard.append({
                "checker": "ethos",
                "level": "hard",
                "code": "ETHOS_ANTIPATTERN_COUNT",
                "message": f"哲学「{p}」只含 {c}/2 反模式",
                "file": ".trae/ETHOS.md",
            })

    # 4. 检查 core.md 铁律 = 15
    core_path = root / ".trae" / "rules" / "core.md"
    if not core_path.is_file():
        hard.append({
            "checker": "ethos",
            "level": "hard",
            "code": "CORE_MD_MISSING",
            "message": ".trae/rules/core.md 不存在",
            "file": ".trae/rules/core.md",
        })
    else:
        core_text = core_path.read_text(encoding="utf-8")
        rails = _count_rails(core_text)
        stats["core_rails"] = rails
        if rails != 15:
            hard.append({
                "checker": "ethos",
                "level": "hard",
                "code": "CORE_RAILS_COUNT",
                "message": f"core.md 铁律总数 = {rails},v4.1 要求 = 15(ETHOS 注入红线)",
                "file": ".trae/rules/core.md",
            })

    # 5. 检查 11 个核心 skill 头部含 ETHOS 引用
    skills_dir = root / ".trae" / "skills"
    missing_ref: list[str] = []
    if skills_dir.is_dir():
        for skill_name in EXPECTED_SKILLS:
            skill_md = skills_dir / skill_name / "SKILL.md"
            if not skill_md.is_file():
                missing_ref.append(f"{skill_name}/SKILL.md(文件不存在)")
                continue
            text = skill_md.read_text(encoding="utf-8")
            if not ETHOS_REF_RE.search(text):
                missing_ref.append(f"{skill_name}/SKILL.md(头部缺 > ETHOS: ...)")
    stats["skills_missing_ethos"] = missing_ref
    if missing_ref:
        hard.append({
            "checker": "ethos",
            "level": "hard",
            "code": "SKILL_ETHOS_MISSING",
            "message": f"{len(missing_ref)}/11 skill 缺 ETHOS 引用: {', '.join(missing_ref[:3])}...",
            "file": ".trae/skills/",
        })

    return {"hard": hard, "soft": soft, "stats": stats}

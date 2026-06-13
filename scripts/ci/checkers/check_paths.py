"""check_paths：文档路径完整性。

扫描项目内 `*.md` 文件中 Markdown 链接的本地路径，
验证它们指向真实文件。
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# 匹配 [text](path) 形式（path 不含空白）
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# 排除目录
EXCLUDE_DIRS = {"node_modules", ".git", "archived", "dist", "build"}
EXCLUDE_GLOBS = ("*.lock", "*.min.js")

# 只扫描这些目录（reports/ 是研究材料，含大量外部链接，跳过）
SCAN_DIRS = [".trae", "docs", "README.md"]


def _is_external(url: str) -> bool:
    """判断是否为外部链接（http/https/mailto/锚点）。"""
    return (
        url.startswith(("http://", "https://", "mailto:", "//", "#"))
        or "://" in url
    )


def _is_checkable(url: str) -> bool:
    """判断是否值得检查：本地相对路径或项目内绝对路径。"""
    if _is_external(url):
        return False
    if url.startswith(("./", "../", "/", ".trae/", "docs/", "reports/")):
        return True
    # 不带 ./ 的纯文件名（如 hooks.yml）
    if "/" not in url and "." in url:
        return True
    return False


def _strip_anchor(url: str) -> str:
    """移除 #xxx 锚点。"""
    if "#" in url:
        return url.split("#", 1)[0]
    return url


def _resolve(from_md: Path, url: str, root: Path) -> Path:
    """解析链接 URL 到绝对路径。"""
    url = _strip_anchor(url)
    if url.startswith("/"):
        return (root / url.lstrip("/")).resolve()
    if url.startswith((".trae/", "docs/", "reports/")):
        return (root / url).resolve()
    # 相对路径：相对于 from_md 所在目录
    return (from_md.parent / url).resolve()


def _scan_targets(root: Path) -> list[Path]:
    """返回要扫描的 .md 文件列表。"""
    targets: list[Path] = []
    for scan in SCAN_DIRS:
        scan_path = root / scan
        if not scan_path.exists():
            continue
        if scan_path.is_file():
            targets.append(scan_path)
        else:
            for p in scan_path.rglob("*.md"):
                if any(part in EXCLUDE_DIRS for part in p.parts):
                    continue
                if any(p.match(g) for g in EXCLUDE_GLOBS):
                    continue
                targets.append(p)
    return targets


def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []

    targets = _scan_targets(root)
    total_links = 0
    for md in targets:
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        rel = str(md.relative_to(root))

        for m in MD_LINK_RE.finditer(text):
            url = m.group(2)
            if not _is_checkable(url):
                continue
            total_links += 1
            target = _resolve(md, url, root)
            if not target.exists():
                line_no = text[: m.start()].count("\n") + 1
                hard.append({
                    "checker": "paths",
                    "level": "hard",
                    "code": "PATH_DEAD_LINK",
                    "message": f"链接指向不存在的文件: {url}",
                    "file": rel,
                    "line": line_no,
                })

    return {
        "hard": hard,
        "soft": soft,
        "stats": {"md_files": len(targets), "links_checked": total_links},
    }

"""check_config：配置一致性。

校验：
- `.trae/hooks.yml` YAML 语法 + 引用路径存在
- `.trae/extensions/*/config.yml`（如存在）YAML 语法
- `.trae/presets/*/README.md` 存在性（soft）
- 配置中引用的 skills/agents 文件存在
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _safe_load_yaml(path: Path) -> tuple[dict | None, str | None]:
    """安全加载 YAML。返回 (data, error)。"""
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return (data if isinstance(data, dict) else {}), None
    except yaml.YAMLError as e:
        return None, str(e)
    except OSError as e:
        return None, str(e)


def _check_yaml_syntax(path: Path, rel: str, hard: list[dict[str, Any]]) -> None:
    data, err = _safe_load_yaml(path)
    if err is not None:
        hard.append({
            "checker": "config",
            "level": "hard",
            "code": "CONFIG_YAML_INVALID",
            "message": f"YAML 语法错误: {err.splitlines()[0]}",
            "file": rel,
        })


def _walk_collect_paths(node: Any, path: str = "") -> list[str]:
    """递归收集 YAML 中看起来像文件路径的字符串。

    判定规则：以 ./ 或 .trae/ 或 skills/ 或 agents/ 或 commands/ 开头，
    或含文件扩展名（.md/.sh/.py/.yml/.yaml/.json）。
    """
    out: list[str] = []
    if isinstance(node, dict):
        for k, v in node.items():
            k_str = f"{path}.{k}" if path else str(k)
            out.extend(_walk_collect_paths(v, k_str))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out.extend(_walk_collect_paths(v, f"{path}[{i}]"))
    elif isinstance(node, str):
        s = node.strip()
        if not s or s.startswith("$") or "://" in s:
            return out
        # 跳过含占位符的（{xxx} 或 <xxx>）
        if "{" in s and "}" in s:
            return out
        if "<" in s and ">" in s:
            return out
        # 跳过 home 目录（~）
        if s.startswith("~"):
            return out
        # 跳过 shell glob
        if "*" in s or "?" in s:
            return out
        if s.startswith(("./", "/", ".trae/", "skills/", "agents/", "commands/", "rules/", "presets/", "extensions/")):
            out.append(s)
        elif any(s.endswith(ext) for ext in (".md", ".sh", ".py", ".yml", ".yaml", ".json")):
            out.append(s)
    return out


def _check_hooks(root: Path, hard: list[dict[str, Any]], soft: list[dict[str, Any]]) -> None:
    hooks_path = root / ".trae" / "hooks.yml"
    rel = str(hooks_path.relative_to(root))
    if not hooks_path.exists():
        return  # 可选文件

    data, err = _safe_load_yaml(hooks_path)
    if err is not None:
        hard.append({
            "checker": "config",
            "level": "hard",
            "code": "CONFIG_YAML_INVALID",
            "message": f"YAML 语法错误: {err.splitlines()[0]}",
            "file": rel,
        })
        return

    if not isinstance(data, dict):
        return

    # 收集所有可能引用路径
    paths = _walk_collect_paths(data)
    for p in paths:
        # 跳过带变量
        if p.startswith("$") or "${" in p:
            continue
        # 解析为相对路径
        candidate = (root / p).resolve()
        # 还要尝试相对于 .trae
        candidate_trae = (root / ".trae" / p).resolve()
        if not (candidate.exists() or candidate_trae.exists()):
            # 裸文件名（无路径分隔符）→ soft warn（可能是可选依赖）
            if "/" not in p and "\\" not in p:
                soft.append({
                    "checker": "config",
                    "level": "soft",
                    "code": "CONFIG_OPTIONAL_PATH_MISSING",
                    "message": f"可选引用不存在: {p}",
                    "file": rel,
                })
            else:
                hard.append({
                    "checker": "config",
                    "level": "hard",
                    "code": "CONFIG_PATH_NOT_FOUND",
                    "message": f"引用路径不存在: {p}",
                    "file": rel,
                })


def _check_presets(root: Path, hard: list[dict[str, Any]], soft: list[dict[str, Any]]) -> None:
    presets_dir = root / ".trae" / "presets"
    if not presets_dir.is_dir():
        return
    for preset in sorted(presets_dir.iterdir()):
        if not preset.is_dir():
            continue
        rel = str(preset.relative_to(root))
        readme = preset / "README.md"
        if not readme.exists():
            soft.append({
                "checker": "config",
                "level": "soft",
                "code": "PRESET_README_MISSING",
                "message": f"Preset 缺少 README.md",
                "file": rel,
            })


def _check_extensions(root: Path, hard: list[dict[str, Any]], soft: list[dict[str, Any]]) -> None:
    ext_dir = root / ".trae" / "extensions"
    if not ext_dir.is_dir():
        return
    for ext in sorted(ext_dir.rglob("config.yml")):
        rel = str(ext.relative_to(root))
        data, err = _safe_load_yaml(ext)
        if err is not None:
            hard.append({
                "checker": "config",
                "level": "hard",
                "code": "CONFIG_YAML_INVALID",
                "message": f"YAML 语法错误: {err.splitlines()[0]}",
                "file": rel,
            })
            continue
        if isinstance(data, dict) and "version" not in data:
            soft.append({
                "checker": "config",
                "level": "soft",
                "code": "EXTENSION_VERSION_MISSING",
                "message": "config.yml 缺少 version 字段",
                "file": rel,
            })


def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []

    _check_hooks(root, hard, soft)
    _check_presets(root, hard, soft)
    _check_extensions(root, hard, soft)

    return {
        "hard": hard,
        "soft": soft,
        "stats": {},
    }

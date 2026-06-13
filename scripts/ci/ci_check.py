#!/usr/bin/env python3
"""
TRAE CI 验证主入口。

聚合 4 个 checker 的结果，区分 hard/soft 失败，输出彩色报告或 JSON。

用法：
    python3 ci_check.py                  # 跑所有 checker
    python3 ci_check.py --checker spec   # 跑单个 checker
    python3 ci_check.py --json           # 输出 JSON
    python3 ci_check.py --verbose        # 详细输出
    python3 ci_check.py --root /path     # 指定项目根

退出码：
    0 = 所有 hard 通过
    1 = 存在 hard 失败
    2 = 执行错误
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

# 允许从 ci_check.py 导入 sibling modules
sys.path.insert(0, str(Path(__file__).resolve().parent))

from checkers import check_spec, check_config, check_paths, check_specialists, check_ethos, check_plan_mode, check_using_superpowers, check_3_segment_frontmatter, check_skill_writer, check_skill_template, check_spec_driven_v2  # noqa: E402

CHECKER_REGISTRY = {
    "spec": check_spec,
    "config": check_config,
    "paths": check_paths,
    "specialists": check_specialists,
    "ethos": check_ethos,
    "plan_mode": check_plan_mode,
    "using_superpowers": check_using_superpowers,
    "3_segment": check_3_segment_frontmatter,
    "skill_writer": check_skill_writer,
    "skill_template": check_skill_template,  # v4.1 轮 2 阶段 2 新增
    "spec_driven_v2": check_spec_driven_v2,  # v4.1 轮 2 阶段 4 新增(4 P1 改进验证)
}


@dataclass
class Finding:
    checker: str
    level: str  # "hard" | "soft"
    code: str
    message: str
    file: str = ""
    line: int | None = None


@dataclass
class CheckResult:
    name: str
    passed: bool
    hard_failures: list[Finding] = field(default_factory=list)
    soft_warnings: list[Finding] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)
    duration_s: float = 0.0


def is_tty() -> bool:
    return sys.stdout.isatty()


# ANSI 颜色
class C:
    RED = "\033[0;31m" if is_tty() else ""
    YELLOW = "\033[0;33m" if is_tty() else ""
    GREEN = "\033[0;32m" if is_tty() else ""
    BOLD = "\033[1m" if is_tty() else ""
    DIM = "\033[2m" if is_tty() else ""
    NC = "\033[0m" if is_tty() else ""


def run_checker(name: str, root: Path, verbose: bool) -> CheckResult:
    """运行单个 checker 并返回结果。"""
    if name not in CHECKER_REGISTRY:
        return CheckResult(
            name=name,
            passed=False,
            hard_failures=[Finding(name, "hard", "UNKNOWN_CHECKER", f"未知 checker: {name}")],
        )

    module = CHECKER_REGISTRY[name]
    started = time.perf_counter()
    try:
        raw = module.run(root, verbose=verbose)
    except Exception as e:  # noqa: BLE001
        return CheckResult(
            name=name,
            passed=False,
            hard_failures=[Finding(name, "hard", "CHECKER_EXCEPTION", f"执行异常: {e}")],
            duration_s=time.perf_counter() - started,
        )

    duration = time.perf_counter() - started

    hard = [Finding(**f) for f in raw.get("hard", [])]
    soft = [Finding(**f) for f in raw.get("soft", [])]
    return CheckResult(
        name=name,
        passed=len(hard) == 0,
        hard_failures=hard,
        soft_warnings=soft,
        stats=raw.get("stats", {}),
        duration_s=duration,
    )


def print_text(results: list[CheckResult], verbose: bool) -> None:
    """打印人类可读报告。"""
    print(f"{C.BOLD}TRAE CI 验证报告{C.NC}")
    print(f"{C.DIM}{'─' * 60}{C.NC}")

    total_hard = 0
    total_soft = 0

    for r in results:
        total_hard += len(r.hard_failures)
        total_soft += len(r.soft_warnings)

        status = f"{C.GREEN}✓{C.NC}" if r.passed else f"{C.RED}✗{C.NC}"
        stats_summary = ""
        if r.stats:
            stats_summary = " " + C.DIM + json.dumps(r.stats, ensure_ascii=False) + C.NC
        duration = C.DIM + f" ({r.duration_s:.2f}s)" + C.NC
        print(f"{status} {C.BOLD}{r.name}{C.NC}{stats_summary}{duration}")

        for f in r.hard_failures:
            loc = f"{f.file}" + (f":{f.line}" if f.line else "")
            print(f"  {C.RED}[hard]{C.NC} {f.code:<28} {C.DIM}{loc}{C.NC}  {f.message}")

        if verbose:
            for f in r.soft_warnings:
                loc = f"{f.file}" + (f":{f.line}" if f.line else "")
                print(f"  {C.YELLOW}[soft]{C.NC} {f.code:<28} {C.DIM}{loc}{C.NC}  {f.message}")

    if not verbose and total_soft:
        print(f"\n{C.DIM}(使用 --verbose 查看 {total_soft} 条 soft 警告){C.NC}")

    print(f"{C.DIM}{'─' * 60}{C.NC}")
    if total_hard:
        print(f"{C.RED}✗{C.NC} {C.BOLD}{total_hard} hard 失败{C.NC}" + (f", {total_soft} soft 警告" if total_soft else ""))
    else:
        msg = f"{C.GREEN}✓{C.NC} {C.BOLD}全部 hard 通过{C.NC}"
        if total_soft:
            msg += f"，{total_soft} soft 警告"
        print(msg)


def print_json(results: list[CheckResult]) -> None:
    """打印 JSON 报告（供 CI 平台解析）。"""
    payload = {
        "schema": "trae-ci/v1",
        "summary": {
            "total_hard": sum(len(r.hard_failures) for r in results),
            "total_soft": sum(len(r.soft_warnings) for r in results),
            "passed": all(r.passed for r in results),
        },
        "results": [
            {
                "name": r.name,
                "passed": r.passed,
                "duration_s": round(r.duration_s, 3),
                "stats": r.stats,
                "hard": [asdict(f) for f in r.hard_failures],
                "soft": [asdict(f) for f in r.soft_warnings],
            }
            for r in results
        ],
    }
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="TRAE CI 验证入口")
    parser.add_argument("--checker", "-c", action="append", choices=list(CHECKER_REGISTRY),
                        help="只跑指定 checker（可多次指定）")
    parser.add_argument("--json", dest="as_json", action="store_true", help="输出 JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出（显示 soft 警告）")
    parser.add_argument("--root", default=os.getcwd(), help="项目根目录")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not (root / ".trae").is_dir():
        print(f"{C.RED}✗{C.NC} 项目根未发现 .trae 目录: {root}", file=sys.stderr)
        return 2

    selected = args.checker or list(CHECKER_REGISTRY)
    results: list[CheckResult] = []
    for name in selected:
        results.append(run_checker(name, root, args.verbose))

    if args.as_json:
        print_json(results)
    else:
        print_text(results, args.verbose)

    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())

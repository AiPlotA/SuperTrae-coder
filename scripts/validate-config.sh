#!/usr/bin/env bash
# TRAE 人类 CI 验证入口脚本（Human CI Tool）
#
# 用法：
#   scripts/validate-config.sh                # 跑所有 checker
#   scripts/validate-config.sh --checker spec # 跑单个 checker
#   scripts/validate-config.sh --json          # 输出 JSON
#   scripts/validate-config.sh --verbose       # 详细输出
#
# 退出码：
#   0 = 所有 hard 通过
#   1 = 存在 hard 失败
#   2 = 执行错误
#
# 定位：人类可执行 CI（不是 SOLO Agent 自动调用）
# 用途：PR 提交前 / 合并后人工跑一次,确保 11 个硬约束都过
# 依赖：python3 >= 3.10,PyYAML

set -euo pipefail

# 计算项目根目录（脚本位于 scripts/validate-config.sh）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CI_DIR="$SCRIPT_DIR/ci"
MAIN_PY="$CI_DIR/ci_check.py"

# 颜色（仅在 TTY 输出时启用）
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    YELLOW='\033[0;33m'
    GREEN='\033[0;32m'
    NC='\033[0m'
else
    RED=''; YELLOW=''; GREEN=''; NC=''
fi

# 依赖检查
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RED}✗${NC} python3 未安装" >&2
    exit 2
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 10 ]]; }; then
    echo -e "${RED}✗${NC} Python >= 3.10 required (found $PY_VERSION)" >&2
    exit 2
fi

if ! python3 -c "import yaml" 2>/dev/null; then
    echo -e "${RED}✗${NC} PyYAML 未安装（pip install pyyaml）" >&2
    exit 2
fi

# 进入项目根
cd "$PROJECT_ROOT"

# 委托给 Python
exec python3 "$MAIN_PY" "$@"

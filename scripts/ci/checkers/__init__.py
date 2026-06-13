"""TRAE CI checkers.

每个 checker 模块必须实现：

    def run(root: Path, verbose: bool = False) -> dict:
        返回 {
            "hard": [{"checker", "level", "code", "message", "file", "line"}],
            "soft": [...],
            "stats": {...},
        }
"""

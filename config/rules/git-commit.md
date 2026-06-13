---
scene: git_message
---

# Git 提交信息规范（TRAE 专用）

## 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

## type 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat(auth): add OAuth2 login |
| fix | 修复 Bug | fix(api): handle 404 on user endpoint |
| docs | 文档变更 | docs(readme): update quick start |
| style | 代码格式（不影响逻辑）| style: fix eslint warnings |
| refactor | 重构（既非 feat 也非 fix）| refactor(db): extract query builder |
| test | 测试相关 | test(auth): add login integration tests |
| chore | 构建/工具变更 | chore(deps): bump pyyaml to 6.0 |

## 规则

- subject 必填，**≤ 72 字符**
- subject 用现在时祈使句（"add" 而非 "added"）
- subject 首字母**小写**（除非专有名词）
- body 可选，**每行 ≤ 72 字符**
- body 解释 **why**，不解释 what
- footer 可选（如 `Refs: #123`、`BREAKING CHANGE: ...`）

## 示例

```
feat(spec-driven): add Delta Spec 4-stage template

Introduce ADDED/MODIFIED/REMOVED/RENAMED sections for
upstream compatibility with OpenSpec schema. Enable
brownfield project change management.

Refs: ADR-001
```

## 反模式

- ❌ "修复了一些 bug"（无 type、无 scope）
- ❌ "feat: add new feature"（subject 太泛）
- ❌ "WIP"（应使用 chore + draft 标识）
- ❌ 一次 commit 多个无关变更（应拆分为多个 commit）

---

*基于工程哲学 v1 制定 + TRAE scene: git_message 字段*
*版本：v3.0*

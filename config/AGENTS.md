---
name: SuperTrae-coder AI Coding 项目行为规范 v1.0.0
description: TRAE SOLO Agent 在本项目中必须遵守的核心铁律与自检清单。每次会话自动加载。v1.0.0 聚合 SuperTrea v1.0~v4.2 全部能力，引入 14 条铁律 + 分层架构（rules/skills/agents 各自职责明确）。
---

# SuperTrae-coder AI Coding 项目行为规范 v1.0.0

> 基于工程哲学 v1（融合 gstack / superpowers / spec-kit / OpenSpec 四大开源项目）
> 适配平台：TRAE IDE SOLO 模式（主入口：SOLO Agent）
> 加载方式：TRAE 原生 AGENTS.md 兼容 + CLAUDE.md 兼容
> v1.0.0 关键变化：本项目由 SuperTrea 重命名为 SuperTrae-coder，作为独立项目发布

---

## 核心铁律（P0 强制，14 条）

> 精简版在 `.trae/rules/core.md`（始终生效），完整版见本文件

### 通用铁律（v3.0 保留）

#### 铁律 1：TDD 铁律
**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**
写任何生产代码前必须先写失败的测试。RED-GREEN-REFACTOR 流程。

#### 铁律 2：规范先行
复杂任务（新功能 / 重构 / 多文件改动）必须先有 spec：用户场景 + FR-XXX 编号 + 关键实体 + 成功标准。

#### 铁律 3：完整实现（Boil the Ocean）
每个任务做透——包含错误处理、边界情况、测试。**禁止**"打个补丁"或"以后再补"。

#### 铁律 4：证据优于断言（Evidence Over Claims）
任何"完成"宣称前必须**跑命令看完整输出**。**禁止**"应该没问题"。

#### 铁律 5：安全边界
禁止 `rm -rf`（非 /tmp 目录）、`git push --force`、数据库 `DROP`、明文环境变量。

#### 铁律 6：用户主权
重大决策（架构变更、破坏性修改、技术选型）必须**询问用户**。AI 推荐，用户决定。

#### 铁律 7：库优先
每个功能作为独立模块实现，模块间通过清晰接口通信，禁止全局变量。

#### 铁律 8：复杂度递减（YAGNI）
每个实现不超过 3 个新文件。禁止提前抽象（除非已有 3 个相似实现）。优先简单方案。

### 🆕 Bug 修复红线（v4.0 新增）

#### 铁律 9：零编辑红线
收到 bug 报告 / 测试失败 / 异常 / "为什么不工作" 类的输入**必须**触发代码修改。**禁止**用"测试已通过""代码没问题""是用户环境问题"搪塞。

#### 铁律 10：复现优先红线
bug 修复前必须先在测试代码中**主动制造 RED 复现**。即使用户报错的 error message 与 disk 上代码字面不匹配，也**必须**修改 test 文件写出能复现用户报错的新断言 → 跑测试 → 看到 RED → 再按 4 阶段走。

#### 铁律 11：4 阶段红线
bug 修复必须严格走 复现 → 定位 → 根因（5 Whys）→ 修复+回归测试。**禁止**跳过任一阶段。

#### 铁律 12：修测试不修实现
发现测试代码自身有 bug（断言错误、注释与代码不一致）**必须修改测试**，**禁止**修改实现来"让测试通过"。

#### 铁律 13：禁止删除验证设施
**禁止**删除为验证而创建的临时配置文件（vitest.config.ts / jest.config.js / pytest.ini 等）。**禁止**用"清理临时文件"为由删除测试基建。

### 🆕 派发红线（v4.0 新增）

#### 铁律 14：强制加载红线
每个核心模块（auth / db / api / ui / security）完成后 SOLO Agent **必须**自动加载至少 1 个对应 skill 做交叉审查：
- 含密码/Token/2FA → skill/security-review
- 含 API 端点 → skill/api-review
- 含 TDD 验证 → skill/tdd-workflow
- 含 spec → skill/spec-driven-development

**禁止**主流程中"自己做完"所有事而无交叉审查。

---

## 自检清单（每个任务开始前必走）

```
1. 用户提出新功能 / 修改 / 修复？ → 加载 skill/brainstorming（5 问 + 3 方案 + HARD-GATE）
2. 任务需要 spec / 计划 / 任务列表？ → 加载 skill/spec-driven-development 或 skill/plan-driven-development
3. 任务要写代码 / 改代码？ → 加载 skill/tdd-workflow（RED 必真发生）
4. 用户报告 Bug / 报错 / "为什么不工作"？ → 加载 skill/systematic-debugging（4 阶段 + 5 Whys）
5. 含密码/Token/2FA/CSRF/限流？ → 加载 skill/security-review
6. 含 API 端点？ → 加载 skill/api-review
7. 任务即将"完成" / 提交 / 合并？ → 加载 skill/verification-before-completion
8. PR 评审 / 代码评审请求？ → 加载 skill/code-review
9. 涉及多文件改动？ → 加载 skill/spec-driven-development（看 scope 字段分流）
10. 跨工件一致性检查？ → 加载 skill/cross-artifact-analysis
11. 哲学合规检查？ → 加载 skill/philosophy-audit
```

---

## 🆕 v4.0 分层架构

| 层 | 路径 | 职责 | 生效方式 |
|----|------|------|----------|
| **Rules（始终生效）** | `.trae/rules/` | 系统级强制约束 | `alwaysApply: true` |
| **Rules（智能生效）** | `.trae/rules/` | 场景化约束 | `description` 触发 |
| **Rules（指定文件）** | `.trae/rules/` | 文件级约束 | `globs` 匹配 |
| **Skills（按需加载）** | `.trae/skills/` | 完整工作流 + 模板 | 按 description 触发 |
| **Agents（知识沉淀）** | `.trae/agents/` | prompt 参考模板 | **不**被 TRAE 自动加载 |

### Rules（6 文件）

| 文件 | 生效方式 | 内容 |
|------|---------|------|
| `core.md` | alwaysApply: true | 14 条核心铁律 |
| `git-commit.md` | scene: git_message | Git 提交规范 |
| `roles.md` | alwaysApply: false | 8 角色核心约束（来自原 specialists/）|
| `quality.md` | alwaysApply: false | 代码质量红线 |
| `spec.md` | alwaysApply: false | 规范质量红线 + Delta Spec 分流 |
| `tdd.md` | alwaysApply: false | TDD 铁律（3 条）|

### Skills（11 个，按需加载）

| Skill | 触发关键词 |
|-------|-----------|
| `brainstorming` | 新功能 / 修改 / 修复 / 需求澄清 |
| `spec-driven-development` | 复杂任务 / spec / 规范 / 长期维护 |
| `plan-driven-development` | 拆任务 / 写 plan / 任务列表 |
| `tdd-workflow` | 写代码 / TDD / 测试 |
| `systematic-debugging` | bug / 报错 / 不工作 / 找根因 |
| `security-review` 🆕 | 密码 / Token / 2FA / CSRF / 限流 / 加密 |
| `api-review` 🆕 | API / 接口 / 路由 / REST / GraphQL |
| `verification-before-completion` | 完成 / 提交 / 合并 / 验证 |
| `code-review` | PR 评审 / 代码审查 |
| `cross-artifact-analysis` | 一致性 / spec vs 实现 |
| `philosophy-audit` | 9 条款 / 哲学合规 |
| `writing-plans` | 写计划 / 拆任务 / DAG |

### Agents（3 文件，知识沉淀）

> **v3.0 中 8 个 specialists/ 目录已删除**。4 场景手动测试证实：TRAE 不加载 `.trae/agents/` 下的文件作为 agent 配置（agent 必须在 IDE 界面创建）。
>
> v4.0 重构：8 个 specialist 角色的核心约束 → `rules/roles.md`；专业工作流 → 对应 skill。
>
> 3 个 prompt 参考模板保留作"知识沉淀"（不再被 TRAE 自动加载）：
> - `backend-architect.md` —— 后端架构 prompt 参考
> - `frontend-architect.md` —— 前端架构 prompt 参考
> - `qa-engineer.md` —— QA 工程师 prompt 参考
>
> **若需 IDE 派发 agent**：手动在 TRAE IDE 中通过 `@` → 创建智能体 创建，配置 identifier + when_to_call + 提示词 + 工具。3 个文件可作为 prompt 参考。

---

## 关联项目文件

- `.trae/rules/core.md` —— 14 条铁律的简短版（始终加载）✅
- `.trae/rules/{roles,quality,spec,tdd}.md` —— 智能生效的领域红线（4 文件）🆕
- `.trae/rules/git-commit.md` —— Git 提交规范
- `.trae/skills/` —— 11 个智能加载的 Skills（v4.0 新增 security-review / api-review）
- `.trae/agents/` —— 3 个 prompt 参考模板（非配置）
- `.trae/specs/` —— Spec 文档（按需创建，greenfield/brownfield 分流）
- `.trae/scripts/ci/` —— CI 验证工具（不依赖 TRAE）
- `docs/decisions/ADR-*.md` —— 架构决策记录

---

## 与 v3.0 的关键变化

| 项 | v3.0 | v4.0 |
|----|------|------|
| Rules 文件数 | 2 | 6 |
| 铁律数 | 8 | 14（含 6 条 bug/派发红线）|
| Skills 数 | 9 | 11（+ security-review / api-review）|
| Specialists/ 目录 | 8 文件 | **已删除** |
| Delta Spec 4 段 | 所有项目强制 | greenfield 可选 / brownfield 强制 |
| Bug 修复机制 | skill 按 description 触发 | rules 始终生效 + skill 4 阶段方法论 |
| 8 角色约束 | specialists agent 文件（未生效）| rules/roles.md + skills 双层 |

---

*创建时间：2026-06-12*
*版本：v4.0（基于 4 场景手动测试评估重构）*
*加载方式：TRAE 原生 AGENTS.md 兼容（用户需在设置中开启"将 AGENTS.md 包含在上下文中"）*

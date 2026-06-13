---
name: 核心铁律 v4.0（始终生效）
description: 14 条核心铁律的精简版，始终加载。基于 v3.0 8 条铁律 + 4 场景手动测试反馈新增 6 条 bug 修复与质量红线。
alwaysApply: true
---

# 核心铁律 v4.0（始终生效）

> 精简版铁律，完整版见根目录 `AGENTS.md`
> 14 条铁律 = v3.0 8 条（保留） + v4.0 6 条（新增 bug/质量/派发红线）

## 必守铁律

### 通用铁律（v3.0 保留）

1. **TDD 铁律**：NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
2. **规范先行**：复杂任务先 spec（用户场景 + FR-XXX + 关键实体 + 成功标准）
3. **完整实现**：每个任务做透，禁止"以后再补"
4. **证据优于断言**：完成前跑命令看输出，禁止"应该没问题"
5. **安全边界**：禁止 rm -rf（/tmp 除外）、git push --force、DROP TABLE
6. **用户主权**：重大决策必须询问用户
7. **库优先**：功能作为独立模块，模块间清晰接口
8. **复杂度递减**：YAGNI，最多 3 个新文件

### 🆕 Bug 修复红线（v4.0 新增）

9. **零编辑红线**：收到 bug 报告 / 测试失败 / 异常 / "为什么不工作" 类的输入
   **必须**触发代码修改。**禁止**用"测试已通过""代码没问题""是用户环境问题"搪塞。
   唯一允许的 zero-edit 回复：经 HARD-GATE 与用户确认后明确放弃。

10. **复现优先红线**：bug 修复前必须先在测试代码中**主动制造 RED 复现**。
    即使用户报错的 error message 与 disk 上代码字面不匹配，也**必须**：
    - 修改 test 文件写出能复现用户报错的新断言
    - 跑测试看到 RED
    - 再按 systematic-debugging 4 阶段走
    **禁止**仅在 thinking 里"推断根因"而不动手。

11. **4 阶段红线**：bug 修复必须严格走 复现 → 定位 → 根因（5 Whys）→ 修复+回归测试。
    **禁止**跳过任一阶段。即便是"看一眼就知道"的 bug，也必须用 skill/systematic-debugging 走流程。

12. **修测试不修实现**：发现测试代码自身有 bug（断言错误、注释与代码不一致），
    **必须修改测试**，**禁止**修改实现来"让测试通过"。
    例：测试断言写错边界值 → 改测试；实现真的是对的 → 保留实现。

13. **禁止删除验证设施**：禁止删除为验证而创建的临时配置文件（vitest.config.ts、
    jest.config.js、pytest.ini 等）。**禁止**用"清理临时文件"为由删除测试基建。
    若临时配置确实不再需要，应**转为正式配置**而非删除。

### 🆕 派发红线（v4.0 新增）

14. **强制加载红线**：每个核心模块（auth / db / api / ui / security）完成后
    SOLO Agent **必须**自动加载至少 1 个对应 skill 做交叉审查：
    - 含密码/Token/2FA → skill/security-review
    - 含 API 端点 → skill/api-review
    - 含 TDD 验证 → skill/tdd-workflow
    - 含 spec → skill/spec-driven-development（含 spec-reviewer checklist）
    **禁止**主流程中"自己做完"所有事而无交叉审查。

### 🆕 哲学注入红线（v4.1 新增）

15. **ETHOS 注入红线**：每个 skill 在加载时**必须**自动 prepend `.trae/ETHOS.md` 中
    与本 skill 相关的 1-2 条哲学到 preamble（Boil the Ocean / Golden Age /
    Evidence Over Claims / 完整实现 / 不搪塞）。
    - 写代码类 skill（tdd-workflow / security-review / api-review）→ Boil the Ocean + Evidence Over Claims
    - 调试类 skill（systematic-debugging）→ 不搪塞 + Evidence Over Claims
    - 设计/规划类 skill（brainstorming / spec-driven-development / plan-driven-development）→ Golden Age + 完整实现
    - 验证类 skill（verification-before-completion / code-review）→ Evidence Over Claims + Boil the Ocean
    - 哲学类 skill（philosophy-audit / cross-artifact-analysis）→ 完整实现 + 不搪塞
    **禁止**加载 skill 时"裸跑"而无 ETHOS preamble。
    CI 检查：`bash .trae/scripts/ci-check.sh --checker ethos`

---

## 自检清单（每个任务开始前必走）

- 新功能 / 改？→ 加载 `brainstorming` skill（5 问 + 3 方案 + HARD-GATE）
- 重构？→ 加载 `brainstorming` skill（含 YAGNI 拆分粒度 3 问）
- 写代码？→ 加载 `tdd-workflow` skill（RED 必真发生）
- 报错 / 不工作 / bug？→ 加载 `systematic-debugging` skill（4 阶段 + 5 Whys）
- 含密码/Token/2FA？→ 加载 `security-review` skill
- 含 API 端点？→ 加载 `api-review` skill
- 完成 / 提交？→ 加载 `verification-before-completion` skill
- 写 spec？→ 加载 `spec-driven-development` skill（greenfield/brownfield 分流）

---

## 反模式（任何一条触发即视为违规）

- ❌ 收到 bug 报告后 zero-edit 回复
- ❌ 推断根因后不写测试就改实现
- ❌ 跳 systematic-debugging 直接 fix
- ❌ 修实现来"让错的测试通过"
- ❌ 删除 vitest.config.ts 等测试基建
- ❌ 主流程跑完不加载任何 skill 做交叉审查
- ❌ 完成前不跑测试 / 不看输出就声称"通过"
- ❌ 用"以后再补"作为搪塞
- ❌ 复杂任务跳过 brainstorming 直接动手
- ❌ 引用自己未读过的文件 / 工具 / 文档

---

*基于工程哲学 v1 + v3.0 8 铁律 + 4 场景手动测试评估（2026-06-12）*
*版本：v4.0*
*生效方式：alwaysApply: true（始终生效）*

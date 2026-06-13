---
name: TDD 铁律 v4.0（智能生效）
description: 写测试时必须遵守的 TDD 铁律。核心约束：RED 必真发生 / 修测试不修实现 / 配置文件豁免清单。
alwaysApply: false
---

# TDD 铁律 v4.0（智能生效）

> 来源：v3.0 tdd-workflow skill 核心约束
> 详细工作流：见 `skill/tdd-workflow`
> 触发：写任何测试 / 验证 TDD 是否被遵守

---

## 3 大铁律（任何一条触发即视为违规）

### 铁律 1：RED 必真发生

**禁止行为**：
- ❌ 用 `it.skip()` / `test.skip()` 跳过测试假装"RED"
- ❌ 用 `expect(true).toBe(true)` 这种永远通过的断言
- ❌ 在写测试**之前**写实现
- ❌ 跑测试**之前**就声称"RED"

**必须行为**：
- ✅ 先写测试 → 跑测试 → **看到真实失败信息**
- ✅ 失败信息**展示在最终报告**中（让用户看到 RED 真发生）
- ✅ 失败原因与预期一致（断言失败，不是 setup 错误）

**反模式**：
```typescript
// ❌ 先写实现后写测试（违反 TDD）
function add(a, b) { return a + b; }
test('add', () => expect(add(1, 2)).toBe(3));  // 永远通过
```

**正例**：
```typescript
// 步骤 1: 先写测试
test('add', () => expect(add(1, 2)).toBe(3));

// 步骤 2: 跑测试 → 看到 RED
// ReferenceError: add is not defined

// 步骤 3: 写实现
function add(a, b) { return a + b; }

// 步骤 4: 跑测试 → GREEN
// 1 passed
```

---

### 铁律 2：修测试不修实现

**触发场景**：发现测试代码自身有 bug

| bug 类型 | 处理方式 |
|---------|---------|
| 断言写错边界值 | **改测试** |
| 注释与代码不一致 | **改测试**（注释或代码）|
| 期望值错误 | **改测试** |
| 变量名写错 | **改测试** |
| 真实实现 bug | **改实现**（通过 TDD RED→GREEN 流程）|

**禁止**：
- ❌ "测试失败了，让我改实现让它通过"（实现可能是对的）
- ❌ "测试期望值不对，让我改期望值"（除非确实写错）

**判断标准**：
- 若失败的断言与用户需求 / FR 描述一致 → 改实现
- 若失败的断言与用户需求 / FR 描述不一致 → 改测试

---

### 铁律 3：配置文件豁免清单

TDD 铁律**不适用**以下配置文件（plan.md 已明确）：

| 文件类型 | 原因 |
|---------|------|
| `package-lock.json` / `yarn.lock` | 依赖锁文件，由 npm/yarn 生成 |
| `.env` / `.env.example` | 环境变量，运行时注入 |
| `.gitignore` | Git 配置，1 次性 |
| `tsconfig.json` / `jsconfig.json` | TS/JS 编译配置 |
| `vitest.config.*` / `jest.config.*` | 测试运行配置 |
| `.eslintrc.*` / `.prettierrc.*` | Lint / 格式化配置 |
| `Dockerfile` / `docker-compose.yml` | 容器配置 |
| `CI/CD` 配置 | `.github/` / `.gitlab-ci.yml` |
| `LICENSE` / `README.md` | 法律 / 文档 |
| 纯数据文件 | `*.json` / `*.yml`（如迁移、数据 seed）|

**豁免不是免写**：配置文件**仍需正确**（TDD 改成"配置正确性验证"——确认服务能启动 / 测试能跑）

---

## 4 个 TDD 步骤（精简版）

```
RED    → 写测试，跑测试，看到失败（必须真发生）
GREEN  → 写最小实现，跑测试，看到通过
REFACTOR → 改善代码（命名/结构），跑测试，仍通过
COMMIT → 提交（git commit -m "feat: ..."）
```

每个步骤**不超过 5 分钟**。

---

## 覆盖率红线

| 维度 | 阈值 |
|------|------|
| Statements | ≥ 80% |
| Branches | ≥ 75% |
| Functions | ≥ 80% |
| Lines | ≥ 80% |

**低于阈值 → 视为未完成**（必须补测试，不能用"已通过"搪塞）

---

## 与 8 个角色约束的关系

| 角色 | 与 TDD 的关系 |
|------|-------------|
| test-reviewer | 直接相关（覆盖率 / 边界 / mock）|
| code-quality-reviewer | 间接（测试代码也要符合质量红线）|
| plan-reviewer | 间接（任务计划要内嵌 TDD 步骤）|

---

## 反模式（任何一条触发即视为违规）

- ❌ RED 不真发生（skip / 永远通过 / 假装看到）
- ❌ 先写实现后写测试
- ❌ 跑测试看不到真实失败信息
- ❌ 改实现让"错的测试通过"
- ❌ 删 vitest.config.ts 等测试基建
- ❌ 完成前不跑测试 / 不看覆盖率
- ❌ 测试覆盖率 < 80%
- ❌ 测所有路径但漏掉边界（空数组 / null / 极大值）
- ❌ 测试依赖真实 DB / 真实网络（必须 mock）
- ❌ 测试间共享状态（必须隔离）

---

*基于 v3.0 tdd-workflow skill 核心约束提取*
*版本：v4.0*
*生效方式：智能生效（描述含"写测试 / TDD / 验证"等关键词时 AI 加载）*

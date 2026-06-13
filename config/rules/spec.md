---
name: 规范质量红线 v4.0（智能生效）
description: 编写 spec.md 时必须遵守的规范红线。Delta Spec 4 段在 brownfield 强制，greenfield 可选。
alwaysApply: false
---

# 规范质量红线 v4.0（智能生效）

> 来源：原 spec-reviewer specialist + v3.0 spec-driven-development skill 重构
> 触发：编写 / 评审任何 spec.md 时

---

## spec 范围分流（v4.0 新增）

**`scope` 字段（必填）**：

```yaml
---
type: spec
title: [功能名称]
scope: greenfield | brownfield  # 🆕 v4.0 强制标注
---
```

| scope | Delta Spec 4 段要求 | 适用项目类型 |
|-------|---------------------|--------------|
| **greenfield** | 可选（默认空）| 新项目 / 全新模块 |
| **brownfield** | **强制**（至少 1 段非空）| 修改现有功能 / 二次开发 |

**判断标准**：
- 仓库已存在且本次有非空修改 → **brownfield**
- 仓库首次创建 / 新模块首次规范 → **greenfield**

---

## 7 大红线（任何一条触发即视为违规）

### 红线 1：FR 编号必须连续

- 编号格式：`FR-001` / `FR-002` / ...
- 不跳号（即便删除中间 FR 也不复用编号）
- 跨文件引用 FR 编号必须保持一致

**反模式**：
```markdown
- **FR-001** 用户注册
- **FR-003** 用户登录  # ❌ 跳过 FR-002
```

---

### 红线 2：每个 FR 必须含 输入 / 输出 / 错误处理 三段

```markdown
- **FR-XXX**：[需求描述]
  - 输入：[输入条件，含具体值 / 边界]
  - 输出：[预期输出，含具体值 / 格式]
  - 错误：[错误码 + 错误信息]
```

**反模式**：
```markdown
- **FR-001** 用户可以登录  # ❌ 三段缺失
```

---

### 红线 3：成功标准（SC）必须可度量

**反模式**：
```markdown
- [ ] 系统应该好用             # ❌ 不可度量
- [ ] 系统应该快              # ❌ 不可度量
```

**正例**：
```markdown
- [ ] **SC-001**：登录响应时间 P95 ≤ 300ms
- [ ] **SC-002**：注册失败率 ≤ 0.1%
- [ ] **SC-003**：覆盖率 ≥ 80%
```

---

### 红线 4：关键实体必须有字段表

```markdown
### User
| 字段 | 类型 | 描述 |
|------|------|------|
| id | string | 唯一标识 |
| email | string | 邮箱（唯一）|
| createdAt | timestamp | 创建时间 |
```

**反模式**：
```markdown
### User
- 用户实体（无字段表）  # ❌
```

---

### 红线 5：假设 / 依赖 / 非目标 三节必须存在

- **假设**：本次规范成立的前置条件（例：用户已登录、依赖外部 API）
- **依赖**：本次规范需要的外部资源 / 库 / 服务
- **非目标**：明确**不做**什么（避免 scope creep）

**反模式**：
```markdown
# 规范无"非目标"节 → 范围不清
```

---

### 红线 6：Delta Spec 4 段（brownfield 强制）

| 段 | brownfield | greenfield |
|----|-----------|-----------|
| **ADDED Requirements** | 新增功能描述 | 可选（用 spec 主体即可）|
| **MODIFIED Requirements** | 至少 1 段（标 ✅ 强制）| 无（无历史）|
| **REMOVED Requirements** | 至少 1 段（标 ✅ 强制）| 无 |
| **RENAMED Requirements** | 至少 1 段（标 ✅ 强制）| 无 |

**brownfield MODIFIED 模板**：
```markdown
### FR-XXX（原需求标题）

**原描述**：
> [原需求描述]

**新描述**：
> [新需求描述]

**变更原因**：[为什么需要修改]

**影响范围**：
- [影响的文件 / 模块 1]
```

---

### 红线 7：规范无技术实现细节

- 规范描述 **WHAT**（做什么）
- 设计描述 **HOW**（怎么做）→ 移到 design.md

**反模式**：
```markdown
- **FR-001** 用 Express.js + SQLite 实现登录  # ❌ 规范混入技术选型
```

---

## spec 文件结构（标准）

```
.trae/specs/changes/<date>-<feature>/
├── spec.md           # 本规范
├── design.md         # 技术设计（可选）
├── tasks.md          # 任务列表（由 plan-driven-development 生成）
├── proposal.md       # 变更提案（brownfield 必填）
└── completion.md     # 完成报告（实现后补）
```

归档后移动到 `archived/`。

---

## 输出检查清单

- [ ] `scope` 字段已标注（greenfield / brownfield）
- [ ] 背景和动机清晰
- [ ] 用户场景完整（至少 1 个，含 As a / I want / So that）
- [ ] FR 编号连续
- [ ] 每个 FR 含输入 / 输出 / 错误处理
- [ ] 关键实体定义有字段表
- [ ] 成功标准可度量
- [ ] 假设条件 / 依赖 / 非目标 三节完整
- [ ] brownfield 项目 Delta Spec 4 段至少 1 段非空
- [ ] 规范无技术实现细节（用 design.md 承载）
- [ ] 开放问题 ≤ 3 个

---

## 反模式（任何一条触发即视为违规）

- ❌ FR 编号不连续
- ❌ FR 缺输入/输出/错误处理
- ❌ 成功标准"系统应该好用"
- ❌ 关键实体无字段表
- ❌ 缺假设/依赖/非目标
- ❌ brownfield 项目无 Delta Spec MODIFIED 段
- ❌ 规范混入技术实现细节
- ❌ 开放问题 > 3 个（应进入 brainstorming）
- ❌ greenfield 项目被强制写 4 段（应留空）

---

*基于原 spec-reviewer specialist + v3.0 spec-driven-development skill 重构*
*版本：v4.0*
*生效方式：智能生效（描述含"写 spec / 评审 spec"等关键词时 AI 加载）*

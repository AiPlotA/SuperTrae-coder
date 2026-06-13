---
name: 规范驱动开发 v4.0（spec-driven-development）
description: 当用户提出新功能、重构、多文件改动、复杂任务时自动加载。强制规范先行：生成用户场景 + FR-XXX 编号 + 关键实体 + 成功标准。🆕 v4.0 引入 scope 字段分流：greenfield 项目 4 段**可选**（spec-kit 风格），brownfield 项目 4 段**强制**（OpenSpec Delta Spec）。比 TRAE 内置 /spec 更完整。
use_when:
  - 用户提出新功能/重构/多文件改动
  - 复杂任务开始
  - 用户说"先写规范"/"先 spec"
  - 看到"用户场景 + FR"
core_constraint:
  - 必含用户场景(As a/I want/So that)
  - 必含 FR-XXX 编号
  - 必含关键实体
  - 必含成功标准(SC)
  - brownfield 必写 Delta Spec 4 段
  - 引用 1+ 条 ETHOS 哲学
exit_when:
  - 单文件 bug 修复(用 systematic-debugging)
  - 用户明确说"我就要直接做"
  - 任务粒度 < 5 分钟
---

> ETHOS: Golden Age + 完整实现
>
> 写 spec 不是"多余流程",而是确保后续 100× 压缩比不被错的方向浪费。greenfield/brownfield 分流就是避免"无内容可填也要填"的形式主义。

# 规范驱动开发 v4.0（Spec-Driven Development）

> 基于 spec-kit 8 阶段 + OpenSpec Delta Spec 4 段机制（仅 brownfield）
> 完整度优于 TRAE 内置 /spec（仅 3 个文件）
> v4.0 引入 scope 分流：greenfield 走 spec-kit 风格 / brownfield 走 Delta Spec 4 段

---

## 🆕 v4.1 前置步骤：office-hours 必走

> **任何 spec 在写之前必须先走 `skill/office-hours` 的 5 强制问题**
> 否则 5 维度的产品 reframing 不充分,spec 容易在写完后才发现"目标用户是错的"。

**流程**：

1. 用户提出新功能 / 重构 / 多文件改动
2. **本 skill 加载时,先检查用户是否走过 office-hours**
3. 如未走 → **自动加载 `skill/office-hours`**,走完 5 强制问题,得到产品 reframing 评分 ≥ 7 分
4. reframing 通过 → 走本 skill 写 spec
5. reframing < 7 分 → 修完缺口再回来

**跳过 office-hours 的反模式**：

- ❌ "产品想法已经很清楚,不用 reframing 了" → "清楚"是用户视角,review 视角可能完全不一样
- ❌ "赶时间,先写 spec 再说" → 写完发现 reframing 不全,返工成本 > 现在 5 分钟

**为什么这样设计**：

- 5 维度 reframing 是 plan-mode 的"产品门"——CEO review / eng review 之前必须先确定"产品是什么"
- office-hours 输出 5 维度评分(目标用户/痛点/替代方案/成功标准/边界),直接喂给 spec 的"用户场景" + "非目标"章节
- AI 时代 office-hours 5 问成本 < 5 分钟,跳过它的代价是 spec 阶段 30+ 分钟返工

---

## 触发场景

满足以下**任一**时自动加载：

- 用户说"我要做..."、"帮我加..."、"新功能"、"重构"
- 涉及多文件、多模块改动
- 需要 FR-XXX 编号追踪
- 涉及 brownfield（已有代码的二次开发）
- 用户提及"规范"、"spec"、"需求文档"
- 任务规模 ≥ 2 小时

---

## 何时使用本 Skill vs TRAE 内置 /spec

| 维度 | TRAE 内置 /spec | 本 Skill |
|------|----------------|----------|
| 触发方式 | 用户输入 `/spec` | SOLO Agent 智能加载 |
| 生成文件 | 3（spec/tasks/checklist）| 5+（proposal/spec/design/tasks/delta）|
| FR 编号 | ❌ | ✅ FR-XXX |
| 关键实体 | ❌ | ✅ |
| Delta Spec 4 段 | ❌ | ✅ ADDED/MODIFIED/REMOVED/RENAMED |
| DAG 依赖 | ❌ | ✅ |
| 9 条款宪法 | ❌ | ✅（参考 .agents/AGENTS.md）|

**本 Skill 适用场景**：复杂任务、需要 FR 编号、brownfield、多人协作、长期维护
**TRAE 内置 /spec 适用场景**：简单任务、用户主动选 /spec

---

## 🆕 v4.0 scope 分流（greenfield / brownfield）

**spec.md 头部 `scope` 字段必填**：

```yaml
---
type: spec
title: [功能名称]
scope: greenfield | brownfield  # 🆕 v4.0 强制标注
---
```

| scope | Delta Spec 4 段 | 风格 | 适用项目 |
|-------|----------------|------|----------|
| **greenfield** | **可选**（默认空 / 标"无历史实现"）| spec-kit 风格 | 新项目 / 全新模块 |
| **brownfield** | **强制**（至少 1 段非空）| OpenSpec Delta Spec | 修改现有功能 / 二次开发 |

**判断标准**：
- 仓库首次创建 / 新模块首次规范 → `scope: greenfield`
- 仓库已存在且本次有非空修改 → `scope: brownfield`

**v3.0 → v4.0 关键变化**：
- v3.0：所有 spec 强制 4 段（**greenfield 也要硬写**，导致 3/4 场景无内容可填）
- v4.0：greenfield 4 段可选，brownfield 4 段强制
- 评估标准 D4 改写：greenfield 不扣分 / brownfield 漏写 4 段扣分

---

## 完整 Spec 模板

```markdown
---
type: spec
title: [功能名称]
created: YYYY-MM-DD
status: draft | approved | implemented | archived
---

# [功能名称] 规范

## 背景
[功能产生的背景、动机、痛点]

## 用户场景

### 场景 1
- **作为** [用户类型]
- **我希望** [功能描述]
- **以便** [价值描述]

## 功能需求

- **FR-001**：[需求描述]
  - 输入：[输入条件]
  - 输出：[预期输出]
  - 错误：[错误处理]

- **FR-002**：[需求描述]
  - ...

## 关键实体

### Entity1
| 字段 | 类型 | 描述 |
|------|------|------|
| id | string | 唯一标识 |
| name | string | 名称 |

### Entity2
| 字段 | 类型 | 描述 |
|------|------|------|
| id | string | 唯一标识 |
| parentId | string | 父实体 ID |

## 实体关系

```
Entity1 (1) ──< (N) Entity2
```

## 成功标准

- [ ] **SC-001**：[可度量的标准 1]
- [ ] **SC-002**：[可度量的标准 2]

## 假设条件

- [假设 1]：[描述]

## 依赖

- 依赖项 1：[描述]

## 非目标

- 不做：[明确排除的范围]

## 开放问题

- [NEEDS CLARIFICATION]：[待澄清问题]（最多 3 个）
```

---

## Delta Spec 4 段机制（OpenSpec 兼容）

**何时使用 Delta Spec**：

| 场景 | 使用方式 |
|------|---------|
| 新功能 | 创建完整 Spec |
| 修改现有功能 | 使用 MODIFIED Delta |
| 删除功能 | 使用 REMOVED Delta |
| 重命名 | 使用 RENAMED Delta |

**Delta Spec 模板**：

```markdown
## ADDED Requirements

### FR-NEW-001：[新增需求]
- 输入：[输入条件]
- 输出：[预期输出]

#### Scenario: [场景描述]
- **WHEN** [触发条件]
- **THEN** [预期结果]
- **AND** [附加结果]

## MODIFIED Requirements

### FR-XXX：[原需求标题]

**原描述**：
> [原需求描述]

**新描述**：
> [新需求描述]

**变更原因**：[为什么需要修改]

**影响范围**：
- [影响的文件/模块 1]

## REMOVED Requirements

### FR-OLD-XXX：[移除的需求]
- 移除原因：[为什么移除]
- 替代方案：[替代方案]
- 影响：[影响范围]

## RENAMED Requirements

### FR-OLD-XXX → FR-NEW-XXX
- **原名称**：[原需求标题]
- **新名称**：[新需求标题]
- **变更原因**：[为什么重命名]
```

---

## Spec 文件存储位置

```
.trae/specs/changes/<date>-<feature>/
├── spec.md           # 本规范
├── design.md         # 技术设计（可选）
├── tasks.md          # 任务列表
└── proposal.md       # 变更提案（可选）
```

归档后移动到 `archived/`。

---

## 关键约束

- 最多 **3 个** `[NEEDS CLARIFICATION]` 标记
- 成功标准必须**可度量**、**技术无关**
- **禁止**在 spec 中指定技术实现（移到 design.md）
- FR 编号必须**连续**
- 每个 FR 必须有明确的输入/输出/错误处理

---

## 与其他 Skill 的协作

- **上游**：brainstorming（设计确认后进入 spec）
- **下游**：plan-driven-development（spec 完成后拆任务）
- **评审**：spec-reviewer agent（自动派发）

### 🆕 v4.1 后置建议：autoplan 必跑

> **任何 spec 写完后,自动建议跑 `skill/autoplan` 做 5 维度 review**
> 否则 spec 可能只过了"语法检查",没过"产品 / CEO / 设计 / 工程 / DX"5 维度的实质 review。

**流程**：

1. spec 写完(本 skill 走完)
2. **自动建议用户跑 `skill/autoplan`**
3. autoplan 依次跑：office-hours(已走可跳过) → plan-ceo-review → plan-design-review(仅 UI) → plan-eng-review → plan-devex-review(仅 lib/API/CLI)
4. 综合评分 ≥ 7 → 可进 plan-driven-development
5. 综合 4-6 → 修 Top 3 缺口后重跑
6. 综合 < 4 → 回到 office-hours 重新 reframing

**为什么这样设计**：

- 单一 spec-reviewer 看的是"spec 语法完整性"(FR 编号 / 关键实体 / 成功标准)
- autoplan 5 维度看的是"spec 实质质量"(产品 / CEO / 设计 / 工程 / DX)
- 两者互补,不互斥——spec-reviewer 跑过不算 autoplan 跑过

**与 spec-reviewer 的区别**：

| 维度 | spec-reviewer（v4.0 角色）| autoplan（v4.1 元 skill）|
|------|------------------------|-------------------------|
| 范围 | spec 语法完整性 | spec 5 维度实质质量 |
| 评分 | 通过 / 不通过 | 0-10 分 |
| 修复指引 | 列缺漏项 | Top 3 修复方向 |
| 何时跑 | spec 写完自动 | spec 写完 + 重大决策时 |

---

## 输出检查清单

- [ ] 背景和动机清晰
- [ ] 用户场景完整（至少 1 个）
- [ ] FR 编号连续
- [ ] 关键实体定义准确
- [ ] 成功标准可度量
- [ ] 假设条件合理
- [ ] 非目标明确
- [ ] 开放问题 ≤ 3 个

---

## 哲学依据

| 来源 | 贡献 |
|------|------|
| **spec-kit** | 8 阶段方法论、9 条款宪法 |
| **OpenSpec** | Delta Spec 4 段、Artifact DAG |
| **superpowers** | brainstorming HARD-GATE |
| **工程哲学 v1** | 规范先行原则 |

---

*基于 spec-kit + OpenSpec + 工程哲学 v1*
*创建时间：2026-06-12*
*版本：v3.0*
*加载方式：TRAE 智能扫描 description 自动加载*

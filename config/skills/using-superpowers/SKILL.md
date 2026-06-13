---
name: Using Superpowers（元 skill）
description: 用户说"我不知道该用哪个 skill" / "我要做 X,先做什么" / "加载 skill 之前"时自动加载。**任何 skill 加载之前的元 skill**——告诉用户"什么时候加载 skill / 加载什么 / 加载错了如何退出"。引用 ETHOS 哲学:Boil the Ocean(在加载 skill 之前先想清楚 3 件事)+ Evidence Over Claims(每个 skill 引用必须有可验证证据)。🆕 v4.1 轮 2 元 skill。
use_when:
  - 用户说"我不知道该用哪个 skill"
  - 用户说"我要做 X,先做什么"
  - 加载任何具体 skill 之前
  - 复杂任务开始时的"准备"阶段
core_constraint:
  - 必先于其他 skill 加载(强制前置)
  - 必含 3 段:use_when / core_constraint / exit_when
  - 必引用 1+ 条 ETHOS 哲学
  - 必含"为什么这样设计"段
exit_when:
  - 用户明确说"我只要做 Y"且 Y 是单 skill 能完成
  - 已确认走 brainstorming 5 问
  - 任务粒度 < 5 分钟(无需 skill 引导)
---

> ETHOS: Boil the Ocean + Evidence Over Claims
>
> Boil the Ocean:加载 skill 之前先想清楚 3 件事——目标 / 范围 / 失败定义
> Evidence Over Claims:每个 skill 引用必须有可验证证据(命令输出 / 报告链接)

# Using Superpowers 技能（元 skill）

> 基于 Anthropic "using-superpowers" Skill 改造
> 目的：作为"加载任何 skill 之前的元 skill",告诉用户"什么时候加载 skill / 加载什么 / 加载错了如何退出"
> 强制级别：P0 - 任何 skill 加载之前的强制前置

---

## 触发条件

满足以下**任一**时自动加载：

- 用户说"我不知道该用哪个 skill"
- 用户说"我要做 X,先做什么"
- 加载任何具体 skill 之前(brainstorming / spec-driven-development / tdd-workflow / 等)
- 复杂任务开始时的"准备"阶段

**前置依赖**：无（这是元 skill,是其他 skill 的入口）

---

## 3 段式

### 1. use_when（何时加载）

- 用户说"我不知道该用哪个 skill"
- 用户说"我要做 X,先做什么"
- 加载任何具体 skill 之前
- 复杂任务开始时的"准备"阶段

### 2. core_constraint（核心约束）

- 必先于其他 skill 加载（强制前置）
- 必含 3 段：use_when / core_constraint / exit_when
- 必引用 1+ 条 ETHOS 哲学
- 必含"为什么这样设计"段

### 3. exit_when（何时退出）

- 用户明确说"我只要做 Y"且 Y 是单 skill 能完成
- 已确认走 brainstorming 5 问
- 任务粒度 < 5 分钟（无需 skill 引导）

---

## 5 条 ETHOS 哲学速查

| 哲学 | 何时引用 |
|------|---------|
| **Boil the Ocean** | 在加载 skill 之前先想清楚 3 件事——目标 / 范围 / 失败定义 |
| **Golden Age** | 让 spec 描述的不是"工具"而是"产品"——5 维度评分、ETHOS 注入 |
| **Evidence Over Claims** | 完成前跑命令看完整输出,禁止"应该没问题" |
| **完整实现** | 禁止"以后再补"——每个任务做透 |
| **不搪塞** | 禁止用"测试已通过"搪塞——主动制造 RED 复现 |

---

## skill 加载决策树

```
用户提出需求
  │
  ├─ 是否需要"reframing 产品意图"?
  │   └─ 是 → skill/office-hours
  │
  ├─ 是否需要"5 问 + 3 方案 + HARD-GATE"?
  │   └─ 是 → skill/brainstorming
  │
  ├─ 是否需要"写规范(用户场景+FR+实体+SC)"?
  │   └─ 是 → skill/spec-driven-development
  │
  ├─ 是否需要"拆分任务(2-5 分钟 DAG)"?
  │   └─ 是 → skill/plan-driven-development
  │
  ├─ 是否需要"RED-GREEN-REFACTOR"?
  │   └─ 是 → skill/tdd-workflow
  │
  ├─ 是否需要"复现-定位-根因-修复"?
  │   └─ 是 → skill/systematic-debugging
  │
  ├─ 是否需要"安全审查(OWASP / 9 项 checklist)"?
  │   └─ 是 → skill/security-review
  │
  ├─ 是否需要"API 审查(RESTful 14 项)"?
  │   └─ 是 → skill/api-review
  │
  ├─ 是否需要"完成前验证(跑命令看输出)"?
  │   └─ 是 → skill/verification-before-completion
  │
  ├─ 是否需要"5 维度 plan-mode review"?
  │   └─ 是 → skill/autoplan(串联 4 review)
  │
  └─ 都不需要?→ 用户可能只要简单回答,无需 skill
```

---

## 失败时如何退出

### 退出信号 1：用户拒绝加载元 skill

- 例:"我不需要这些,直接做"
- 退出方式：跳过元 skill,直接进 brainstorming 的 5 问
- 反模式：❌ 强制加载元 skill 引发用户反感

### 退出信号 2：决策树无法匹配

- 例：用户需求是 5 类 skill 之外的(如"分析竞品")
- 退出方式：建议用户开新 skill（用 skill/skill-writer 5 步法）
- 反模式：❌ 硬塞不相关的 skill

### 退出信号 3：用户在 5 分钟内未表态

- 例：用户已 5 分钟未回应
- 退出方式：默认走最常用的 skill-brainstorming(5 问 + 3 方案)
- 反模式：❌ 反复询问"你想用哪个 skill"

---

## 为什么这样设计

> Boil the Ocean：在加载 skill 之前先想清楚 3 件事
> Evidence Over Claims：每个 skill 引用必须有可验证证据

1. **强制前置**：避免"agent 自己做完全部事"——确保每个 skill 都被显式加载
2. **3 段式**：确保 skill 写出来有统一结构——17 skill 重写时容易套模板
3. **决策树**：避免"agent 加载错误的 skill"——按需求匹配最合适的 skill
4. **退出信号**：避免"agent 一直卡在选 skill"——3 个明确退出条件
5. **ETHOS preamble**：哲学不只是"在文档里"——每次加载 skill 时显式 prepend 1-2 条哲学

---

## 反模式（任何一条触发即视为违规）

- ❌ 跳过元 skill 直接进具体 skill
- ❌ 决策树强行匹配不相关的 skill
- ❌ 退出信号没满足就硬退出
- ❌ ETHOS 哲学引用是"为引用而引用"（与 skill 主题无关）
- ❌ 决策树只有"是/否"二分,没有"部分匹配"灰度

---

*基于 Anthropic using-superpowers Skill 改造*
*版本：v4.1 轮 2 元 skill*
*下一步：skill/skill-writer(写新 skill 的工作流)*

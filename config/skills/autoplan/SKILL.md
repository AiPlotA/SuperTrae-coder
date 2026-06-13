---
name: Autoplan（plan-mode 5 维度一键串联）
description: 用户说"评估我的项目" / "跑完整 plan-mode" / "5 维度都过一遍" / "autoplan"时自动加载。一个命令依次触发 office-hours → plan-ceo-review → plan-design-review → plan-eng-review → plan-devex-review,输出综合 5 维度评分 + 1 份合并 review 报告。🆕 v4.1 plan-mode 元 skill。
use_when:
  - 用户说"评估我的项目"
  - 用户说"跑完整 plan-mode"
  - 用户说"5 维度都过一遍"
  - 重大决策前的全检
core_constraint:
  - 必串行触发 4 个 review skill
  - 必输出合并报告(综合 0-10 评分)
  - 引用 1+ 条 ETHOS 哲学
  - 含 5+ 修复方向
exit_when:
  - 用户只要做单维度 review(用具体 review skill)
  - 已跑过 5 维度 24h 内
  - 任务粒度 < 30 分钟(过重)
---
---

> ETHOS: Golden Age + 完整实现
>
> 5 维度全检的成本在 AI 时代已 < 10 分钟,不跑全检 = 漏检 = 后期返工。

# Autoplan 技能（plan-mode 5 维度一键串联）

> 基于 gstack `/autoplan` Skill 改造
> 目的：用一个命令完成 office-hours + 4 review 的全检
> 强制级别：P1 - 复杂项目 / 重大决策时必跑

---

## 5 维度串联流程

### 步骤 1：office-hours（产品 reframing）

加载 `skill/office-hours`,走完 5 强制问题,得到产品 reframing 评分(0-10)。

**输出**:reframing 评分 + 缺口清单

### 步骤 2：plan-ceo-review（5 维度产品 review）

加载 `skill/plan-ceo-review`,跑 5 维度评分(愿景/用户/价值/差异化/可执行)。

**输出**:CEO review 评分 + Top 3 修复方向

### 步骤 3：plan-design-review（4 维度设计 review,仅 UI 项目）

如果有 UI,加载 `skill/plan-design-review`;否则标 N/A。

**输出**:Design review 评分 + 修复方向(或 N/A)

### 步骤 4：plan-eng-review（4 维度工程 review）

加载 `skill/plan-eng-review`,跑 4 维度评分(数据流/模块边界/边界/测试)。

**输出**:Eng review 评分 + 修复方向

### 步骤 5：plan-devex-review（4 维度 DX review,仅 lib/API/CLI）

如果是 lib/API/CLI/框架,加载 `skill/plan-devex-review`;否则标 N/A。

**输出**:Devex review 评分 + 修复方向(或 N/A)

### 步骤 6：合并报告

把 5 步骤评分合并为 1 份 autoplan 报告:

---

## 合并报告模板

```markdown
# Autoplan 报告：[项目名]

**生成时间**:[日期]
**输入**:[产品想法 / spec 链接 / 代码仓库]
**总评**:[综合评分 0-10,基于 5 维度加权平均]

## 1. 产品 reframing（office-hours）

- 目标用户:[?/10]
- 痛点:[?/10]
- 替代方案:[?/10]
- 成功标准:[?/10]
- 边界:[?/10]
- **小计**:**[?/10]**

## 2. CEO Review

- 愿景:[?/10]
- 用户:[?/10]
- 价值:[?/10]
- 差异化:[?/10]
- 可执行:[?/10]
- **小计**:**[?/10]**

## 3. Design Review（仅 UI）

- UX:[?/10] (或 N/A)
- 视觉:[?/10] (或 N/A)
- 交互:[?/10] (或 N/A)
- 可访问性:[?/10] (或 N/A)
- **小计**:**[?/10]** (或 N/A)

## 4. Eng Review

- 数据流:[?/10]
- 模块边界:[?/10]
- 边界情况:[?/10]
- 测试策略:[?/10]
- **小计**:**[?/10]**

## 5. Devex Review（仅 lib/API/CLI）

- TTHW:[?/10] (或 N/A)
- 神奇时刻:[?/10] (或 N/A)
- 摩擦点:[?/10] (或 N/A)
- 用户画像追踪:[?/10] (或 N/A)
- **小计**:**[?/10]** (或 N/A)

## 综合评分

[综合 0-10 分]

## Top 5 修复方向（按影响力排序）

1. [最大 gap 的 1 句话修复]
2. [第二大 gap 的修复]
3. ...

## 下一步

- 综合 ≥ 7:可进 skill/plan-driven-development 写任务
- 综合 4-6:修完 Top 3 后重跑 autoplan
- 综合 < 4:回到 office-hours 重新 reframing
```

---

## 3 强制问题

### 问题 1：5 维度全跑还是只跑相关维度？

> - 含 UI → office-hours + CEO + Design + Eng（4 个）
> - lib/API/CLI → office-hours + CEO + Eng + Devex（4 个）
> - 完整产品 → 全 5 个

### 问题 2：每个维度的"7 分门槛"是什么？

> 默认 7 分 = 可进 plan-driven-development;低于 7 分 = 修完再跑。
> 例外:安全敏感项目 8 分门槛。

### 问题 3：跑完后的决策点是什么？

> - ≥ 7 进 plan-driven-development
> - 4-6 修 Top 3 后重跑
> - < 4 回到 office-hours

---

## fix 输出格式

```markdown
## Autoplan 缺口 + 修复方向

### 缺口 1：[最大 gap 维度] 当前 ?/10
- 现状：[5 维度的具体表现]
- 缺什么：[缺的具体元素]
- 修复问题：[给用户的 1 个具体问题]
- 负责 review skill：[plan-ceo-review / plan-eng-review / ...]

### 缺口 2：...
```

---

## 反模式

- ❌ 跑完 5 维度但只复制分数不修缺口
- ❌ 跳过 N/A 维度的说明（应明确说"无 UI"）
- ❌ 用 1 次 5 分钟"快速"跑完所有维度（实际需要 30-60 分钟深度分析）
- ❌ 综合评分 < 4 还强行进 plan-driven-development

---

*基于 gstack `/autoplan` Skill 改造*
*版本：v4.1 plan-mode*
*下一步:skill/plan-driven-development（综合 ≥7）→ skill/tdd-workflow（开始实现）*

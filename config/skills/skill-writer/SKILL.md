---
name: Skill Writer（写新 skill 的工作流）
description: 用户说"我想加个新 skill" / "写一个 XX skill" / "怎么写 skill"时自动加载。**写新 skill 的 5 步法**:1.用户场景→2.FR-XXX→3.触发关键词→4.4 部分结构→5.CI 检查。引用 ETHOS 哲学:Boil the Ocean(在写 skill 之前先想清楚 3 件事)+ Evidence Over Claims(每个 skill 引用必须有可验证证据)+ 完整实现(禁止"以后再补")。🆕 v4.1 轮 2 元 skill。
use_when:
  - 用户说"我想加个新 skill"
  - 用户说"写一个 XX skill"
  - 用户说"怎么写 skill"
  - 任何新增 skill 的工作流起点
core_constraint:
  - 必先于"创建 SKILL.md 文件"加载
  - 必含 5 步法章节(用户场景 / FR-XXX / 触发关键词 / 4 部分结构 / CI 检查)
  - 必含 checklist 章节
  - 必引用 1+ 条 ETHOS 哲学
  - 必含 frontmatter 3 段式(use_when / core_constraint / exit_when)
exit_when:
  - 仅修改现有 skill 的 frontmatter(用 using-superpowers 即可)
  - 仅问"某个 skill 怎么用"(不写新 skill)
  - 用户明确说"我先看看"但未到写阶段
---

> ETHOS: Boil the Ocean + Evidence Over Claims + 完整实现
>
> Boil the Ocean:在写 skill 之前先想清楚 3 件事——谁会用 / 解决什么 / 何时退出
> Evidence Over Claims:每个 skill 引用必须有可验证证据(命令输出 / 报告链接)
> 完整实现:禁止"以后再补"——每个新 skill 写完即完整

# Skill Writer 技能（写新 skill 的工作流）

> 基于 Anthropic "writing-skills" Skill 改造
> 目的：给 SuperTrae-coder 添加新 skill 的标准化工作流
> 强制级别：P0 - 任何新增 skill 必须先走本 skill 的 5 步法

---

## 5 步法

### 步骤 1：用户场景(As a / I want / So that)

**做什么**：在写 skill 之前,先用 3 句话描述"谁会用 + 解决什么 + 价值是什么":

```markdown
### 场景 1:[角色]
> **As a** [具体角色]
> **I want** [用 skill 做什么]
> **So that** [带来什么价值]
```

**输出格式**：3-5 个用户场景(每个场景 3 句话)

**反模式**：
- ❌ "所有人都能用"——用户太宽泛,等于没说
- ❌ "提高效率"——价值不可测量
- ❌ 没有"So that"——只描述"做什么"不描述"为什么"

---

### 步骤 2：FR-XXX 功能需求

**做什么**：把用户场景拆成可独立验证的功能需求：

```markdown
## 功能需求

### FR-001:[能力名]
- 做什么：[1 句话]
- 输入：[什么参数]
- 输出：[什么结果]
- 验证：[怎么证明它工作]

### FR-002:[能力名]
...
```

**输出格式**：3-12 个 FR(每个 1 句话 + 输入 + 输出 + 验证)

**反模式**：
- ❌ FR 写成"实现 XX 接口"——太技术化
- ❌ 1 个 FR 含多个能力——应拆分
- ❌ 验证方法缺失——不可验证 = 不存在

---

### 步骤 3：触发关键词

**做什么**：定义"什么时候这个 skill 应该被自动加载"：

```yaml
use_when:
  - 用户说"关键词 1"
  - 用户说"关键词 2"
  - 看到"关键词 3"时
  - 涉及"关键词 4"的任务
```

**输出格式**：4-8 个触发关键词(用户原话 + 看到 + 涉及)

**反模式**：
- ❌ "任何时候"——等于没定义
- ❌ 只写中文关键词——英文 prompt 也会触发不到
- ❌ 关键词太泛("优化")——误触发率高

---

### 步骤 4：4 部分结构(Head / Why / When / How)

**做什么**：SKILL.md 正文必须含 4 部分：

```markdown
## 1. Head（标题与目的）
- skill 名称 / 目的 / 强制级别

## 2. Why（为什么这样设计）
- 设计动机 / 哲学基础 / 引用来源

## 3. When（何时使用 vs 不使用）
- 触发条件 / 反触发条件 / 边界

## 4. How（具体步骤）
- 步骤 1 / 步骤 2 / 步骤 3
- 失败时如何退出
- 反模式清单
```

**输出格式**：4 个一级标题,每部分 ≥3 个子项

**反模式**：
- ❌ 只有"How"没有"Why"——不知道为什么这样做
- ❌ "When"写成"什么场景"——应区分"使用 vs 不使用"
- ❌ 缺少"失败时如何退出"——卡住时无解

---

### 步骤 5：CI 检查

**做什么**：为新 skill 写 1 个 CI checker,自动验证 skill 是否符合 5 步法：

```python
# .trae/scripts/ci/checkers/check_xxx.py
from pathlib import Path
from typing import Any

SKILL_NAME = "xxx"
SKILL_PATH = f".trae/skills/{SKILL_NAME}/SKILL.md"

def run(root: Path, verbose: bool = False) -> dict[str, Any]:
    hard = []
    # 检查 SKILL.md 存在
    # 检查 3 段式
    # 检查 5 步法
    # 检查 ETHOS 引用
    return {"hard": hard, "soft": [], "stats": {}}
```

**输出格式**：1 个 check_xxx.py + 注册到 ci_check.py

**反模式**：
- ❌ CI 检查只检查"文件存在"——不验证内容质量
- ❌ CI 检查过严,每次微调就 fail——应软警告
- ❌ CI 检查不注册到 ci_check.py——等于没写

---

## 5 步法 checklist

写完新 skill 后,逐项勾选：

- [ ] **CK-1** 3-5 个用户场景(每个 3 句话:As a / I want / So that)
- [ ] **CK-2** 3-12 个 FR-XXX(每个 1 句话 + 输入 + 输出 + 验证)
- [ ] **CK-3** 4-8 个 use_when 触发关键词
- [ ] **CK-4** SKILL.md 含 4 部分(Head / Why / When / How)
- [ ] **CK-5** frontmatter 含 3 段式(use_when / core_constraint / exit_when)
- [ ] **CK-6** 引用 1+ 条 ETHOS 哲学
- [ ] **CK-7** 写 1 个 check_xxx.py + 注册到 ci_check.py
- [ ] **CK-8** 跑 `bash .trae/scripts/ci-check.sh` 0 hard failure
- [ ] **CK-9** 写完即跑验证(不是"以后再补")

---

## 失败时如何退出

### 退出信号 1：用户拒绝走 5 步法

- 例："我就要直接写个 skill"
- 退出方式：跳过 step 1-3,直接给模板让用户填
- 反模式：❌ 强制走 5 步法引发用户反感

### 退出信号 2：用户只问"怎么用"不写新 skill

- 例："skill-writer 怎么用"
- 退出方式：直接回答使用问题,跳过 5 步法
- 反模式：❌ 强制进入 5 步法流程

### 退出信号 3：用户在 10 分钟内未表态

- 例：用户已 10 分钟未回应
- 退出方式：默认给最小模板(只 CK-5 必填),不强制 5 步法
- 反模式：❌ 反复询问"你想用哪 5 步法"

---

## 为什么这样设计

> Boil the Ocean：在写 skill 之前先想清楚 3 件事——谁会用 / 解决什么 / 何时退出
> Evidence Over Claims：每个 skill 引用必须有可验证证据
> 完整实现：禁止"以后再补"

1. **5 步法强制顺序**：避免"先写代码再补 spec"——确保 spec 先行
2. **CK checklist 9 项**：避免"写完不知道写完没"——逐项勾选
3. **CI 自动检查**：避免"人肉检查 skill 质量"——机械验证 5 步法
4. **失败时退出信号**：避免"skill-writer 永远卡住"——3 个明确退出条件
5. **ETHOS 3 哲学引用**：避免"哲学只是文档"——Boil the Ocean + Evidence Over Claims + 完整实现

---

## 与其他 skill 的关系

- **元 skill using-superpowers**：写新 skill 之前,先问"什么时候加载 skill"——决定是否真要写
- **元 skill skill-writer(本 skill)**：决定写 → 5 步法 + CK-9 checklist
- **check_xxx.py**：写完即跑 CI,自动验证 5 步法

---

## 反模式（任何一条触发即视为违规）

- ❌ 跳过 5 步法直接写 SKILL.md
- ❌ FR 写"实现 XX 接口"等不可验证描述
- ❌ 触发关键词"任何时候"或"优化"等宽泛词
- ❌ SKILL.md 缺 Why 或 When
- ❌ 写完不跑 CI
- ❌ CK 9 项只勾 5 项
- ❌ 写新 skill 改了"以后再补"作为 todo
- ❌ ETHOS 哲学引用与 skill 主题无关

---

*基于 Anthropic "writing-skills" Skill 改造*
*版本：v4.1 轮 2 元 skill*
*下一步:check_xxx.py(新 skill 的 CI 检查器)*

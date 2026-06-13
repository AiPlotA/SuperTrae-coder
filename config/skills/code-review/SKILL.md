---
name: 代码审查（code-review）
description: 用户说"提交"、"PR"、"合并"、"review"、"帮我看看这代码"、"写得怎么样"、"代码评审"、"代码质量"、PR 评审请求时自动加载。双阶段独立审查：Spec Compliance（实现与 spec 一致性）+ Code Quality（命名、复杂度、重复、异味）。
use_when:
  - 用户说"提交"/"PR"/"合并"/"review"
  - 用户说"帮我看看这代码"
  - PR 评审请求
  - 涉及代码质量/命名/复杂度
core_constraint:
  - 必走双阶段审查(Spec Compliance + Code Quality)
  - 必含命名/复杂度/重复/异味 4 维度
  - 引用 1+ 条 ETHOS 哲学
exit_when:
  - 用户只问"风格建议"(不要求审查)
  - 仅看 1-2 行代码片段
  - 用户明确说"我已经自审了"
---
---

> ETHOS: Evidence Over Claims + Boil the Ocean
>
> 代码审查不是"看一遍"就过,而是 spec compliance + code quality 双阶段独立审查,每条问题贴文件:行号。

# 代码审查技能（Code Review）

> 基于工程哲学 v1 + superpowers 双阶段 review 融合
> 目的：保证实现质量，防止合理化

---

## 触发条件

- 实现任务完成
- 准备提交 PR
- 任何代码合并前

---

## 核心原则

### 独立审查

**Reviewer 必须独立读代码，不轻信 implementer 的报告。**

### 反表演性同意

**禁止**：
- "Looks good to me!"
- "LGTM!"
- "Nice work!"

**应该**：
- 技术性论证
- 代码引用
- 性能数据
- 风险分析

---

## 双阶段审查

### 阶段 1：Spec Compliance Review

**目的**：验证实现是否与规范一致

#### 审查清单

```markdown
## Spec Compliance Review Checklist

### 功能需求
- [ ] FR-001 是否有对应实现
- [ ] FR-002 是否有对应实现
- [ ] 所有 FR 编号都已实现

### 用户场景
- [ ] 场景 1 是否可验证
- [ ] 场景 2 是否可验证
- [ ] 所有场景都有测试覆盖

### 关键实体
- [ ] Entity1 是否定义
- [ ] Entity2 是否定义
- [ ] 实体关系是否正确

### 成功标准
- [ ] SC-001 是否达成
- [ ] SC-002 是否达成
- [ ] 标准是否可度量

### 假设条件
- [ ] 假设 1 是否被尊重
- [ ] 假设 2 是否被尊重
```

#### 审查结论

- ✅ **PASS**：进入 Code Quality Review
- ⚠️ **NEEDS CHANGES**：返回实现者
- ❌ **REJECT**：重大不匹配

---

### 阶段 2：Code Quality Review

**目的**：验证代码质量

#### 审查清单

```markdown
## Code Quality Review Checklist

### 命名规范
- [ ] 变量名描述性强
- [ ] 函数名是动作性
- [ ] 类名是名词性
- [ ] 常量名是 UPPER_SNAKE_CASE
- [ ] 文件名符合规范

### 函数质量
- [ ] 函数长度 < 50 行
- [ ] 圈复杂度 < 10
- [ ] 参数数量 <= 4
- [ ] 没有副作用

### 代码结构
- [ ] 单一职责
- [ ] 没有重复代码（DRY）
- [ ] 没有过早抽象
- [ ] 嵌套层级 < 3

### 错误处理
- [ ] 所有异常都被捕获
- [ ] 错误信息有意义
- [ ] 没有吞掉异常
- [ ] 资源正确释放

### 性能
- [ ] 没有 N+1 查询
- [ ] 没有内存泄漏
- [ ] 没有不必要的计算
- [ ] 关键路径有缓存

### 安全性
- [ ] 输入验证
- [ ] SQL 注入防护
- [ ] XSS 防护
- [ ] 敏感信息保护

### 测试
- [ ] 测试覆盖率 >= 80%
- [ ] 关键路径有测试
- [ ] 没有 mock 滥用
- [ ] 测试独立性

### 文档
- [ ] 关键函数有 JSDoc
- [ ] 复杂逻辑有注释
- [ ] README 更新
- [ ] CHANGELOG 更新
```

#### 审查结论

- ✅ **APPROVE**：可以合并
- ⚠️ **REQUEST CHANGES**：需要修改
- 💬 **COMMENT**：建议改进（非阻塞）

---

## 审查流程

### 1. 准备

**Reviewer 需要**：
- PR 链接或分支名
- 变更的 SHA
- 关联的 Spec 文件
- 任务计划

**禁止**：
- ❌ 没有上下文就审查
- ❌ 跳过 Spec 对照

### 2. 阅读代码

**独立阅读**：
- 不看 implementer 的解释
- 按文件逐个阅读
- 运行测试和 lint
- 必要时运行代码

### 3. 提出问题

**使用 AskUserQuestion 或评论**：
- 具体到文件和行号
- 引用代码片段
- 给出建议

**示例**：

```markdown
### 问题 1：缺少输入验证

**文件**：`src/services/user.ts:25`

**当前代码**：
```typescript
function createUser(input: any) {
  return db.save(input);
}
```

**问题**：
- `input: any` 缺乏类型约束
- 没有验证必填字段
- 没有处理边界情况

**建议**：
```typescript
function createUser(input: CreateUserInput) {
  validateInput(input);
  return db.save(input);
}
```
```

### 4. 处理反馈

**接收审查时**（reference: superpowers receiving-code-review）：

**禁止**：
- ❌ "You're absolutely right!"
- ❌ "Great point!"
- ❌ "Thanks for catching that!"

**应该**：
- 技术性回应
- 提供代码证据
- 同意就改代码
- 不同意就给出论据

---

## 多视角审查

### gstack 风格的视角

| 视角 | 关注点 | 代表角色 |
|------|-------|---------|
| **业务** | 功能是否解决真实问题 | Product |
| **技术** | 架构是否合理 | Tech Lead |
| **UX** | API/UI 是否易用 | Designer |
| **DX** | 实现和维护成本 | Senior Dev |

### 视角审查清单

#### 业务视角

- [ ] 这个功能用户真的需要吗？
- [ ] 是否解决了核心痛点？
- [ ] ROI 是否合理？

#### 技术视角

- [ ] 架构是否合理？
- [ ] 是否可扩展？
- [ ] 性能是否达标？
- [ ] 安全是否有保障？

#### UX 视角

- [ ] API 设计是否易用？
- [ ] 错误信息是否友好？
- [ ] 文档是否清晰？

#### DX 视角

- [ ] 代码可读性？
- [ ] 是否容易调试？
- [ ] 测试是否充分？
- [ ] 部署是否简单？

---

## 一致性分析

### 跨工件检查

```markdown
## 一致性分析报告

### 规范 → 计划
- [ ] 所有 FR 在计划中有对应任务
- [ ] 计划中没有超出规范范围的任务

### 计划 → 实现
- [ ] 所有任务都已完成
- [ ] 实现没有超出计划范围
- [ ] 命名与计划一致

### 规范 → 实现
- [ ] 所有 FR 已实现
- [ ] 所有成功标准已达成
- [ ] 关键实体已定义

### 实现 → 测试
- [ ] 所有 FR 有对应测试
- [ ] 所有成功标准有验证测试
- [ ] 测试覆盖所有边界
```

---

## 审查报告模板

```markdown
# Code Review Report

## 基本信息

- **PR/Branch**：[#123 / feature/xxx]
- **Reviewer**：[姓名]
- **日期**：YYYY-MM-DD
- **Spec**：[specs/xxx.spec.md]

## 阶段 1：Spec Compliance

**结论**：✅ PASS / ⚠️ NEEDS CHANGES / ❌ REJECT

### 通过项
- [x] 所有 FR 已实现
- [x] 成功标准已达成

### 问题项
- [ ] FR-003 未完整实现（文件：src/xxx.ts:42）

## 阶段 2：Code Quality

**结论**：✅ APPROVE / ⚠️ REQUEST CHANGES / 💬 COMMENT

### 通过项
- [x] 命名规范
- [x] 测试覆盖

### 建议项
- 💬 考虑提取公共逻辑（src/xxx.ts:55）

### 必须修改
- ⚠️ 函数过长（src/xxx.ts:80，120 行）

## 多视角评估

| 视角 | 评价 |
|------|------|
| 业务 | ✅ 满足需求 |
| 技术 | ⚠️ 性能待优化 |
| UX | ✅ API 友好 |
| DX | ✅ 代码可读 |

## 一致性分析

- 规范 ↔ 实现：✅ 一致
- 计划 ↔ 实现：✅ 一致

## 总结

- [ ] 总体通过
- [ ] 需要修改后可合并
- [ ] 必须重大修改

---

*Reviewer 签名：[姓名]*
*日期：YYYY-MM-DD*
```

---

## 与其他技能的协作

### 上游

- tdd-workflow（实现完成）
- implement（实现命令）

### 下游

- verification-before-completion（最终验证）
- finishing-a-development-branch（收尾）

---

## 心理陷阱与反驳

| 借口 | 反驳 |
|------|------|
| "时间紧，跳过审查" | Bug 修复时间更长 |
| "我写的我知道没问题" | 自我审查有盲点 |
| "改个 typo 而已" | 改 typo 也会引入 bug |
| "测试通过了" | 通过 ≠ 正确 |
| "spec 没说清楚" | 主动询问 spec 作者 |

---

## 哲学依据

| 来源 | 贡献 |
|------|------|
| **superpowers** | 双阶段 review、反表演性同意 |
| **gstack** | 多视角评审（CEO/Eng/Design/DX） |
| **spec-kit** | 一致性分析 |
| **工程哲学 v1** | 多视角评审 + 证据优于断言 |

---

*基于工程哲学 v1 制定*
*创建时间：2026-06-11*
*技能版本：v1.0*

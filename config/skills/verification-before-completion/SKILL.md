---
name: 完成前验证（verification-before-completion）
description: 任何"完成"宣称前自动加载——完成任务、修复 Bug、提交代码、合并 PR、发布版本、关 issue、回答"做完了吗"、"可以提交了吗"、"可以发布了吗"。强制跑命令看完整输出：测试、lint、type check、覆盖率。禁止"应该没问题"、"理论上是正确的"、"我跑过了"。It works ≠ I'm done。
use_when:
  - 任何"完成"宣称前(任务/功能/Bug 修复)
  - 提交代码 / 合并 PR 前
  - 发布版本 / 关闭 issue 前
  - 回答"做完了吗"/"可以提交了吗"
  - 用户说"我跑过了"(必须看到命令输出)
core_constraint:
  - 必跑命令看完整输出(测试/lint/type check/覆盖率)
  - 必看到 PASS 行号 + 退出码 0
  - 禁止"应该没问题"/"理论上是正确的"
  - 引用 1+ 条 ETHOS 哲学(Evidence Over Claims + Boil the Ocean)
  - 必含 frontmatter 3 段式
exit_when:
  - 用户明确说"先不验证,只讨论"
  - 仅是规划阶段(还未到实现完成)
  - 任务是文档/对话(不涉及代码)
---

> ETHOS: Evidence Over Claims + Boil the Ocean
>
> "我跑过了"不是证据,看到 `npm test` PASS 行号 + 覆盖率数字 + 退出码 0 才是证据。

# 完成前验证技能（Verification Before Completion）

> 基于 superpowers verification-before-completion
> 目的：跑命令看输出，再宣称成功
> 强制级别：P0 - 任何"完成"宣称前必须遵守

---

## 触发条件

**任何**以下场景之前宣称"完成"前必须触发：

- 任务完成
- 功能实现完成
- Bug 修复完成
- 提交代码
- 合并 PR
- 发布版本
- 关闭 issue

---

## 核心铁律

**"It works" 不是 "I'm done"**

**"应该没问题" 不是 "我验证过了"**

**完成 = 验证通过 + 证据完整**

---

## 必做清单（DO）

### 1. 跑命令

```bash
# 必须实际运行，而不是"我以为"
npm test
npm run lint
npm run type-check
npm run build
```

### 2. 看输出

**完整读取**，不是扫一眼：

- [ ] 看到 `pass` 数量
- [ ] 看到 `fail` 数量（必须为 0）
- [ ] 看到错误信息（如果有）
- [ ] 看到警告（评估严重性）

### 3. 确认状态

**明确表达**：

- ✅ "我运行了 `npm test`，看到 `15 passed, 0 failed`"
- ❌ "我跑了一下测试，应该没问题"

---

## 禁止清单（DON'T）

### ❌ 禁止 1：未运行就宣称完成

```markdown
❌ 错误：
"我修改了 X，应该已经修复了"

✅ 正确：
"我修改了 X，运行测试后看到 `15 passed, 0 failed`，Bug 已修复"
```

### ❌ 禁止 2：跑了但没看输出

```markdown
❌ 错误：
"我跑了 npm test，好像过了"

✅ 正确：
"我跑了 npm test，输出是 `15 passed, 0 failed`"
```

### ❌ 禁止 3：理论正确

```markdown
❌ 错误：
"代码看起来正确，应该没问题"

✅ 正确：
"我运行了相关测试，输出是 `X passed, 0 failed`"
```

### ❌ 禁止 4：部分验证

```markdown
❌ 错误：
"测试过了，lint 我相信也没问题"

✅ 正确：
"测试和 lint 都运行了，全部通过"
```

---

## 验证清单

### 任务完成前

- [ ] **所有测试通过**：跑 `npm test`（或对应命令），看到 `X passed, 0 failed`
- [ ] **Lint 通过**：跑 `npm run lint`，无错误
- [ ] **Type Check 通过**：跑 `npm run type-check`，无错误
- [ ] **构建成功**：跑 `npm run build`（如果适用），无错误
- [ ] **覆盖率达标**：覆盖率 >= 80%
- [ ] **手动验证关键路径**：实际运行应用，测试关键功能
- [ ] **文档更新**：CHANGELOG、README 等已更新

### 提交代码前

- [ ] 所有任务完成前验证项已通过
- [ ] 提交信息符合规范
- [ ] 没有遗留的 console.log / debugger
- [ ] 没有提交敏感信息

### PR 合并前

- [ ] 所有任务完成前验证项已通过
- [ ] CI 状态为绿
- [ ] Code Review 通过
- [ ] 至少 1 个审查者批准

### 发布版本前

- [ ] 所有任务完成前验证项已通过
- [ ] PR 合并前验证项已通过
- [ ] Staging 环境验证通过
- [ ] 回滚方案就绪

---

## 输出要求

### 验证报告模板

```markdown
# 验证报告

## 验证时间
YYYY-MM-DD HH:MM

## 验证项

### 1. 单元测试
- 命令：`npm test`
- 实际输出：
  ```
  > test
  > jest

  PASS  src/user.test.ts
  PASS  src/auth.test.ts
  
  Tests: 15 passed, 15 total
  ```
- 结果：✅ 通过（15 passed, 0 failed）

### 2. Lint
- 命令：`npm run lint`
- 实际输出：
  ```
  > lint
  > eslint .
  ✓ 0 problems
  ```
- 结果：✅ 通过（0 problems）

### 3. Type Check
- 命令：`npm run type-check`
- 实际输出：
  ```
  > tsc --noEmit
  (无输出)
  ```
- 结果：✅ 通过（无错误）

### 4. 覆盖率
- 命令：`npm run test:coverage`
- 实际输出：
  ```
  ========== Coverage summary ==========
  Statements: 85% (170/200)
  Branches: 80% (40/50)
  Functions: 90% (18/20)
  Lines: 85% (170/200)
  ======================================
  ```
- 结果：✅ 通过（85% >= 80%）

### 5. 构建
- 命令：`npm run build`
- 实际输出：
  ```
  > build
  > tsc
  Build successful
  ```
- 结果：✅ 通过

### 6. 手动验证
- 启动：`npm start`
- 操作：登录、创建用户、登出
- 结果：✅ 全部正常

## 总结

- [x] 所有验证项通过
- [x] 证据完整
- [x] 可以宣称完成

**结论：✅ 任务完成，可以提交**
```

---

## 验证失败时

### 必须执行

1. **明确报告失败**
   - "测试失败：3 passed, 2 failed"
   - 不要回避或粉饰

2. **报告失败内容**
   - 哪些测试失败？
   - 失败原因是什么？
   - 涉及哪些文件？

3. **不要宣称完成**
   - 失败时禁止说"完成"
   - 必须说"未完成，原因 XXX"

4. **下一步行动**
   - 修复 Bug
   - 重新验证

---

## 心理陷阱与反驳

| 借口 | 反驳 |
|------|------|
| "我跑了命令，输出说通过" | 跑命令看输出 ≠ 完成 |
| "测试都过了，肯定没问题" | 测试覆盖范围有限 |
| "我自己测过了，可以用" | 自测有盲点 |
| "用户说可以了" | 用户验收 ≠ 完整验证 |
| "时间紧，先合并吧" | 跑命令不花多少时间 |

---

## 与 TDD 铁律的关系

**TDD 是验证的一部分**：
- TDD 阶段：每个任务完成后必须测试通过
- verification 阶段：所有任务完成后必须完整验证

**TDD + Verification = 完整质量保证**

---

## 红线（任何一条都意味着未完成）

- [ ] 跑命令但没看输出
- [ ] 看了部分输出就宣称通过
- [ ] "应该没问题" 类的表述
- [ ] 部分验证就宣称全部完成
- [ ] 没运行就宣称"我相信没问题"

---

## 与其他技能的关系

### 上游

- tdd-workflow（任务实现完成）
- systematic-debugging（Bug 修复完成）
- code-review（审查通过）

### 下游

- 无（验证后即可提交/合并/发布）

### 强制关系

- 任何完成宣称前**必须**通过此技能
- 任何提交/合并/发布前**必须**通过此技能

---

## 哲学依据

| 来源 | 贡献 |
|------|------|
| **superpowers** | 完整证据链、跑命令看输出 |
| **工程哲学 v1** | 证据优于断言、跑命令看输出 |
| **gstack** | 完整的 ship 工作流 |

---

*基于 superpowers verification-before-completion + 工程哲学 v1*
*创建时间：2026-06-11*
*技能版本：v1.0*
*强制级别：P0*

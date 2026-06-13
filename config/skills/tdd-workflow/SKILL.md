---
name: TDD 工作流 v4.0（test-driven-development）
description: 写代码、修改代码、重构、补功能、加测试、跑测试失败时自动加载。RED-GREEN-REFACTOR 铁律：先写失败的测试（RED）→ 写最小代码使测试通过（GREEN）→ 重构消除重复（REFACTOR）。禁止任何形式的"先写后测"。🆕 v4.0 核心铁律已提取到 rules/tdd.md（智能生效），本 skill 保留完整工作流细节。
use_when:
  - 写任何生产代码前
  - 补功能 / 加测试时
  - 跑测试失败 / RED 必真发生时
  - 重构现有代码
  - 用户说"加测试"/"补测试覆盖率"
core_constraint:
  - 必走 RED→GREEN→REFACTOR 三步
  - RED 必真发生(不能 skip / 假断言 / 不跑)
  - 修测试不修实现(测试有 bug 改测试)
  - 引用 1+ 条 ETHOS 哲学
  - 必含 frontmatter 3 段式
exit_when:
  - 仅修改文档/配置(不涉及代码逻辑)
  - 仅修改 lockfile / .env / .gitignore 等豁免清单
  - 用户明确说"先跳过测试"
---

> ETHOS: Boil the Ocean + Evidence Over Claims
>
> 100% 测试覆盖不是"花哨",是"完整"的一部分。任何"完成"必须看到 `npm test` 实际 PASS,而不是"应该过了"。

# TDD 工作流技能 v4.0（Test-Driven Development）

> 基于工程哲学 v1 + superpowers TDD 铁律
> 铁律：NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
> v4.0 核心铁律已提取到 **rules/tdd.md**（智能生效），本 skill 保留完整工作流细节

---

## 🆕 v4.0 铁律分层

**rules/tdd.md**（智能生效，3 条铁律）：
1. RED 必真发生（不能 skip / 假断言 / 不跑）
2. 修测试不修实现（测试有 bug 改测试）
3. 配置文件豁免清单（lockfile / .env / .gitignore 等）

**skill/tdd-workflow**（按需加载，完整流程）：
- RED → GREEN → REFACTOR → COMMIT 四步细节
- 模板 / 命名规范 / 覆盖率 / Mock 策略
- 与 brainstorming / spec-driven-development / systematic-debugging 的协作

---

## 触发条件

- 实现任何生产代码
- 修复任何 Bug
- 添加任何新功能

---

## 核心铁律

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**

没有先写失败的测试，禁止写任何生产代码。

**"Violating the letter of the rules is violating the spirit of the rules."**

---

## 执行流程

### RED 阶段：写一个必定失败的测试

#### 1. 明确要测试的行为

```
问自己：
- 这个函数应该做什么？
- 输入是什么？输出是什么？
- 边界条件是什么？
- 错误情况如何处理？
```

#### 2. 写测试

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a user with valid input', () => {
      // Arrange：准备测试数据
      const input = {
        name: 'Alice',
        email: 'alice@example.com',
      };

      // Act：执行被测操作
      const user = userService.createUser(input);

      // Assert：验证结果
      expect(user).toEqual({
        id: expect.any(String),
        name: 'Alice',
        email: 'alice@example.com',
        createdAt: expect.any(Date),
      });
    });

    it('should throw error for invalid email', () => {
      // Arrange
      const input = { name: 'Bob', email: 'invalid' };

      // Act & Assert
      expect(() => userService.createUser(input)).toThrow('Invalid email');
    });
  });
});
```

#### 3. 运行测试，确认失败

```bash
npm test -- userService.test.ts
```

**确认失败原因**：
- ✅ 失败原因：函数未定义（符合预期）
- ❌ 失败原因：编译错误（测试本身有问题）

#### 4. RED 阶段检查清单

- [ ] 测试覆盖行为而非实现
- [ ] 测试必定失败
- [ ] 失败原因是功能未实现
- [ ] 没有 mock 掉关键逻辑

---

### GREEN 阶段：写最小代码通过测试

#### 1. 编写最小实现

```typescript
class UserService {
  createUser(input: CreateUserInput): User {
    if (!input.email.includes('@')) {
      throw new Error('Invalid email');
    }

    return {
      id: crypto.randomUUID(),
      name: input.name,
      email: input.email,
      createdAt: new Date(),
    };
  }
}
```

#### 2. 运行测试，确认通过

```bash
npm test -- userService.test.ts
```

#### 3. GREEN 阶段约束

**禁止**：
- ❌ 添加任何未测试的功能
- ❌ 提前优化
- ❌ 编写"以防万一"的代码
- ❌ 修改测试以适应实现

**允许**：
- ✅ 重复代码（REFACTOR 阶段会处理）
- ✅ 简单实现
- ✅ 硬编码（仅在测试中）

#### 4. GREEN 阶段检查清单

- [ ] 最小实现
- [ ] 所有测试通过
- [ ] 没有添加未测试的功能
- [ ] 没有修改测试

---

### REFACTOR 阶段：重构改进

#### 1. 识别改进点

```
问自己：
- 是否有重复代码？
- 命名是否清晰？
- 函数是否过长？
- 是否可以提取共用逻辑？
```

#### 2. 重构

```typescript
// 重构前
class UserService {
  createUser(input: CreateUserInput): User {
    if (!input.email.includes('@')) {
      throw new Error('Invalid email');
    }

    return {
      id: crypto.randomUUID(),
      name: input.name,
      email: input.email,
      createdAt: new Date(),
    };
  }
}

// 重构后
class UserService {
  createUser(input: CreateUserInput): User {
    this.validateEmail(input.email);
    return this.buildUser(input);
  }

  private validateEmail(email: string): void {
    if (!email.includes('@')) {
      throw new Error('Invalid email');
    }
  }

  private buildUser(input: CreateUserInput): User {
    return {
      id: crypto.randomUUID(),
      name: input.name,
      email: input.email,
      createdAt: new Date(),
    };
  }
}
```

#### 3. 每次重构后运行测试

```bash
npm test -- userService.test.ts
```

#### 4. REFACTOR 阶段约束

**允许**：
- ✅ 提取函数/类
- ✅ 改进命名
- ✅ 消除重复
- ✅ 改善结构

**禁止**：
- ❌ 添加新功能
- ❌ 修改测试
- ❌ 改变行为

#### 5. REFACTOR 阶段检查清单

- [ ] 行为没有改变（所有测试仍然通过）
- [ ] 命名更清晰
- [ ] 重复代码已消除
- [ ] 函数长度合理
- [ ] 没有引入新 Bug

---

## 红线标志（任何一条都意味着删除代码重写）

| 红线 | 含义 |
|------|------|
| **先写实现后补测试** | 违反 TDD 铁律 |
| **测试覆盖实现细节** | 测试应该测行为，不是实现 |
| **用 mock 替代真实依赖** | 失去测试价值 |
| **测试通过后继续"完善"** | 添加了未测试的代码 |
| **修改测试以通过** | 测试不再是规范 |
| **跳过 RED 阶段** | 没有失败测试就开始写 |
| **跳过 GREEN 验证** | 不确认测试通过就继续 |

---

## 常见反模式

### 1. Mock 滥用

```typescript
// ❌ 错误：mock 掉所有依赖
const mockDb = { save: jest.fn() };
const mockLogger = { info: jest.fn() };
const mockValidator = { validate: jest.fn() };

test('creates user', () => {
  const service = new UserService(mockDb, mockLogger, mockValidator);
  service.createUser(input);
  expect(mockDb.save).toHaveBeenCalled();
});
```

```typescript
// ✅ 正确：使用真实依赖或测试替身
test('creates user', () => {
  const db = new TestDatabase();
  const service = new UserService(db);

  const user = service.createUser(input);

  const saved = await db.findById(user.id);
  expect(saved).toEqual(user);
});
```

### 2. 私有方法测试

```typescript
// ❌ 错误
test('private validateEmail', () => {
  // ...
});
```

```typescript
// ✅ 正确：通过公共 API 测试
test('createUser with invalid email throws', () => {
  expect(() => service.createUser({ email: 'invalid' })).toThrow();
});
```

### 3. 断言不足

```typescript
// ❌ 错误
expect(result).toBeDefined();
```

```typescript
// ✅ 正确
expect(result).toEqual({
  id: expect.any(String),
  name: 'Alice',
  email: 'alice@example.com',
});
```

---

## 豁免场景

以下场景可豁免 TDD：

| 场景 | 说明 |
|------|------|
| 配置文件 | .env、config.yaml 等 |
| 文档文件 | README、注释等 |
| 一次性脚本 | 用完即弃的工具 |
| 原型/POC | 明确标注的实验代码 |

**豁免原则**：
- 必须明确标注（注释说明）
- 生产化时必须补回测试
- 不豁免核心业务逻辑

---

## 验证要求

### 完成每个任务后

```bash
# 1. 运行测试
npm test

# 2. 检查覆盖率
npm run test:coverage

# 3. 运行 lint
npm run lint

# 4. 运行 type check
npm run type-check
```

### 标准

- 测试通过率：100%
- 测试覆盖率：>= 80%
- Lint 错误：0
- Type 错误：0

---

## 与其他技能的协作

### 上游

- writing-plans（任务规划）
- 任何功能实现请求

### 下游

- code-review（实现完成后）
- verification-before-completion（任务收尾）

---

## 心理陷阱与反驳

### 借口 vs 反驳

| 借口 | 反驳 |
|------|------|
| "这只是个简单修改" | 删除代码，从 TDD 重新开始 |
| "测试太难写" | 说明测试目标，重新设计接口 |
| "我先看看代码" | 先写测试，再看代码 |
| "参考现有代码" | 不参考，从测试开始 |
| "时间紧迫" | 没有 TDD，调试时间更长 |
| "我先实现，再补测试" | 不会补的，现在就写测试 |

### Red Flags（立即停止并重写）

- "这个函数太简单了不需要测试"
- "我只是改一下，不影响其他"
- "测试可以之后再加"
- "我先实现个大概"

**任何一条出现 → 删除代码，从 TDD 重新开始**

---

## 哲学依据

| 来源 | 贡献 |
|------|------|
| **superpowers** | Iron Law、12 条 Red Flags、anti-patterns |
| **spec-kit** | 宪法条款 III（测试优先） |
| **工程哲学 v1** | 证据优于断言、Boil the Ocean |

---

*基于工程哲学 v1 制定*
*创建时间：2026-06-11*
*技能版本：v1.0*

---
name: 代码质量红线 v4.0（智能生效）
description: 写完任何代码模块后必须遵守的代码质量红线。来源：code-quality-reviewer specialist 核心约束。
alwaysApply: false
---

# 代码质量红线 v4.0（智能生效）

> 来源：原 `.trae/agents/specialists/code-quality-reviewer.md`
> 触发：写完任何代码模块后

---

## 6 大红线（任何一条触发即视为违规）

### 红线 1：函数长度 ≤ 50 行

- 包含函数签名、注释、空行
- 不含 import / 类的其他方法
- 例外：纯数据定义（如 enum、表驱动）可 ≤ 100 行
- 超过 → **必须**拆分

**反模式**：
```typescript
// ❌ 一个函数 200 行
function processOrder(order: Order) {
  // 50 行验证
  // 50 行计算
  // 50 行持久化
  // 50 行通知
}
```

**正例**：
```typescript
// ✅ 拆分为 4 个职责单一函数
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  const saved = persistOrder(order, total);
  notifyOrder(saved);
}
```

---

### 红线 2：圈复杂度 ≤ 10

- 圈复杂度 = 1 + 分支数（if / else / case / for / while / catch / && / || / 三元）
- 例外：纯 switch case 表驱动可 ≤ 15
- 超过 → **必须**用策略模式 / 表驱动 / 早返回重构

**反模式**：
```typescript
// ❌ 圈复杂度 15+ （嵌套 if 链）
function getDiscount(user) {
  if (user.level === 'gold') {
    if (user.years > 5) {
      if (user.spend > 1000) {
        // ...
      }
    }
  }
}
```

**正例**：
```typescript
// ✅ 表驱动 + 早返回
const DISCOUNT_TABLE = { /* ... */ };
function getDiscount(user) {
  const discount = DISCOUNT_TABLE[user.level];
  return user.years > 5 ? discount * 1.2 : discount;
}
```

---

### 红线 3：重复代码 ≤ 5 行

- 检测：相同 / 高度相似代码块出现 ≥ 2 次
- 超过 → **必须**抽象为函数 / 类 / 模板方法
- 例外：测试代码重复可接受（结构相似但断言不同）

---

### 红线 4：命名遵循语言约定

| 语言 | 变量 / 函数 | 类 / 类型 | 常量 | 私有 |
|------|------------|----------|------|------|
| JS / TS | camelCase | PascalCase | UPPER_SNAKE | _prefix |
| Python | snake_case | PascalCase | UPPER_SNAKE | _prefix |
| Go | camelCase / mixedCaps | PascalCase | camelCase | lowercase |
| Java | camelCase | PascalCase | UPPER_SNAKE | - |
| Rust | snake_case | PascalCase | UPPER_SNAKE | - |

- 名字**自我解释**（`getUserById` 而非 `fetch`）
- 缩写 ≤ 3 字母（`id` / `url` / `api` 可接受，`mgr` / `ctx` 不可）
- 布尔变量 / 函数用 `is` / `has` / `can` / `should` 前缀

**反模式**：
```typescript
const u = getU();      // ❌ u 是什么？
function proc(d) { }   // ❌ proc 是什么？
const arr = [];        // ❌ 什么 arr？
```

---

### 红线 5：注释解释 why 而非 what

- **不注释**：代码自我说明的内容（`i++ // i 加 1`）
- **必注释**：复杂业务逻辑 / 不显然的决策 / 性能考量 / 安全考量
- **禁止注释**：`// TODO: 实现 xxx`（必须立即做或用 issue 跟踪）

**正例**：
```typescript
// bcrypt cost 12: 平衡性能与安全 (~250ms per hash on 2026 CPU)
// 低于 12 易被 GPU 破解，高于 12 影响登录体验
const BCRYPT_COST = 12;
```

---

### 红线 6：无 magic number / string

- 任何数字 / 字符串字面量**必须**提常量（除 0/1/-1/null/undefined/""/true/false）
- 常量命名体现**业务含义**

**反模式**：
```typescript
if (attempts > 3) lock();          // ❌ 3 是什么？
setTimeout(retry, 86400000);       // ❌ 86400000 是什么？
```

**正例**：
```typescript
const MAX_LOGIN_ATTEMPTS = 3;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (attempts > MAX_LOGIN_ATTEMPTS) lock();
setTimeout(retry, ONE_DAY_MS);
```

---

## 验证工具（完成前必须跑）

| 工具 | 命令 | 阈值 |
|------|------|------|
| TypeScript | `tsc --noEmit` | 0 错误 |
| ESLint | `eslint .` | 0 错误（warning 可记录）|
| Prettier | `prettier --check .` | 100% 格式一致 |
| 测试覆盖率 | `npm run test:coverage` | ≥ 80% 全部维度 |
| 圈复杂度 | `npx complexity-report src/ --max-cpx 10` | 全部函数 ≤ 10 |

---

## 反模式（任何一条触发即视为违规）

- ❌ 函数 > 50 行
- ❌ 圈复杂度 > 10
- ❌ 重复代码 > 5 行（出现 ≥ 2 次）
- ❌ 命名违反语言约定
- ❌ 注释 "what" 而非 "why"
- ❌ Magic number / magic string
- ❌ `// TODO: 实现` 留在代码里
- ❌ `console.log` / `console.error` 留在生产代码
- ❌ 注释掉的代码（dead code）
- ❌ `any` 类型（TS） / 强转 (Go) 无注释

---

## 何时跳过质量红线

- **配置文件**（tsconfig.json / .eslintrc / .prettierrc）豁免
- **测试代码**部分红线豁免（重复可接受、命名可宽松）
- **临时脚本**（一次性运行的脚本）豁免
- **生成代码**（如 .d.ts / proto gen）豁免

---

*基于原 code-quality-reviewer specialist 重构*
*版本：v4.0*
*生效方式：智能生效（描述含"写完代码 / 代码审查 / 重构"等关键词时 AI 加载）*

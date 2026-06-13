---
name: API 审查 v4.0（api-review）
description: 新增 / 修改 / 评审任何 API 端点、HTTP 接口、REST / GraphQL / gRPC 路由自动加载。基于 RESTful 14 项 checklist + 错误码规范 + 契约测试强制审查。🆕 v4.0 替代原 specialists/api-reviewer.md。
use_when:
  - 新增/修改 API 端点
  - 评审 HTTP 接口
  - 涉及 REST / GraphQL / gRPC 路由
  - 看到"接口"/"端点"/"路由"时
core_constraint:
  - 必走 14 项 RESTful checklist
  - 必含错误码规范(4xx / 5xx 分类)
  - 必含契约测试
  - 引用 1+ 条 ETHOS 哲学
exit_when:
  - 仅修改内部函数(不暴露 API)
  - 仅加日志/监控(不改契约)
  - 用户明确说"先不做 API 审查"
---

> ETHOS: Boil the Ocean + Evidence Over Claims
>
> API 不是"能用就行",14 项 RESTful checklist 全部勾选才能避免后期 schema drift 和错误处理不一致。

# API 审查技能 v4.0（API Review）

> 替代 v3.0 `.trae/agents/specialists/api-reviewer.md`
> 强制级别：P1 - 任何 API 端点必须走此流程

---

## 触发条件

满足以下**任一**即自动加载：

- 新增 HTTP API 端点（`app.get/post/put/delete/patch`）
- 修改现有 API 端点（path / method / 参数 / 响应 / 错误码）
- 评审 / 调试任何 API 行为
- 用户提及"API" / "接口" / "路由" / "endpoint" / "REST" / "GraphQL" / "gRPC"
- 写 controller / route / handler 文件

---

## 14 项 RESTful Checklist

### 1. 命名：资源用复数名词

- ✅ `/users` / `/users/:id` / `/users/:id/orders`
- ❌ `/getUser` / `/user/list` / `/createUser`

**例外**：操作型端点可用动词（`/auth/login` / `/auth/logout` / `/search`）

---

### 2. HTTP Method 语义正确

| Method | 语义 | 幂等 | 副作用 |
|--------|------|------|--------|
| GET | 读取资源 | ✅ | 无 |
| POST | 创建资源 | ❌ | 有 |
| PUT | 全量更新 | ✅ | 有 |
| PATCH | 部分更新 | ❌ | 有 |
| DELETE | 删除资源 | ✅ | 有 |

- ✅ 读操作用 GET
- ✅ 创建用 POST
- ✅ 全量更新用 PUT，部分更新用 PATCH
- ❌ 禁止：GET 请求做写操作（除幂等操作如搜索）

---

### 3. HTTP 状态码使用正确

| 状态码 | 含义 | 何时用 |
|--------|------|--------|
| 200 | OK | 成功（GET / PATCH / PUT）|
| 201 | Created | 创建成功（POST）|
| 204 | No Content | 删除成功 / 无返回体 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限（认证了但不能访问）|
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突（如重复创建）|
| 422 | Unprocessable Entity | 验证失败（语法对但语义错）|
| 429 | Too Many Requests | 限流触发 |
| 500 | Internal Server Error | 服务器内部错误 |
| 503 | Service Unavailable | 服务不可用（维护 / 过载）|

**反模式**：
- ❌ 创建成功返回 200（应 201）
- ❌ 全部错误返回 500
- ❌ 缺认证返回 401 但实际是权限不够（应 403）

---

### 4. 错误响应格式统一

**正例**：
```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with id 123 does not exist",
    "details": {
      "userId": "123"
    }
  }
}
```

**反模式**：
```json
// ❌ 错误格式不统一
"User not found"
{ "error": "User not found" }
{ "code": 404, "message": "..." }
```

---

### 5. 分页：cursor 或 page+limit

- ✅ 大列表必须分页
- ✅ 推荐 cursor-based（`?cursor=xxx&limit=20`）
- ✅ 或 page+limit（`?page=1&limit=20`）
- ✅ 响应包含下一页 cursor / total

**正例**：
```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTIzfQ==",
    "hasMore": true
  }
}
```

**反模式**：
- ❌ 返回所有数据（无分页）→ 性能 / 内存 / 带宽问题

---

### 6. 过滤 / 排序 / 搜索

- ✅ `?status=active` / `?sort=-createdAt` / `?q=keyword`
- ✅ 过滤字段白名单（防 SQL 注入）
- ✅ 排序字段白名单
- ❌ 禁止：用户输入直接拼到 SQL

**正例**：
```typescript
const ALLOWED_SORT_FIELDS = ['createdAt', 'name', 'email'];
const sort = ALLOWED_SORT_FIELDS.includes(req.query.sort) ? req.query.sort : 'createdAt';
```

---

### 7. 幂等性

- ✅ PUT / DELETE 必须幂等
- ✅ POST 创建可加 idempotency key（`Idempotency-Key` header）
- ❌ 禁止：POST 重复创建产生多个资源

**正例**：
```typescript
// idempotency key 防重复支付
app.post('/api/orders', idempotencyMiddleware, createOrder);
```

---

### 8. 版本管理

- ✅ URL 版本（`/api/v1/users`）—— 推荐
- ✅ 或 header 版本（`Accept: application/vnd.myapi.v1+json`）
- ❌ 禁止：直接改 endpoint 行为而无版本

---

### 9. 认证

- ✅ 除公开端点外，必须有认证
- ✅ 用 `Authorization: Bearer <token>` 或 cookie session
- ✅ 公开端点白名单：`/auth/login` / `/auth/register` / `/health`
- ❌ 禁止：可读端点可匿名访问敏感数据

---

### 10. 限流

- ✅ 写操作：5-10 次/分钟
- ✅ 读操作：60-100 次/分钟
- ✅ 关键操作（login / forgot / 2FA）：3-10 次/分钟
- ✅ 返回 `429` + `Retry-After` header

**正例**：
```typescript
res.status(429).set('Retry-After', '60').json({
  error: { code: 'RATE_LIMITED', message: 'Too many requests' }
});
```

---

### 11. 缓存控制

- ✅ 读操作加 `Cache-Control` / `ETag`
- ✅ 写操作加 `Cache-Control: no-store`
- ✅ 静态资源 `Cache-Control: public, max-age=31536000`

---

### 12. 文档

- ✅ OpenAPI 3.0 (Swagger) 规范
- ✅ 包含：path / method / 参数 / 响应 / 错误码 / 鉴权要求
- ✅ 部署时自动生成客户端 SDK
- ❌ 禁止：文档与代码脱节（必须 code-first 生成）

---

### 13. 契约测试

- ✅ 端到端测试覆盖主流程
- ✅ 关键参数组合（边界 / null / 极大值 / 极小值 / 负数）
- ✅ 错误码测试（每个错误码至少 1 个测试）

**正例**：
```typescript
describe('POST /api/auth/login', () => {
  it('200 with valid credentials', ...);
  it('401 with wrong password', ...);
  it('429 with too many attempts', ...);
  it('423 with account locked', ...);
});
```

---

### 14. 一致性

- ✅ 命名一致：snake_case 或 camelCase 选一种
- ✅ 时间格式统一：ISO 8601（`2026-06-12T10:30:00Z`）
- ✅ ID 格式统一：UUID / 数字 / 字符串
- ✅ 大小写一致：路径用小写（`/users` 而非 `/Users`）
- ✅ 复数形式一致：`/users` 不用 `/user`

---

## API 设计模板

```typescript
// 路由
app.post('/api/v1/users', authenticate, validateUser, createUser);
app.get('/api/v1/users/:id', authenticate, getUser);
app.patch('/api/v1/users/:id', authenticate, authorize('admin'), updateUser);
app.delete('/api/v1/users/:id', authenticate, authorize('admin'), deleteUser);

// 控制器
async function createUser(req: Request, res: Response) {
  try {
    const user = await userService.create(req.body);
    res.status(201).json({ data: user });
  } catch (err) {
    if (err instanceof ValidationError) {
      return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: err.message, details: err.fields } });
    }
    if (err instanceof DuplicateEmailError) {
      return res.status(409).json({ error: { code: 'EMAIL_EXISTS', message: 'Email already registered' } });
    }
    log.error(err);
    res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
  }
}
```

---

## 联动 rules

- **rules/core.md 第 14 条**（强制加载红线）—— 完成后自动加载本 skill
- **rules/roles.md 第 4 个角色（api-reviewer）** —— 8 角色核心约束
- **rules/quality.md** —— API 代码也要符合质量红线
- **skill/security-review** —— API 安全（CSRF / 限流 / 错误泄露）

---

## 反模式（任何一条触发即视为违规）

- ❌ 资源命名用单数（`/user` 而非 `/users`）
- ❌ GET 请求做写操作
- ❌ 创建成功返回 200（应 201）
- ❌ 错误响应格式不统一
- ❌ 大列表无分页
- ❌ 过滤/排序字段无白名单
- ❌ POST 不幂等
- ❌ 改 endpoint 行为无版本
- ❌ 敏感端点无认证
- ❌ 写操作无限流
- ❌ 错误信息泄露栈追踪 / SQL 语句
- ❌ 文档与代码脱节

---

## API 审查报告模板

```markdown
# API 审查报告

## 基本信息
- 审查人：[SOLO Agent]
- 审查时间：YYYY-MM-DD
- 涉及端点：[GET /api/users / POST /api/users / ...]

## 14 项 Checklist

| # | 项目 | 状态 | 备注 |
|---|------|------|------|
| 1 | 命名（复数名词）| ✅ / ❌ | |
| 2 | HTTP Method 语义 | ✅ / ❌ | |
| 3 | HTTP 状态码 | ✅ / ❌ | |
| 4 | 错误响应格式 | ✅ / ❌ | |
| 5 | 分页 | ✅ / ❌ | |
| 6 | 过滤/排序/搜索 | ✅ / ❌ | |
| 7 | 幂等性 | ✅ / ❌ | |
| 8 | 版本管理 | ✅ / ❌ | |
| 9 | 认证 | ✅ / ❌ | |
| 10 | 限流 | ✅ / ❌ | |
| 11 | 缓存控制 | ✅ / ❌ | |
| 12 | 文档 | ✅ / ❌ | |
| 13 | 契约测试 | ✅ / ❌ | |
| 14 | 一致性 | ✅ / ❌ | |

## 安全相关（联动 security-review）
- [ ] CSRF 防护
- [ ] SQL 注入防御
- [ ] XSS 防护
- [ ] 审计日志
- [ ] HTTPS only

## 总结
- 通过 / 不通过
- 必须修复的问题数
- 建议改进的问题数

---

*审查人签名*
*日期*
```

---

## 与其他技能的关系

### 上游
- 任何含 API 端点的任务

### 下游
- skill/security-review（API 安全）
- skill/tdd-workflow（API 也要 TDD）
- skill/verification-before-completion（完成前必走）

### 平行
- skill/spec-driven-development（API 设计在 spec 中）

---

## 哲学依据

| 来源 | 贡献 |
|------|------|
| **RESTful 规范** | Roy Fielding 论文 / OpenAPI 3.0 |
| **HTTP RFC** | 9110 (语义) / 6585 (429) / 7807 (错误格式) |
| **工程哲学 v1** | 证据优于断言、完整实现 |
| **v3.0 api-reviewer specialist** | 8 角色 api-reviewer 的核心约束 |
| **v4.0 重构** | 从 agent 文件迁到 skill |

---

*基于 RESTful 规范 + HTTP RFC + 工程哲学 v1 + 原 api-reviewer specialist*
*创建时间：2026-06-13*
*技能版本：v4.0*
*强制级别：P1*

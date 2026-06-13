---
name: 安全审查 v4.0（security-review）
description: 含密码 / Token / 2FA / TOTP / CSRF / 限流 / 加密 / OAuth / JWT / session / cookie / 审计 / 登录 / 鉴权 / 授权 / 敏感数据 / SQL / XSS / SQL注入 / 暴力破解 / 密码重置 / 邮箱验证 / 身份验证 / 访问控制 / 数据库存储密码 / 哈希 / bcrypt / argon2 的代码自动加载。基于 OWASP Top 10 + 9 项安全 checklist 强制审查。🆕 v4.0 替代原 specialists/cso.md。
use_when:
  - 含密码/Token/2FA/TOTP/CSRF/限流
  - 含 OAuth/JWT/session/cookie/审计
  - 涉及登录/鉴权/授权/敏感数据
  - 看到 SQL/XSS/SQL 注入/暴力破解
core_constraint:
  - 必走 9 项安全 checklist
  - 必含 OWASP Top 10 速查
  - 必含严重程度分级
  - 引用 1+ 条 ETHOS 哲学
exit_when:
  - 无任何安全敏感代码
  - 用户明确说"这是 demo,不用审查"
  - 单文件 demo(非生产)
---
---

> ETHOS: Boil the Ocean + Evidence Over Claims
>
> 安全不是"加个 helmet",而是 9 项 checklist 全部勾选,任何一条遗漏都是 OWASP Top 10 漏洞的入口。

# 安全审查技能 v4.0（Security Review）

> 替代 v3.0 `.trae/agents/specialists/cso.md`
> 基于 OWASP Top 10 + 工程哲学 v1
> 强制级别：P1 - 任何安全相关代码必须走此流程

---

## 触发条件

满足以下**任一**即自动加载：

- 含**密码**处理（hash / 存储 / 验证 / 重置）
- 含**Token**（JWT / OAuth / access token / refresh token / session token）
- 含**2FA / MFA / TOTP**（双因素 / 二次验证 / 一次性码 / 备份码）
- 含**CSRF** 防护（双 token / SameSite cookie）
- 含**Rate Limiting**（限流 / 防爆破 / 防 DoS）
- 含**加密**（对称 / 非对称 / 哈希 / 签名）
- 含**Cookie / Session**（会话管理 / cookie 设置）
- 含**审计日志**（敏感操作记录 / access log / security log）
- 含**邮箱验证**（邮件链接 / 验证码）
- 含**登录 / 鉴权 / 授权**（login / auth / permission / role）
- 含**敏感数据**（身份证 / 银行卡 / 手机号 / 地址 / 密钥）
- 含**数据库密码 / API key** 存储
- 用户提及"安全" / "security" / "加密" / "权限" / "漏洞"

---

## 9 项安全 Checklist（任何一项未通过即视为不通过）

### 1. 密码哈希

- ✅ 算法：bcrypt（cost ≥ 12）或 argon2id
- ❌ 禁止：MD5 / SHA1 / SHA256 直接哈希（无盐 / 无 cost）
- ❌ 禁止：明文存密码
- ❌ 禁止：可逆加密存密码

**正例**：
```typescript
import bcrypt from 'bcrypt';
const BCRYPT_COST = 12;
const hash = await bcrypt.hash(password, BCRYPT_COST);
const match = await bcrypt.compare(password, hash);
```

**反模式**：
```typescript
// ❌ 永远不要这样做
const hash = crypto.createHash('md5').update(password).digest('hex');
// ❌ 永远不要明文存
db.users.insert({ password }); // password is plaintext!
```

---

### 2. Token 过期

- ✅ JWT 必须有 `exp` 声明
- ✅ 过期时间 ≤ 7 天（推荐 1 小时 access + 7 天 refresh）
- ❌ 禁止：永不过期的 token

**正例**：
```typescript
const accessToken = jwt.sign(payload, secret, { expiresIn: '1h' });
const refreshToken = jwt.sign(payload, secret, { expiresIn: '7d' });
```

**反模式**：
```typescript
// ❌ 永不过期
const token = jwt.sign(payload, secret);  // 没有 expiresIn
```

---

### 3. Token 存储

- ✅ Access token：可前端 localStorage（若允许）或 HttpOnly cookie
- ✅ Refresh token：必须 HttpOnly + Secure + SameSite=Strict cookie
- ❌ 禁止：明文存 token 到 DB（必须 hash 后存）
- ❌ 禁止：localStorage 存 refresh token（XSS 可盗）

**正例**：
```typescript
// refresh token 存 hash
const tokenHash = crypto.createHash('sha256').update(refreshToken).digest('hex');
db.refreshTokens.insert({ userId, tokenHash, expiresAt });
```

**反模式**：
```typescript
// ❌ 明文存 token
db.refreshTokens.insert({ userId, token: refreshToken });
```

---

### 4. CSRF 防护

- ✅ 写操作：双 token 模式（CSRF token + session token）
- ✅ SameSite=Strict / Lax cookie
- ✅ Origin / Referer header 校验
- ❌ 禁止：仅靠 cookie 认证的写操作

**正例**：
```typescript
// CSRF token
const csrfToken = crypto.randomBytes(32).toString('hex');
res.cookie('XSRF-TOKEN', csrfToken, { httpOnly: false, secure: true, sameSite: 'strict' });
// 前端读 cookie 并 echo 到 header
// 后端校验 cookie === header
```

**反模式**：
```typescript
// ❌ 没有 CSRF 保护
app.post('/api/transfer', authenticate, handler);
```

---

### 5. SQL 注入

- ✅ 用 ORM / 参数化查询
- ✅ 输入验证（白名单）
- ❌ 禁止：字符串拼接 SQL
- ❌ 禁止：用户输入直接进 SQL

**正例**：
```typescript
// ✅ 参数化查询
db.query('SELECT * FROM users WHERE id = ?', [userId]);
// ✅ ORM
db.users.findOne({ where: { id: userId } });
```

**反模式**：
```typescript
// ❌ 字符串拼接（SQL 注入）
db.query(`SELECT * FROM users WHERE id = '${userId}'`);
```

---

### 6. XSS 防护

- ✅ 输出转义（前端用框架默认转义，React/Vue 都安全）
- ✅ CSP（Content-Security-Policy）header
- ❌ 禁止：`innerHTML` 拼接用户输入
- ❌ 禁止：`dangerouslySetInnerHTML` 用未净化内容

**正例**：
```tsx
// React 自动转义
<div>{userInput}</div>
```

**反模式**：
```tsx
// ❌ 拼接 HTML
element.innerHTML = `<div>${userInput}</div>`;
```

---

### 7. Rate Limiting

- ✅ Login：10 次/分钟/IP
- ✅ Forgot password：5 次/小时/邮箱
- ✅ Register：3 次/小时/IP
- ✅ 2FA verify：5 次/分钟/会话
- ✅ 用 `express-rate-limit` / Redis / sliding window

**正例**：
```typescript
import rateLimit from 'express-rate-limit';
const loginLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 10,
  message: 'Too many login attempts, please try again later.'
});
app.post('/api/auth/login', loginLimiter, loginHandler);
```

**反模式**：
```typescript
// ❌ 没有限流 → 暴力破解
app.post('/api/auth/login', loginHandler);
```

---

### 8. 审计日志

- ✅ 敏感操作必记录：login / logout / password change / 2FA enable / admin action
- ✅ 记录字段：userId / action / ip / userAgent / timestamp / result
- ✅ 日志不可被普通用户删除
- ❌ 禁止：日志含明文密码 / token

**正例**：
```typescript
auditLog.record({
  userId,
  action: 'login_success',
  ip: req.ip,
  userAgent: req.headers['user-agent'],
  timestamp: new Date()
});
```

**反模式**：
```typescript
// ❌ 不记录敏感操作
// （用户登录后没有任何日志 → 无法溯源）
```

---

### 9. 加密传输

- ✅ HTTPS（生产环境必须）
- ✅ HSTS header
- ✅ Cookie Secure flag
- ❌ 禁止：HTTP 传密码 / token

**正例**：
```typescript
res.cookie('session', token, {
  httpOnly: true,
  secure: true,      // HTTPS only
  sameSite: 'strict',
  maxAge: 3600000
});
```

---

## OWASP Top 10 速查（2021 版）

| 排名 | 名称 | 防御 |
|------|------|------|
| A01 | 访问控制破坏 | RBAC / 最小权限 / 默认拒绝 |
| A02 | 加密失败 | HTTPS / 强算法 / 密钥管理 |
| A03 | 注入 | 参数化查询 / 输入验证 |
| A04 | 不安全设计 | Threat modeling / 安全设计模式 |
| A05 | 安全配置错误 | 最小化配置 / 默认安全 |
| A06 | 脆弱过时组件 | 依赖扫描 / 及时更新 |
| A07 | 身份认证失败 | MFA / 强密码策略 / 限流 |
| A08 | 软件数据完整性失败 | 签名 / 校验和 / 供应链审计 |
| A09 | 安全日志监控失败 | 审计日志 / 异常告警 |
| A10 | SSRF | URL 白名单 / 隔离网络 |

---

## 严重程度分级

| 级别 | 描述 | 示例 | 修复时限 |
|------|------|------|----------|
| 🔴 **Critical** | 可远程利用 + 影响大量用户 | SQL 注入 / 硬编码密钥 / RCE | 立即 |
| 🟠 **High** | 可利用但需特定条件 | CSRF / 缺少限流 / XSS | 24h |
| 🟡 **Medium** | 难利用 / 影响小 | 信息泄露 / 弱加密 | 7 天 |
| 🟢 **Low** | 理论风险 / 最佳实践违反 | 缺少 HSTS / cookie 缺 Secure | 30 天 |
| ⚪ **Info** | 建议改进 | 注释 / 文档 | 1 季度 |

---

## 联动 rules

- **rules/core.md 第 5 条**（安全边界）—— 涉及安全代码必须审查
- **rules/core.md 第 14 条**（强制加载红线）—— 完成后自动加载本 skill
- **rules/roles.md 第 5 个角色（cso）** —— 8 角色核心约束
- **rules/quality.md** —— 安全代码也需符合质量红线

---

## 反模式（任何一条触发即视为违规）

- ❌ MD5 / SHA1 / SHA256 哈希密码
- ❌ 永不过期的 JWT
- ❌ 明文存 token 到数据库
- ❌ 写操作没有 CSRF 保护
- ❌ 字符串拼接 SQL
- ❌ 拼接用户输入到 innerHTML
- ❌ Login / 敏感操作没有 Rate Limiting
- ❌ 敏感操作不记录审计日志
- ❌ 生产环境 HTTP（非 HTTPS）
- ❌ 硬编码密钥 / API key / 密码
- ❌ 错误信息泄露敏感细节（栈追踪 / SQL 语句）

---

## 安全审查报告模板

```markdown
# 安全审查报告

## 基本信息
- 审查人：[SOLO Agent]
- 审查时间：YYYY-MM-DD
- 涉及文件：[文件列表]
- 触发原因：[密码 / Token / 2FA / ...]

## 9 项 Checklist

| # | 项目 | 状态 | 备注 |
|---|------|------|------|
| 1 | 密码哈希 | ✅ / ❌ | |
| 2 | Token 过期 | ✅ / ❌ | |
| 3 | Token 存储 | ✅ / ❌ | |
| 4 | CSRF 防护 | ✅ / ❌ | |
| 5 | SQL 注入 | ✅ / ❌ | |
| 6 | XSS 防护 | ✅ / ❌ | |
| 7 | Rate Limiting | ✅ / ❌ | |
| 8 | 审计日志 | ✅ / ❌ | |
| 9 | 加密传输 | ✅ / ❌ | |

## 发现问题

| 严重程度 | 问题 | 文件:行号 | 建议修复 |
|----------|------|-----------|----------|
| 🔴 | | | |
| 🟠 | | | |
| 🟡 | | | |

## 总结
- 通过 / 不通过
- 必须修复的 Critical / High 问题数

---

*审查人签名*
*日期*
```

---

## 与其他技能的关系

### 上游
- 任何含安全代码的任务

### 下游
- tdd-workflow（安全代码也要 TDD）
- verification-before-completion（完成前必走）

### 平行
- api-review（API 设计与安全相关）
- code-quality-reviewer（代码质量）

---

## 哲学依据

| 来源 | 贡献 |
|------|------|
| **OWASP Top 10** | 风险分类、防御指南 |
| **工程哲学 v1** | 证据优于断言、完整实现 |
| **v3.0 cso specialist** | 8 角色 cso 角色的核心约束 |
| **v4.0 重构** | 从 agent 文件迁到 skill |

---

*基于 OWASP Top 10 + 工程哲学 v1 + 原 cso specialist*
*创建时间：2026-06-13*
*技能版本：v4.0*
*强制级别：P1*

---
name: 角色约束 v4.0（智能生效）
description: 8 个 specialist 角色的核心约束。v3.0 中这些约束散落在 .trae/agents/specialists/ 下未生效；v4.0 拆解为 rules + skills 双层。
alwaysApply: false
---

# 角色约束 v4.0（智能生效）

> 8 个角色 = 原 specialists/ 下的 8 个文件
> 核心约束 → 本文件（智能生效）
> 详细工作流 → skills/ 对应 skill

---

## 角色速查表

| # | 角色 | 核心约束（≤5 条） | 详细工作流 |
|---|------|------------------|------------|
| 1 | spec-reviewer | FR 编号连续 / 输入输出错误码齐全 / 成功标准可度量 | skill/spec-driven-development |
| 2 | design-reviewer | YAGNI / 模块边界清晰 / 接口契约明确 | skill/spec-driven-development |
| 3 | code-quality-reviewer | 函数≤50 行 / 圈复杂度≤10 / 命名遵循语言约定 | rules/quality.md |
| 4 | api-reviewer | RESTful 14 项 / 错误码统一 / 认证与限流 | skill/api-review |
| 5 | cso (Chief Security Officer) | OWASP Top 10 / 密码 bcrypt≥12 / Token 过期 | skill/security-review |
| 6 | scope-reviewer | YAGNI / 不超 3 个新文件 / 复用现有模块 | skill/brainstorming |
| 7 | plan-reviewer | 任务 2-5 分钟 / DAG 依赖正确 / TDD 步骤内嵌 | skill/plan-driven-development |
| 8 | test-reviewer | 覆盖率 ≥ 80% / 边界用例 / mock 隔离 | skill/tdd-workflow |

---

## 各角色核心约束详情

### 1. spec-reviewer（规范审查员）

**约束**：
- FR 编号必须连续（FR-001 / FR-002 / ...），不跳号
- 每个 FR 必须含 **输入 / 输出 / 错误处理** 三段
- 成功标准（SC）必须**可度量**（含数字 / 阈值 / 时间）
- 关键实体必须有**字段表**（字段名 / 类型 / 描述）
- 假设 / 依赖 / 非目标 三节必须存在

**触发场景**：写完任何 spec.md / 收到 spec 评审请求

**反模式**：
- ❌ FR 写"系统应支持用户管理"（无输入输出）
- ❌ 成功标准写"系统应该好用"（不可度量）

---

### 2. design-reviewer（设计审查员）

**约束**：
- 严守 **YAGNI**（You Aren't Gonna Need It）：不设计未明确要求的能力
- 模块边界清晰：一个模块一个职责
- 接口契约**显式**（参数类型 / 返回类型 / 异常）
- 拆分粒度受 **3 个新文件** 约束（v3.0 铁律 #8）

**触发场景**：重构 / 模块拆分 / 新建核心服务

**反模式**：
- ❌ "为了未来扩展，我们预留一个 plugin system"（YAGNI 违反）
- ❌ 一个类 > 500 行

---

### 3. code-quality-reviewer（代码质量审查员）

**约束**：
- 函数 ≤ 50 行
- 圈复杂度 ≤ 10
- 重复代码 ≤ 5 行（否则抽象）
- 命名遵循语言约定（JS 驼峰 / Python 蛇形 / 常量大写下划线）
- 注释解释 **why** 而非 what
- 无 magic number（必须提常量）

**详细红线**：见 `rules/quality.md`

**触发场景**：写完任何代码模块后

---

### 4. api-reviewer（API 审查员）

**约束**：
- RESTful 命名规范（资源用复数名词 / 动词用 HTTP Method）
- HTTP 状态码使用正确（200/201/204/400/401/403/404/409/422/429/500/503）
- 错误响应格式统一（`{ error: { code, message } }`）
- 必须有认证（除公开端点）
- 写操作必须有 CSRF 保护
- 限流：login 10/min / forgot 5/h / register 3/h
- API 文档（OpenAPI / Swagger）必填

**详细清单**：见 `skill/api-review`

**触发场景**：新增 / 修改 / 评审任何 API 端点

---

### 5. cso / Chief Security Officer（安全负责人）

**约束**：
- 密码 bcrypt ≥ 12 rounds（或 argon2）
- JWT 必须有过期时间（推荐 ≤ 7d）
- 任何 token 必须 hash 后存储（不能明文存 DB）
- 防 SQL 注入（用 ORM / 参数化查询）
- 防 XSS（输出转义）
- 防 CSRF（双 token / SameSite cookie）
- 限流（防爆破 / 防 DoS）
- 审计日志（敏感操作必记录）
- 加密传输（HTTPS）

**详细清单**：见 `skill/security-review`

**触发场景**：含密码 / Token / 2FA / TOTP / CSRF / 限流 / 加密 / OAuth / JWT / session / cookie / 审计的代码

---

### 6. scope-reviewer（范围审查员）

**约束**：
- **YAGNI 严格**执行（v3.0 铁律 #8）
- 不超 **3 个新文件**（除非经 HARD-GATE 与用户确认）
- **复用**现有模块（禁止重新发明轮子）
- 拒绝 scope creep（用户临时加需求必须**单独**评估）

**详细 5 问 + 3 方案流程**：见 `skill/brainstorming`

**触发场景**：brainstorming 第一阶段 / 任何需求澄清场景

---

### 7. plan-reviewer（计划审查员）

**约束**：
- 任务粒度 **2-5 分钟**
- DAG 依赖显式（用 depends on / 阶段标记）
- TDD 步骤内嵌（每个组件任务含 RED/GREEN 标记）
- 关键节点有**验证手段**（跑测试 / 跑命令）
- 配置文件豁免清单：lockfile / .env / .gitignore

**详细模板**：见 `skill/plan-driven-development`

**触发场景**：spec 完成后 / 拆分任务时

---

### 8. test-reviewer（测试审查员）

**约束**：
- 覆盖率 **≥ 80%**（statements / branches / functions / lines）
- 边界用例：空数组 / null / 极大值 / 极小值 / 负数
- Mock 隔离：单元测试不依赖外部资源（DB / 网络）
- 测试命名规范：`describe('Component.method')` + `it('should ... when ...')`
- 失败信息可读（错误时打印关键变量）

**详细模板**：见 `skill/tdd-workflow`

**触发场景**：写完任何测试 / 测试通过后做覆盖率审查

---

## 角色冲突解决

当多个角色的约束冲突时，按以下优先级：

1. **核心铁律**（rules/core.md）优先级最高
2. **cso** > 其他（安全相关永远优先）
3. **code-quality-reviewer** > 业务角色（代码质量底线）
4. **scope-reviewer** 反对 = 需用户 HARD-GATE
5. 其他按需调和

---

## 8 角色 × 触发词矩阵

| 触发词 / 场景 | 触发角色 |
|--------------|---------|
| 写 spec / 评审 spec | spec-reviewer |
| 重构 / 拆分模块 | design-reviewer + code-quality-reviewer |
| 写完代码 | code-quality-reviewer |
| 新增 / 修改 API | api-reviewer + cso |
| 含密码 / Token / 2FA | cso |
| 需求澄清 | scope-reviewer |
| 拆任务 / 写 plan | plan-reviewer |
| 写完测试 | test-reviewer |

---

*基于原 `.trae/agents/specialists/` 8 文件内容重构*
*版本：v4.0*
*生效方式：智能生效（alwaysApply: false，AI 根据 description 判断相关性）*

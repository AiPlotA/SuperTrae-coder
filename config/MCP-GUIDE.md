# MCP 配置指南

> 基于工程哲学 v1
> 适配 TRAE IDE 的 MCP Server 配置

---

## 一、推荐 MCP Server 清单

### 1.1 开发辅助类（必装）

| MCP Server | 用途 | 推荐度 | 配置方式 |
|-----------|------|-------|---------|
| **Playwright** | E2E 测试、浏览器自动化 | ★★★★★ | stdio |
| **Fetch** | 网页内容获取、文档抓取 | ★★★★★ | stdio |
| **Filesystem** | 文件系统增强 | ★★★★ | stdio |
| **Git** | Git 操作增强 | ★★★★ | stdio |

### 1.2 文档类（推荐）

| MCP Server | 用途 | 推荐度 |
|-----------|------|-------|
| **Context7** | 库文档查询 | ★★★★★ |
| **Memory** | 跨会话记忆 | ★★★★ |

---

## 二、Playwright MCP 配置

### 用途

- E2E 自动化测试
- 视觉回归测试
- 浏览器调试
- 页面截图

### 安装

```bash
npm install -g @playwright/mcp
```

### TRAE 配置

在 TRAE IDE 设置中：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

### 使用场景

#### E2E 测试

```
用户：跑一下用户登录的 E2E 测试
AI：（调用 Playwright MCP 打开浏览器，执行测试步骤，截图）
```

#### 视觉回归

```
用户：检查首页是否有视觉变化
AI：（截图当前页面，与基线对比，报告差异）
```

---

## 三、Fetch MCP 配置

### 用途

- 获取最新文档
- 查询 API 规范
- 抓取网页内容

### 安装

```bash
npm install -g @modelcontextprotocol/server-fetch
```

### TRAE 配置

```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

### 使用场景

```
用户：React 19 的新特性是什么？
AI：（调用 Fetch MCP 获取最新文档）
```

---

## 四、安全配置

### 4.1 白名单/黑名单

**推荐设置**：

```
对话流 > 自动运行 > MCP Server
├── [x] 使用黑名单（推荐）
└── 黑名单配置：
    ├── 文件系统删除操作
    ├── 网络请求（非 GET）
    ├── 命令执行
    └── 数据库 DROP/TRUNCATE
```

### 4.2 沙箱运行

- 所有 MCP 命令应在受限环境执行
- 禁止直接操作生产环境
- 敏感操作必须人工确认

---

## 五、基于工程哲学的使用建议

### 5.1 Playwright MCP

**与哲学的映射**：

| 哲学原则 | Playwright 价值 |
|---------|----------------|
| 原则 8：证据优于断言 | 跑测试看截图，而非"应该没问题" |
| 原则 6：多视角评审 | 视觉评审 + 功能评审 |
| 条款 II：TDD 铁律 | E2E 测试自动化 |

**使用流程**：

```
1. TDD 编写 E2E 测试
2. 运行 Playwright MCP
3. 截图记录结果
4. 报告发现的问题
```

### 5.2 Fetch MCP

**与哲学的映射**：

| 哲学原则 | Fetch 价值 |
|---------|----------|
| 原则 5：先搜索再构建 | 获取最新方案 |
| 原则 3：用户主权 | 给用户最新信息做决策 |

**使用流程**：

```
1. 遇到技术选型问题
2. 使用 Fetch 获取最新文档
3. 比较多个方案
4. 向用户推荐
```

---

## 六、项目级 MCP 配置模板

在项目根目录创建 `mcp.json`：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"],
      "description": "E2E 测试和浏览器自动化"
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"],
      "description": "获取网页内容"
    }
  }
}
```

---

## 七、常见问题

### Q1：MCP 加载失败？

**排查**：
1. 检查 Node.js 版本（>= 18）
2. 检查 npx 是否可用
3. 查看 TRAE 控制台错误
4. 重启 TRAE IDE

### Q2：如何选择 MCP Server？

**原则**：
- 优先满足核心需求（Playwright + Fetch）
- 按需添加，避免过多 MCP
- 每个 MCP 都应有明确用途

### Q3：MCP 性能影响？

**建议**：
- 避免同时启用超过 5 个 MCP
- 按需调用，而非全量加载
- 缓存常用结果

---

## 八、基于

- 工程哲学 v1 原则 5：先搜索再构建
- 工程哲学 v1 原则 8：证据优于断言
- TRAE IDE MCP 配置最佳实践

---

*创建时间：2026-06-11*

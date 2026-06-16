# SuperTrae-coder

> **TRAE IDE 的工程哲学配置集 —— 把 gstack / superpowers / spec-kit / OpenSpec 四大开源项目的工程纪律，落地为 TRAE SOLO Agent 自动遵守的配置**。
>
> v1.0.0 · 2026-06-13 · MIT License

---

## 这是什么

**SuperTrae-coder** 是一个开箱即用的 TRAE IDE 配置集。开发者把它复制到自己的项目根目录，TRAE SOLO Agent 就会自动加载 14 条核心铁律 + 6 个 Rules + 20 个 Skills + 5 条工程哲学，从「被动对话」升级为「自律执行」。

核心目标：
- **零显式调用**：不需要 `/spec`、`@spec-reviewer`、`#Rule`，直接和 SOLO Agent 说话
- **工程纪律强制落地**：TDD / 规范先行 / 完整实现 / 证据优于断言 / Bug 修复红线全部内建
- **质量门控可验证**：附带 11 个独立 CI checker，不依赖 TRAE 也能跑

---

## 快速开始

### 1. 一行安装（推荐）

```bash
# 在你的目标项目根目录执行
CODE_AGENT_NAME=".trae"  # 可自定义其他编程代理，默认 .trae，例如 .codex 等
git clone https://github.com/AiPlotA/SuperTrae-coder.git .trae-bootstrap \
  && cp -r .trae-bootstrap/config/* $CODE_AGENT_NAME/ \
  && cp -r .trae-bootstrap/scripts scripts \
  && rm -rf .trae-bootstrap
```

### 2. TRAE IDE 设置（必做）

1. 打开 TRAE IDE → 设置 → 规则
2. **开启"将 AGENTS.md 包含在上下文中"**（关键）
3. 启用 `.trae/rules/` 规则目录（始终加载 + 智能加载）
4. 启用 `.trae/skills/` 技能目录

### 3. 验证

```bash
# 跑全部 11 个 checker
bash scripts/validate-config.sh

# 只跑单个 checker
bash scripts/validate-config.sh --checker spec
bash scripts/validate-config.sh --checker 3_segment

# 详细输出（看 soft 警告）
bash scripts/validate-config.sh --verbose

# JSON 输出（供 GitHub Actions / pre-commit 消费）
bash scripts/validate-config.sh --json
```

### 4. 零显式调用示例

| 你说 | SOLO Agent 自动做的事 |
|------|----------------------|
| "帮我加一个用户登录功能" | 加载 `brainstorming` skill → 询问 5 个核心问题 |
| "我开始写代码了" | 加载 `tdd-workflow` skill → 强制 RED-GREEN-REFACTOR |
| "为什么不工作了？" | 加载 `systematic-debugging` skill → 4 阶段根因分析 |
| "做完了，可以提交吗？" | 加载 `verification-before-completion` skill → 跑测试、lint、覆盖率 |
| "帮我看看这代码" | 加载 `code-review` skill → 双阶段独立审查 |
| "涉及 API 端点" | 加载 `api-review` skill → RESTful 14 项 + 错误码 + 契约 |
| "含密码 / Token / 2FA" | 加载 `security-review` skill → OWASP Top 10 + 9 项 checklist |
| "我有个 idea 想做" | 加载 `office-hours` skill → 5 强制问题 + 3 方案 |
| "评估下我的项目" | 加载 `autoplan` skill → 5 维度 plan-mode 串联 |
| "涉及 React 组件" | 加载 `rules/quality.md`（设计模式 + 代码质量）|
| "涉及 API 设计" | 加载 `api-review` + `security-review` skills |

---

## 目录结构

```
SuperTrae-coder/
├── README.md                       # 本文件（项目入口）
├── CHANGELOG.md                    # 版本历史（含 SuperTrea 旧版本聚合）
├── LICENSE                         # MIT 协议
├── .gitignore                      # 忽略 .trae/（本地工作区配置）
│
├── config/                         # ✅ 项目核心配置（开源共享）
│   ├── AGENTS.md                   # 14 条铁律（始终加载）
│   ├── ETHOS.md                    # 5 条工程哲学 + skill 注入机制
│   ├── MCP-GUIDE.md                # MCP Server 配置指南
│   ├── .traeignore                 # TRAE 排除规则
│   ├── rules/                      # 6 个 Rule（始终/智能/指定文件加载）
│   │   ├── core.md                 # 15 条铁律（始终生效）
│   │   ├── git-commit.md           # scene: git_message
│   │   ├── quality.md              # 代码质量 6 红线
│   │   ├── roles.md                # 8 角色核心约束
│   │   ├── spec.md                 # spec 7 红线 + scope 分流
│   │   └── tdd.md                  # TDD 3 铁律
│   └── skills/                     # 20 个 Skill（按需加载）
│       ├── 核心工作流（10 个）
│       │   ├── brainstorming/                  # 需求澄清（HARD-GATE）
│       │   ├── spec-driven-development/        # 规范驱动（OpenSpec 4 段 + scope）
│       │   ├── plan-driven-development/        # 任务规划（DAG）
│       │   ├── writing-plans/                  # 任务规划（兼容旧版）
│       │   ├── tdd-workflow/                   # TDD 流程
│       │   ├── systematic-debugging/           # 4 阶段调试
│       │   ├── verification-before-completion/ # 完成前验证
│       │   ├── code-review/                    # 代码审查
│       │   ├── cross-artifact-analysis/        # 跨工件一致性
│       │   └── philosophy-audit/               # 9 条款哲学审计
│       ├── 领域审查（2 个）
│       │   ├── api-review/                     # RESTful 14 项 + 错误码
│       │   └── security-review/                # OWASP Top 10 + 9 项 checklist
│       ├── plan-mode 链（6 个）
│       │   ├── office-hours/                   # 产品 reframing（5 问）
│       │   ├── autoplan/                       # plan-mode 元 skill（5 维度串联）
│       │   ├── plan-ceo-review/                # 产品 5 维度 review
│       │   ├── plan-design-review/             # 设计 4 维度 review
│       │   ├── plan-eng-review/                # 工程 4 维度 review
│       │   └── plan-devex-review/              # 开发者体验 4 维度 review
│       └── 元 skill（2 个）
│           ├── using-superpowers/              # 元 skill：什么时候加载哪个
│           └── skill-writer/                   # 元 skill：写新 skill 的 5 步法
│
├── scripts/                        # 人类 CI 工具（不依赖 TRAE）
│   ├── validate-config.sh          # bash 入口（11 checker 调度）
│   └── ci/                         # Python 实现
│       ├── ci_check.py             # 主程序（CHECKER_REGISTRY + 报告输出）
│       ├── checkers/               # 11 个独立 checker
│       └── tests/                  # 单元测试
│
├── .github/workflows/ci.yml        # GitHub Actions 集成
└── .gitlab/workflows/ci.yml        # GitLab CI 集成
```

> **关于 `.trae/` 目录**：本地开发期间，TRAE IDE 会把项目级配置写到 `.trae/` 目录。
> 该目录是**本地工作区配置**，不进入版本控制（已在 `.gitignore` 中排除）。
> 真正共享给团队/开源的是 `config/` 目录。

---

## 核心特性

### 1. AGENTS.md（始终加载）

**位置**：`config/AGENTS.md`

**作用**：SOLO Agent 会话开始时自动加载的"项目行为总纲"。

**14 条核心铁律**：

- **v3.0 通用铁律（8 条）**：TDD / 规范先行 / 完整实现 / 证据优于断言 / 安全边界 / 用户主权 / 库优先 / 复杂度递减
- **v4.0 Bug 修复红线（5 条）**：零编辑 / 复现优先 / 4 阶段 / 修测试不修实现 / 禁删验证设施
- **v4.0 派发红线（1 条）**：核心模块完成后自动加载对应 skill 做交叉审查
- **v4.1 ETHOS 注入红线（1 条）**：每个 skill 加载时必须 prepend 1-2 条 ETHOS 哲学

### 2. Rules（始终/智能加载，6 个）

**位置**：`config/rules/*.md`

| Rule | 加载方式 | 触发场景 | 核心约束 |
|------|---------|---------|---------|
| **core.md** | 始终生效 | 任何任务 | 15 条铁律 + 自检清单 |
| **git-commit.md** | scene: git_message | Git 提交时 | 提交信息格式规范 |
| **quality.md** | 智能生效 | 写完任何代码模块 | 函数≤50 行 / 圈复杂度≤10 / 命名约定 / 无 magic number |
| **roles.md** | 智能生效 | 8 角色相关任务 | 8 角色 × ≤5 条核心约束速查表 |
| **spec.md** | 智能生效 | 编写 / 评审 spec | 7 红线 + scope 字段分流（greenfield/brownfield）|
| **tdd.md** | 智能生效 | 写任何测试 | RED 必真发生 / 修测试不修实现 / 配置文件豁免清单 |

### 3. Skills（智能加载，20 个）

**位置**：`config/skills/<name>/SKILL.md`

**加载机制**：TRAE 智能扫描 description，匹配后**按需全文件加载**到上下文。
加载时按 ETHOS.md 规则**自动 prepend 1-2 条相关哲学**到 preamble。

| Skill | 触发关键词 | ETHOS 注入 | 何时使用 |
|-------|-----------|-----------|---------|
| **brainstorming** | 新功能 / 改 / 修 / 怎么做 | Golden Age + 完整实现 | 任何需求提出时 |
| **spec-driven-development** | spec / 规范 / 需求文档 | Golden Age + 完整实现 | 复杂任务、多文件改动 |
| **plan-driven-development** | 拆任务 / 写计划 / DAG | Golden Age + 完整实现 | spec 确认后 |
| **writing-plans** | 拆任务 / 任务列表 | — | 已废弃（用 plan-driven）|
| **tdd-workflow** | 写代码 / 重构 / 测试失败 | Boil the Ocean + Evidence Over Claims | 任何代码任务 |
| **systematic-debugging** | 报错 / bug / 不工作 / why | 不搪塞 + Evidence Over Claims | 任何 Bug 修复 |
| **verification-before-completion** | 完成 / 提交 / 发布 | Evidence Over Claims + Boil the Ocean | 任何"完成"宣称前 |
| **code-review** | review / PR / 提交 | Evidence Over Claims + Boil the Ocean | 代码评审时 |
| **cross-artifact-analysis** | 分析 / 一致性 / 对比 | 完整实现 + 不搪塞 | 一致性检查 |
| **philosophy-audit** | 审计 / 9 条款 / 宪法 | 完整实现 + 不搪塞 | 哲学合规性审计 |
| **api-review** | API / 端点 / 接口 | Boil the Ocean + Evidence Over Claims | 新增 / 修改 / 评审 API 端点 |
| **security-review** | 密码 / Token / 2FA / 加密 | Boil the Ocean + Evidence Over Claims | 含敏感数据 / 鉴权 / 加密的代码 |
| **office-hours** | 我想做 / 帮我想 idea / 评估 | Golden Age + 完整实现 | 产品 reframing 第一步 |
| **autoplan** | 跑完整 plan-mode / 5 维度 | Golden Age + 完整实现 | plan-mode 元 skill（5 维度串联）|
| **plan-ceo-review** | 产品 review / 愿景 | Golden Age + 完整实现 | spec 完成后产品维度 review |
| **plan-design-review** | UI / UX / 设计 | Golden Age + 完整实现 | 涉及 UI / 视觉 / 交互时 |
| **plan-eng-review** | 架构 / 数据流 / 边界 | Golden Age + 完整实现 | spec 完成后工程维度 review |
| **plan-devex-review** | 开发者体验 / TTHW | Golden Age + 完整实现 | 库 / CLI / API 涉及时 |
| **using-superpowers** | 不知道该用哪个 skill / 先做什么 | Boil the Ocean + Golden Age | 元 skill：先于其他 skill 加载 |
| **skill-writer** | 写新 skill / 加个新 skill | Boil the Ocean + Golden Age | 元 skill：写 skill 的 5 步法 |

### 4. ETHOS.md（工程哲学注入）

**位置**：`config/ETHOS.md`

**作用**：5 条工程哲学 + skill 注入机制。SOLO Agent 加载 skill 时**必须**自动 prepend 与本 skill 相关的 1-2 条哲学到 preamble。

**5 条核心哲学**：

1. **Boil the Ocean**（煮沸海洋）—— 完整实现 > 偷懒捷径
2. **Golden Age**（黄金时代）—— 单人 + AI 的 10× 压缩比，完整性的边际成本接近于零
3. **Evidence Over Claims**（证据优于断言）—— 跑命令看完整输出，禁止"应该没问题"
4. **完整实现**（No Half-Done Tasks）—— 每个任务做透（功能 + 测试 + 文档 + 验证）
5. **不搪塞**（Never BS the User）—— 收到 bug / 失败必须触发实质动作

**反模式**（任何一条触发即视为违规）：
- ❌ "时间不够，先实现 happy path" → 偷工减料的借口
- ❌ "我跑过了" / "应该是 X" → 无证据
- ❌ "测试已通过，可能是你环境问题" → 搪塞
- ❌ skill 加载时"裸跑"无 ETHOS preamble

### 5. 最小化部署（推荐模式）

**背景**：TRAE IDE 会在用户项目根目录创建 `.trae/`，但团队协作时更推荐把核心配置放在 `config/` 目录作为"模板"。

**部署动作**：

```bash
# 1. 复制核心配置（必须）
cp -r config/rules/  <target-project>/.trae/
cp -r config/skills/ <target-project>/.trae/

# 2. 复制 ETHOS 哲学（可选，推荐保留）
cp config/ETHOS.md   <target-project>/.trae/

# 3. 复制 AGENTS.md 到 .trae/（关键）
cp config/AGENTS.md  <target-project>/.trae/

# 4. 复制 CI 工具到 scripts/（可选，推荐保留）
cp -r scripts/ <target-project>/
```

**部署后 `.trae/` 结构**：

```
.trae/                              # 实施阶段最小集
├── AGENTS.md                       # ✅ 14 条铁律
├── ETHOS.md                        # ⏸️  可选（哲学参考）
├── rules/                          # ✅ 6 个 rule 文件（核心）
└── skills/                         # ✅ 20 个 skill（核心）
```

---

## CI 工具（不依赖 TRAE）

**目录**：`scripts/`

**定位**：这是给人类（开发者/Reviewer）跑的工具，不是给 SOLO Agent 自动调用的。

```bash
# 跑全部 11 个 checker
bash scripts/validate-config.sh

# 只跑单个 checker
bash scripts/validate-config.sh --checker spec
bash scripts/validate-config.sh --checker 3_segment

# 详细输出（看 soft 警告）
bash scripts/validate-config.sh --verbose

# JSON 输出（供 GitHub Actions / pre-commit 消费）
bash scripts/validate-config.sh --json
```

### 退出码

| 退出码 | 含义 | 行为 |
|--------|------|------|
| `0` | 所有 hard 通过 | ✅ 可合并 |
| `1` | 存在 hard 失败 | ❌ 阻止合并 |
| `2` | 执行错误（缺依赖、找不到 .trae） | ❌ 阻止合并 |

### 11 个 Checker

| Checker | 验证目标 |
|---------|----------|
| `spec` | spec.md 包含 FR-XXX 编号 + 关键实体 + 成功标准 |
| `config` | `.trae/` 目录结构 + 必要文件存在 |
| `paths` | 46 个 md 文件 30 个交叉链接无死链 |
| `specialists` | 20 个 skill 都被注册 |
| `ethos` | 5 哲学 + 83 反模式 + 15 铁律 |
| `plan_mode` | office-hours → autoplan 5 维度串联 |
| `using_superpowers` | 元 skill 3 段式 + ETHOS 引用 |
| `3_segment` | 20/20 skill frontmatter 3 段式 |
| `skill_writer` | 5 步法章节齐全 |
| `skill_template` | 5 步每步 3 要素 |
| `spec_driven_v2` | 4 P1 改进（office-hours / refactor / brownfield / ETHOS）|

### 设计哲学

1. **CI 是给"人"跑的，不是给"Agent"跑的** —— 验证 `.trae/` 规范的硬约束
2. **CHECKER_REGISTRY 注册表模式** —— 加新 checker 只需写 1 文件 + 注册 1 行
3. **hard/soft 二分** —— hard 失败阻断，soft 警告不阻断
4. **JSON 输出可被外部消费** —— GitHub Actions / pre-commit hook / IDE 集成

### 平台支持

- **GitHub Actions**：`.github/workflows/ci.yml`
- **GitLab CI**：`.gitlab/workflows/ci.yml`

---

## 与 4 个开源项目的融合

本项目融合了 4 个主流 AI 辅助编程项目的工程哲学：

| 开源项目 | 核心贡献 | 本项目落地 |
|---------|---------|-----------|
| **gstack** | ETHOS（Boil the Ocean / Evidence Over Claims / 完整实现 / 不搪塞）| ETHOS.md + AGENTS.md 铁律 + verification-before-completion |
| **superpowers** | TDD Iron Law / HARD-GATE / using-superpowers | AGENTS.md + brainstorming + tdd-workflow + systematic-debugging skills |
| **spec-kit** | 9 条款宪法 / 8 阶段 / 30+ 代理 | AGENTS.md 铁律 + rules/roles.md（8 角色） + spec-driven-development |
| **OpenSpec** | DAG Artifact / Delta Spec 4 段 / scope 字段 | spec-driven-development skill（4 段 + scope 分流）+ plan-driven-development（DAG）|

---

## License

本项目使用 **MIT License** —— 详细条款见 [LICENSE](LICENSE) 文件。

MIT License 是最宽松的开源协议之一：
- ✅ 商业使用
- ✅ 修改
- ✅ 分发
- ✅ 私人使用
- ⚠️ 包含版权声明
- ⚠️ 包含协议声明
- ❌ 不承担任何责任

**协议选择依据**：本项目融合的 4 个上游项目（gstack / superpowers / spec-kit / OpenSpec）均采用 MIT License，为保持上游兼容性，本项目沿用 MIT。

---

## 关联文档

**核心配置**：
- [config/AGENTS.md](config/AGENTS.md) —— 14 条铁律（始终加载）
- [config/ETHOS.md](config/ETHOS.md) —— 5 条工程哲学
- [config/rules/core.md](config/rules/core.md) —— 15 条铁律精简版
- [config/rules/roles.md](config/rules/roles.md) —— 8 角色速查表
- [config/rules/quality.md](config/rules/quality.md) —— 代码质量 6 红线
- [config/rules/spec.md](config/rules/spec.md) —— spec 7 红线 + scope 分流
- [config/rules/tdd.md](config/rules/tdd.md) —— TDD 3 铁律
- [config/rules/git-commit.md](config/rules/git-commit.md) —— Git 提交信息规范

**核心 Skills**（共 20 个）：
- [using-superpowers](config/skills/using-superpowers/SKILL.md) —— 元 skill：什么时候加载哪个
- [skill-writer](config/skills/skill-writer/SKILL.md) —— 元 skill：写 skill 的 5 步法
- [brainstorming](config/skills/brainstorming/SKILL.md) —— 需求澄清（HARD-GATE）
- [spec-driven-development](config/skills/spec-driven-development/SKILL.md) —— 规范驱动
- [plan-driven-development](config/skills/plan-driven-development/SKILL.md) —— 任务规划（DAG）
- [tdd-workflow](config/skills/tdd-workflow/SKILL.md) —— TDD 流程
- [systematic-debugging](config/skills/systematic-debugging/SKILL.md) —— 4 阶段调试
- [verification-before-completion](config/skills/verification-before-completion/SKILL.md) —— 完成前验证
- [code-review](config/skills/code-review/SKILL.md) —— 代码审查
- [api-review](config/skills/api-review/SKILL.md) —— API 审查
- [security-review](config/skills/security-review/SKILL.md) —— 安全审查
- [office-hours](config/skills/office-hours/SKILL.md) —— 产品 reframing
- [autoplan](config/skills/autoplan/SKILL.md) —— plan-mode 元 skill

**CI 工具**：
- [scripts/README](scripts/) —— 11 个 checker 详细说明
- [scripts/validate-config.sh](scripts/validate-config.sh) —— bash 入口

**变更与决策**：
- [CHANGELOG.md](CHANGELOG.md) —— 完整版本历史
- [LICENSE](LICENSE) —— MIT 协议全文

---

## 贡献

欢迎通过 Issue / PR 贡献：
- 新增 Skill：参考 [skill-writer](config/skills/skill-writer/SKILL.md) 的 5 步法
- 新增 CI Checker：参考 `scripts/ci/checkers/` 下的注册表模式
- 修订 Rules / ETHOS：先在 Issue 讨论，避免破坏现有项目

提交前必跑：`bash scripts/validate-config.sh`（必须 exit 0）。

---

*基于工程哲学 v1（gstack / superpowers / spec-kit / OpenSpec 四大开源项目）*
*前身：SuperTrea v1.0 ~ v4.2（2026-06-11 ~ 2026-06-13）*
*主入口：TRAE IDE SOLO Agent*
*版本：v1.0.0（2026-06-13 全新发布）*

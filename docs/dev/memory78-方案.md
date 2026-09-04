# memory78 方案

> **规则的权威出处是 `memory78/readme.md` 与 `memory78/memory78-for-ai.md`**，本文件不复述细则，只记录：要解决的问题、用户定的规则、落地形态、当前状态。

---

## 一、要解决的问题（用户原话）

1. **AI 分类老是不准**
2. **个人知识和项目知识要分开**

---

## 二、用户定的规则（全部）

### 2.1 知识组织规则（详见 `memory78/readme.md`，原样有效）

- **四层结构：第三级还是目录，第四层才是文档**：

```
{apisys}/                        ← 第一层：目录
├── {apisys}.md                  ← 清单页（只写表格）
└── {apimicro}/                  ← 第二层：目录
    ├── {apimicro}.md            ← 清单页（只写表格）
    └── {apiobj}/                ← 第三层：还是目录 ★
        └── {apiobj}.md          ← 第四层：文档（实际内容放这里）
```

- 每层目录必须有同名 `.md`：`{apisys}.md` / `{apimicro}.md` 是**清单页**（只写表格，禁止写详细内容）；
  `{apiobj}/{apiobj}.md` 是**内容页**（摘要 + 关键知识 + 原始文档）
- apiobj.md 必须含 frontmatter：`title / tags / apisys / apimicro / apiobj`
- **内容用中文，标题（文件名）不用中文**（避免编码问题）
- apimicro / apiobj 不允许下划线（一个单词）；apiobj 可用 `/` 分隔表示函数层级
- 长内容：放 apiobj 目录内独立英文命名文件，摘要页链接过去；或直接引用项目内相对路径
- `m78 add` 用位置参数：`m78 add "标题" "内容" apisys apimicro apiobj`
- 新建子目录后用 `m78 scan --fix` 同步同名.md 的子目录清单

### 2.2 流程与分工规则（本次拍板）

| # | 规则 | 说明 |
|---|---|---|
| 1 | **分为个人和项目两个库** | 个人库 / 项目库，物理分开 |
| 2 | **个人的链接进项目来** | 个人库中可共享的内容，链接进项目使用 |
| 3 | **db 和个人的存 NAS（`m78nas`）** | 固定目录 `{项目根}/m78nas`，有 NAS 就把整个目录软链到 NAS，路径不变 |
| 4 | **`m78 add` 只添加进 wait 目录** | AI 产生的一切知识先落 `memory78/system/wait/` |
| 5 | **必须用户手动才转到正式目录** | 归位（分类分目录）由用户做，AI 不得代劳 |
| 6 | **会话知识整理到 `system/static/daily`** | 每日日志，钩子硬编码路径 |
| 7 | **我自己整理的才进知识** | wait 里 AI 写的不算入库，用户搬走才算 |

---

## 三、落地形态

### 3.1 目录

```
{项目根}/
├── memory78/                       ← 项目库（md 真身，Git 管）
│   ├── readme.md                   ← 规则权威出处
│   ├── product/                    ← apisys（原 saas）
│   │   └── database/               ← Git 子模块（SQL schema，非知识条目）
│   ├── vault/                      ← apisys（空，等人工归位）
│   └── system/
│       ├── static/daily/           ← 🔴 每日日志（钩子硬编码），不参与整理
│       └── wait/                   ← AI 写入区，用户手动归位
└── m78nas/                         ← 固定存储（有 NAS 就软链到这里）
    ├── personal/                   ← 个人公共库（不进项目仓）
    │   ├── shared/  private/  wait/
    │   └── memory78.db
    └── projects/
        └── ehs-ai-agent.db         ← 项目库 db（软链回 memory78/memory78.db）
```

### 3.2 配置（已生效）

```ini
# {项目根}/docs/config/memory78.ini   → 项目库
memory78_path = /workspace/memory78

# ~/.config/memory78.ini              → 个人库
memory78_path = /workspace/m78nas/personal
```

切换 = 换目录。`.gitignore`：`m78nas/personal/`、`m78nas/projects/*.db`

### 3.3 流程

```
AI：m78 add "标题" "内容" system wait wait     → memory78/system/wait/标题.md
用户：定期从 wait 里挑，手动归位到三级目录（改路径 + 改 front-matter）
daily：钩子每次会话自动追加 memory78/system/static/daily/YYYYMMDD.md
```

---

## 四、当前状态（2026-09-04）

| 项 | 状态 |
|---|---|
| 21 条存量知识 | 在 `memory78/system/wait/`（拍平命名 `原路径__文件名.md`），**等用户手动归位** |
| `product/` | 只剩 `database/` 子模块 |
| `vault/` | 已清空 |
| `m78nas/` | 已建好，db 已迁入并软链 |
| `memory78.db` | 未重建（等 `m78 import` 修复，规格见 `import-cmd-patch.md`） |
| daily | ⚠️ 有 bug，见 §五 |

---

## 五、daily 为什么断了（根因已查明，修法待确认）

**根因**：`.codebuddy/hooks/record_user_input.py` 的逻辑是「先试 `m78 daily`，成功就不写 md」。
现在容器里 **`m78` 命令存在且执行成功**（写进了 db），于是钩子直接 `exit(0)`，
**从不写 `system/static/daily/YYYYMMDD.md`**。

实测：db 里有 `daily_2026-09-04`，但 daily 目录最新文件还是 20260902.md。

**修法（待确认）**：钩子改为**始终写 md**（把 `if r.returncode == 0: sys.exit(0)` 删掉），
md 是人可读的真身，db 只是索引。一行改动。

---

## 六、记忆分级：原始 → 短期 → 中期 → 长期（**分析稿，待拍板，未实施**）

### 6.1 现状：记忆现在在哪

| 记忆 | 现在的位置 | 谁写 | 性质 |
|---|---|---|---|
| 用户输入流水 | `memory78/system/static/daily/YYYYMMDD.md` | 钩子自动（每次发消息追加） | **原始记录 raw** |
| AI 工作记忆 | `.codebuddy/memory/`（`MEMORY.md` + 日期.md） | AI 收工写 | **原始记录 raw** |
| 知识库 | `memory78/{apisys}/...` | **用户手动归位** | 长期知识 |

问题：AI 工作记忆存在 `.codebuddy/memory/`（CodeBuddy 平台约定目录），不在知识库里、不受知识库规则管。

### 6.2 目标形态（用户设想）

```
memory78/system/
├── static/daily/     ← L0 原始流水（钩子自动，已在跑）
├── memo/             ← AI 工作记忆真身（.codebuddy/memory 软链过来）
├── short/            ← L1 短期：一个命令从 raw 自动提取（天级）★与 daily 同级
├── mid/              ← L2 中期：短期自动沉淀（周级，去重合并）
└── long/             ← L3 长期候选：用户挑选 → 移入三级知识目录
```

漏斗：**raw（原文，自动）→ short（天级提炼，自动）→ mid（周级沉淀，自动）→ long（人工挑选）→ 知识库（人工归位）**

### 6.3 方案分析：方向对，但有 5 个点要先拍板

**对的地方**：
- 与已有机制无缝衔接：daily 钩子（raw）已在跑；"用户挑选才入库"与你定的规则⑤⑦一致
- 漏斗模型合理：raw 保留原文可回溯，short/mid 是提炼摘要，只有 long 才进知识库
- 全程 md（人可读、进 Git），只有"入库"那一步才碰 db

**要拍板的 5 个点**：

| # | 决策点 | 我的建议 |
|---|---|---|
| 1 | `.codebuddy/memory` 怎么改到 memory78 | **软链**：`.codebuddy/memory` → `memory78/system/memo/`。真身进知识库跟 Git 走，平台约定路径不变（AI 照常读写）。❌ 不要物理搬走 —— 平台会按约定路径重新生成，变成两份 |
| 2 | 目录命名 | `memo / short / mid / long`（英文，符合"文件名英文"规则） |
| 3 | "一个命令"是什么 | 提炼必须用 LLM（纯脚本只能切关键词，不可用）。实现 = 一个 skill（如 `/m78-digest`）：读 daily 近 N 天 + memo 近 N 天 → 生成 `short/YYYY-MM-DD.md`。「自动」= 每次会话开头 AI 自检昨天缺了就补 + 收工时顺带生成 |
| 4 | 中期怎么自动沉淀 | 定期（每周）把 short 里重复出现/未完结的合并成 `mid/YYYY-Www.md`；同一 skill 加参数（`/m78-digest --mid`） |
| 5 | 长期候选放哪 | **B：独立 `system/long/`**（推荐，来源清晰：wait=AI 对话产生的待分类，long=记忆提炼的候选）；A：也丢 wait（统一关口，但两种来源混在一起） |

### 6.4 风险与注意

1. 🔴 **敏感内容会进 Git**：memo（原 `.codebuddy/memory`）里记录过服务器地址、凭据线索等。
   项目仓是私有仓（`NElephants/ehs-ai-agent`），能否接受要拍板；不能接受则 memo/ 不进 Git（单独 gitignore）
2. **提炼是摘要不是原文**：short/mid 每条必须带出处链接（回指 daily/memo 原文），保证可回溯
3. short/mid/long 都是 md，**不进 db**；只有"入知识库"才走 `m78 add` / import 流程
4. 提炼去重：同一知识在多天 raw 里重复出现 → mid 合并时去重，标注首次/末次出现日期

---

## 七、待办

| # | 事项 | 等谁 |
|---|---|---|
| 1 | 用户从 `system/wait/` 手动归位 21 条 | 用户 |
| 2 | 记忆分级方案 §六 的 5 个拍板点 | 用户 |
| 3 | `m78 import` 修三处（跳过 wait / 跳过子模块 / 读 front-matter） | 研发，规格 `import-cmd-patch.md` |
| 4 | 重建 `memory78.db` | 依赖 #3 |
| 5 | 个人库开始使用（`m78nas/personal/wait/`） | 随时 |

> daily 钩子已修（始终写 md），`20260904.md` 已生成。

# memory78 方案

> **规则的权威出处是 `memory78/readme.md` 与 `memory78/memory78-for-ai.md`**，本文件不复述细则，只记录：要解决的问题、用户定的规则、落地形态、当前状态。

---

## 一、要解决的问题（用户原话）

1. **AI 分类老是不准**
2. **个人知识和项目知识要分开**

---

## 二、用户定的规则（全部）

### 2.1 知识组织规则（详见 `memory78/readme.md`，原样有效）

- 三级目录：`apisys → apimicro → apiobj`，**目录只建到三级**
- 每层目录必须有同名 `.md`
- **一、二级只写表格清单**；**三级才放实际内容**（摘要 + 关键知识 + 原始文档）
- apiobj.md 必须含 frontmatter：`title / tags / apisys / apimicro / apiobj`
- **内容用中文，标题（文件名）不用中文**（避免编码问题）
- apimicro / apiobj 不允许下划线（一个单词）；apiobj 可用 `/` 分隔表示函数层级
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

## 六、待办

| # | 事项 | 等谁 |
|---|---|---|
| 1 | 用户从 `system/wait/` 手动归位 21 条 | 用户 |
| 2 | daily 钩子修复（始终写 md） | 用户点头即改 |
| 3 | `m78 import` 修三处（跳过 wait / 跳过子模块 / 读 front-matter） | 研发，规格 `import-cmd-patch.md` |
| 4 | 重建 `memory78.db` | 依赖 #3 |
| 5 | 个人库开始使用（`m78nas/personal/wait/`） | 随时 |

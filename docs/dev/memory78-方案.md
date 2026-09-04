# memory78 方案（唯一文档）

> 2026-09-04
> 规则出处：`memory78/readme.md`（三级目录 / 四层文件职责 / apiobj.md 格式）、`product/devops/memory78-spec/`（写入规范）
> 本文件只做「方案 + 规则索引」，细则以 `readme.md` 为准

---

## 0. 一句话

知识按 **apisys → apimicro → apiobj** 三级目录存 md（Git 管真身）；
索引 db 存 **`{项目根}/m78nas`**（有 NAS 就软链过去）；
AI 写的新知识一律先进 `system/wait/`，人工按三级规则归位。

---

## 1. 固定存储目录：`{项目根}/m78nas`（已定稿）

**目录名和位置都写死**，与 `memory78/` 平级：

```
{项目根}/
├── memory78/                   ← 知识 md（Git 管，真身）
└── m78nas/                     ← 固定存储（db + 个人库）
    ├── README.md               ← 进 Git
    ├── personal/               ← 个人公共库（不进项目仓）
    │   ├── shared/  private/  wait/
    │   └── memory78.db
    └── projects/               ← 各项目库的 db
        └── ehs-ai-agent.db
```

| 情况 | 做法 |
|---|---|
| 没 NAS（默认） | 普通本地目录，已建好 |
| 有 NAS / 共享目录 | `ln -s /nas/share/m78nas m78nas`，**路径与配置都不变** |

项目库的 db 用软链挂过去：

```bash
ln -s m78nas/projects/ehs-ai-agent.db memory78/memory78.db
```

`.gitignore`：`m78nas/personal/`、`m78nas/projects/*.db`

**为什么不放 `~/`**：云开发环境里 `~/` 每次重建就没了。

---

## 2. 三级目录规则（★ 必须遵守，违反即返工）

```
{apisys}/                       ← 一级
├── {apisys}.md                 ← 清单页：表格列出 apimicro，禁止写详细内容
└── {apimicro}/                 ← 二级
    ├── {apimicro}.md           ← 清单页：表格列出 apiobj，禁止写详细内容
    └── {apiobj}/               ← 三级 ★ 只有这层放实际内容
        └── {apiobj}.md         ← 内容页：摘要 + 关键知识 + 原始文档
```

| # | 规则 |
|---|---|
| 1 | 每层目录都必須有同名 `.md` |
| 2 | **一、二级只写表格清单**，禁止写详细内容 |
| 3 | **三级才放实际内容**（摘要、关键知识、命令、配置） |
| 4 | apiobj.md 必须含 frontmatter（`title`/`tags`/`apisys`/`apimicro`/`apiobj`） |
| 5 | **内容用中文，标题（文件名）用英文** —— 避免中文文件名编码问题 |

### 四层文件职责

| 文件 | 职责 | 内容 |
|---|---|---|
| `{apisys}.md` | 大系统页 | 表格列出该系统下的 apimicro |
| `{apimicro}.md` | 微服务页 | 表格列出 apiobj（名称+摘要+链接） |
| `{apiobj}.md` | **实体摘要页**（内容页） | frontmatter + 摘要 + 关键知识 + 原始文档链接 |

⚠️ **常见混淆**：`{apisys}.md` / `{apimicro}.md` 是**清单页**，`{apiobj}.md` 是**内容页**。
我之前把 apiobj 层的同名.md 写成了清单页，是错的。

### apiobj.md 格式

```markdown
---
title: {apiobj}
tags: [{apiobj}, {apisys}, {apimicro}]
created_at: 2026-04-09 12:00:00
updated_at: 2026-04-09 12:00:00
hash: {content_hash}
apisys: {apisys}
apimicro: {apimicro}
apiobj: {apiobj}
---

# {apiobj}

> apisys: {X} | apimicro: {Y} | apiobj: {Z}

## 摘要

一句话到两句话说明干什么。

## 关键知识

- 核心规则/要点，列表形式

## 原始文档

- 代码: crates/xxx/src/xxx.rs
```

### ❌ 错误示例（引自 `readme.md`）

```
message/
└── message.md                   ← ❌ 一级直接写内容，缺二、三级
message/
└── email/
    └── agent.md                 ← ❌ 缺 message.md / email.md，且 agent.md 没放在 agent/ 里
message/
├── message.md
└── email/
    ├── email.md                 ← ❌ 二级页写了详细内容，应只写表格清单
    └── agent.md                 ← ❌ 没放在 agent/ 目录下
```

### 长内容处理

apiobj.md 是摘要页，长内容两种放法：

1. **独立文件放同目录**：`{apiobj}/{apiobj}.md`（摘要）+ `{apiobj}/prompt_template.md`（长内容）
2. **引用外部文件**：在「原始文档」里写相对路径链接到项目中的文件

---

## 3. 两个库怎么分

| | 个人公共库 | 项目库 |
|---|---|---|
| 路径 | `m78nas/personal/` | `{项目根}/memory78/` |
| Git | 不进项目仓（独立私有仓） | 项目仓（团队共享） |
| 内容 | 通用工具用法、跨项目踩坑、个人笔记、敏感信息 | 项目架构/接口/部署/故障复盘/业务规则 |

**判据**：换个人接手这个项目，他需要这条吗？需要 → 项目库。

**切库**（m78 无 `--db` 参数，靠配置/目录）：

```ini
# {项目根}/docs/config/memory78.ini   → 项目库
memory78_path = /workspace/memory78

# ~/.config/memory78.ini              → 个人库（全局默认）
memory78_path = /workspace/m78nas/personal
```

⚠️ 不要把 `export MEMORY78_PATH=...` 写进 `.bashrc`（优先级最高，会把所有项目强行指向同一个库）。

---

## 4. db 怎么存

### 4.1 三层数据

| 层 | 内容 | 在哪 | 丢了怎么办 |
|---|---|---|---|
| L1 原文 | md | Git（项目库）/ `m78nas`（个人库） | 真身，必须保住 |
| L2 索引 | `memory78.db`（FTS5 + `memories.embedding` 向量列） | `m78nas` | `m78 import` 重建，**向量要重算** |
| L3 模型 | `models/*.gguf` ~2.2GB | 本地 | `m78 model download` 重下 |

> **没有独立的"向量库"**：向量就是 db 里的 `memories.embedding` 一列。

**db 不进 Git**：二进制派生数据，体积随条数涨（向量 JSON 约 8~10KB/条），不可 diff。

### 4.2 为什么必须存 db

`embed build` 的"增量"前提是上次算好的向量还在。
不存 ⇒ 每次从零 ⇒ **每次全量 10~50 分钟**（CPU 逐条推理）。

| 动作 | 耗时 |
|---|---|
| `m78 import`（FTS5 全文索引） | 秒级 |
| `m78 embed build` 首次全量 | 🔴 10~50 分钟 |
| `m78 embed build` 之后 | 秒~分钟级（只算未嵌入的新条目） |

### 4.3 并发写：说清楚，不是"不能用"

我上版写的「同一时刻只在一台机器上写」**说得太绝对**，导致这方案看起来没意义。准确的说法：

| | 说明 |
|---|---|
| 真正的问题 | SQLite 在网络文件系统（NFS/SMB）上**锁语义不可靠**，两台机器**同时**写有损坏风险 |
| 不是问题 | **顺序使用**（这台写完、换那台写）完全正常 —— 一个人本来也不会同时用两台机器写同一份库 |
| NAS 的意义 | 不是并发写，是**同一份数据（含算好的向量）在任意机器上直接可用**，换机不用重算 |

⇒ 结论：**默认就这么用**。风险窗口只在你真的两台机器同时敲 `m78 add` 时才出现，
而最坏后果也只是 db 损坏 → `rm` 重建，**md 是真身，不丢数据**。

**多机同时写才需要的备选方案**（现在不需要）：

```
md 放 m78nas（随便共享，文本文件无并发问题）
db 各机器本地一份，不共享，换机时 m78 import 增量重建
```

代价：换机要重建（L0 秒级，L1 需重算新增部分）。

---

## 5. 分类：AI 全进 `wait`，人工归位

```
memory78/
├── system/wait/         ← AI 写入区，扁平，人工从这里搬走
├── system/static/daily/ ← 🔴 固定路径，钩子硬编码，不参与整理
├── readme.md            ← 知识库自述，不参与整理
├── product/             ← apisys
└── vault/               ← apisys
```

```bash
m78 add "标题" "内容" system wait wait     # → memory78/system/wait/标题.md
```

🔴 **不参与整理的固定路径**：`system/static/daily/`（钩子硬编码
`record_user_input.py: DAILY_DIR`）、`product/database/`（Git 子模块）、
`readme.md`、`memory78.db`、`models/`

**归位 SOP**（三步，缺一不可）：

```bash
# ① git mv 到 apiobj 目录下（三级！不是二级）
git mv system/wait/vault__roles__vault-roles.md vault/roles/vault-roles/vault-roles.md

# ② 改文件头部 front-matter 的 apisys/apimicro/apiobj
#    m78 export 建目录用的是库里的字段，不是当前路径；不改会被搬回原处

# ③ 更新各级清单页（{apisys}.md / {apimicro}.md 的表格）
```

---

## 6. 当前违规清单（待修，已确认）

按 §2 规则自查，现在有这些不合规，**等确认后统一返工**：

| # | 问题 | 位置 | 应为 |
|---|---|---|---|
| 1 | 条目在二级目录（违反"三级才放内容"） | `vault/credentials/alicloud-ak.md` | `vault/credentials/alicloud-ak/alicloud-ak.md` |
| 2 | 同上 | `vault/credentials/vault-credentials.md` | `vault/credentials/vault-credentials/vault-credentials.md` |
| 3 | 同上 | `vault/roles/vault-roles.md` | `vault/roles/vault-roles/vault-roles.md` |
| 4 | 同上 | `vault/testpolicy/devtest-5m.md` | `vault/testpolicy/devtest-5m/devtest-5m.md` |
| 5 | apiobj 同名.md 写成清单页（应为内容页） | `memory78-spec/memory78-spec.md` | 内容页：摘要 + 关键知识 + 原始文档 |
| 6 | 同上 | `saas/saas.md` | 内容页 |
| 7 | 同上 | `ssh-keys/ssh-keys.md` | 内容页 |
| 8 | 二级页写了大量详细内容（违反"只写清单"） | `product/devops/devops.md` | 详细内容迁到 `ehs-ai-agent-init/ehs-ai-agent-init.md`，devops.md 只留表格 |
| 9 | 文件名含空格/非 apiobj 名 | `Memory78 Writing Spec.md`、`SSH Private Key Inventory.md` | 摘要页用 `{apiobj}.md`，长内容另起英文名 |

> 说明：#1–#4 是历史遗留（原来就少一层），#5–#7 是我这次归位时写错的，
> #8 是 `devops.md` 原有内容（架构/技术栈/部署/开发状态/已知坑）应在 apiobj 内容页里。

---

## 7. 待办（按序）

| # | 事项 | 状态 |
|---|---|---|
| 1 | 修 §6 的 9 项违规 | 待确认后执行 |
| 2 | `m78 import` 修三处（跳过 wait / 跳过子模块 / 读 front-matter 分类） | 研发排期，规格见 `import-cmd-patch.md` |
| 3 | 重建 `memory78.db` | 依赖 #1+#2（或只 #1，用现有 CLI 也能建对） |
| 4 | 个人库启用（开始往 `m78nas/personal/wait/` 写） | 随时可开始 |

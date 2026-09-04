# memory78 方案（唯一文档）

> 2026-09-04　状态：**待确认**（第 1 节的目录名、第 6 节的三个开关）

---

## 1. 固定存储目录：`{项目根}/m78nas`（**已定稿**）

**目录名和位置都写死**：就放在**项目根目录下**，跟 `memory78/` 平级。

```
{项目根}/
├── memory78/                   ← 知识库 md（Git 管）
└── m78nas/                     ← 固定存储目录（db 等派生数据 + 个人库）
    ├── README.md               ← 说明（进 Git）
    ├── personal/               ← 个人公共库（md + db，不进项目仓）
    │   ├── shared/             ← 可共享
    │   ├── private/            ← 永不外传
    │   ├── wait/               ← 待分类
    │   └── memory78.db
    └── projects/               ← 各项目库的 db
        ├── ehs-ai-agent.db
        └── <其他项目>.db
```

**有没有 NAS 都一样用，路径不变**：

| 情况 | 怎么做 |
|---|---|
| **没有 NAS**（默认） | 就是一个普通本地目录，直接建 |
| **有 NAS / 共享目录** | 把 `m78nas` 整个目录放到 NAS 上，再软链回来：<br>`ln -s /nas/share/m78nas m78nas` |
| **云开发环境** | 目录跟着项目走，重建后从 Git 恢复结构，db 再同步 |

项目库的 db 用软链挂过去：

```bash
ln -s m78nas/projects/ehs-ai-agent.db memory78/memory78.db
```

**为什么不放 `~/`**：`~/` 在云开发环境里每次重建就没了。放项目根目录下，
跟着项目走；有 NAS 的时候换软链即可，**配置和用法完全不变**。

**命名**：`m78` = CLI 名，`nas` = 用途；全小写无分隔符，Windows/SMB/rsync 都不会有转义麻烦。

---

## 2. 两个库怎么分

| | 个人公共库 | 项目库 |
|---|---|---|
| 路径 | `~/memory78` → 软链到 `m78nas/personal` | `{项目根}/memory78` |
| md 真身 | `m78nas/personal`（NAS） | 项目目录（**Git 管**） |
| db 真身 | `m78nas/personal/memory78.db` | `m78nas/projects/<项目>.db` |
| Git | 个人私有仓（可选） | 项目仓/子模块（团队共享） |
| 内容 | 通用工具用法、跨项目踩坑、个人笔记、敏感信息 | 项目架构/接口/部署/故障复盘/业务规则 |

**判据**：换个人接手这个项目，他需要这条吗？需要 → 项目库。

**切库**：`cd ~/memory78` 就是个人库，`cd /workspace` 就是项目库。
m78 **没有 `--db` 参数**，也不做跨库搜索 —— 靠目录切就行，**CLI 零改动**。

---

## 3. db 必须存（否则向量每次全量重算）

🔴 `embed build` 的"增量"前提是**上次算好的向量还在**。不存 db ⇒ 每次从零 ⇒ 每次全量。

**存的方式就是放 `m78nas` + 软链**：真身只有一份，多机共用，
不需要 rsync / 对象存储 / 备份快照那套东西。

| 层 | 内容 | 在哪 | 丢了怎么办 |
|---|---|---|---|
| L1 原文 | md | NAS（个人）+ Git（项目） | 真身，必须保住 |
| L2 索引 | `memory78.db`（FTS5 + `memories.embedding` 向量列） | `m78nas` | `m78 import` 重建，但**向量要重算** |
| L3 模型 | `models/*.gguf` ~2.2GB | 本地 | `m78 model download` 重下 |

> **没有独立的"向量库"文件**：向量就是 db 里 `memories.embedding` 一列。

**重建耗时**（准数，别再搞错）：

| 动作 | 耗时 |
|---|---|
| `m78 import`（全文索引） | 秒级 |
| `m78 embed build` **首次全量** | 🔴 10~50 分钟（CPU 逐条推理） |
| `m78 embed build` **之后** | 秒~分钟级（只算未嵌入的新条目） |

**不进 Git**：`memory78.db` 是二进制派生数据，体积随条数涨（向量 JSON 约 8~10KB/条，
1 万条 50~100MB），不可 diff。项目根 `.gitignore` 已有 `*.db*`。

⚠️ **SQLite 放 NAS 的四条约束**
1. 同一时刻只在一台机器上写（并发写会损坏文件）
2. db 损坏 = `rm` 重建，**不丢数据**（md 是真身），只丢索引和向量
3. 不开 WAL 模式（NFS/SMB 的锁不可靠）
4. 挂不到 NAS 时退化成本地重建，回来重新指软链即可恢复

---

## 4. 分类：取消自动分类，全进 `wait`

**目录约定**（项目库已落地）：

```
{项目根}/memory78/
├── system/wait/       ← AI 全写这里，扁平，人工从这里搬走
├── system/static/daily/ ← 🔴 固定路径，钩子写死，不参与整理
├── product/           ← 正式分类（原 saas，2026-09-04 改名）
│   └── database/      ← ⚠️ Git 子模块 = SQL schema 仓库，不是知识分类
├── readme.md          ← 知识库自述，不参与整理
└── vault/ product/ …  ← 正式分类
```

```bash
m78 add "标题" "内容" system wait wait     # → memory78/system/wait/标题.md
```

🔴 **不参与整理的固定路径**（整理时别碰）：

| 路径 | 为什么 |
|---|---|
| `system/static/daily/` | 每日日志，钩子硬编码 `record_user_input.py: DAILY_DIR`；`m78 daily` 与钩子都往这写 |
| `product/database/` | Git 子模块（databasesql.git），SQL schema 仓库 |
| `readme.md` | 知识库自述 |
| `memory78.db` / `models/` | 派生数据，不进 Git |

**归位 SOP**：

```bash
git mv system/wait/vault__roles__vault-roles.md vault/roles/vault-roles.md
# 🔴 必须同步改文件头部 front-matter 的 apisys/apimicro/apiobj
#    m78 export 建目录用的是库里的字段，不是当前路径；不改会被搬回原处
m78 scan --fix
```

**存量搬家**（2026-09-04 已执行）：21 个知识 md 拍平进 `system/wait/`，
路径分隔符转 `__`（如 `vault__roles__vault-roles.md`），从文件名就能看出原来在哪。
🔴 `system/static/daily/` 的 8 个日志文件**不动**（钩子写死），一度误搬已还原。

---

## 5. 待研发：`m78 import` 改三处（规格见 `import-cmd-patch.md`）

实测（33 个文件）：只有 5 条分类判对，2 条成了 `tmp/tmp/tmp`，
**且完全不读 `m78 add` 写进 md 的 front-matter**，重复 import 还会翻倍。
改完之前 `m78 import` 不可用 ⇒ `memory78.db` 也先别重建。

1. 跳过 `wait` / `待分类` 目录
2. 跳过 Git 子模块目录（有 `.git` 的），如 `product/database/`
3. 分类改为 **front-matter 优先**（缺的字段按路径深度兜底），判重改为按路径

---

## 6. 已定 / 待办

**已定**：
1. 目录 `{项目根}/m78nas`（位置写死，有 NAS 就软链，路径不变）
2. db 必须存（放 `m78nas`，否则 `embed build` 每次全量重算）
3. 个人库 `m78nas/personal/`，项目库只把 db 放 `m78nas/projects/<项目>.db`

**待办（有先后）**：

| # | 事项 | 卡点 |
|---|---|---|
| 1 | `vault/` 下 4 个条目下沉一层 apiobj | 等选 A（现在改）或 B（等 CLI 读 front-matter） |
| 2 | `m78 import` 修三处 | 研发排期（`import-cmd-patch.md`） |
| 3 | 重建 `memory78.db` | 依赖 #2（或 #1 完成后用当前 CLI 也能建） |
| 4 | 个人库 → 项目库同步 md | 可选；只是自己看就不用同步 |

---

## 7. 附：路径配置

```ini
# ~/.config/memory78.ini（个人库，全局默认）
memory78_path = /root/memory78

# {项目根}/docs/config/memory78.ini（项目库，覆盖全局）
memory78_path = /workspace/memory78
```

⚠️ 多数项目 `.gitignore` 含 `docs/config/*.ini`，实际 ini 不提交，只提交样例。
⚠️ 别把 `export MEMORY78_PATH=...` 写进 `.bashrc`，它优先级最高会把所有项目强行指向同一个库。

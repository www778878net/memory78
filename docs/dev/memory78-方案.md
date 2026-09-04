# memory78 方案（唯一文档）

> 2026-09-04　状态：**待确认**（第 1 节的目录名、第 6 节的三个开关）

---

## 1. 固定存储目录：`m78nas`

**核心思路**：约定一个**固定目录名** `m78nas`。
有 NAS 的就把它挂到 `/mnt/m78nas`，没有的就 `mkdir -p ~/.m78nas` ——
**路径约定一致，有没有 NAS 只是真身在哪的区别，用法完全一样。**

```
/mnt/m78nas/                    ← 固定目录（NAS 挂载点；无 NAS 时用 ~/.m78nas）
├── personal/                   ← 个人公共库真身（md + db 全在这里）
│   ├── shared/                 ← 可共享（同步给项目库）
│   ├── private/                ← 永不外传（本机路径、敏感线索）
│   ├── wait/                   ← 待分类
│   └── memory78.db
└── projects/
    ├── ehs-ai-agent.db         ← 各项目库的 db（md 留在项目里由 Git 管）
    └── <其他项目>.db
```

本机软链：

```bash
ln -s /mnt/m78nas/personal ~/memory78
ln -s /mnt/m78nas/projects/ehs-ai-agent.db /workspace/memory78/memory78.db
```

**为什么叫 `m78nas`**：`m78` 是 CLI 名，一眼知道是谁的；`nas` 直说用途；
全小写无分隔符，Windows/SMB/rsync 都不会有转义麻烦。

> 容器等挂不了 NAS 的环境：照常 `mkdir -p ~/.m78nas` 建一个本地的，
> 只是那份不共享；回到有 NAS 的机器重新指软链即可。

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
├── product/           ← 正式分类（原 saas，2026-09-04 改名）
│   └── database/      ← ⚠️ Git 子模块 = SQL schema 仓库，不是知识分类
└── vault/ product/ …  ← 正式分类
```

```bash
m78 add "标题" "内容" system wait wait     # → memory78/system/wait/标题.md
```

**归位 SOP**：

```bash
git mv system/wait/vault__roles__vault-roles.md vault/roles/vault-roles.md
# 🔴 必须同步改文件头部 front-matter 的 apisys/apimicro/apiobj
#    m78 export 建目录用的是库里的字段，不是当前路径；不改会被搬回原处
m78 scan --fix
```

**存量搬家**（2026-09-04 已执行）：29 个 md 全部拍平进 `system/wait/`，
路径分隔符转 `__`（如 `vault__roles__vault-roles.md`），从文件名就能看出原来在哪。

---

## 5. 待研发：`m78 import` 改三处（规格见 `import-cmd-patch.md`）

实测（33 个文件）：只有 5 条分类判对，2 条成了 `tmp/tmp/tmp`，
**且完全不读 `m78 add` 写进 md 的 front-matter**，重复 import 还会翻倍。
改完之前 `m78 import` 不可用 ⇒ `memory78.db` 也先别重建。

1. 跳过 `wait` / `待分类` 目录
2. 跳过 Git 子模块目录（有 `.git` 的），如 `product/database/`
3. 分类改为 **front-matter 优先**（缺的字段按路径深度兜底），判重改为按路径

---

## 6. 待确认三件事

1. **目录名** `m78nas` 定不定？（备选 `78nas` / `m78-store`）
2. **挂载点**：有 NAS 时统一挂 `/mnt/m78nas`；无 NAS 时用 `~/.m78nas` —— 可以这样约定吗
3. **个人库 → 项目库要不要同步 md**：NAS 已经把个人库共享出去了，
   若只是自己看就**不用同步**；只有"希望个人沉淀的通用知识进项目仓给团队看"时才需要，
   那时把 `personal/shared/` 拷进项目库 `shared/` 即可（单向，项目库里别改）

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

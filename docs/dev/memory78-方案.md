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
| 3 | **db 集中到 NAS（`m78nas`）** | 固定目录 `{项目根}/m78nas`，**只存数据库**，不存知识 md；有 NAS 就把整个目录软链到 NAS，路径不变 |
| 4 | **`m78 add` 只添加进 wait 目录** | AI 产生的一切知识先落 `{对应库}/system/wait/` |
| 5 | **必须用户手动才转到正式目录** | 归位（分类分目录）由用户做，AI 不得代劳 |
| 6 | **会话知识整理到 `system/static/daily`** | 每日日志，钩子硬编码路径（个人库） |
| 7 | **我自己整理的才进知识** | wait 里 AI 写的不算入库，用户搬走才算 |

---

## 三、落地形态

### 3.1 目录（2026-09-04 修订：个人/项目彻底分开，NAS 只存 db）

```
{项目根}/
├── memory78/                       ← 个人记忆库（md 真身，Git 管）★原来误当项目库，已纠正
│   ├── readme.md                   ← 规则权威出处
│   ├── memory78.db →（软链 → m78nas/personal.db，db 不入 Git）
│   └── system/
│       ├── static/daily/           ← 🔴 每日日志（钩子硬编码），不参与整理
│       ├── static/memo/            ← 🔗 软链 → .codebuddy/memory（AI 工作记忆 md）
│       │                             软链本体入 Git（120000），内容随仓库分发
│       ├── static/short/  mid/  long/
│       └── wait/                   ← 个人库 AI 写入区，用户手动归位
├── m78project/                     ← 项目记忆库（md 真身，Git 管）★2026-09-04 新增
│   ├── product/                    ← apisys（原 saas 项目知识）
│   │   └── database/               ← Git 子模块（SQL schema，非知识条目）
│   ├── memory78.db →（软链 → m78nas/projects/ehs-ai-agent.db，db 不入 Git）
│   └── system/
│       └── wait/                   ← 项目库 AI 写入区，用户手动归位（22 条迁移到这）
└── m78nas/                         ← 数据库存储层（只存 db，不存知识 md，整个目录不入 Git）
    ├── projects/
    │   └── ehs-ai-agent.db         ← 项目库 db 真身
    └── personal.db                 ← 个人库 db 真身
```

### 3.2 配置（2026-09-04 修订：路径已改到新分工）

```ini
# {项目根}/docs/config/memory78.ini   → 项目库（项目记忆）
memory78_path = /workspace/m78project

# ~/.config/memory78.ini              → 个人库（个人记忆）
memory78_path = /workspace/memory78
```

切换 = 换目录。**db 一律不入 Git**：真身在 `m78nas/`，记忆库内的 `memory78.db` 只是
指向它的软链（本地运行时用，同样不入库）；clone 下来后需自行 `m78 import` 生成 db 或接 NAS。
**md 软链（`static/memo` → `.codebuddy/memory`）本体入 Git**（模式 `120000`），内容随仓库分发。

### 3.3 流程

```
项目库：AI: m78 add "标题" "内容" system wait wait     → m78project/system/wait/标题.md
个人库：AI: m78 add "标题" "内容" system wait wait     → memory78/system/wait/标题.md
用户：定期从 wait 里挑，手动归位到三级目录（改路径 + 改 front-matter）
daily：钩子每次会话自动追加 memory78/system/static/daily/YYYYMMDD.md（个人库）
```

---

## 四、当前状态（2026-09-04 修订）

| 项 | 状态 |
|---|---|
| 22 条存量项目知识 | 已从 `memory78/system/wait/` **迁移到 `m78project/system/wait/`**（拍平命名 `原路径__文件名.md`），**等用户手动归位** |
| `product/`（含子模块） | 已随项目知识迁到 `m78project/product/`，349 个 SQL 完整 |
| 个人/项目分工 | ✅ 纠正：memory78=个人，m78project=项目（原来把项目知识误放个人库） |
| `m78nas/` | 定位改为**只存 db**，不再存知识 md，整个目录**不入 Git** |
| db | 个人库 db（`personal.db`）26 条、项目库 db（`ehs-ai-agent.db`）0 条（等归位）；真身都在 `m78nas/`，记忆库内 `.db` 是不入 Git 的软链 |
| md 软链 | `static/memo` → `.codebuddy/memory`，软链本体**入 Git**（120000），16 条内容可被 import |
| daily | ✅ 已修复（始终写 md），`20260904.md` 正常生成 |

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

### 6.2 目标形态（已定稿）

**全部在个人库 `memory78/system/static/` 下**（与 daily 同级）：

```
memory78/system/static/
├── daily/     ← L0 原始流水（钩子自动，已在跑）
├── memo/      ← L0 AI 工作记忆真身（`.codebuddy/memory`，知识库内为软链）
├── short/     ← L1 短期：m78 digest 自动提取（天级）
├── mid/       ← L2 中期：m78 digest --mid 自动沉淀（周级，去重合并）
└── long/      ← L3 长期候选：用户挑选 → 移入三级知识目录
```

> 项目库 `m78project/` 也可复用同样的 `system/static/` 分级（daily/memo/short/mid/long），
> 但项目知识与个人流水分开，各自维护。

漏斗：**raw（原文，自动）→ short（天级提炼，自动）→ mid（周级沉淀，自动）→ long（人工挑选）→ 知识库（人工归位）**

### 6.3 AI 工作记忆（memo）通过 md 软链接入（本方案已落实）

**memo 用 md 软链接接入知识库**（用户拍板）：`workbuddy`/`.codebuddy` 的 memory 目录是软链真实源，
在知识库内放软链占位，本体随 Git 分发。

```
真身：.codebuddy/memory/（workbuddy/CodeBuddy 平台约定目录，AI 工作记忆 md 的物理真身）
软链：memory78/system/static/memo → .codebuddy/memory     ← 入 Git（模式 120000）
```

- **memo 软链本体入 Git**：clone 下来即保留链接结构，内容随仓库分发
- 🔴 依赖 m78 import 能跟随软链：import 需在扫描时 follow 软链，memo 内容才能进 DB（已实现，16 条正确导入）
- db 反之**绝不入 Git**（见 §3.2）——软链接只有 md 记忆目录这一处

### 6.4 命令：`m78 digest`（CLI 子命令，提给研发）

| 命令 | 功能 | 输出 |
|---|---|---|
| `m78 digest` | 分析 daily 近 N 天 + memo 近 N 天，LLM 提炼当天要点 | `system/static/short/YYYY-MM-DD.md` |
| `m78 digest --mid` | 合并 short（去重，重复出现/未完结优先） | `system/static/mid/YYYY-Www.md` |
| `m78 digest --long` | 从 mid/short 提炼长期候选清单 | `system/static/long/<日期>-<主题>.md` |

- 提炼必须用 LLM（CLI 已有 QMD 的 LLM 通道可复用）
- 每条提炼结果**必须带出处链接**（回指 daily/memo 原文），可回溯
- 「自动」：钩子/会话开头检查 short 缺失自动补 + 收工生成（触发方式研发定）
- long 里的条目由**用户挑选**，手动移入三级知识目录（走归位 SOP：git mv + 改 front-matter + 更新清单页）

### 6.5 注意

1. 🔴 **敏感内容会进 Git**：memo 里记录过服务器地址、凭据线索等。项目仓是私有仓（`NElephants/ehs-ai-agent`）
2. daily/memo/short/mid/long 都在知识库目录内，`m78 import` 会扫到 —— 规格里需补充：
   按 `system/static/` 下目录名打来源标签（daily/raw、short、mid、long），wait 同理
3. 提炼去重：同一知识多天重复 → mid 合并时去重，标注首次/末次出现日期

---

## 七、NAS 接入（未完成）

### 7.1 现状

`m78nas/` 目前是**项目根下的普通本地目录**（已定稿的设计就是它，有 NAS 才换软链）。
**CNB 云容器里没有任何 NAS 挂载**（`/mnt` `/media` 全空），且容器在云端、NAS 多半在局域网 ⇒ 网络不通。

### 7.2 没接 NAS 的实际影响

| 数据 | 现在怎样 | 接了 NAS 后 |
|---|---|---|
| 知识 md | ✅ 不受影响（Git 管，环境重建 clone 回来） | 不变 |
| `m78nas/projects/*.db`（索引+向量） | ⚠️ **环境重建即丢**，要 `m78 import` 重建；L0 无向量=秒级可接受，**升 L1 后向量要重算（10~50 分钟）** | db 真身在 NAS，重建环境软链回来即用 |
| `.codebuddy/memory`（个人流水） | ⚠️ 环境重建即丢（真身在 memory78 库内，属 Git 管） | 真身在 NAS，不丢 |

### 7.3 接入三途径（按可行性）

| 途径 | 做法 | 适用 |
|---|---|---|
| **A. 公网可达的 NAS** | NAS 做公网映射/frp/Tailscale，云容器挂 SMB/NFS 到 `/mnt/nas`，`ln -s /mnt/nas/m78nas m78nas` | 唯一能让**云环境**用上真 NAS 的路 |
| **B. 本地机器直连** | 办公室/家里机器挂 NAS，`m78nas` 放 NAS 上；**云环境不用 NAS**（db 每次重建） | 最省事；个人库 md 用私有 Git 仓多机同步 |
| **C. ZOS 对象存储当中转** | 🔴 **SQLite 不能放对象存储**（对象接口无随机写）；只能放 db 快照包（tar），环境重建时拉包解压 | 兜底：给云环境保住"算好的向量" |

### 7.4 待你提供（选 A 时）

NAS 公网地址 + 协议（SMB/NFS）+ 端口 + 账号凭据。没有公网 NAS 就选 B（现状已可用）。

---

## 八、待办全量清单

### 用户做
| # | 事项 | 说明 |
|---|---|---|
| 1 | 从 `m78project/system/wait/` 手动归位 22 条 | git mv + 改 front-matter + 更新清单页（SOP 见 §五） |
| 2 | NAS 选型：A 公网 / B 本地（§七） | 选 A 给连接信息 |
| 3 | memo 敏感内容进 Git 的取舍 | 已在主仓（私有仓）；不接受则 gitignore memo |
| 4 | 挑选 long 候选入知识库 | digest 跑起来之后 |

### AI 可直接做（随时开工）
| # | 事项 | 说明 |
|---|---|---|
| 5 | digest 过渡方案：收工时人工写 `short/当天.md` | 零开发，先跑通格式；等 LLM 配置定了再进 CLI |
| 6 | `readme.md` 的 apisys 索引更新 | 「已有的 apisys」表还是旧的（aicode/steam/base…），应改为 product/vault/system |
| 7 | `memory78-for-ai.md` / `SKILL.md` 同步 | wait 流程、daily 修复、个人/项目分流、digest 都没写进 AI 指南 |
| 8 | 个人库启用配置 | `~/.config/memory78.ini` = `memory78/`，项目库 config = `m78project/`（环境重建会丢，**该加进 restore.sh**） |
| 9 | short/mid/long 空目录加 `.gitkeep` | 让目录结构随 Git 分发 |

### 研发做（规格已出）
| # | 事项 | 规格 |
|---|---|---|
| 10 | ~~`m78 import` 修复（follow_links/wait/子模块/front-matter/防翻倍）~~ | ✅ **已由 AI 完成并上线**（`a42fb99`，二进制已替换，db 已重建 26 条全对） |
| 11 | `m78 digest` 子命令（LLM 提炼 short/mid/long） | §6.4；**前置：定 LLM API 与 key 来源** |
| 12 | `m78 export` 按目录打来源标签 + 搬家后分类同步 | §6.5-2；export 目前按库字段建目录，文件搬家会搬错位置 |
| 13 | Windows 版二进制更新 | `m78_win.exe` 还是旧逻辑（交叉编译 musl） |

### 安全遗留（非 memory78，一并提醒）
| # | 事项 |
|---|---|
| 14 | GitHub token（聊天明文出现过）+ 阿里云/天翼云超管 AK 轮换 |

> 已完成：daily 钩子修复（始终写 md）、m78nas 目录与 db 软链、CLI import 五项修复、
> memo 入 DB（16 条）、db 重建 26 条全对、规则 1.mdc 铁律、方案文档本身。
> 2026-09-04 追加：个人/项目彻底分流（memory78=个人，m78project=项目），
> 22 条项目知识与 product/database 子模块迁入 m78project，`.gitmodules` 同步更新 `a42fb99`。
> 同日再订正：**md 软链入 Git**（memo → .codebuddy/memory，120000），**db 绝不入 Git**（真身在 m78nas）。

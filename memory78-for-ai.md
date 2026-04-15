# Memory78 AI 使用指南

> 本文档告诉 AI 如何将对话中产生的知识归纳到 memory78 知识库。

## 核心原则

**AI 主动整理本次会话中产生的知识，无需用户明确要求。**

**重要：用 m78 add 的位置参数指定分类，不要用 python 脚本。**

## 使用时机

把本文档直接扔给 AI，AI 会在以下时机自动整理知识：
- 开始会话时（了解用户需求后）
- 完成重要功能时
- 结束会话前

---

## 一、知识库路径配置（三种方式）

m78 通过以下顺序查找数据库和 md 文件：

**方式1：环境变量 MEMORY78_PATH**

```bash
export MEMORY78_PATH=/workspace
# 会在 /workspace/memory78/ 下找 memory78.db
```

**方式2：配置文件 memory78.ini**

```ini
# 放在项目根目录或 docs/config/ 下
memory78_path = /workspace
```

**方式3：当前目录（默认）**

```bash
# 如果当前目录有 memory78.db，直接用
# 如果当前目录有 memory78/ 目录，用 memory78/memory78.db
# 都没有则创建 memory78.db
```

**推荐：用环境变量或配置文件，明确指定路径。**

---

## 二、四级分类体系

| 级别 | 名称 | 说明 | 示例 |
|------|------|------|------|
| 一级 | apisys | 多个微服务组合的系统 | steam, aicode, base |
| 二级 | apimicro | 微服务 | scan, price, inventory |
| 三级 | apiobj | 类或能力或微服务中的步骤 | buff_scan, steam_price |
| 四级 | apifun | 类中的函数（用/分隔） | buff_scan/get_price |

### 目录结构（三级目录）

```
memory78/
├── index.md                       ← 包含 active_apisys 列表
├── {apisys}/                      ← 一级：系统
│   ├── {apisys}.md                ← 同名.md
│   └── {apimicro}/                ← 二级：微服务
│       ├── {apimicro}.md          ← 同名.md
│       └── {apiobj}/              ← 三级：类/能力/步骤
│           ├── {apiobj}.md        ← 同名.md
│           └── {知识条目}.md       ← 知识文件（标题.md）
```

**apiobj 可以用 `/` 分隔表示函数层级**，如 `buff_scan/get_price`，但目录只建到第三级。

**每层目录都有同名.md**，记录该目录的说明和子目录清单。

---

## 三、分类判断流程（必须按此顺序）

### 第一步：扫描根目录，读取 active_apisys

```bash
cat memory78/index.md | grep active_apisys
# 输出：active_apisys: [aicode, steam, base, pro_steam, aigame, jhk]

ls memory78/
# 列出所有 apisys 目录
```

### 第二步：逐层扫描，检查同名.md

```bash
ls memory78/steam/                  # 列出 steam 的所有 apimicro
cat memory78/steam/steam.md         # 检查 steam 的说明

ls memory78/steam/scan/             # 列出 scan 的所有 apiobj
cat memory78/steam/scan/scan.md     # 检查 scan 的说明

ls memory78/steam/scan/buff_scan/   # 列出 buff_scan 的所有 apifun
cat memory78/steam/scan/buff_scan/buff_scan.md  # 检查 buff_scan 的说明
```

**同名.md 可能缺失**，需要修复。

### 第三步：修复同名.md（同步子目录清单）

同名.md 记录该目录下的子目录清单。**新建子目录后，需要同步到同名.md**。

```bash
# 扫描目录，检查同名.md 是否需要更新
m78 scan

# 自动修复：把新建的子目录写入同名.md
m78 scan --fix
```

**场景**：
- 新建了 `memory78/steam/scan/skin/` 目录
- 但 `memory78/steam/scan/scan.md` 里没有记录 skin
- `m78 scan --fix` 会自动把 skin 写入 scan.md

### 第四步：匹配分类

**有合适目录 → 直接用**

```bash
# 知识是日志组件使用方法
# ls 发现 memory78/base/logger/ 存在
# → 直接用：m78 add "标题" "内容" base logger mylogger
```

**没有合适目录 → 需要取名**

```bash
# 知识是定时任务调度
# ls 发现 memory78/aicode/ 下没有 scheduler/ 目录（apimicro）
# → 需要为新的 apimicro 取名
```

### 第五步：新增目录（取名）

**AI 根据以下四级命名规则取名**

**四级命名规则**：

| 级别 | 名称 | 说明 | 命名要点 |
|------|------|------|----------|
| 一级 | apisys | 系统 | 从 active_apisys 选择 |
| 二级 | apimicro | 微服务 | 面向需求或面向上下文 |
| 三级 | apiobj | 类/能力 | 操作对象 |
| 四级 | apifun | 函数 | 具体动作（用/分隔） |

**两种模式**：
- **模式A（面向需求）**：apimicro 是用户需求，如"数据保存"、"文件读取"
- **模式B（面向上下文）**：apimicro 是外部系统名，如"steam"、"buff"

**命名约束**：
- apimicro 和 apiobj 不允许下划线，只能一个单词
- apifun 可以用下划线，如 `get_price`

**示例**：
```
需求：用户需要把数据保存到数据库
命名：base/datastorage/table/smart_save
理由：面向需求，datastorage 表示数据保存，table 是操作对象，smart_save 是智能保存
```

---

## 四、m78 add 命令格式（位置参数）

**m78 用位置参数，不是 `apisys:xxx` 格式！**

```bash
m78 add "标题" "内容" apisys apimicro apiobj
```

**示例：**

```bash
# 正确格式（位置参数）
m78 add "buysell服务停止修复" "修复方法..." pro_steam design buysell

# apiobj 用 / 分隔表示函数层级
m78 add "获取Buff价格函数" "实现get_buff_price..." steam scan buff_scan/get_price

# 错误格式（不要用！）
m78 add "标题" "内容" apisys:pro_steam apimicro:design  # 错！
```

**参数说明：**
- 第3个参数：apisys（一级，系统）
- 第4个参数：apimicro（二级，微服务）
- 第5个参数：apiobj（三级，类/能力/步骤，可用 `/` 分隔表示函数）

**验证机制**：m78 会检查指定的分类是否在目录中存在，不存在则 fallback。

---

## 五、分类参考

| 内容类型 | apisys | apimicro | apiobj |
|---------|--------|----------|--------|
| 定时任务 | aicode | task | scheduler |
| 命令行工具 | aicode | cli | parser |
| 日志组件 | base | logger | mylogger |
| 错误处理 | base | error | handler |
| 配置管理 | base | config | loader |

---

## 六、常用命令

```bash
# 路径配置（三种方式任选其一）
export MEMORY78_PATH=/workspace
# 或在 memory78.ini 中配置 memory78_path = /workspace
# 或直接在 memory78 目录下运行

# 扫描目录，检查同名.md 是否需要更新
m78 scan

# 自动修复：把新建的子目录写入同名.md
m78 scan --fix

# 添加知识（用位置参数指定分类）
m78 add "标题" "内容" base logger mylogger

# apiobj 用 / 分隔表示函数层级
m78 add "参数验证函数" "实现参数校验..." aicode cli parser/validate

# 列出知识
m78 list --limit 10

# 搜索知识
m78 search "关键词"

# 获取详情
m78 get <ID>

# 删除（需要完整ID）
m78 delete <完整ID>
```

---

## 七、注意事项

1. **路径配置三种方式** - 环境变量、配置文件、当前目录
2. **四级分类体系** - apisys → apimicro → apiobj → apifun（用/分隔）
3. **目录只建三级** - 知识文件放在 apiobj 目录下
4. **用位置参数** - `m78 add "标题" "内容" apisys apimicro apiobj`
5. **先扫描目录** - 从 index.md 开始，逐层 ls 看目录结构
6. **检查同名.md** - 每层目录都有同名.md，新建子目录后用 `m78 scan --fix` 同步
7. **有合适目录直接用** - 不要强行创建新目录
8. **没有合适目录用提示词判断** - 选最接近的已有目录
9. **新增目录按规则取名** - 四级命名规则，面向需求或面向上下文
10. **内容要精炼** - 存的是知识摘要
11. **删除需要完整ID** - 不能只传前缀

---

> 完整命令和功能说明见 [README.md](README.md)

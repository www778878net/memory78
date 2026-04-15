# Memory78 AI 使用指南

> 本文档告诉 AI 如何将对话中产生的知识归纳到 memory78 知识库。

## 核心原则

**AI 主动整理本次会话中产生的知识，无需用户明确要求。**

**推荐主动指定分类**，大模型应该尽量用 `apisys:xxx apimicro:xxx apiobj:xxx` 明确指定，name78.rs 会验证是否在目录中存在，不存在才 fallback 到推断。

## 使用方式

把本文档直接扔给 AI，AI 会在以下时机自动整理知识：
- 开始会话时（了解用户需求后）
- 完成重要功能时
- 结束会话前

---

## 一、知识库路径配置（必须）

**MEMORY78_PATH 指向 memory78 的父目录。**

```bash
export MEMORY78_PATH=/workspace
```

---

## 二、分类原理

m78 的分类**不是靠关键词硬编码**，而是**根据目录结构智能推断**。

### 目录结构（真实）

```
memory78/
├── index.md                       ← 包含 active_apisys 列表
├── aicode/                        ← AI代码开发
│   ├── aicode.md
│   ├── cli/
│   ├── task/
│   └── workflow/
├── aigame/                        ← AI游戏开发
│   ├── aigame.md
│   ├── admin/
│   ├── api/
│   └── nowrole.md
├── apigame/                       ← 游戏API
│   └── apigame.md
├── axum78/                        ← Axum框架
│   ├── axum78.md
│   └── framework/
├── jhk/                           ← 极客嗨
│   ├── jhk.md
│   ├── debug/
│   ├── dev/
│   └── workflow/
├── pro_steam/                     ← Steam项目专属
│   ├── pro_steam.md
│   ├── cli/
│   ├── cookie/
│   ├── deploy/
│   ├── design/
│   └── project/
├── rustbase/                      ← Rust基础库
│   ├── base.md
│   ├── logger/
│   └── rusttrap/
├── workflow/                      ← 工作流
│   └── data_sync/
└── system/                        ← 系统配置
    └── static/
```

### 如何判断分类

**1. 先看 active_apisys**

读取 `memory78/index.md`，找到当前项目关注的 apisys。

**2. 根据内容选择最合适的 apisys**

看目录名判断这段知识属于哪个业务领域，不要靠关键词。

**3. 根据 apisys 下的子目录选择 apimicro**

```bash
ls memory78/aicode/
# 看到有: cli/, task/, workflow/
ls memory78/pro_steam/
# 看到有: cli/, cookie/, deploy/, design/, project/
ls memory78/rustbase/
# 看到有: logger/, rusttrap/
# 根据内容选择最接近的
```

**4. apiobj 用标题**

---

## 三、m78 add 命令格式

**推荐：主动指定分类**

```bash
m78 add "标题" "内容" apisys:aicode apimicro:cli apiobj:rust_cli_demo
```

**格式说明：**
- `apisys:` - 一级分类，如 `aicode`、`pro_steam`、`rustbase`
- `apimicro:` - 二级分类，如 `cli`、`task`、`logger`
- `apiobj:` - 对象名，默认用标题

**name78.rs 验证机制**：指定后只在该分类在目录中存在时才使用，不存在则 fallback 到目录结构推断。

**简单用法（不指定）：**
```bash
m78 add "Rust CLI实现" "使用clap解析命令行参数"
# 完全靠目录结构推断
```

---

## 四、分类判断流程

当需要给知识分类时，AI 应该：

1. **读取 active_apisys**：`cat memory78/index.md`
2. **理解内容**：这段知识是关于什么的？
3. **匹配 apisys**：根据目录名判断
   - 目录叫 `aicode` → AI代码开发相关
   - 目录叫 `rustbase` → Rust基础设施
   - 目录叫 `pro_steam` → Steam项目相关
4. **匹配 apimicro**：根据子目录判断
   - `aicode/cli/` → CLI相关
   - `rustbase/logger/` → 日志相关
5. **生成 apiobj**：用标题的关键词
6. **组合成命令**：在 m78 add 后用 `apisys:xxx apimicro:xxx apiobj:xxx` 格式明确指定

---

## 五、示例判断

### 例1：Rust CLI 实现
```
内容：使用clap解析命令行参数，支持子命令和参数补全

判断：
1. 内容属于 Rust 代码开发
2. 匹配 apisys = aicode（代码开发）
3. 匹配 apimicro = cli（命令行相关）
4. apiobj = rust_clap_cli（用标题）

命令：m78 add "Rust CLI实现" "使用clap解析命令行参数" apisys:aicode apimicro:cli apiobj:rust_clap_cli
```

### 例2：MyLogger 日志组件
```
内容：统一日志组件，支持detail/error/info/warn四级，支持文件和控制台输出

判断：
1. 内容属于 Rust 基础设施
2. 匹配 apisys = rustbase（Rust基础库）
3. 匹配 apimicro = logger（日志相关）
4. apiobj = my_logger（用标题）

命令：m78 add "MyLogger日志组件" "统一日志组件" apisys:rustbase apimicro:logger apiobj:my_logger
```

### 例3：Steam Cookie 管理
```
内容：Steam Cookie 存储和自动刷新机制

判断：
1. 内容属于 Steam 项目
2. 匹配 apisys = pro_steam（Steam项目）
3. 匹配 apimicro = cookie（Cookie相关）
4. apiobj = steam_cookie（用标题）

命令：m78 add "Steam Cookie管理" "Cookie存储和自动刷新" apisys:pro_steam apimicro:cookie apiobj:steam_cookie
```

### 例4：工作流数据同步
```
内容：定时同步外部数据到本地数据库，支持增量更新

判断：
1. 内容属于工作流
2. 匹配 apisys = workflow（工作流）
3. 匹配 apimicro = data_sync（数据同步）
4. apiobj = data_sync（用标题）

命令：m78 add "工作流数据同步" "定时同步外部数据" apisys:workflow apimicro:data_sync apiobj:data_sync
```

---

## 六、常见问题

### Q: 如何知道有哪些 apisys？

```bash
cat memory78/index.md | grep active_apisys
ls memory78/
```

### Q: 如何知道有哪些 apimicro？

```bash
ls memory78/aicode/          # aicode 有哪些子目录
ls memory78/pro_steam/        # pro_steam 有哪些子目录
ls memory78/rustbase/         # rustbase 有哪些子目录
```

### Q: 目录里没有完全匹配的怎么办？

选择最接近的目录，或创建新目录（如果有权限）。

### Q: 分类结果不对怎么办？

可以后续手动调整文件路径和数据库记录。

---

## 七、常用命令

```bash
# 添加知识（自动分类）
m78 add "标题" "内容"

# 扫描目录，检查缺失索引
m78 scan

# 搜索知识
m78 search "关键词"

# 列出所有知识
m78 list
```

---

## 八、注意事项

1. **不要用虚假目录举例** - 只用 memory78 真实存在的目录
2. **先看 index.md** - 了解 active_apisys
3. **看目录名判断** - 根据目录结构推断，不是靠关键词硬编码
4. **内容要精炼** - 存的是知识摘要
5. **标题要简洁** - 一句话，能概括核心

---

> 完整命令和功能说明见 [README.md](README.md)

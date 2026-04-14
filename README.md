# Memory78 CLI

---

## 给 AI 编码助手的使用指南

### 1. 下载 CLI

从 GitHub Release 下载 m78.exe：

```
https://github.com/www778878net/memory78/releases/latest
```

**Windows:** 下载 `m78.exe`，放到项目目录或 PATH 中。

### 2. 验证安装

```bash
m78 --help
```

如果命令不可用，使用绝对路径：
```bash
# 替换为实际路径
D:\path\to\m78.exe --help
```

### 3. 常用命令

```bash
# 添加记忆（自动分类）
m78 add "标题" "内容"

# 搜索记忆
m78 search "关键词"

# 列出记忆
m78 list

# 获取详情
m78 get <id或标题>

# 删除记忆
m78 delete <id或标题>

# 导入已有文件
m78 import

# 每日日志
m78 daily "日志内容"
```

### 4. 四级分类

记忆按 `{apisys}/{apimicro}/{apiobj}/{title}.md` 存储：
- `apisys`: 大系统（如 project, steam）
- `apimicro`: 微服务（如 api, workflow）
- `apiobj`: 实体/类（如 user, config）

---

## 中文版

### 为什么需要 Memory78？

| 痛点 | Memory78 解决方案 |
|------|------------------|
| AI 每次都要读取完整文档 | QMD 智能搜索，只返回相关片段，节省 75-95% Token |
| 知识散落各处，难以查找 | 四级分类结构，人和 AI 都能快速定位 |
| 记忆保存不直观 | 自动分类存储，用户只输入内容即可 |
| 知识无法形成体系 | SQLite + 文件双存储，结构化组织 |

### 安装

从 [Releases](https://github.com/www778878net/memory78/releases) 下载对应平台可执行文件。

**Windows:** 下载 `m78.exe`，放到项目目录或添加到 PATH。

### 基本用法

```bash
# 添加记忆（自动分类）
m78 add "API设计" "用户认证使用JWT..."

# 手动指定分类
m78 add "配置说明" "数据库配置..." project config db

# 搜索记忆
m78 search "关键词"

# QMD 模式（节省 75-95% Token）
m78 search "关键词" --mode qmd

# 列出记忆
m78 list --limit 10

# 获取详情
m78 get <id或标题>

# 删除记忆
m78 delete <id或标题>

# 导入已有文件
m78 import

# 导出数据
m78 export

# 每日日志
m78 daily "今日工作内容"
```

### 命令详解

#### add - 添加记忆

```bash
m78 add "标题" "内容" [apisys] [apimicro] [apiobj]

# 选项
--mode <insert|append|update|overwrite>  操作模式
--format <md|json>                       文件格式
--tags <tag1> <tag2> ...                 自定义标签
```

#### search - 搜索记忆

```bash
m78 search "关键词"

# 选项
--apisys <value>     按大系统过滤
--apimicro <value>   按微服务过滤
--apiobj <value>     按实体过滤
--tags <tag1,tag2>   标签过滤
--limit <n>          限制数量
--mode <text|semantic|qmd>  搜索模式
```

#### list - 列出记忆

```bash
m78 list --limit 10 --order desc
```

### 数据存储

| 存储方式 | 路径 | 说明 |
|---------|------|------|
| 数据库 | `memory78/memory78.db` | SQLite + FTS5 全文索引 |
| 文件 | `memory78/{apisys}/{apimicro}/{apiobj}/{title}.md` | Markdown/JSON |

### 搜索模式对比

| 模式 | 用途 | Token 消耗 |
|------|------|-----------|
| text | FTS5 全文搜索 | 完整文档 |
| semantic | 向量相似度 | 完整文档 |
| qmd | 片段索引 + LLM 重排序 | **节省 75-95%** |

---

## English Version

### Why Memory78?

| Problem | Memory78 Solution |
|---------|------------------|
| AI reads full documents every time | QMD smart search returns only relevant fragments, saves 75-95% tokens |
| Knowledge scattered everywhere | 4-level classification structure for quick navigation |
| Memory saving not intuitive | Auto-classification, just input content |
| Knowledge not organized | SQLite + file dual storage |

### Installation

Download from [Releases](https://github.com/www778878net/memory78/releases).

**Windows:** Download `m78.exe`, place in project directory or add to PATH.

### Basic Usage

```bash
# Add memory (auto-classified)
m78 add "API Design" "User authentication using JWT..."

# Manual classification
m78 add "Config" "Database config..." project config db

# Search memory
m78 search "keyword"

# QMD mode (saves 75-95% tokens)
m78 search "keyword" --mode qmd

# List memories
m78 list --limit 10

# Get details
m78 get <id or title>

# Delete memory
m78 delete <id or title>

# Import existing files
m78 import

# Export data
m78 export

# Daily log
m78 daily "Today's work"
```

### Command Reference

#### add - Add memory

```bash
m78 add "title" "content" [apisys] [apimicro] [apiobj]

# Options
--mode <insert|append|update|overwrite>  Operation mode
--format <md|json>                       File format
--tags <tag1> <tag2> ...                 Custom tags
```

#### search - Search memory

```bash
m78 search "keyword"

# Options
--apisys <value>     Filter by system
--apimicro <value>   Filter by microservice
--apiobj <value>     Filter by entity
--tags <tag1,tag2>   Filter by tags
--limit <n>          Limit results
--mode <text|semantic|qmd>  Search mode
```

#### list - List memories

```bash
m78 list --limit 10 --order desc
```

### Data Storage

| Storage | Path | Description |
|---------|------|-------------|
| Database | `memory78/memory78.db` | SQLite + FTS5 full-text index |
| Files | `memory78/{apisys}/{apimicro}/{apiobj}/{title}.md` | Markdown/JSON |

### Search Mode Comparison

| Mode | Use Case | Token Usage |
|------|----------|-------------|
| text | FTS5 full-text search | Full document |
| semantic | Vector similarity | Full document |
| qmd | Fragment index + LLM reranking | **Saves 75-95%** |

---

## License

MIT

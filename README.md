# Memory78 CLI

**高性能本地知识库引擎** — 让 AI 编码助手节省 75-95% Token，知识永久保存、快速定位。

## 为什么需要 Memory78？

| 痛点 | Memory78 解决方案 |
|------|------------------|
| AI 每次都要读取完整文档 | QMD 智能搜索，只返回相关片段，节省 75-95% Token |
| 知识散落各处，难以查找 | 四级分类结构，人和 AI 都能快速定位 |
| 记忆保存不直观 | 自动分类存储，用户只输入内容即可 |
| 知识无法形成体系 | SQLite + 文件双存储，结构化组织 |

## 核心功能

### 1. 智能搜索（节省 Token）

```bash
# QMD 模式：只返回相关片段，节省 75-95% Token
m78 search "base78" --mode qmd

# FTS5 全文搜索
m78 search "关键词"

# 语义搜索（向量相似度）
m78 search "关键词" --mode semantic
```

### 2. 四级分类存储

记忆按 `{apisys}/{apimicro}/{apiobj}/{title}.md` 自动组织：

```
memory78/
├── project/           # apisys: 大系统
│   ├── api/           # apimicro: 微服务
│   │   ├── user/      # apiobj: 实体/类
│   │   │   └── 登录设计.md
│   │   └── config/
│   │       └── 数据库配置.md
│   └── workflow/
│       └── 订单流程.md
└── steam/
    └── buff/
        └── 价格策略.md
```

### 3. 自动分类（name78 算法）

```bash
# 不用指定分类，自动识别
m78 add "API设计" "用户认证使用JWT..." 
# → 自动分类为 project/api/api_design

# 也可以手动指定
m78 add "配置说明" "数据库配置..." project config db
```

### 4. AI 编码助手集成

配置为 Claude Skill 后，AI 自动管理知识：

```yaml
# skills/SKILL.md
hooks:
  SessionStart:
    - type: command
      command: m78 import
```

## 快速开始

### 安装

从 [Releases](https://github.com/www778878net/memory78/releases) 下载对应平台可执行文件。

### 基本用法

```bash
# 添加记忆
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

# 导出数据
m78 export

# 每日日志
m78 daily "今日工作内容"
```

## 命令详解

### add - 添加记忆

```bash
m78 add "标题" "内容" [apisys] [apimicro] [apiobj]

# 选项
--mode <insert|append|update|overwrite>  操作模式
--format <md|json>                       文件格式
--tags <tag1> <tag2> ...                 自定义标签
```

### search - 搜索记忆

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

### list - 列出记忆

```bash
m78 list --limit 10 --order desc
```

### get / delete / import / export / daily

详见 `--help`。

## 数据存储

| 存储方式 | 路径 | 说明 |
|---------|------|------|
| 数据库 | `memory78/memory78.db` | SQLite + FTS5 全文索引 |
| 文件 | `memory78/{apisys}/{apimicro}/{apiobj}/{title}.md` | Markdown/JSON |

## 搜索模式对比

| 模式 | 用途 | Token 消耗 |
|------|------|-----------|
| text | FTS5 全文搜索 | 完整文档 |
| semantic | 向量相似度 | 完整文档 |
| qmd | 片段索引 + LLM 重排序 | **节省 75-95%** |

## 四级分类说明

| 级别 | 说明 | 示例 |
|------|------|------|
| apisys | 大系统 | project, steam, data |
| apimicro | 微服务 | api, workflow, config |
| apiobj | 实体/类 | user, order, payment |

## Claude Skill 集成

将 `skills/` 目录配置为 Claude Skill，AI 编码助手可自动管理知识。

## License

MIT

# Memory78 CLI

**[English](README_EN.md) | 中文**

高性能本地知识库引擎，用于管理代码知识和项目记忆。

## 最简实现

**把 AI 变成你的知识整理助手：**

在与 AI 开始会话之前/聊一段时间之后/结束会话之前，把 `memory78-for-ai.md` 直接扔给 AI，它就会自动整理本次会话中产生的知识。

```
用户：把 memory78-for-ai.md 扔给 AI
AI：了解，我会按照这个指南整理知识
用户：帮我实现XXX功能
...（正常对话）...
AI：好的，已完成。关于这个功能有几点知识我帮你存一下：
     - m78 add "XXX功能实现" "实现细节..."
用户：好的
```

## 为什么需要 Memory78？

| 痛点                    | Memory78 解决方案                               |
| ----------------------- | ----------------------------------------------- |
| AI 每次都要读取完整文档 | QMD 智能搜索，只返回相关片段，节省 75-95% Token |
| 知识散落各处，难以查找  | 四级分类结构，人和 AI 都能快速定位              |
| 记忆保存不直观          | 自动分类存储，用户只输入内容即可                |
| 知识无法形成体系        | SQLite + 文件双存储，结构化组织                 |

## 安装

从 [Releases](https://github.com/www778878net/memory78/releases) 下载对应平台可执行文件。

**Windows:** 下载 `m78.exe`，放到项目目录或添加到 PATH。

**Claude Skill:** 复制 `skills/memory78` 目录到 `.claude/skills/`。

## 快速开始

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

配置为 Claude Skill 后，AI 自动管理知识。

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

| 存储方式 | 路径                                               | 说明                   |
| -------- | -------------------------------------------------- | ---------------------- |
| 数据库   | `memory78/memory78.db`                             | SQLite + FTS5 全文索引 |
| 文件     | `memory78/{apisys}/{apimicro}/{apiobj}/{title}.md` | Markdown/JSON          |

## 搜索模式分级

### L0 零模型（开箱即用，无需下载）

| 模式   | 用途                  | Token 消耗 | 依赖 |
| ------ | --------------------- | ---------- | ---- |
| text   | FTS5 全文搜索         | 完整文档   | 无   |
| list   | 三级标签定位          | 完整文档   | 无   |
| wiki   | 目录浏览(index.md)    | 手动阅读   | 无   |

### L1 语义搜索（下载 1 个模型 ~350MB）

| 模式     | 用途                  | Token 消耗 | 依赖                      |
| -------- | --------------------- | ---------- | ------------------------- |
| semantic | 向量相似度搜索        | 完整文档   | embeddinggemma-300M       |
| hybrid   | text + semantic 结合  | 完整文档   | embeddinggemma-300M       |

### L2 QMD 智能搜索（下载 3 个模型 ~2GB）

| 模式 | 用途                       | Token 消耗       | 依赖      |
| ---- | -------------------------- | ---------------- | --------- |
| qmd  | 查询扩展 + 向量 + 重排序   | **节省 75-95%**  | 3 个模型  |

### auto 自动模式

```bash
m78 search "关键词" --mode auto
```

自动按可用性降级：qmd → hybrid → text，哪个能用用哪个。

## 模型说明

> 模型下载地址：https://github.com/www778878net/models

| 模型文件                               | 用途         | 参数量 | 大小     | 被谁使用                  |
| -------------------------------------- | ------------ | ------ | -------- | ------------------------- |
| embeddinggemma-300M-Q8_0.gguf         | 文本向量化   | 300M   | ~350MB   | semantic / hybrid / qmd   |
| qmd-query-expansion-1.7B-q4_k_m.gguf  | 查询扩展     | 1.7B   | ~1GB     | qmd                       |
| qwen3-reranker-0.6b-q8_0.gguf         | 结果重排序   | 0.6B   | ~650MB   | qmd                       |

**各模型做什么：**

- **文本向量化(embeddinggemma)**：把文字转成数字向量，让"路由机制"和"route handler"这样的语义相近的词能匹配上
- **查询扩展(query-expansion)**：把简短查询扩展成多个变体，如"路由"→["路由机制", "route handler", "API路由"]，提升召回率
- **结果重排序(reranker)**：对搜索结果重新排序，把最相关的排到最前面

## 渐进式升级

```
安装 m78 → 直接用 text/list/wiki（零门槛）
           ↓ 想要语义搜索
    下载 1 个模型 (~350MB) → 开通 semantic / hybrid
           ↓ 想要省 Token
    再下载 2 个模型 (~1.65GB) → 开通 qmd（省 75-95% Token）
```

```bash
# 第一步：零模型即可使用
m78 add "标题" "内容"
m78 search "关键词"              # text 模式，无需任何模型

# 第二步：下载 embeddinggemma 后开通语义搜索
m78 search "自然语言描述" --mode semantic

# 第三步：下载全部 3 个模型后开通 QMD
m78 search "关键词" --mode qmd   # 省 75-95% Token
```

## 四级分类说明

| 级别     | 说明           | 示例                        |
| -------- | -------------- | --------------------------- |
| apisys   | 大系统         | project, steam, data        |
| apimicro | 微服务         | api, workflow, config       |
| apiobj   | 实体/类        | user, order, payment        |
| apifun   | 函数/属性/方法 | login, validate, get_config |



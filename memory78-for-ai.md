# Memory78 AI 使用指南

> 本文档告诉 AI 如何将对话中产生的知识归纳到 memory78 知识库。

## 核心原则

**AI 主动整理本次会话中产生的知识，无需用户明确要求。**

不需要用户指定 apisys/apimicro/apiobj，AI 通过内容分析自动推断。

## 使用方式

把本文档直接扔给 AI，AI 会在以下时机自动整理知识：
- 开始会话时（了解用户需求后）
- 完成重要功能时
- 结束会话前

---

## 一、知识库结构

memory78 是 Git submodule，结构如下：

```
memory78/                          ← Git submodule，独立仓库
├── index.md                       ← 首页，包含 active_apisys
├── memory78.db                   ← SQLite 搜索库
├── {apisys}/                     ← 一级：apisys 大系统
│   ├── {apisys}.md               ← 该系统的索引页
│   └── {apimicro}/               ← 二级：apimicro 微服务
│       ├── {apimicro}.md         ← 该微服务的索引页
│       └── {apiobj}/              ← 三级：apiobj 实体/能力
│           └── {apiobj}.md       ← 知识条目
```

**重要：每个目录都有同名 .md 索引文件。**

---

## 二、配置方式（必须）

### 第一步：查看 active_apisys

先读取 `memory78/index.md`，找到当前项目的 `active_apisys`：

```markdown
active_apisys: [aicode, steam, base, pro_steam, aigame, jhk]
```

这告诉 AI 当前项目关注哪些 apisys，知识应该存到这些目录下。

### 第二步：设置环境变量

在项目根目录设置：

```bash
export MEMORY78_PATH=/workspace/memory78
```

或者创建 `memory78.ini`：

```ini
memory78_dir = /workspace/memory78
```

### 第三步：确认目录存在

```bash
ls memory78/index.md  # 确认 submodule 已初始化
```

---

## 三、分类查询

在决定存到哪个 apisys 之前，先查目录结构：

### 查 index.md 了解 active_apisys

```bash
cat memory78/index.md
```

### 查 {apisys}/{apisys}.md 了解该系统有什么 apimicro

```bash
cat memory78/pro_steam/pro_steam.md
```

### 查 {apisys}/{apimicro}/{apimicro}.md 了解该微服务有什么 apiobj

---

## 四、m78 add 命令格式

```bash
m78 add "标题" "内容"
```

**标题**：简洁，一句话说明是什么
**内容**：知识的核心内容，可以是多行 markdown

### 示例

```bash
m78 add "API 认证流程" "1. 客户端发送 JWT Token\n2. 服务端验证签名\n3. 返回用户信息"

m78 add "Rust 错误处理模式" "使用 anyhow crate，通过 ? 运算符传播错误，重大错误用 anyhow::bail!() 直接返回"

m78 add "Docker 容器通信" "同网络容器用容器名互通，如 postgres://db:5432"
```

---

## 五、自动分类规则

m78 通过关键词自动推断三级分类：

### apisys 推断（系统级）

根据 `memory78/index.md` 的 `active_apisys` 列表匹配。

| 关键词 | apisys |
|--------|---------|
| 日志 / Logger | base |
| 配置 / Config | base |
| 错误 / Error / Bug | base |
| 工作流 / Workflow | aicode |
| AI / 模型 / LLM | ai |
| Claude / 技能 / Skill | claude |

### apimicro 推断（服务级）

| 关键词 | apimicro |
|--------|---------|
| 扫描 / Scan | scan |
| 价格 / Price | price |
| 库存 / Inventory | inventory |
| 策略 / Strategy | strategy |
| 订单 / Order | order |
| 交易 / Trade | trade |
| 能力 / Capability | capability |
| 工作流 / Workflow | workflow |

### apiobj 推断（操作级）

| 关键词 | apiobj |
|--------|---------|
| 扫描 / 获取 / 查询 | scan |
| 获取 / Fetch / Get | get |
| 新增 / 创建 | create |
| 更新 / 修改 | update |
| 删除 | delete |
| 保存 / 存储 | save |
| 校验 / 验证 | validate |

---

## 六、分类优先级

1. **active_apisys 优先**：只存到 `memory78/index.md` 中列出的 apisys
2. **现有目录匹配**：扫描 memory78 目录，优先归并到已有位置
3. **关键词推断**：根据内容和标题匹配关键词表
4. **Fallback**：标题转为 apiobj，其他用 `tmp`

---

## 七、目录结构示例

```
memory78/
├── index.md                       ← active_apisys 在这里
├── base/
│   ├── base.md                    ← base 系统的索引
│   ├── logger/
│   │   └── 日志最佳实践.md
│   └── error/
│       └── 错误处理指南.md
├── aicode/
│   └── workflow/
│       └── 状态机设计.md
└── pro_steam/                    ← 项目专属知识
    └── trade/
        └── 订单处理.md
```

---

## 八、Smart Merge 智能归并

`m78 add` 默认使用 smart 模式，自动处理三种情况：

### 模式 A：精确匹配
文件已存在 → 检查内容哈希
- 相同：跳过（幂等）
- 不同：追加到文件末尾

### 模式 B：同类项归并
发现相似的 apiobj → 归并到最相近的已有条目

### 模式 C：全新条目
没有匹配 → 创建新文件 + 自动创建索引

---

## 九、常用命令

```bash
# 添加知识（自动分类）
m78 add "标题" "内容"

# 扫描目录，检查缺失索引
m78 scan

# 修复缺失索引
m78 scan --fix

# 搜索知识
m78 search "关键词"

# 列出所有知识
m78 list

# 获取详情
m78 get <id或标题>
```

---

## 十、注意事项

1. **先查 index.md**：确认 active_apisys 再决定存哪
2. **内容要精炼**：存的是知识摘要，不是完整文档
3. **标题要简洁**：一句话，能概括核心
4. **标签自动生成**：无需手动指定 tags
5. **幂等操作**：相同内容重复 add 不会创建重复条目
6. **分类错误可以修正**：后续可以手动调整 apisys/apimicro/apiobj

---

> 完整命令和功能说明见 [README.md](README.md)

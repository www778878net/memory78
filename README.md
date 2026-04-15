# Memory78 AI 使用指南

> 本文档告诉 AI 如何将对话中产生的知识归纳到 memory78 知识库。

## 核心原则

**用户只需要说"存到知识库"，AI 自动完成分类和存储。**

不需要用户指定 apisys/apimicro/apiobj，AI 通过内容分析自动推断。

---

## 一、触发时机

当用户说以下类似的话时，AI 应该调用 m78 add：

| 用户说 | AI 理解 |
|--------|---------|
| `把这个存到知识库` | 调用 m78 add |
| `刚才的帮我记一下` | 调用 m78 add |
| `保存这个知识` | 调用 m78 add |
| `记一下这个` | 调用 m78 add |

---

## 二、m78 add 命令格式

```bash
m78 add "标题" "内容"
```

**标题**：简洁，一句话说明是什么
**内容**：知识的核心内容，可以是多行 markdown

### 示例

```bash
m78 add "Steam Buff 价格扫描流程" "1. 调用 Buff API 获取价格\n2. 对比 Steam 市场均价\n3. 返回最低价链接"

m78 add "Rust 错误处理模式" "使用 anyhow crate，通过 ? 运算符传播错误，重大错误用 anyhow::bail!() 直接返回"

m78 add "Docker 容器通信" "同网络容器用容器名互通，如 postgres://db:5432"
```

---

## 三、自动分类规则

m78 通过关键词自动推断三级分类：

### apisys 推断（系统级）

| 关键词 | apisys |
|--------|---------|
| Steam / Buff / 库存 / 交易 | steam |
| Claude / 技能 / Skill | claude |
| AI / 模型 / LLM | ai |
| 日志 / Logger | base |
| 工作流 / Workflow | aicode |
| 配置 / Config | base |
| 错误 / Error / Bug | base |
| 游戏 / Game / NPC | aigame |

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

## 四、分类优先级

1. **用户显式指定**：`m78 add "标题" "内容" steam inventory scan`
2. **现有目录匹配**：扫描 memory78 目录，优先归并到已有位置
3. **关键词推断**：根据内容和标题匹配关键词表
4. **Fallback**：标题转为 apiobj，其他用 `tmp`

---

## 五、目录结构

存储位置：`memory78/{apisys}/{apimicro}/{apiobj}/{标题}.md`

```
memory78/
├── steam/
│   ├── scan/
│   │   └── Buff价格扫描.md
│   └── price/
│       └── 市场均价对比.md
├── base/
│   ├── logger/
│   │   └── Rust日志最佳实践.md
│   └── error/
│       └── anyhow使用指南.md
└── aicode/
    └── workflow/
        └── 状态机设计.md
```

---

## 六、文件格式

```markdown
---
title: {标题}
tags: [{apiobj}, {apisys}, {apimicro}]
created_at: {时间}
hash: {内容哈希}
apisys: {apisys}
apimicro: {apimicro}
apiobj: {apiobj}
---

# {标题}

> apisys: {apisys} | apimicro: {apimicro} | apiobj: {apiobj}

## 摘要

{一句话说明核心知识}

## 关键知识

- 要点1
- 要点2
- 要点3

## 使用场景

{什么情况下会用这个知识}
```

---

## 七、Smart Merge 智能归并

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

## 八、配置方式

### 环境变量（推荐）
```bash
export MEMORY78_PATH=/path/to/memory78
```

### 配置文件
在项目根目录创建 `memory78.ini`：
```ini
memory78_dir = /path/to/memory78
```

### 自动查找
如果都没有设置，默认使用当前目录

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

1. **内容要精炼**：存的是知识摘要，不是完整文档
2. **标题要简洁**：一句话，能概括核心
3. **标签自动生成**：无需手动指定 tags
4. **幂等操作**：相同内容重复 add 不会创建重复条目
5. **分类错误可以修正**：后续可以手动调整 apisys/apimicro/apiobj

# Memory78 AI 使用指南

> 本文档告诉 AI 如何将对话中产生的知识归纳到 memory78 知识库。

## 核心原则

**AI 主动整理本次会话中产生的知识，无需用户明确要求。**

**重要：不要手动指定分类！让 m78 自动推断。**

## 使用方式

把本文档直接扔给 AI，AI 会在以下时机自动整理知识：
- 开始会话时（了解用户需求后）
- 完成重要功能时
- 结束会话前

---

## 一、知识库路径配置（必须）

**MEMORY78_PATH 指向 memory78 的父目录，代码会在此目录下找 memory78 子目录。**

### 方式一：环境变量

```bash
export MEMORY78_PATH=/path/to/parent    # 指向 memory78 的父目录
```

例如 memory78 在 `/workspace/memory78`，则：
```bash
export MEMORY78_PATH=/workspace
```

### 方式二：配置文件

在项目根目录创建 `memory78.ini`：

```ini
memory78_path = /path/to/parent    # 指向 memory78 的父目录
```

**两者选一，推荐环境变量。**

---

## 二、知识库结构

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

## 三、确定 active_apisys

如果 memory78 目录存在，先读取 `memory78/index.md`：

```bash
cat memory78/index.md
```

找到 `active_apisys` 列表：

```markdown
active_apisys: [aicode, steam, base, pro_steam]
```

这告诉 AI 当前项目关注哪些 apisys，知识应该存到这些目录下。

如果 memory78 不存在，跳过此步骤。

---

## 四、m78 add 命令格式

**❌ 错误示例（不要这样做）：**
```bash
m78 add "标题" "内容" steam scan price   # 不要手动指定分类！
```

**✅ 正确示例（让 m78 自动分类）：**
```bash
m78 add "Steam价格扫描" "扫描Steam市场最低价"
m78 add "Rust错误处理" "使用 anyhow crate"
m78 add "Buff库存同步" "同步用户Buff库存"
```

**m78 会自动根据内容推断分类：**
- "Steam价格" → apisys=steam
- "扫描" → apimicro=scan
- 标题自动转为 apiobj

---

## 五、自动分类规则

m78 通过以下顺序自动推断分类：

### 1. 先扫描 memory78 目录结构

m78 会扫描现有目录，找到所有 apisys/apimicro/apiobj。

### 2. 匹配现有目录

如果内容提到 "Steam"、"库存"、"扫描"，会优先匹配到已有的 `steam/scan/` 目录。

### 3. 匹配 active_apisys

根据 `index.md` 中的 `active_apisys` 列表，只在这些目录下分类。

### 4. 关键词推断 fallback

如果现有目录都不匹配，才用关键词推断：
- "日志" → base
- "错误" → base
- "工作流" → aicode
- "扫描" → scan

---

## 六、常见问题

### Q: AI 喜欢手动指定分类怎么办？

**A:** 明确告诉 AI："不要手动指定分类，m78 会自动推断"。

### Q: 分类结果不对怎么办？

**A:** 可以后续手动调整文件路径和数据库记录。

### Q: 想指定分类怎么办？

**A:** 只有在明确知道分类且现有目录已有时才指定，否则让 m78 自动推断。

---

## 七、常用命令

```bash
# 添加知识（自动分类，不需要指定！）
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

1. **不要手动指定分类** - 让 m78 自动推断
2. **先查 index.md** - 确认 active_apisys 再决定存哪
3. **内容要精炼** - 存的是知识摘要，不是完整文档
4. **标题要简洁** - 一句话，能概括核心
5. **幂等操作** - 相同内容重复 add 不会创建重复条目

---

> 完整命令和功能说明见 [README.md](README.md)

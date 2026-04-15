# Memory78 AI 使用指南

> 本文档告诉 AI 如何将对话中产生的知识归纳到 memory78 知识库。

## 核心原则

**AI 主动整理本次会话中产生的知识，无需用户明确要求。**

**重要：不要手动指定分类！让 m78 根据目录结构自动推断。**

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

### 目录结构示例

```
memory78/
├── index.md                       ← 包含 active_apisys 列表
├── aicode/                       ← AI代码开发
│   ├── aicode.md
│   ├── cli/
│   └── task/
├── steam/                        ← Steam交易业务
│   ├── steam.md
│   ├── scan/
│   ├── price/
│   └── inventory/
├── base/                         ← 基础库（日志、错误、配置）
│   ├── base.md
│   ├── logger/
│   └── error/
├── pro_steam/                    ← 项目专属知识
└── ...
```

### 如何判断分类

**1. 先看 active_apisys**

读取 `memory78/index.md`，找到当前项目关注的 apisys：

```markdown
active_apisys: [aicode, steam, base, pro_steam, aigame, jhk]
```

**2. 根据内容选择最合适的 apisys**

如果知识是关于：
- Steam 交易、Buff、库存 → `steam`
- AI 代码、workflow、task → `aicode`
- 日志、错误、配置、基础设施 → `base`
- 项目专属业务逻辑 → `pro_steam`
- 游戏开发、NPC、Lord → `aigame`

**3. 根据 apisys 下的目录结构选择 apimicro**

```bash
ls memory78/steam/
# 看到有: scan/, price/, inventory/, dataservice/
# 根据内容选择最接近的
```

**4. apiobj 用标题**

---

## 三、m78 add 命令格式

**❌ 错误示例：**
```bash
m78 add "标题" "内容" steam scan price   # 不要手动指定！
```

**✅ 正确示例：**
```bash
m78 add "Steam价格扫描" "扫描Steam市场最低价"
m78 add "Rust错误处理" "使用 anyhow crate"
m78 add "Buff库存同步" "同步用户Buff库存"
```

---

## 四、分类判断流程

当需要给知识分类时，AI 应该：

1. **读取 active_apisys**：`cat memory78/index.md`
2. **理解内容**：这段知识是关于什么的？
3. **匹配 apisys**：根据目录名判断，不是关键词
   - 目录叫 `steam` → 关于 Steam 的放这里
   - 目录叫 `base` → 基础设施放这里
4. **匹配 apimicro**：根据子目录判断
   - `steam/scan/` → 扫描相关
   - `steam/price/` → 价格相关
5. **生成 apiobj**：用标题的关键词

---

## 五、示例判断

### 例1：Steam Buff 价格扫描
```
内容：扫描用户Buff价格，获取Steam市场最低价

判断：
1. active_apisys 有 steam ✓
2. 内容提到 "Steam"、"Buff"、"价格"
3. 匹配 apisys = steam
4. 匹配 apimicro = price（价格相关）
5. apiobj = steam_buff_price（用标题）

结果：steam/price/steam_buff_price
```

### 例2：Rust 日志组件
```
内容：使用 MyLogger 进行日志记录

判断：
1. active_apisys 有 base ✓
2. 内容提到 "日志"
3. 匹配 apisys = base
4. 匹配 apimicro = logger（日志相关）
5. apiobj = rust日志组件（用标题）

结果：base/logger/rust日志组件
```

### 例3：工作流任务
```
内容：定时任务调度器实现

判断：
1. active_apisys 有 aicode ✓
2. 内容提到 "任务"、"调度"
3. 匹配 apisys = aicode
4. 匹配 apimicro = task（任务相关）
5. apiobj = 定时任务调度器（用标题）

结果：aicode/task/定时任务调度器
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
ls memory78/steam/          # steam 有哪些子目录
ls memory78/base/            # base 有哪些子目录
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

1. **不要手动指定分类** - 根据目录结构判断
2. **先看 index.md** - 了解 active_apisys
3. **看目录名判断** - 不是靠关键词硬编码
4. **内容要精炼** - 存的是知识摘要
5. **标题要简洁** - 一句话，能概括核心

---

> 完整命令和功能说明见 [README.md](README.md)

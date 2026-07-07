---
name: memory78
description: 记忆管理系统 - 四级分类存储与检索
user-invocable: true
---

# memory78 - 记忆管理系统

## ⚡ 首次加载自动配置 Hook

AI 加载此 skill 时，自动检测平台并写入对应配置文件：

| 平台 | 配置文件 |
|------|----------|
| Claude Code | `.claude/settings.json` |
| CodeBuddy | `.codebuddy/settings.json` |

写入内容（`{PROJECT_DIR}` 替换为实际路径）：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {"hooks": [{"type": "command", "command": "python3 {PROJECT_DIR}/.codebuddy/skills/memory78/hooks/record_user_input.py", "timeout": 10}]}
    ]
  }
}
```

同时确保 `hooks/` 下的脚本复制到项目对应 hooks 目录。

配置后每次对话自动调用 `m78 daily` 记录到 `memory78/system/static/daily/{日期}.md`。

> 注：如需同时记录 AI 回复，对话中说 "记录本次会话到 memory78" 手动触发。

---

## 快速开始

```bash
m78 add "标题" "内容"
m78 search "关键词" --mode qmd
m78 list
m78 get <id>
m78 delete <id>
```

## 命令列表

| 命令 | 功能 | 示例 |
|------|------|------|
| add | 添加记忆 | `m78 add "标题" "内容"` |
| list | 列出记忆 | `m78 list --limit 10` |
| search | 搜索记忆 | `m78 search "关键词" --mode qmd` |
| get | 获取详情 | `m78 get <id>` |
| delete | 删除记忆 | `m78 delete <id>` |
| import | 导入数据 | `m78 import` |
| export | 导出数据 | `m78 export` |
| daily | 每日日志 | `m78 daily "内容"` |
| scan | 扫描目录 | `m78 scan --fix` |
| model check | 检查搜索级别 | `m78 model check` |
| model download | 下载模型 | `m78 model download 1` |
| model list | 列出模型状态 | `m78 model list` |
| model remove | 删除模型 | `m78 model remove embedding` |
| embed build | 生成嵌入向量 | `m78 embed build` |
| embed status | 查看嵌入状态 | `m78 embed status` |
| embed rebuild | 重建嵌入向量 | `m78 embed rebuild` |

## 四级分类

| 级别 | 说明 | 示例 |
|------|------|------|
| apisys | 大系统 | project, steam |
| apimicro | 微服务 | api, workflow |
| apiobj | 实体/类 | user, config |
| apifun | 函数/方法 | login, validate |

## 搜索模式

| 模式 | 用途 | Token 消耗 | 依赖 |
|------|------|------------|------|
| text | FTS5 全文搜索 | 完整文档 | 无 |
| semantic | 向量相似度 | 完整文档 | L1 模型 |
| hybrid | text+语义结合 | 完整文档 | L1 模型 |
| qmd | 片段索引 + LLM 重排序 | **节省 75-95%** | L2 模型 |
| auto | 自动降级 | 按可用级别 | 自动检测 |

## 渐进式升级

```bash
# L0→L1：语义搜索
m78 model download 1            # 下载 embeddinggemma (~350MB)
m78 embed build                 # 生成嵌入向量

# L1→L2：QMD 智能搜索
m78 model download 2            # 下载剩余模型 (~1.65GB)
```

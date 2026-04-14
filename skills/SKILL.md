---
name: memory78
description: 记忆管理系统 - 四级分类存储与检索
user-invocable: true
---

# memory78 - 记忆管理系统

## 快速开始

```bash
# 添加记忆
m78 add "标题" "内容"

# 搜索记忆
m78 search "关键词"

# 列出记忆
m78 list

# 获取详情
m78 get <id>

# 删除记忆
m78 delete <id>
```

## 命令列表

| 命令 | 功能 | 示例 |
|------|------|------|
| add | 添加记忆 | `m78 add "标题" "内容"` |
| list | 列出记忆 | `m78 list --limit 10` |
| search | 搜索记忆 | `m78 search "关键词"` |
| get | 获取详情 | `m78 get <id>` |
| delete | 删除记忆 | `m78 delete <id>` |
| import | 导入数据 | `m78 import` |
| export | 导出数据 | `m78 export` |
| daily | 每日日志 | `m78 daily "内容"` |

## 四级分类

记忆按 `{apisys}/{apimicro}/{apiobj}/{title}.md` 结构存储：

| 级别 | 说明 | 示例 |
|------|------|------|
| apisys | 大系统 | project, steam |
| apimicro | 微服务 | api, workflow |
| apiobj | 实体/类 | user, config |

## 使用场景

1. **保存代码知识** - API设计、配置说明、错误解决方案
2. **项目记忆** - 架构决策、技术选型、最佳实践
3. **每日日志** - 工作记录、问题追踪

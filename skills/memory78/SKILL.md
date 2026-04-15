---
name: memory78
description: 记忆管理系统 - 四级分类存储与检索
user-invocable: true
---

# memory78 - 记忆管理系统

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

## 四级分类

| 级别 | 说明 | 示例 |
|------|------|------|
| apisys | 大系统 | project, steam |
| apimicro | 微服务 | api, workflow |
| apiobj | 实体/类 | user, config |
| apifun | 函数/方法 | login, validate |

## 搜索模式

| 模式 | 用途 | Token 消耗 |
|------|------|------------|
| text | FTS5 全文搜索 | 完整文档 |
| semantic | 向量相似度 | 完整文档 |
| qmd | 片段索引 + LLM 重排序 | **节省 75-95%** |

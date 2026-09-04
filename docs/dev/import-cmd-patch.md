# m78 import 改动规格（提给研发）

> 对应仓库：`crates/memory78-cli`（本仓 `other/memory78cli` 是其一份源码副本，实现在闭源版 `memory78-cli-pro`）
> 改动文件：`src/cli/import_cmd.rs`（主）、`src/cli/add.rs`（可选增强）
> 日期：2026-09-04

---

## 一、背景：现在的 import 结果不可用

`src/cli/import_cmd.rs: parse_file()` 只在相对路径 **≥4 段** 时才取前三级，且**完全不读 front-matter**：

```rust
let (apisys, apimicro, apiobj) = if parts.len() >= 4 {
    (parts[0].clone(), parts[1].clone(), parts[2].clone())
} else {
    ("tmp".to_string(), "tmp".to_string(), "tmp".to_string())
};
```

实测（项目库副本，33 个 md）：

| 分类结果 | 条数 | 原因 |
|---|---|---|
| `saas/devops/ehs-ai-agent-init` | 5 | 深度 ≥4，判对 |
| `system/static/daily` | 8 | 深度 4（`system/static/daily/xxx.md`），碰巧判对 |
| `tmp/tmp/tmp` | 2 | 更浅的目录全落 tmp |
| （重复跑会翻倍） | | 每次生成新 UUID，判重只按 id |

后果：`m78 search` / `m78 export` 出来的分类是错的；导出会把文件按错误分类重新落地。

---

## 二、需求 1：跳过待分类目录

**规则**：`wait` / `待分类` 目录下的文件**不导入**。

> 待分类是"暂存区"，内容未经人工确认，进索引会污染搜索结果；
> 人工归位后就不再在 wait 里了，那时自然会被导入。

改法（`run()` 的 WalkDir 过滤）：

```rust
const SKIP_DIRS: [&str; 2] = ["wait", "待分类"];

let walker = WalkDir::new(&base_dir)
    .into_iter()
    .filter_entry(|e| {
        // 目录名命中即整棵子树跳过
        !e.file_type().is_dir()
            || !SKIP_DIRS.iter().any(|d| {
                e.file_name().to_string_lossy().eq_ignore_ascii_case(d)
            })
    })
    .filter_map(|e| e.ok());
```

⚠️ 注意大小写：Windows 上目录名可能是 `Wait`。

---

## 三、需求 2：跳过 Git 子模块目录

**规则**：任何**自身含 `.git` 的目录**（子模块 / 嵌套仓库）整棵跳过。

原因：`memory78/product/database/` 是 `databasesql.git` 子模块，里面的 `schema.md` / `readme.md`
是 SQL schema 仓库的自述文件，**不是知识条目**，导进来就是噪音。

改法（接在需求 1 的 filter 后面）：

```rust
.filter_entry(|e| {
    if !e.file_type().is_dir() {
        return true;
    }
    // 子模块 / 嵌套仓库：目录内直接有 .git
    !e.path().join(".git").exists()
})
```

> 也顺带解决"知识库里 clone 了别的仓库"的误扫问题。

---

## 四、需求 3：分类解析顺序改为「front-matter 优先」

`m78 add` 写出的 md 头部已经带分类：

```markdown
---
title: xxx
tags: [...]
created_at: ...
updated_at: ...
hash: ...
apisys: vault
apimicro: roles
apiobj: vault-roles
---
```

**新解析顺序**：

1. **读 front-matter**：`apisys` / `apimicro` / `apiobj` 齐全 → 直接用（与 `m78 add` 写出格式对齐）
2. 没有 front-matter → 按路径深度兜底：

| 相对路径段数 | apisys | apimicro | apiobj |
|---|---|---|---|
| ≥4 | `parts[0]` | `parts[1]` | `parts[2]` |
| 3 | `parts[0]` | `parts[1]` | `parts[1]` |
| 2 | `parts[0]` | `parts[0]` | `parts[0]` |
| 1 | `tmp` | `tmp` | `tmp` |

3. front-matter 只有部分字段 → 缺的字段用路径兜底补齐，不整体退回 tmp

front-matter 解析（无需引入 yaml 依赖，格式固定）：

```rust
fn parse_front_matter(content: &str) -> Option<(String, String, String)> {
    if !content.starts_with("---") { return None; }
    let rest = &content[3..];
    let end = rest.find("\n---")?;
    let head = &rest[..end];
    let get = |key: &str| -> Option<String> {
        head.lines().find_map(|l| {
            let l = l.trim();
            let v = l.strip_prefix(key)?.trim().strip_prefix(':')?.trim();
            if v.is_empty() || v == "-" { None } else { Some(v.to_string()) }
        })
    };
    Some((get("apisys")?, get("apimicro")?, get("apiobj")?))
}
```

---

## 五、需求 4：判重改为按路径，重复导入不翻倍

现状：每次 `parse_file` 生成新 UUID，判重只按 id ⇒ 同一份 md 反复 import 会一条变多条。

改法：

1. `memories` 表加列 `src_path TEXT`（md 相对路径），并建唯一索引
2. `insert` 改为 upsert：
   - 按 `src_path` 找到已有记录 → **更新** title / content / apisys / apimicro / apiobj（保留 id、保留 embedding）
   - 不存在 → 插入
3. `content_hash` 未变化则跳过写库（增量导入更快）

> 这一步做完，"恢复 SOP" 就可以从「先删 db 再 import」简化成「直接 `m78 import`」。

---

## 六、需求 5（可选）：`m78 add` 支持只给一级参数

现状：`m78 add "标题" "内容" system` 因缺少第二、第三个参数，会走自动分类器（正是我们要取消的行为）。

改法（`src/cli/add.rs`）：只给了 apisys 时，后两级自动补成同一个值：

```rust
let apisys  = args.apisys.clone().unwrap();
let apimicro = args.apimicro.clone().unwrap_or_else(|| apisys.clone());
let apiobj   = args.apiobj.clone().unwrap_or_else(|| apisys.clone());
```

这样 AI 侧可以简写成：

```bash
m78 add "标题" "内容" wait        # → wait/wait/wait/标题.md
m78 add "标题" "内容" system wait # → system/wait/wait/标题.md
```

---

## 七、验收标准

```bash
# 准备：项目库当前状态（system/wait 下有 30 个文件，product/database 是子模块）
cd /workspace
rm -f memory78/memory78.db
m78 import

# 期望输出
#   [导入] 导入 0 条记录            ← wait 目录被跳过
#   （若把某个 wait 文件 git mv 到 vault/ops/x/ 下，再 import 一次）
#   [导入] 导入 1 条记录
#   分类: vault/ops/x               ← 来自 front-matter 或路径
#   没有任何 tmp/tmp/tmp
#   没有任何 product/database 下的条目

# 重复导入不翻倍
m78 import   # 第二次
m78 list --limit 100 | grep -c .   # 条数不变
```

# Memory78 CLI

**English | [中文](README.md)**

High-performance local knowledge base engine for managing code knowledge and project memory.

## Why Memory78?

| Problem | Memory78 Solution |
|---------|------------------|
| AI reads full documents every time | QMD smart search returns only relevant fragments, saves 75-95% tokens |
| Knowledge scattered everywhere | 4-level classification structure for quick navigation |
| Memory saving not intuitive | Auto-classification, just input content |
| Knowledge not organized | SQLite + file dual storage |

## Installation

Download from [Releases](https://github.com/www778878net/memory78/releases).

**Windows:** Download `m78.exe`, place in project directory or add to PATH.

## Quick Start

```bash
# Add memory (auto-classified)
m78 add "API Design" "User authentication using JWT..."

# Manual classification
m78 add "Config" "Database config..." project config db

# Search memory
m78 search "keyword"

# QMD mode (saves 75-95% tokens)
m78 search "keyword" --mode qmd

# List memories
m78 list --limit 10

# Get details
m78 get <id or title>

# Delete memory
m78 delete <id or title>

# Import existing files
m78 import

# Export data
m78 export

# Daily log
m78 daily "Today's work"
```

## Core Features

### 1. Smart Search (Save Tokens)

```bash
# QMD mode: returns only relevant fragments, saves 75-95% tokens
m78 search "base78" --mode qmd

# FTS5 full-text search
m78 search "keyword"

# Semantic search (vector similarity)
m78 search "keyword" --mode semantic
```

### 2. 4-Level Classification Storage

Memories are organized as `{apisys}/{apimicro}/{apiobj}/{title}.md`:

```
memory78/
├── project/           # apisys: system
│   ├── api/           # apimicro: microservice
│   │   ├── user/      # apiobj: entity/class
│   │   │   └── login_design.md
│   │   └── config/
│   │       └── database_config.md
│   └── workflow/
│       └── order_flow.md
└── steam/
    └── buff/
        └── price_strategy.md
```

### 3. Auto Classification (name78 Algorithm)

```bash
# No need to specify classification, auto-detected
m78 add "API Design" "User authentication using JWT..."
# → Auto-classified as project/api/api_design

# Or manually specify
m78 add "Config" "Database config..." project config db
```

### 4. AI Coding Assistant Integration

Configure as Claude Skill, AI automatically manages knowledge.

## Command Reference

### add - Add memory

```bash
m78 add "title" "content" [apisys] [apimicro] [apiobj]

# Options
--mode <insert|append|update|overwrite>  Operation mode
--format <md|json>                       File format
--tags <tag1> <tag2> ...                 Custom tags
```

### search - Search memory

```bash
m78 search "keyword"

# Options
--apisys <value>     Filter by system
--apimicro <value>   Filter by microservice
--apiobj <value>     Filter by entity
--tags <tag1,tag2>   Filter by tags
--limit <n>          Limit results
--mode <text|semantic|qmd>  Search mode
```

### list - List memories

```bash
m78 list --limit 10 --order desc
```

### get / delete / import / export / daily

See `--help` for details.

## Data Storage

| Storage | Path | Description |
|---------|------|-------------|
| Database | `memory78/memory78.db` | SQLite + FTS5 full-text index |
| Files | `memory78/{apisys}/{apimicro}/{apiobj}/{title}.md` | Markdown/JSON |

## Search Mode Comparison

| Mode | Use Case | Token Usage |
|------|----------|-------------|
| text | FTS5 full-text search | Full document |
| semantic | Vector similarity | Full document |
| qmd | Fragment index + LLM reranking | **Saves 75-95%** |

## 4-Level Classification

| Level | Description | Examples |
|-------|-------------|----------|
| apisys | System | project, steam, data |
| apimicro | Microservice | api, workflow, config |
| apiobj | Entity/Class | user, order, payment |



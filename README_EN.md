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

**Claude Skill:** Copy `skills/memory78` directory to `.claude/skills/`.

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
--mode <text|semantic|hybrid|qmd|auto>  Search mode
```

### model - Model management

Manage AI model downloads, checks, and removal.

```bash
# Check current search level and upgrade guide
m78 model check

# Download models (1=L1 semantic, 2=L2 QMD, no arg=upgrade to next level)
m78 model download 1
m78 model download 2
m78 model download              # Auto-upgrade to next level

# Download options
--huggingface                   # Use huggingface.co (for users outside China)

# List all models and download status
m78 model list

# Remove downloaded models
m78 model remove embedding      # Remove specific model
m78 model remove all            # Remove all models
```

**model check output example:**

```
Memory78 Search Level: L0 (Text Search)

Model Status:
  ✗ embedding - Text vectorization (semantic search core) (329MB) [L1]
  ✗ query-expansion - Query expansion (QMD component) (1280MB) [L2]
  ✗ reranker - Result reranking (QMD component) (639MB) [L2]

Available modes: text, list, wiki

Upgrade to L1 (Semantic Search):
  m78 model download 1    # Download ~350MB, enable semantic/hybrid
```

### embed - Embedding management

Manage vector embeddings for knowledge entries, providing data for semantic search.

```bash
# Generate embeddings for entries without vectors
m78 embed build

# Show embedding status
m78 embed status

# Rebuild all embeddings (use after model change)
m78 embed rebuild
```

**embed status output example:**

```
Embedding Status:
  Total:     150
  Embedded:  120 (80%)
  Not embedded: 30

Run m78 embed build to generate embeddings
```

### list - List memories

```bash
m78 list --limit 10 --order desc
```

### get / delete / import / export / daily / scan

See `--help` for details.

## Data Storage

| Storage | Path | Description |
|---------|------|-------------|
| Database | `memory78/memory78.db` | SQLite + FTS5 full-text index + vector embeddings |
| Files | `memory78/{apisys}/{apimicro}/{apiobj}/{title}.md` | Markdown/JSON |
| Models | `memory78/models/` | GGUF format AI models |

Full directory structure:

```
memory78/
├── memory78.db                      # SQLite + FTS5 + vector embeddings
├── models/                          # Model files directory
│   ├── embeddinggemma-300M-Q8_0.gguf
│   ├── qmd-query-expansion-1.7B-q4_k_m.gguf
│   └── qwen3-reranker-0.6b-q8_0.gguf
├── index.md                         # Directory index
├── {apisys}/                        # Level 1: System
│   ├── {apisys}.md
│   └── {apimicro}/                  # Level 2: Microservice
│       ├── {apimicro}.md
│       └── {apiobj}/                # Level 3: Entity/Class
│           ├── {apiobj}.md
│           └── {knowledge_entry}.md
```

## Search Mode Tiers

### L0 Zero Model (Works out of the box, no download needed)

| Mode | Use Case              | Token Usage  | Dependencies |
|------|-----------------------|--------------|--------------|
| text | FTS5 full-text search | Full document | None        |
| list | 3-level tag lookup    | Full document | None        |
| wiki | Directory browsing (index.md) | Manual reading | None |

### L1 Semantic Search (1 model download ~350MB)

| Mode     | Use Case              | Token Usage  | Dependencies             |
|----------|-----------------------|--------------|--------------------------|
| semantic | Vector similarity     | Full document | embeddinggemma-300M      |
| hybrid   | text + semantic combo | Full document | embeddinggemma-300M      |

### L2 QMD Smart Search (3 model downloads ~2GB)

| Mode | Use Case                              | Token Usage         | Dependencies |
|------|----------------------------------------|---------------------|--------------|
| qmd  | Query expansion + vector + reranking   | **Saves 75-95%**   | 3 models     |

### auto Mode

```bash
m78 search "keyword" --mode auto
```

Automatically degrades by availability: qmd → hybrid → text.

## Progressive Upgrade

```
Install m78 → m78 model check → Shows L0, suggests upgrade steps
              ↓
m78 model download 1 → Downloads embeddinggemma (~350MB)
m78 embed build → Generates embeddings → semantic/hybrid search available
              ↓
m78 model download 2 → Downloads query-expansion + reranker (~1.65GB)
m78 search "keyword" --mode qmd → QMD search available
```

```bash
# Step 1: Works without any models
m78 add "Title" "Content"
m78 search "keyword"              # text mode, no models needed

# Step 2: One command to upgrade to L1 semantic search
m78 model download 1            # Download embeddinggemma (~350MB)
m78 embed build                 # Generate embeddings
m78 search "natural language query" --mode semantic  # Enabled!

# Step 3: One command to upgrade to L2 QMD
m78 model download 2            # Download remaining models (~1.65GB)
m78 search "keyword" --mode qmd  # Saves 75-95% tokens
```

## Model Details

| Model File                              | Purpose          | Params | Size     | Used By                   |
|-----------------------------------------|------------------|--------|----------|---------------------------|
| embeddinggemma-300M-Q8_0.gguf          | Text embedding   | 300M   | ~350MB   | semantic / hybrid / qmd   |
| qmd-query-expansion-1.7B-q4_k_m.gguf   | Query expansion  | 1.7B   | ~1GB     | qmd                       |
| qwen3-reranker-0.6b-q8_0.gguf          | Result reranking | 0.6B   | ~650MB   | qmd                       |

**What each model does:**

- **Text Embedding (embeddinggemma)**: Converts text to numeric vectors, so semantically similar terms like "routing mechanism" and "route handler" can match
- **Query Expansion (query-expansion)**: Expands short queries into multiple variants, e.g. "routing" → ["routing mechanism", "route handler", "API routing"], improving recall
- **Result Reranking (reranker)**: Reorders search results to put the most relevant ones first

**Model download source:**

- China users: Auto-downloads from hf-mirror.com (direct access, no proxy needed)
- International users: `m78 model download --huggingface` to use huggingface.co
- Resume support for interrupted downloads

## 4-Level Classification

| Level | Description | Examples |
|-------|-------------|----------|
| apisys | System | project, steam, data |
| apimicro | Microservice | api, workflow, config |
| apiobj | Entity/Class | user, order, payment |
| apifun | Function/Method | login, validate, get_config |

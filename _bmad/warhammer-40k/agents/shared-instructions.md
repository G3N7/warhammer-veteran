# Warhammer 40K Agents - Shared Instructions

**All agents in this module MUST follow these protocols.**

---

## CRITICAL: Source of Truth Protocol

### Army Lists Directory as Single Source of Truth

**The `army-lists/` directory is the SINGLE SOURCE OF TRUTH for all army-related data.**

| Data Type | Source of Truth | How to Discover |
|-----------|-----------------|-----------------|
| Army lists | `army-lists/{faction}/*.md` | Glob `army-lists/**/*.md` |
| Paint schemes | BRUSHMASTER SECTION in army lists | Grep for `<!-- BRUSHMASTER SECTION` |
| User's factions | Directory structure | Check which `army-lists/{faction}/` dirs exist |

### At Session Start

1. Load `memories.md` - user preferences and learned patterns ONLY
2. Glob `army-lists/**/*.md` to discover existing armies (filenames only, not content)
3. DO NOT duplicate inventories in memories.md

### Deriving State from Files

**When user asks "what armies/schemes/factions do I have?":**
- Query the filesystem - don't read from memories.md
- Derive faction ownership from directory contents (`army-lists/orks/` = user has Orks)

**When you need army details:**
- Read the specific army list file on demand
- Don't cache full content in memories

### What memories.md Should Contain

✅ **DO store:**
- User preferences (playstyle, favorite techniques, preferred brands)
- Learned patterns (recurring questions, skill level)
- Protocols and conventions established with user
- Personal notes (wife's army theme, play group info)

❌ **DO NOT store:**
- Inventory of armies (derive from `army-lists/`)
- List of paint schemes (derive from BRUSHMASTER SECTIONs)
- Faction lists (derive from directory structure)
- Session history that duplicates file state

### Cross-Agent Data Sharing

Agents share data through `army-lists/` files AND the shared data directory:

| Agent | Writes | Reads |
|-------|--------|-------|
| **Tacticus** | Army list content, army-registry.yaml | validation-rules.yaml, faq-registry.yaml |
| **Brushmaster** | BRUSHMASTER SECTION (paint schemes) | Army faction context, user-profile.yaml |
| **Arbitrator** | faq-registry.yaml, rulings | Army composition, validation-rules.yaml |
| **Chronicler** | CHRONICLER SECTION (campaign metadata) | Army lists, user-profile.yaml |
| **Lorekeeper** | Lore sections in army lists | Faction info, user-profile.yaml |
| **Artisan** | ARTISAN SECTION (assembly/magnetization) | Army composition, user-profile.yaml |

### Shared Data Directory

`_bmad/warhammer-40k/agents/shared/` contains cross-agent registries:

| File | Purpose | Updated By |
|------|---------|------------|
| `army-registry.yaml` | Central index of all armies + completion status | Any agent |
| `user-profile.yaml` | User preferences, playstyle, faction ownership | Any agent |

### Templates

`_bmad/warhammer-40k/templates/` contains standardized document templates:
- `army-list-template.md` - Full army list with all agent sections
- `paint-scheme-template.md` - Brushmaster paint scheme format
- `cheatsheet-template.md` - Game day quick reference
- `assembly-guide-template.md` - Artisan assembly/magnetization format

### Section Boundaries

When multiple agents write to the same file, use HTML comments to mark sections:

```markdown
<!-- BRUSHMASTER SECTION - Tacticus ignore -->
## Paint Scheme: ...
<!-- END BRUSHMASTER SECTION -->

<!-- ARTISAN SECTION - Tacticus ignore -->
## Model Assembly & Magnetization Guide
<!-- END ARTISAN SECTION -->

<!-- CHRONICLER SECTION - Tacticus ignore -->
## Campaign Metadata
<!-- END CHRONICLER SECTION -->
```

Agents MUST respect other agents' sections and not modify them.

---

## Context Optimization

### Lazy Loading Protocol

**DO NOT load all files at startup. This wastes context.**

- Load `memories.md` first (small, user preferences)
- Glob to discover files (filenames only)
- Read specific files on demand when user references them

**Never Pre-Load:**
- All knowledge base files at once
- Full content of all army list files
- Data for factions not being discussed

---

## Auto-Commit Protocol

After any file update:
1. Stage changes: `git add` relevant files
2. Commit with agent-specific emoji prefix:
   - `⚔️ Tacticus:` - army lists
   - `🎨 Brushmaster:` - paint schemes
   - `📜 Arbitrator:` - rules/rulings
   - `📖 Chronicler:` - campaigns/battles
   - `🔮 Lorekeeper:` - lore content
   - `🔧 Artisan:` - projects/conversions
3. Never push without user approval

---

*Version: 1.1*
*Last Updated: 2026-02-09*
*Applies to: All warhammer-40k agents*

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

Agents share data through the `army-lists/` files:

| Agent | Writes | Reads |
|-------|--------|-------|
| **Tacticus** | Army list content (units, points, tactics) | — |
| **Brushmaster** | BRUSHMASTER SECTION (paint schemes) | Army faction context |
| **Arbitrator** | — | Army composition for rules context |
| **Chronicler** | — | Army lists for campaign tracking |
| **Lorekeeper** | — | Faction info for lore context |
| **Artisan** | — | Army composition for conversion ideas |

### Section Boundaries

When multiple agents write to the same file, use HTML comments to mark sections:

```markdown
<!-- BRUSHMASTER SECTION - Tacticus ignore -->
## Paint Scheme: ...
...
<!-- END BRUSHMASTER SECTION -->
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

*Version: 1.0*
*Last Updated: 2025-12-30*
*Applies to: All warhammer-40k agents*

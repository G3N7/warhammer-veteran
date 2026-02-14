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

## Anti-Hallucination Protocol (ALL AGENTS)

**Every agent MUST follow these rules to prevent fabricating information.**

### 1. CITE YOUR SOURCE

**Every factual claim in output MUST include its source.** This is non-negotiable.

| Data Type | Citation Format | Example |
|-----------|----------------|---------|
| Points values | `[Cache: YYYY-MM-DD]` | "340pts [Cache: 2026-02-09]" |
| Rules text | `[Wahapedia: Section Name]` | "According to [Wahapedia: Core Rules - Fight Phase]..." |
| Lore facts | `[Source: Book/Codex]` | "[Source: Codex Space Wolves 10th Ed]" |
| FAQ/Errata | `[FAQ: YYYY-MM-DD]` | "[FAQ: 2026-01-15 Balance Dataslate]" |
| Paint data | `[Paint DB: file.json]` | "Greedy Gold (#FFD700) [Paint DB: army-painter-warpaints.json]" |
| User preference | `[memories.md]` | "User prefers castle playstyle [memories.md]" |
| Training knowledge | `[UNVERIFIED - from training data]` | Mark ANY claim not backed by a file or web source |

**If you cannot cite a source: say so.** "I believe X but cannot verify this from cached data -- should I web search to confirm?"

### 2. ASSUME ILLEGAL UNTIL PROVEN

When uncertain about any rules legality (unit composition, wargear, enhancement eligibility, detachment rules):

- **DEFAULT: Assume it is ILLEGAL**
- **THEN: Search for proof it is legal** (cache, validation-rules.yaml, web search)
- **ONLY IF PROVEN: Include it in output**
- **NEVER: Ask user to confirm legality and then include based on their say-so alone** -- user memory is fallible too

### 3. DATA FRESHNESS ENFORCEMENT

**Every knowledge file and data source has a shelf life.**

| Data Type | Max Age | Action When Stale |
|-----------|---------|-------------------|
| Datasheet cache | 30 days | Warn user, offer refresh |
| Knowledge base files | 90 days | Flag `[STALE: last verified YYYY-MM-DD]` in output |
| Meta/tournament data | 30 days | Do NOT cite as current -- say "as of [date]" |
| FAQ registry | 60 days | Web search for newer FAQs before citing |
| Paint data | 180 days | Acceptable (paint lines change slowly) |

**Every knowledge file MUST include a freshness header:**
```markdown
<!-- VERIFIED: YYYY-MM-DD | SOURCE: description | NEXT REVIEW: YYYY-MM-DD -->
```
If this header is missing, treat the file as UNVERIFIED and flag in output.

### 4. WEB SEARCH PROTOCOL

When web searching for Warhammer 40K data:

**Trusted Sources (use these):**
- `wahapedia.ru` -- Primary rules/datasheet reference
- `warhammer-community.com` -- Official GW announcements, FAQs, Balance Dataslates
- `goonhammer.com` -- Tournament meta analysis (editorial, not rules source)

**Untrusted Sources (NEVER cite as authoritative):**
- Fan wikis (40k wiki, Lexicanum) -- for lore context only, not rules
- YouTube/Reddit comments -- opinions, not rules
- Older edition content -- verify it says "10th Edition" explicitly

**Search Protocol:**
1. Always include "10th edition" or "warhammer 40k 10th" in search terms
2. Check publication date -- reject anything before December 2023 (10th Ed launch window)
3. If two sources disagree: cite both, flag the conflict, ask user which is current
4. After finding data via web: add to local cache/knowledge base for future use

### 5. CROSS-AGENT VERIFICATION

When multiple agents contribute to the same file or topic:

- **After Tacticus builds a list:** Arbitrator SHOULD verify rules compliance if invoked
- **After Brushmaster writes a paint scheme:** Verify paint names exist in paint DB
- **After Lorekeeper writes lore:** Flag any claims as `[UNVERIFIED - from training data]` unless cited
- **After Chronicler references mechanics:** Verify Crusade rules against Arbitrator knowledge base

**Any agent can flag another agent's section** with `<!-- NEEDS VERIFICATION: [reason] -->` if they spot a potential issue during cross-reads.

### 6. TRAINING DATA DISCLAIMER

All agents are built on LLM training data that may contain:
- **Outdated edition rules** (7th, 8th, 9th Edition content mixed in)
- **Retconned lore** (old Black Library novels, removed storylines)
- **Discontinued products** (OOP kits, old paint ranges)
- **Incorrect stats** (points change quarterly, abilities get errata'd)

**When relying on training data (no local file or web source):**
- Prefix with: `[UNVERIFIED]`
- Offer to web search for confirmation
- NEVER present training data as confirmed fact

---

## Auto-Commit Protocol

After any file update:
1. Stage changes: `git add` relevant files
2. Commit with agent-specific emoji prefix:
   - `⚔️ Tacticus:` - army lists
   - `🎨 Brushmaster:` - paint schemes
   - `⚖️ Arbitrator:` - rules/rulings
   - `📖 Chronicler:` - campaigns/battles
   - `🔮 Lorekeeper:` - lore content
   - `🔧 Artisan:` - projects/conversions
3. Never push without user approval

---

*Version: 2.0*
*Last Updated: 2026-02-14*
*Applies to: All warhammer-40k agents*

# Warhammer Veteran - Project Instructions

## Compact Instructions

**CRITICAL: These instructions MUST be preserved across context compaction.**

When context is compacted, immediately reload these critical files before continuing work:

1. **Agent instructions**: `_bmad/warhammer-40k/agents/{agent}-sidecar/instructions.md`
2. **Validation rules**: `_bmad/warhammer-40k/agents/tacticus-sidecar/validation-rules.yaml` (12 blocking gates)
3. **Shared protocols**: `_bmad/warhammer-40k/agents/shared-instructions.md` (source of truth)
4. **FAQ registry**: `_bmad/warhammer-40k/agents/arbitrator-sidecar/faq-registry.yaml`
5. **Army registry**: `_bmad/warhammer-40k/agents/shared/army-registry.yaml`
6. **Compact context**: `_bmad/warhammer-40k/compact-context.md` (minimal agent roster)

When using `/compact`, always include focus on the active agent's sidecar directory to preserve agent-specific rules.

---

## Agent System

This project uses BMAD agents for Warhammer 40K hobby management:

| Agent | Emoji | Domain | Key Files |
|-------|-------|--------|-----------|
| Tacticus | ⚔️ | Army lists, validation, cheatsheets | validation-rules.yaml, lists.md |
| Arbitrator | 📜 | Rules, FAQ, disputes | faq-registry.yaml, rulings.md |
| Brushmaster | 🎨 | Paint schemes, techniques | color-registry in army lists |
| Lorekeeper | 🔮 | Faction lore, timelines | lore sections in army lists |
| Chronicler | 📖 | Campaigns, battle logs | campaign metadata |
| Artisan | 🔧 | Conversions, assembly, hobby | assembly guides in army lists |

## Key Protocols

- **Source of Truth**: `army-lists/` directory is the single source of truth for all army data
- **Lazy Loading**: Never pre-load all files. Load memories.md first, glob to discover, read on demand
- **Section Boundaries**: Use `<!-- AGENT SECTION -->` HTML comments when multiple agents write to same file
- **Auto-Commit**: Use agent emoji prefixes (⚔️/🎨/📜/📖/🔮/🔧)
- **Templates**: Use `_bmad/warhammer-40k/templates/` for consistent formatting
- **Cross-Agent Data**: `_bmad/warhammer-40k/agents/shared/` for shared registries

## Data Locations

```
army-lists/                           # Source of truth for all army data
  {faction}/                          # One dir per faction
    *.md                              # Army list documents
    *.cheatsheet.json                 # Game cheatsheets
_bmad/warhammer-40k/
  agents/shared/                      # Cross-agent shared data
    army-registry.yaml                # Central army index
    user-profile.yaml                 # User preferences
  agents/{name}-sidecar/              # Per-agent knowledge
  templates/                          # Standardized document templates
  compact-context.md                  # Minimal context for post-compaction
```

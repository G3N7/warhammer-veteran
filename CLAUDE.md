# Warhammer Veteran - Project Instructions

## Compact Instructions

**CRITICAL: These instructions MUST be preserved across context compaction.**

When context is compacted, immediately reload these critical files before continuing work:

1. **Agent skills**: `.claude/skills/warhammer-40k-agents-{name}/SKILL.md` (full agent definitions)
2. **Validation rules**: `_bmad-output/warhammer-40k/agents/tacticus-sidecar/validation-rules.yaml` (12 blocking gates)
3. **Hallucination registry**: `_bmad-output/warhammer-40k/shared/hallucination-registry.yaml` (13 known patterns)
4. **Retcon registry**: `_bmad-output/warhammer-40k/shared/retcon-registry.yaml` (5 known retcons)
5. **Army registry**: `_bmad-output/warhammer-40k/shared/army-registry.yaml`
6. **Improvement plan**: `_bmad-output/warhammer-40k/IMPROVEMENT-PLAN.md`

When using `/compact`, always include focus on the active agent's skill and sidecar directory.

---

## Agent System

This project uses BMAD skills for Warhammer 40K hobby management. Agents are defined in `.claude/skills/` and registered in `_bmad/_config/agent-manifest.csv`.

### Warhammer 40K Agent Skills

| Agent | Skill Name | Emoji | Domain |
|-------|-----------|-------|--------|
| Tacticus | `warhammer-40k-agents-tacticus` | ⚔️ | Army lists, validation, competitive meta |
| Arbitrator | `warhammer-40k-agents-arbitrator` | ⚖️ | Rules, FAQ, disputes |
| Brushmaster | `warhammer-40k-agents-brushmaster` | 🎨 | Paint schemes, techniques |
| Lorekeeper | `warhammer-40k-agents-lorekeeper` | 🔮 | Faction lore, timelines |
| Chronicler | `warhammer-40k-agents-chronicler` | 📖 | Campaigns, battle logs |
| Artisan | `warhammer-40k-agents-artisan` | 🔧 | Conversions, assembly, hobby |

### Deterministic Data Skills (Anti-Hallucination)

| Skill | Purpose |
|-------|---------|
| `warhammer-40k-army-data` | Queries army lists, unit stats, points, validation rules from FILES — never from memory |
| `warhammer-40k-paint-data` | Queries paint inventory JSON, hex codes, color schemes from FILES — never from memory |

**CRITICAL**: Agents MUST use data skills for factual queries instead of generating from memory. This is the primary defense against hallucination.

## Key Protocols

- **Source of Truth**: `army-lists/` directory is the single source of truth for all army data
- **Deterministic Data**: Use `warhammer-40k-army-data` and `warhammer-40k-paint-data` skills for all factual queries
- **Lazy Loading**: Never pre-load all files. Load sidecar memories first, glob to discover, read on demand
- **Section Boundaries**: Use `<!-- AGENT SECTION -->` HTML comments when multiple agents write to same file
- **Auto-Commit**: Use agent emoji prefixes (⚔️/🎨/⚖️/📖/🔮/🔧)
- **Citation Required**: All factual claims must cite source file: `[Source: filename]` or `[UNVERIFIED]`

## Data Locations

```
army-lists/                                    # Source of truth for all army data
  {faction}/                                   # One dir per faction
    *.md                                       # Army list documents
    *.cheatsheet.json                          # Structured game data (JSON)
.claude/skills/
  warhammer-40k-agents-{name}/                 # Agent skill definitions
    SKILL.md                                   # Full agent persona + instructions
    bmad-skill-manifest.yaml                   # Agent metadata
  warhammer-40k-army-data/                     # Deterministic army data lookup
  warhammer-40k-paint-data/                    # Deterministic paint data lookup
_bmad-output/warhammer-40k/
  agents/{name}-sidecar/                       # Per-agent persistent memory
  shared/                                      # Cross-agent shared registries
    hallucination-registry.yaml                # 13 known hallucination patterns
    retcon-registry.yaml                       # 5 known lore retcons
    army-registry.yaml                         # Central army index
    user-profile.yaml                          # User preferences
  IMPROVEMENT-PLAN.md                          # Persisted improvement roadmap
_bmad/_config/custom/warhammer-40k/
  agents/*.yaml                                # Agent YAML definitions (compact)
  data/paints/*.json                           # Paint inventory data
  module.yaml                                  # Module configuration
_bmad/_config/agent-manifest.csv               # All agents registered here
```

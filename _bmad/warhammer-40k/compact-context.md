# Warhammer 40K Agent Roster (Compact Context)

**Purpose:** Minimal context to restore agent awareness after compaction. Reload full instructions from sidecar directories.

## Active Agents

| Agent | Emoji | Sidecar | Domain |
|-------|-------|---------|--------|
| Tacticus | ⚔️ | tacticus-sidecar/ | Army lists, validation, cheatsheets |
| Arbitrator | ⚖️ | arbitrator-sidecar/ | Rules, FAQ, disputes |
| Brushmaster | 🎨 | brushmaster-sidecar/ | Paint schemes, techniques |
| Lorekeeper | 🔮 | lorekeeper-sidecar/ | Faction lore, timelines |
| Chronicler | 📖 | chronicler-sidecar/ | Campaigns, battle logs |
| Artisan | 🔧 | artisan-sidecar/ | Conversions, assembly, hobby |

## Critical Files to Reload After Compact

- `_bmad/warhammer-40k/agents/tacticus-sidecar/validation-rules.yaml` - 12 blocking gates for army list validation
- `_bmad/warhammer-40k/agents/shared-instructions.md` - Source of truth protocol, lazy loading, auto-commit
- `_bmad/warhammer-40k/agents/arbitrator-sidecar/faq-registry.yaml` - Errata tracking by faction
- `_bmad/warhammer-40k/agents/shared/army-registry.yaml` - Cross-agent army index
- `_bmad/warhammer-40k/agents/shared/user-profile.yaml` - User preferences and playstyle

## Source of Truth

`army-lists/` directory is the SINGLE source of truth. Derive all army data from filesystem, not memory.

## User Quick Profile

- **Primary Faction:** Space Wolves
- **Playstyle:** Castle, artillery, elite forces, tournament-competitive
- **Hobby Focus:** All (competitive + narrative + hobby)
- **Common Themes:** Durability obsession (T10+), big stompy robots, tank spam, synergy-focused

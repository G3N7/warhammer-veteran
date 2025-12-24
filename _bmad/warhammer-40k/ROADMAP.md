# Warhammer-40K Module Roadmap

**Last Updated:** 2024-12-24

## Current State

The module is now BMAD-compliant with 6 expert agents, 3 workflows, and proper sidecar structure. Foundation is solid.

---

## Priority 1: Knowledge Base Infrastructure

**Why:** Agents currently rely on web searches. Local knowledge = faster, more reliable responses.

### 1.1 Faction Knowledge Bases
Create `knowledge/` folders with pre-loaded faction data:
```
agents/tacticus-sidecar/knowledge/
├── space-marines.md      # Chapter tactics, key units, meta tips
├── chaos.md
├── xenos/
│   ├── aeldari.md
│   └── tyranids.md
└── imperium.md
```

### 1.2 Rules Quick Reference
For Arbitrator - common rules lookups without web fetch:
```
agents/arbitrator-sidecar/knowledge/
├── phase-timing.md       # Complete phase sequence
├── common-interactions.md # FAQ-level rules
└── 10th-ed-changes.md    # What changed from 9th
```

### 1.3 Painting Techniques Library
For Brushmaster:
```
agents/brushmaster-sidecar/knowledge/
├── techniques/
│   ├── edge-highlighting.md
│   ├── wet-blending.md
│   └── nmm-basics.md
└── color-theory.md
```

---

## Priority 2: Workflow Expansion

**Why:** Only 3 workflows exist. More structured guidance = better user experience.

### 2.1 Rules Dispute Workflow
**Agent:** Arbitrator
**Purpose:** Step-by-step rules dispute resolution with citation building
**Key features:**
- Identify the rule in question
- Search for relevant FAQ/errata
- Document ruling for future reference

### 2.2 Collection Audit Workflow
**Agents:** Artisan + Tacticus
**Purpose:** Track owned models, identify gaps, plan purchases
**Key features:**
- Import from army lists
- Track painted/unpainted status
- Budget planning

### 2.3 Lore Deep-Dive Workflow
**Agent:** Lorekeeper
**Purpose:** Guided exploration of faction/character/event lore
**Key features:**
- Interactive Q&A format
- Save discoveries to explorations.md
- Build personal lore notes

---

## Priority 3: Cross-Agent Integration

**Why:** Agents work in silos. Integration = richer experience.

### 3.1 Army-to-Paint Pipeline
- Tacticus builds list → Brushmaster gets paint project
- Track which units in list are painted
- Link paint schemes to specific armies

### 3.2 Campaign-to-Lore Integration
- Chronicler campaigns → Lorekeeper provides faction context
- Battle reports enriched with historical parallels
- Character backstories from lore

### 3.3 Party Mode Scenarios
Pre-built multi-agent discussions:
- "Help me decide on a new army" (Tacticus + Lorekeeper + Artisan)
- "Plan my campaign" (Chronicler + Lorekeeper)
- "Review my hobby project" (Brushmaster + Artisan)

---

## Priority 4: Data Layer Enhancement

**Why:** Wahapedia CSV is good but could be better utilized.

### 4.1 Processed Data Improvements
- Pre-compute faction synergies
- Build unit tier lists from tournament data
- Cache meta analysis with refresh dates

### 4.2 User Collection Tracking
New data structure:
```
data/user/
├── collection.json       # Owned models
├── paint-status.json     # Painted/WIP/unpainted
└── wishlists.json        # Purchase plans
```

### 4.3 Session Persistence
Better session management across agents:
- Shared context when switching agents
- Resume workflows after token limits

---

## Priority 5: Documentation & Onboarding

**Why:** Module is complex. Users need guidance.

### 5.1 Module Documentation
```
docs/
├── getting-started.md    # First-time setup
├── agents-guide.md       # What each agent does
├── workflows-guide.md    # Available workflows
└── faq.md
```

### 5.2 Agent Welcome Messages
Each agent should have a first-run experience:
- Explain capabilities
- Ask key preferences (faction, skill level)
- Populate memories.md with initial context

---

## Stretch Goals

### CSV Knowledge Bases
Use BMAD `conversational_knowledge` feature:
```yaml
conversational_knowledge:
  - factions: "{project-root}/_bmad/warhammer-40k/data/kb/factions.csv"
  - units: "{project-root}/_bmad/warhammer-40k/data/kb/units.csv"
```

### Web Bundle
Create deployable web version for non-IDE users.

### Community Sharing
- Export/import paint schemes
- Share army lists
- Campaign templates

---

## Implementation Order

| Phase | Focus | Effort |
|-------|-------|--------|
| **Phase 1** | Knowledge bases for Tacticus + Arbitrator | Medium |
| **Phase 2** | Rules Dispute + Collection Audit workflows | Medium |
| **Phase 3** | Army-to-Paint pipeline integration | Low |
| **Phase 4** | User collection data structure | Medium |
| **Phase 5** | Documentation | Low |

---

## Notes for Future Sessions

- Start with knowledge bases - biggest impact for least effort
- Rules Dispute workflow would be very useful for game nights
- Collection tracking is a "nice to have" but users love it
- Don't forget to update UPGRADE-SUMMARY.md when adding features

# Warhammer Veteran

Comprehensive AI assistance for Warhammer 40k players across all aspects of the hobby - from building competitive army lists with meta analysis, to resolving rules disputes during gameplay, mastering painting techniques, exploring deep lore, and managing narrative campaigns.

## Overview

Warhammer Veteran is a complete BMAD module providing specialized AI agents for every aspect of the Warhammer 40k hobby:

- **⚔️ Competitive Army Building** - Build tournament-ready lists with meta analysis and unit synergies
- **⚖️ Rules Expertise** - Resolve disputes with Wahapedia-cited rulings during gameplay
- **📜 Lore Mastery** - Explore faction histories, character backgrounds, and epic battles
- **🎨 Painting Guidance** - Design color schemes, learn techniques, and plan projects
- **📖 Campaign Management** - Track Crusade campaigns with narrative progression
- **🔨 Hobby Advice** - Plan conversions, basing, and collection strategies

## ✨ Phase 2 Enhancements (NEW!)

**Project Tracking & Continuity:**
- 🆕 **Track Project Progress** - Unified project files linking army lists, paint schemes, and campaigns
- 🆕 **Resume Projects** - Pick up where you left off across sessions with full context
- 🆕 **Session Logging** - Track painting progress, time spent, models completed
- 🆕 **Milestone Tracking** - Automatic detection of 25%, 50%, 75%, completion

**Enhanced Paint Scheme Designer:**
- 🆕 **Paint Set Presets** - Instant inventory for Army Painter, Citadel, Vallejo starter sets
- 🆕 **3-Tier Complexity** - Speed → Standard → Advanced progression in every scheme
- 🆕 **Army List Integration** - Auto-imports model counts and generates painting roadmaps
- 🆕 **Painting Roadmap** - Phased approach: batch paint troops → practice techniques → showcase characters

**Continuous Improvement:**
- 🆕 **Session Retrospective Workflow** - Analyzes conversations to extract requirements
- 🆕 **Preference Learning** - Agents remember your choices and adapt over time

### Data Sources

- **Rules & Units:** [Wahapedia](https://wahapedia.ru/)
- **Tournament Meta:**
  - [40k Event Tracker](https://40k-event-tracker.nuxt.dev/)
  - [Stat Check](https://www.stat-check.com/the-meta)
  - [Spikey Bits](https://spikeybits.com/army-lists/)
  - [Blood of Kittens](https://bloodofkittens.com/)
  - [Warp Friends](https://warpfriends.wordpress.com/)

## Installation

Install the module using BMAD:

```bash
bmad install warhammer-40k
```

During installation, you'll be asked:
1. Where to save generated content (army lists, guides, etc.)
2. Your primary game mode (Matched Play/Crusade/Open Play)
3. Tournament data refresh frequency (Daily/Weekly/Monthly)
4. Meta analysis detail level (Minimal/Standard/Detailed)

## Components

### Agents (6)

**Phase 1 - MVP (Core Gaming):**

1. **⚔️ Tacticus** - Army List Builder & Competitive Strategist
   - Build legal, optimized army lists
   - Meta analysis with tournament data
   - Unit synergy recommendations
   - Points validation

2. **⚖️ Arbitrator** - Rules Judge & Dispute Resolver
   - Resolve complex rule interactions
   - Phase sequencing explanations
   - Wahapedia-cited rulings
   - FAQ database search

**Phase 2 - Enrichment (Hobby & Lore):**

3. **📜 Lorekeeper** - Lore Master & Narrative Historian
   - Faction histories and lore deep-dives
   - Character biographies
   - Battle histories and timelines
   - Narrative context for armies

4. **🎨 Brushmaster** - Painting Guide & Hobby Mentor
   - Interactive paint scheme designer
   - Step-by-step painting tutorials
   - Technique breakdowns
   - Color theory and troubleshooting

**Phase 3 - Advanced (Campaigns & Collections):**

5. **📖 Chronicler** - Campaign Manager & Narrative Coordinator
   - Crusade campaign tracking
   - Battle records and progression
   - Army evolution management
   - Narrative mission generation

6. **🔨 Artisan** - Hobby Advisor & Conversion Specialist
   - Conversion and kitbash guides
   - Basing scheme design
   - Collection planning strategies
   - Tool recommendations

### Workflows (3)

1. **Build Army List** - Interactive list construction with validation and meta analysis
2. **Design Paint Scheme** - Collaborative designer with 3-tier complexity and paint set presets
3. **Session Retrospective** 🆕 - Analyze conversations to extract requirements and improvements

### Tasks (4)

1. **Query Wahapedia** - Centralized rules and unit data retrieval
2. **Fetch Tournament Data** - Cached meta analysis from multiple sources
3. **Validate Army List** - Points calculation and legality checking
4. **Track Project Progress** 🆕 - Unified project tracking across army lists, paint schemes, and campaigns

## Quick Start

### 1. Load an Agent

**For competitive list building:**
```bash
agent tacticus
```

**For rules questions:**
```bash
agent arbitrator
```

**For painting help:**
```bash
agent brushmaster
```

### 2. View Agent Commands

Each agent has a menu of commands. After loading an agent:
```
*menu
```

Or chat directly:
```
CH
```

### 3. Example Workflows

**Build an army list:**
```bash
agent tacticus
BL  # Build List
```

**Design a paint scheme:**
```bash
agent brushmaster
DPS  # Design Paint Scheme
```

**Resolve a rules dispute:**
```bash
agent arbitrator
RQ  # Rules Query
```

## Module Structure

```
warhammer-veteran/
├── agents/                    # 6 specialist agents
│   ├── tacticus.yaml         # Army List Builder
│   ├── arbitrator.yaml       # Rules Judge
│   ├── lorekeeper.yaml       # Lore Master
│   ├── brushmaster.yaml      # Painting Guide
│   ├── chronicler.yaml       # Campaign Manager
│   ├── artisan.yaml          # Hobby Advisor
│   └── [agent]-sidecar/      # Persistent memory folders
├── workflows/                 # Interactive workflows
│   ├── build-army-list/
│   └── design-paint-scheme/
├── tasks/                     # Shared utilities
├── templates/                 # Shared templates
├── data/                      # Module data
├── _module-installer/         # Installation config
├── module.yaml               # Module configuration
├── package.json              # NPM package config
├── README.md                 # This file
└── TODO.md                   # Development roadmap
```

## Configuration

After installation, module settings are stored in `_bmad/warhammer-40k/config.yaml`

**Key Settings:**

- `w40k_output_folder` - Where army lists and guides are saved
- `default_game_mode` - Your primary game mode (matched-play/crusade/open-play)
- `tournament_cache_days` - How often to refresh meta data (1/7/30 days)
- `meta_detail_level` - Tournament analysis verbosity (minimal/standard/detailed)
- `wahapedia_cache_path` - Local cache for Wahapedia queries
- `tournament_cache_path` - Local cache for tournament data

## Agent Features

### Persistent Memory

All agents maintain sidecar memory folders to:
- Remember your faction preferences
- Track past conversations
- Save created content (lists, schemes, campaigns)
- Learn your playstyle and preferences

### Party Mode Integration

All agents support Party Mode for multi-agent collaboration:
```bash
agent tacticus
SPM  # Start Party Mode
```

### Multi-Agent Workflows

Some workflows integrate multiple agents:
- **Design Paint Scheme** consults **Lorekeeper** for faction color accuracy
- Future workflows may combine **Tacticus** + **Arbitrator** for competitive play prep

## Use Cases

### Competitive Players
- Build meta-informed army lists
- Analyze tournament trends
- Resolve rules disputes quickly
- Track win rates and adjustments

### Narrative Players
- Manage Crusade campaigns
- Generate narrative missions
- Track army evolution and stories
- Design lore-accurate paint schemes

### Hobbyists
- Plan painting projects with budget constraints
- Learn new techniques step-by-step
- Design custom color schemes
- Plan conversions and kitbashes

### New Players
- Learn rules with clear explanations
- Explore faction lore to find your army
- Get painting guidance for first models
- Understand competitive meta

## Future Expansion

**Post-MVP Features:**
- Age of Sigmar agent support
- Additional game systems
- Advanced meta prediction AI
- Community army list sharing
- Paint scheme gallery

## Version

**Current Version:** 1.0.0 (Alpha)

## License

This module is part of the BMAD ecosystem.

## Contributing

Contributions, bug reports, and feature requests welcome! This module is in active development.

---

Built with ❤️ for the Warhammer 40k community by BMAD

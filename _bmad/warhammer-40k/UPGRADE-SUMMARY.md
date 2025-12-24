# Warhammer-40K Module BMAD Compliance Upgrade

**Date:** 2024-12-24
**Performed by:** BMAD Builder Agent

## Overview

This module was upgraded to comply with BMAD Method standards based on analysis of:
- `node_modules/bmad-method/src/modules/bmb/docs/` - Architecture documentation
- `node_modules/bmad-method/docs/sample-custom-modules/` - Reference implementations
- Expert agent patterns from `bmb/reference/agents/expert-examples/`

## Changes Made

### 1. Module Definition (NEW)
- **Created:** `_bmad/warhammer-40k/module.yaml`
- Contains: code, name, type, custom config questions (preferred_faction, preferred_game_size, hobby_focus)

### 2. Agent File Renaming
All agents renamed from `*.yaml` to `*.agent.yaml`:
- `tacticus.yaml` → `tacticus.agent.yaml`
- `lorekeeper.yaml` → `lorekeeper.agent.yaml`
- `arbitrator.yaml` → `arbitrator.agent.yaml`
- `artisan.yaml` → `artisan.agent.yaml`
- `brushmaster.yaml` → `brushmaster.agent.yaml`
- `chronicler.yaml` → `chronicler.agent.yaml`

**Also updated:** `.claude/commands/warhammer-40k/agents/*.md` to reference new filenames

### 3. Agent Type Declaration
Added `type: 'expert'` to metadata section of all 6 agents.

### 4. Sidecar Standardization

#### instructions.md (NEW for all agents)
Each agent now has private directives in `{agent}-sidecar/instructions.md`:
- Core directives and domain boundaries
- Behavioral protocols specific to agent role
- Error prevention guidelines
- Knowledge management rules

#### memories.md (NEW for 5 agents)
Created standardized memory files for:
- Arbitrator
- Artisan
- Brushmaster
- Chronicler
- Lorekeeper

(Tacticus already had memories.md)

#### critical_actions Updates
All agents updated to load instructions.md and memories.md first:
```yaml
critical_actions:
  - 'Load COMPLETE file {project-root}/_bmad/warhammer-40k/agents/{agent}-sidecar/instructions.md and follow ALL protocols'
  - 'Load COMPLETE file {project-root}/_bmad/warhammer-40k/agents/{agent}-sidecar/memories.md and integrate all past interactions'
  # ... existing sidecar files ...
  - 'ONLY read/write files in {project-root}/_bmad/warhammer-40k/agents/{agent}-sidecar/'
```

### 5. New Workflows

#### paint-project (NEW)
- **Location:** `_bmad/warhammer-40k/workflows/paint-project/workflow.md`
- **Purpose:** Guide complete painting projects from scheme design to completion
- **Features:** Color scheme creation, batch planning, progress tracking, cross-agent integration
- **Integrated with:** Brushmaster agent via `[PP]` menu option

#### narrative-campaign (NEW)
- **Location:** `_bmad/warhammer-40k/workflows/narrative-campaign/workflow.md`
- **Purpose:** Create and run Crusade campaigns with narrative storytelling
- **Features:** Campaign creation, mission generation, battle recording, progression tracking
- **Integrated with:** Chronicler agent via `[NC]` menu option

### 6. Menu Updates

**Brushmaster:**
- Changed `[DPS] Design Paint Scheme` to `[PP] Paint Project`
- Now routes to paint-project workflow

**Chronicler:**
- Added `[NC] Narrative Campaign` option
- Routes to narrative-campaign workflow

## Current Module Structure

```
_bmad/warhammer-40k/
├── module.yaml                     # Module definition
├── UPGRADE-SUMMARY.md              # This file
├── agents/
│   ├── tacticus.agent.yaml
│   │   └── tacticus-sidecar/
│   │       ├── instructions.md     # Agent protocols
│   │       ├── memories.md         # User preferences
│   │       ├── rules-validated.md  # Rules knowledge base
│   │       ├── datasheet-cache.md  # Cached datasheets
│   │       ├── lists.md            # Saved army lists
│   │       └── sessions/
│   ├── lorekeeper.agent.yaml
│   │   └── lorekeeper-sidecar/
│   │       ├── instructions.md
│   │       ├── memories.md
│   │       ├── explorations.md
│   │       ├── timelines.md
│   │       └── sessions/
│   ├── arbitrator.agent.yaml
│   │   └── arbitrator-sidecar/
│   │       ├── instructions.md
│   │       ├── memories.md
│   │       ├── rulings.md
│   │       ├── faqs.md
│   │       └── sessions/
│   ├── artisan.agent.yaml
│   │   └── artisan-sidecar/
│   │       ├── instructions.md
│   │       ├── memories.md
│   │       ├── projects.md
│   │       ├── collection.md
│   │       └── sessions/
│   ├── brushmaster.agent.yaml
│   │   └── brushmaster-sidecar/
│   │       ├── instructions.md
│   │       ├── memories.md
│   │       ├── projects.md
│   │       ├── techniques.md
│   │       ├── schemes/
│   │       └── sessions/
│   └── chronicler.agent.yaml
│       └── chronicler-sidecar/
│           ├── instructions.md
│           ├── memories.md
│           ├── campaigns.md
│           ├── battles.md
│           └── sessions/
├── workflows/
│   ├── build-army-list/
│   │   └── workflow.md
│   ├── paint-project/              # NEW
│   │   └── workflow.md
│   └── narrative-campaign/         # NEW
│       └── workflow.md
├── data/
│   ├── processed/
│   └── wahapedia-10ed/
└── scripts/
```

## Standards Applied

Per BMAD Method documentation:

1. **Expert Agent Architecture** - All agents have:
   - `type: 'expert'` in metadata
   - Sidecar folders with `-sidecar` suffix
   - `instructions.md` for private protocols
   - `memories.md` for persistent context
   - Domain restriction in critical_actions

2. **Module Structure** - Following sample-wellness-module pattern:
   - `module.yaml` at module root
   - agents/ folder with .agent.yaml files
   - workflows/ folder with workflow.md files

3. **Menu Patterns** - Using multi-trigger format:
   ```yaml
   - multi: '[CODE] Option 1 [CODE2] Option 2'
     triggers:
       - option-1:
           input: CODE or fuzzy match
           route: path/to/workflow.md
           type: exec
   ```

## Future Improvements

Potential enhancements not yet implemented:
- [ ] `knowledge/` folders for domain-specific resources
- [ ] Additional workflows (rules-dispute, collection-audit)
- [ ] Module-level docs/ folder with user guides
- [ ] CSV knowledge bases for conversational_knowledge
- [ ] Party mode cross-agent discussion workflows

## Notes

- Tacticus was already the most developed agent with extensive critical_actions
- Edition enforcement (10th Edition) is handled in Tacticus
- All agents now load instructions.md FIRST for consistent behavior
- Workflows follow step-file architecture pattern but are simplified single-file versions

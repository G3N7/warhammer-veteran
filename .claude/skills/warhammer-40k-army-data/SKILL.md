---
name: warhammer-40k-army-data
description: Deterministic army list data lookup. Use when ANY Warhammer 40K agent needs unit stats, points costs, army composition, leader attachments, validation rules, or faction data. MUST be used instead of generating data from memory to prevent hallucination.
---

# Warhammer 40K Army Data Lookup

## Purpose

This skill provides **deterministic, file-backed data retrieval** for Warhammer 40K army information. It exists to prevent hallucination — agents MUST use this skill instead of generating unit stats, points costs, or rules from memory.

## When to Use

- ANY time an agent needs unit stats, points costs, or weapon profiles
- ANY time an agent needs to verify army list legality
- ANY time an agent needs to know what armies/lists the user has
- ANY time an agent needs leader attachment rules
- ANY time an agent needs detachment rules or faction abilities
- ANY time an agent references validation rules

## Data Sources

All data comes from files in the project. **Never generate data from memory.**

### Source 1: Army List Index

**Location:** `army-lists/` directory

To discover what armies exist:
```
Glob pattern: army-lists/**/*.md
Glob pattern: army-lists/**/*.cheatsheet.json
```

Factions are subdirectories: `army-lists/{faction-slug}/`

### Source 2: Cheatsheet JSON (Primary Structured Data)

**Location:** `army-lists/{faction}/*.cheatsheet.json`

These are the richest structured data files. Schema:
```json
{
  "meta": { "name", "faction", "detachment", "points", "battleSize" },
  "units": [{
    "name": "Unit Name",
    "pts": 105,
    "models": "1",
    "role": "Epic Hero",
    "stats": { "M": "6\"", "T": 5, "SV": "2+", "W": 6, "LD": "6+", "OC": 1, "INV": "4++" },
    "weapons": [{ "name": "Weapon", "profile": "Range | Attacks | Hit | Strength | AP | Damage", "tags": ["keyword"] }],
    "abilities": ["ability description"],
    "core": ["Deep Strike", "Leader"],
    "leads": ["Unit they can lead"],
    "notes": "optional notes"
  }],
  "keywords": { "rule_name": "explanation" },
  "detachmentRule": "description",
  "factionRule": "description",
  "coreStratagems": [...],
  "detachmentStratagems": [...],
  "pointsSummary": [{ "unit": "name", "pts": 105, "qty": 1 }],
  "phaseReminders": { "command": [], "movement": [], "shooting": [], "charge": [], "fight": [], "endOfTurn": [] }
}
```

### Source 3: Faction Datasheets (Full Unit Database)

**Location:** `_bmad/_config/custom/warhammer-40k/data/datasheets/{faction}.json` (full) and `{faction}.compact.json` (compact)

Complete unit datasheets for ALL factions (45 files covering 22+ factions). Contains every unit's stats, weapons, abilities, keywords, points costs, and leader attachment rules.

- **Compact format** (~275 lines per faction): Points, sizes, epic hero status, keywords, leader info. Use for list-building validation.
- **Full format** (~2400 lines per faction): Complete weapon profiles, ability text, detailed tactics. Use for tactical deep-dives.
- **metadata.json**: Index of all available factions and their file dates.

**Available factions:** Space Wolves, Space Marines, Orks, Astra Militarum, Tau Empire, Tyranids, Adepta Sororitas, Imperial Knights, Necrons, Aeldari, Drukhari, Thousand Sons, World Eaters, Death Guard, Chaos Daemons, Chaos Knights, Grey Knights, Adeptus Custodes, Adeptus Mechanicus, Imperial Agents, Leagues of Votann, Emperor's Children

### Source 4: Stratagems Data

**Location:** `_bmad/_config/custom/warhammer-40k/data/stratagems/`

Faction-specific detachment stratagems in JSON format.

### Source 5: Army List Markdown Files

**Location:** `army-lists/{faction}/*.md`

Detailed army lists with narrative, tactical notes, paint schemes, and assembly guides. Read these for full context on a specific army.

### Source 6: Validation Rules

**Location:** `_bmad-output/warhammer-40k/agents/tacticus-sidecar/validation-rules.yaml`

Machine-readable rules for:
- Faction ability specifics (e.g., Space Wolves Oath of Moment = reroll hits only)
- Hard composition rules (Rule of Three, points limits, enhancement eligibility)
- Format-specific constraints (Colosseum: T9 max, no Epic Heroes, 2+ INFANTRY)
- Sequential validation gates

### Source 7: Army Registry

**Location:** `_bmad-output/warhammer-40k/shared/army-registry.yaml`

Central index of all tracked armies with metadata.

### Source 8: Hallucination Registry

**Location:** `_bmad-output/warhammer-40k/shared/hallucination-registry.yaml`

Known hallucination patterns to check against. If your response involves any pattern listed here, STOP and verify against source data.

### Source 9: Retcon Registry

**Location:** `_bmad-output/warhammer-40k/shared/retcon-registry.yaml`

Known lore/rules changes that LLM training data may have wrong.

## How to Execute Queries

### Query: "What armies does the user have?"
```
1. Glob: army-lists/**/*.md → list all files
2. Glob: army-lists/**/*.cheatsheet.json → list structured data
3. Read: _bmad-output/warhammer-40k/shared/army-registry.yaml
4. Present: faction, army name, points level, file path
```

### Query: "What are the stats for [unit] in [army]?"
```
1. Glob: army-lists/{faction}/*.cheatsheet.json
2. Read the JSON file
3. Find the unit in the "units" array
4. Return: stats, weapons, abilities, core rules, leads, points
5. If unit not found in any cheatsheet: SAY SO. Do not guess.
```

### Query: "Is this army list legal?"
```
1. Read: _bmad-output/warhammer-40k/agents/tacticus-sidecar/validation-rules.yaml
2. Read the army's cheatsheet JSON
3. Run each validation gate sequentially
4. Report: pass/fail for each gate with specific violations
```

### Query: "What units can [character] lead?"
```
1. Search cheatsheet JSON for the character
2. Check "leads" array
3. Cross-reference with validation-rules.yaml for any restrictions
4. If not in cheatsheet: check validation-rules.yaml leader-attachment section
5. If not found anywhere: SAY "not in cached data" — do NOT guess
```

### Query: "What are the points costs for [faction]?"
```
1. Read the faction's cheatsheet JSON
2. Extract "pointsSummary" array
3. Calculate total
4. If no cheatsheet exists for this faction: list what IS available and say so
```

## Critical Rules

1. **NEVER generate stats, points, or rules from memory** — always read from files
2. **If data is not in files, say so explicitly** — "This unit/faction is not in our cached data"
3. **Show your source** — always cite which file the data came from: `[Source: army-lists/space-wolves/samelance.cheatsheet.json]`
4. **Check hallucination registry** — before responding about any topic, grep the hallucination registry for relevant patterns
5. **Edition awareness** — all data is for Warhammer 40K 10th Edition (launched June 2023)

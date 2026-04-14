---
name: warhammer-40k-generate-cheatsheet
description: Generate cheatsheet JSON files from army list markdown files and faction datasheets. Use when Tacticus needs to create a new cheatsheet, convert an army list to JSON, or when a faction has army lists but no cheatsheet JSON.
---

# Generate Cheatsheet JSON

## Purpose

Convert army list markdown files into structured cheatsheet JSON for deterministic querying. Cheatsheet JSONs are the primary structured data format that other skills read from.

## When to Use

- When a faction has army list `.md` files but no `.cheatsheet.json`
- When a new army list is created and needs a cheatsheet companion
- When updating an existing cheatsheet after list changes

## Factions Needing Cheatsheets

These factions have army list MDs but no cheatsheet JSON (as of 2026-04-14):
- adepta-sororitas (1 list)
- astra-militarum (2 lists)
- imperial-knights (1 list)
- orks (1 list)
- tau-empire (1 list)
- tyranids (1 list)
- ultramarines (1 list)

## Data Sources

1. **Army list MD**: `army-lists/{faction}/*.md` — the source list to convert
2. **Faction datasheet**: `_bmad/_config/custom/warhammer-40k/data/datasheets/{faction}.json` (full) or `{faction}.compact.json` — for unit stats, weapon profiles, abilities
3. **Cheatsheet schema**: `_bmad/warhammer-40k/agents/tacticus-sidecar/cheatsheet-schema.md` — required output format
4. **Reference example**: `army-lists/space-wolves/samelance.cheatsheet.json` — working example to follow

## Output Schema

```json
{
  "meta": {
    "name": "List Name",
    "faction": "Faction Name",
    "detachment": "Detachment Name",
    "points": 1990,
    "battleSize": "Strike Force (2000pts)"
  },
  "units": [
    {
      "name": "Unit Name",
      "pts": 105,
      "models": "1",
      "role": "Epic Hero | Character | Battleline | Infantry | Vehicle | Beast",
      "stats": { "M": "6\"", "T": 5, "SV": "2+", "W": 6, "LD": "6+", "OC": 1, "INV": "4++" },
      "weapons": [
        { "name": "Weapon", "profile": "Range | Attacks | Hit | Strength | AP | Damage", "tags": ["keyword"] }
      ],
      "abilities": ["shorthand description"],
      "core": ["Deep Strike", "Leader"],
      "leads": ["Unit they can lead"],
      "notes": "optional"
    }
  ],
  "keywords": { "rule_name": "explanation" },
  "detachmentRule": "description",
  "factionRule": "description",
  "coreStratagems": [{ "name": "Name", "cost": "1CP", "when": "phase", "effect": "what it does" }],
  "detachmentStratagems": [{ "name": "Name", "cost": "1CP", "when": "phase", "effect": "what it does" }],
  "pointsSummary": [{ "unit": "name", "pts": 105, "qty": 1 }],
  "phaseReminders": {
    "command": [], "movement": [], "shooting": [],
    "charge": [], "fight": [], "endOfTurn": []
  }
}
```

## Generation Process

### Step 1: Read Source Data
```
1. Read the army list MD file
2. Read the faction's full datasheet JSON
3. Read the cheatsheet schema for format reference
4. Read one example cheatsheet (samelance) for style reference
```

### Step 2: Extract Units
```
For each unit in the army list MD:
1. Find the unit in the faction datasheet JSON
2. Extract: stats (M/T/Sv/W/Ld/OC/Inv), weapons, abilities, core rules, keywords
3. Get points cost from the datasheet
4. Determine role from keywords (BATTLELINE, CHARACTER, EPIC HERO, VEHICLE, etc.)
5. Check leader attachments from datasheet
```

### Step 3: Build Weapon Profiles
```
For each weapon:
1. Format as: "Range | Attacks | Hit | Strength | AP | Damage"
2. Extract weapon tags/keywords (Assault, Rapid Fire X, Dev Wounds, etc.)
3. Separate ranged (has range) from melee (no range)
```

### Step 4: Build Phase Reminders
```
Group abilities by phase they trigger in:
- Command: once-per-turn abilities, CP generation
- Movement: advance rules, fall back and shoot/charge
- Shooting: rerolls, extra hits, target selection
- Charge: charge bonuses, heroic intervention
- Fight: fight first/last, extra attacks
- End of Turn: regeneration, scoring
```

### Step 5: Validate and Save
```
1. Verify total points matches meta.points
2. Verify all units from MD are present in JSON
3. Save to army-lists/{faction}/{list-name}.cheatsheet.json
```

## Critical Rules

1. **ALL stats and weapons MUST come from the datasheet JSON** — never from memory
2. **If a unit is not in the datasheet JSON**, flag it and say so — do not invent stats
3. **Points must match** — verify the JSON total matches the army list MD total
4. **Follow the example** — match the style of samelance.cheatsheet.json exactly
5. **Cite sources**: `Generated from {faction}.json datasheet, {date}`

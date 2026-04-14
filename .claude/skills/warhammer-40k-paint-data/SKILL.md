---
name: warhammer-40k-paint-data
description: Deterministic paint inventory and color scheme lookup. Use when ANY Warhammer 40K agent needs paint names, hex codes, color schemes, or painting product data. MUST be used instead of generating paint data from memory to prevent hallucination (especially discontinued paint ranges).
---

# Warhammer 40K Paint Data Lookup

## Purpose

This skill provides **deterministic, file-backed paint data retrieval**. It exists because LLMs frequently hallucinate discontinued paint names (e.g., old Warpaints range replaced by Warpaints Fanatic in 2024). Agents MUST use this skill for all paint references.

## When to Use

- ANY time an agent needs to reference specific paint names
- ANY time an agent recommends paints for a scheme
- ANY time an agent needs hex color codes
- ANY time an agent discusses paint products or inventory
- ANY time an agent builds a shopping list

## Data Sources

### Source 1: Army Painter Warpaints Inventory

**Location:** `_bmad/_config/custom/warhammer-40k/data/paints/army-painter-warpaints.json`
**Content:** 60 paints with hex codes, coverage levels, categories
**Categories:** Base (■), Layer (▲), Metallic (◆), Wash (●), Effect (★), Primer (▼)

### Source 2: Army Painter Speedpaints Inventory

**Location:** `_bmad/_config/custom/warhammer-40k/data/paints/army-painter-speedpaints.json`
**Content:** 24 speedpaints with hex codes, intensity levels (light/medium/dark)

### Source 3: Paint Inventory Schema

**Location:** `_bmad/_config/custom/warhammer-40k/data/paints/paint-inventory.schema.json`
**Content:** JSON Schema defining paint data structure

### Source 4: Brushmaster Sidecar

**Location:** `_bmad-output/warhammer-40k/agents/brushmaster-sidecar/`
**Content:** User's painting projects, saved schemes, technique notes

### Source 5: Color Schemes in Army Lists

**Location:** `army-lists/{faction}/*.md`
**Content:** Paint schemes embedded in army list markdown files (look for paint/color sections)

## How to Execute Queries

### Query: "What paints do we have?"
```
1. Read: _bmad/_config/custom/warhammer-40k/data/paints/army-painter-warpaints.json
2. Read: _bmad/_config/custom/warhammer-40k/data/paints/army-painter-speedpaints.json
3. Present: categorized list with hex codes
```

### Query: "What paint should I use for [color]?"
```
1. Read both paint JSON files
2. Filter by hex code proximity or category
3. Return: paint name, hex, category, coverage/intensity
4. If no close match: SAY SO — do not invent paint names
```

### Query: "What's the scheme for [army]?"
```
1. Glob: army-lists/{faction}/*.md
2. Read the army file, search for paint/color sections
3. Check brushmaster sidecar for saved schemes
4. Present with source citation
```

## Critical Rules

1. **NEVER generate paint names from memory** — always read from JSON files
2. **The current Army Painter range is Warpaints Fanatic (2024+)** — our JSON files contain verified current names
3. **If a paint name is not in our inventory, say so** — "This paint is not in our tracked inventory"
4. **Always include hex codes** when recommending paints — enables visual verification
5. **Show your source** — cite which file: `[Source: army-painter-warpaints.json]`
6. **Check hallucination registry** — paint name hallucination is a documented pattern

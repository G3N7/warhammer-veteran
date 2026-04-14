---
name: warhammer-40k-validate-list
description: Deterministic army list validation against machine-readable rules. Use when ANY agent needs to check if an army list is legal, validate points totals, check enhancement eligibility, verify leader attachments, or run the Colosseum format rules.
---

# Warhammer 40K Army List Validator

## Purpose

This skill provides **deterministic, rule-based army list validation**. It reads validation rules from YAML and unit data from JSON to produce pass/fail results for each validation gate. No guessing — every check is backed by a specific rule.

## When to Use

- Before presenting ANY army list to the user
- When asked "is this list legal?"
- When checking points totals, force org, wargear, or enhancement legality
- When validating Colosseum (500pt) format-specific restrictions
- After modifying an army list

## Data Sources

### Validation Rules
**Location:** `_bmad-output/warhammer-40k/agents/tacticus-sidecar/validation-rules.yaml`

Contains:
- `faction_abilities` — chapter-specific rules (divergent chapters get weaker Oath of Moment)
- `hard_rules` — violations that make a list ILLEGAL
- `colosseum_format` — 500pt King of the Colosseum restrictions
- `detachments` — detachment-specific enhancements and rules
- `validation_gates` — sequential checks that must ALL pass

### Unit Data
**Location:** `_bmad/_config/custom/warhammer-40k/data/datasheets/{faction}.compact.json`

Contains per-unit: points, sizes, epic_hero flag, keywords, leader info.

### Cheatsheet Data
**Location:** `army-lists/{faction}/*.cheatsheet.json`

Contains per-unit: stats, weapons, abilities, leads array, points.

## Validation Gate Sequence

Run these gates IN ORDER. Stop on first failure.

### Gate 1: Points Total
```
1. Read validation-rules.yaml → hard_rules.points_limit.limits
2. Sum all unit points from the list
3. Sum all enhancement points
4. total = unit_points + enhancement_points
5. IF total > limit → ILLEGAL: "Over by X points"
6. Show itemized breakdown
```

### Gate 2: Rule of Three
```
1. Read validation-rules.yaml → hard_rules.rule_of_three
2. Count units by datasheet name
3. FOR each datasheet with count > 3:
   - Check if unit has BATTLELINE or DEDICATED TRANSPORT keyword
   - IF not exempt AND count > 3 → ILLEGAL: "X copies of Y (max 3)"
```

### Gate 3: Epic Hero Uniqueness
```
1. Read validation-rules.yaml → hard_rules.epic_hero_unique
2. FOR each unit in list:
   - Check if epic_hero == true in datasheet
   - IF same Epic Hero appears twice → ILLEGAL: "Duplicate Epic Hero: X"
```

### Gate 4: Enhancement Eligibility
```
1. Read validation-rules.yaml → hard_rules.enhancement_eligibility
2. FOR each enhancement assigned:
   - Verify target has CHARACTER keyword
   - Verify target does NOT have EPIC HERO keyword
   - IF fails → ILLEGAL: "Enhancement on Epic Hero/non-CHARACTER: X"
3. Read hard_rules.enhancement_limit.limits
4. Count total enhancements
5. IF count > limit for game size → ILLEGAL: "Too many enhancements"
```

### Gate 5: Unit Sizes
```
1. Read validation-rules.yaml → hard_rules.unit_sizes
2. FOR each unit:
   - Read datasheet sizes array
   - IF models not in valid sizes → ILLEGAL: "Invalid unit size for X"
```

### Gate 6: Leader Attachments
```
1. Read validation-rules.yaml → hard_rules.leader_count
2. FOR each unit with attached leader(s):
   - Verify leader's "leads" array includes the bodyguard unit
   - IF two leaders attached, verify BOTH have "alongside" text
   - IF fails → ILLEGAL: "Invalid leader attachment: X to Y"
```

### Gate 7: Faction Abilities (Warning Level)
```
1. Read validation-rules.yaml → faction_abilities
2. IF faction is a divergent chapter (Space Wolves, Blood Angels, etc.):
   - Flag if list assumes full Oath of Moment (+1 wound)
   - WARNING: "Divergent chapter — Oath of Moment is reroll hits ONLY"
```

### Colosseum Format Gates (500pt only)
```
IF game_size == 500 AND format == "colosseum":
  1. Must have at least 1 CHARACTER
  2. No models with Toughness > 9
  3. No Epic Heroes
  4. At least 2 INFANTRY units
  Read full restrictions from colosseum_format section
```

## Output Format

```
## Validation Report: [Army Name]

| Gate | Check | Result | Detail |
|------|-------|--------|--------|
| 1 | Points Total | PASS/FAIL | X/Y pts (Z remaining) |
| 2 | Rule of Three | PASS/FAIL | [details if fail] |
| 3 | Epic Hero Unique | PASS/FAIL | |
| 4 | Enhancement Eligibility | PASS/FAIL | |
| 5 | Unit Sizes | PASS/FAIL | |
| 6 | Leader Attachments | PASS/FAIL | |
| 7 | Faction Abilities | WARN/OK | [divergent chapter note] |

**Verdict:** LEGAL / ILLEGAL (X gates failed)
```

## Critical Rules

1. **Every check reads from files** — never validate from memory
2. **Show which rule was checked** — cite `[validation-rules.yaml: hard_rules.X]`
3. **Stop on first ILLEGAL** — report all failures but the list is illegal on the first one
4. **Points math must be shown** — itemized breakdown, not just the total
5. **If data is missing** — say "Cannot validate: unit X not found in datasheet cache"

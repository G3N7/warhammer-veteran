# Cheatsheet JSON Schema Reference
# Extracted from tacticus.agent.yaml to reduce instruction volume
# Version: 1.0 | Last Updated: 2026-02-16

## JSON Structure

Top-level: `{ meta, units[], keywords{}, detachmentRule, factionRule, coreStratagems[], detachmentStratagems[], pointsSummary[] }`

### META

```json
{
  "meta": {
    "name": "List Name",
    "faction": "Faction Name",
    "detachment": "Detachment Name",
    "points": 1990,
    "battleSize": "Strike Force (2000pts)"
  }
}
```

### UNITS (for each unit in army list)

```json
{
  "name": "Unit Name",
  "pts": 105,
  "models": "1" or "10 (9 + Pack Leader)",
  "qty": 2,  // optional - only if multiple identical units
  "role": "Epic Hero" | "Character" | "Battleline" | "Infantry" | "Vehicle" | "Beast",
  "stats": { "M": "6\"", "T": 5, "SV": "2+", "W": 6, "LD": "6+", "OC": 1, "INV": "4++", "FNP": "5+" },
  "weapons": [
    { "name": "Weapon Name", "profile": "24\" | A6 | 2+ | S6 | 0 | 1", "tags": ["Dev Wounds", "Rapid Fire 2"] }
  ],
  "abilities": ["shorthand ability 1", "shorthand ability 2"],
  "core": ["Deep Strike", "Leader", "Grenades"],
  "leads": ["Unit A", "Unit B"],  // optional - only for Leader characters
  "notes": "optional notes"
}
```

## CORE ARRAY POPULATION (CRITICAL - DO NOT SKIP)

The "core" array MUST include ALL gameplay-relevant abilities/keywords from TWO sources:

### Source 1: abilities.core from datasheet

These are explicit core abilities like:
- Deep Strike, Leader, Deadly Demise X, Feel No Pain X+
- Infiltrators, Scouts X", Lone Operative, Stealth
- Fights First, Hover, Transport X

Always include these directly in the core array.

### Source 2: Gameplay keywords from unit keywords array

The unit "keywords" array contains BOTH faction keywords (INFANTRY, IMPERIUM) AND
gameplay-relevant keywords. Extract ONLY the gameplay keywords:
- GRENADES -> enables Grenade stratagem (critical for infantry)
- SMOKE -> enables Smokescreen stratagem (critical for vehicles/infantry)
- FLY -> can move over models and terrain
- MOUNTED -> Tank Shock, Ride Hard stratagems
- PSYKER -> psychic abilities

DO NOT include faction/type keywords like INFANTRY, BATTLELINE, IMPERIUM, ADEPTUS ASTARTES

### Complete Extraction Example

If datasheet shows:
```
keywords: ["INFANTRY", "BATTLELINE", "GRENADES", "IMPERIUM", "TACTICUS", "BLOOD CLAWS"]
abilities.core: []
```
Then cheatsheet core array should be: `["Grenades"]`

If datasheet shows:
```
keywords: ["INFANTRY", "GRENADES", "SMOKE", "IMPERIUM", "SCOUT SQUAD", "WOLF SCOUTS"]
abilities.core: ["Infiltrators", "Scouts 6\""]
```
Then cheatsheet core array should be: `["Infiltrators", "Scouts 6\"", "Grenades", "Smoke"]`

### Core Array Rules

- **NEVER EMPTY**: If a unit has ANY gameplay keywords (GRENADES, SMOKE, etc.) or core abilities, the core array must NOT be empty. An empty core array means the unit has NO special deployment, keyword-enabled stratagems, or core rules.

### Gameplay Keywords Reference

Always extract these keywords from the keywords array to core:
- GRENADES -> "Grenades" (enables 1CP Grenade strat: D6 attacks S4 AP0 Dmg1 Blast at 6")
- SMOKE -> "Smoke" (enables 1CP Smokescreen strat: -1 to Hit vs unit)
- FLY -> "Fly" (move over models/terrain, measure through air)
- MOUNTED -> "Mounted" (Tank Shock, movement stratagems)
- PSYKER -> "Psyker" (can use psychic abilities)
- TRANSPORT -> "Transport" (can carry units)
- WALKER -> note as "Walker" if relevant to faction rules

## ABILITY SHORTHAND (CRITICAL)

Convert verbose ability text to tournament-friendly shorthand. This saves table space and speeds up gameplay.

### Shorthand Patterns

| Full Text | Shorthand |
|-----------|-----------|
| "roll one D6: on a 4+, do not remove destroyed model" | "4+ FoD (melee)" |
| "you can re-roll the Hit roll and Wound roll" | "Full RR Hit+Wound vs [target]" |
| "re-roll wound rolls of 1" | "RR Wound 1s" |
| "re-roll wound rolls" | "Full RR Wound" |
| "re-roll hit rolls" | "Full RR Hit" |
| "+1 to wound rolls" | "+1 to Wound" |
| "enemy models suffer -1 to hit" | "-1 to Hit (Aura)" or "-1 to Hit vs this unit" |
| "models suffer -1 to wound when Strength > Toughness" | "-1 to Wound when S > T" |
| "Advance and charge in same turn" | "Can charge after Advancing" |
| "set up in Strategic Reserves" | "Deep Strike" (use core ability) |
| "one model destroyed returns to unit" | "Rez 1 model/Cmd phase" |
| "gain +1 Command point each Command phase" | "+1CP each Cmd phase" |
| "6\" aura that grants +1 to Advance and Charge" | "+1 Adv/Chg for [FACTION] w/in 6\" (Aura)" |

- **CONTEXT**: Include target/trigger in parentheses: "(melee)", "(shooting)", "(Aura)", "vs CHAR", "w/in 6\""
- **KEEP IT SHORT**: Target 40-60 characters max per ability. If longer, abbreviate further.

## WEAPON PROFILE FORMAT

### Layout

- Ranged: `"24\" | A6 | 2+ | S6 | 0 | 1"` (Range | Attacks | BS | Strength | AP | Damage)
- Melee: `"A5 | 2+ | S8 | -2 | 3"` (Attacks | WS | Strength | AP | Damage)
- Variable: `"A1 | 3+ | S7/8 | -2/-3 | 1/2"` (for supercharge/overcharge modes)
- Random: `"12\" | D6 | N/A | S5 | -1 | 1"` (for auto-hit weapons like flamers)
- Dice damage: `"| D3"` (roll 1-3), `"| D6"` (roll 1-6), `"| D6+2"` (roll d6+2)

### Damage Notation

- Fixed damage uses plain numbers: 1, 2, 3
- Variable/dice damage uses D prefix: D3, D6, D6+2 (roll the die)

### Weapon Tags

Use standard abbreviations: "Dev Wounds", "Lethal Hits", "Rapid Fire X", "Twin-linked", "Torrent", "Ign Cover", "Hazardous", "Pistol", "Assault", "Anti-X Y+", "Precision"

## STRATAGEMS

### Format

```json
{
  "name": "Stratagem Name",
  "cp": 1,
  "phase": "Fight" | "Shooting" | "Move" | "Charge" | "Any" | "Enemy Shooting" | "Enemy Move/Charge",
  "type": "Battle Tactic" | "Strategic Ploy" | "Epic Deed",  // for detachment strats only
  "effect": "Short description of effect (1 line, ~80 chars)"
}
```

- **CORE STRATAGEMS**: Include Command Re-roll, Counter-offensive, Epic Challenge, Fire Overwatch, Go to Ground, Grenade, Heroic Intervention, Insane Bravery, Rapid Ingress, Smokescreen, Tank Shock
- **DETACHMENT STRATAGEMS**: Include all 5-6 stratagems from the selected detachment. Verify names from Wahapedia or validation-rules.yaml.

## KEYWORDS GLOSSARY

Include definitions for all keywords used by units in the list:

```json
{
  "keywords": {
    "Deep Strike": "Set up in Reserves, arrive 9\"+ from enemies",
    "Deadly Demise X": "On death, 6+ = X mortal wounds to units w/in 6\"",
    "Rapid Fire X": "+X attacks at half range",
    "Grenades": "Enables Grenade strat (1CP): D6 attacks S4 AP0 Dmg1 Blast at 6\"",
    "Smoke": "Enables Smokescreen strat (1CP): -1 to Hit vs unit",
    "Infiltrators": "Set up anywhere 9\"+ from enemy deployment/models",
    "Scouts X\"": "Before T1, make Normal move up to X\""
  }
}
```

**INCLUDE**: Core abilities (Deep Strike, Leader, Deadly Demise, Infiltrators, Scouts), gameplay keywords (Grenades, Smoke, Fly, Mounted), weapon abilities (Dev Wounds, Lethal Hits, Twin-linked, etc.), and any faction-specific keywords

## DETACHMENT AND FACTION RULES

```json
{
  "detachmentRule": { "name": "Rule Name", "effect": "One-line summary" },
  "factionRule": { "name": "Oath of Moment", "effect": "Start of Cmd phase: pick 1 enemy unit. RR Hit rolls vs that unit." }
}
```

## POINTS SUMMARY

```json
{
  "pointsSummary": [
    { "unit": "Unit Name", "pts": 105, "qty": 1 },
    { "unit": "Unit Name (10)", "pts": 340, "qty": 3 }
  ]
}
```

## GENERATION WORKFLOW

1. After completing army list validation, attempt to load `{faction}.json` (full datasheet data). If file is too large (>256KB / Read fails), use LARGE FILE extraction method from main instructions. For each unit in the army list, use Grep: `grep -A 200 '"Unit Name": \{' {faction}.json`
2. For each unit in the list, extract stats/weapons/abilities from datasheet (or extracted JSON block)
3. Build the "core" array for each unit (CRITICAL - most commonly missed):
   - a) Start with abilities.core from datasheet (Deep Strike, Leader, Deadly Demise, etc.)
   - b) Scan unit keywords array for gameplay keywords: GRENADES, SMOKE, FLY, MOUNTED, PSYKER
   - c) Add extracted gameplay keywords to core array (e.g., "Grenades", "Smoke")
   - d) Result: core array contains ALL abilities that affect gameplay or enable stratagems
   - EXAMPLE: Blood Claws has `keywords=["INFANTRY","BATTLELINE","GRENADES",...]`, `abilities.core=[]` -> cheatsheet core array should be: `["Grenades"]`
4. Convert verbose ability text to shorthand using patterns above
5. Build weapon profiles in "Range | A | BS | S | AP | D" format with tags array
6. Add core stratagems (standard set) + detachment stratagems (from detachment)
7. Build keywords glossary from all keywords used in units (include Grenades if any unit has it)
8. Add faction rule and detachment rule summaries
9. Add points summary table
10. Write to `{list-name}.cheatsheet.json` in same directory as army list
11. Inform user they can generate PDF with: `cd {project-root}/tools/cheatsheet-printer && node src/index.js [path]`

## PRINT COMMAND

- **Generate PDF**: After generating cheatsheet, user can run: `cd {project-root}/tools/cheatsheet-printer && npm run print -- {path-to-cheatsheet.json}`
- **Options**: `--no-datasheets`, `--no-keywords`, `--no-points`, `--only-datasheets`, `--only-reference`

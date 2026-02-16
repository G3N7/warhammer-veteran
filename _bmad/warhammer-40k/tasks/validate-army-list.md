# Validate Army List Task

## Purpose
Validates Warhammer 40k army lists for points accuracy, force organization compliance, detachment rules, and unit legality. Provides detailed error messages and suggestions for corrections.

## Usage

**From Agents:**
```yaml
- action: Execute task validate-army-list with list_data={...}
```

**From Workflows:**
```yaml
Execute: validate-army-list
Parameters:
  list_data: {parsed army list}
  game_mode: "matched-play"
  strict_mode: true
```

## Inputs

- `list_data` (required): Structured army list object
  ```json
  {
    "faction": "Space Marines",
    "detachment": "Gladius Task Force",
    "points_limit": 2000,
    "units": [
      {
        "name": "Intercessor Squad",
        "count": 1,
        "size": 10,
        "wargear": ["Bolt Rifles"],
        "enhancements": []
      }
    ]
  }
  ```
- `game_mode` (optional): "matched-play", "crusade", "open-play" (uses config default if not specified)
- `strict_mode` (optional): Enforce all rules strictly vs lenient interpretation (default: true)
- `points_limit` (optional): Override points limit (default: from list_data)

## Outputs

Returns validation results:
- `valid`: Boolean - overall validity
- `total_points`: Calculated points total
- `points_breakdown`: Points by unit/wargear
- `errors`: Array of validation errors
  - `type`: "points", "force_org", "detachment", "wargear", "rule"
  - `severity`: "critical", "warning", "info"
  - `message`: Human-readable error
  - `suggestion`: How to fix
- `warnings`: Non-critical issues
- `force_organization`: Slot usage breakdown
- `detachment_compliance`: Detachment rule checks

## Validation Rules

### 1. Points Calculation
- Sum all unit costs
- Add wargear upgrades
- Include enhancements/relics
- Apply any discounts (battleline, etc.)
- Verify against points limit

### 2. Force Organization (Matched Play)
**Standard Detachment Slots:**
- HQ: 1-2 required
- Troops: 0-6
- Elites: 0-6
- Fast Attack: 0-3
- Heavy Support: 0-3
- Flyer: 0-2
- Dedicated Transports: No limit

**Detachment-Specific Rules:**
- Check detachment eligibility
- Verify faction keywords match
- Enforce detachment restrictions

### 3. Unit Legality
- Valid unit for faction
- Unit size within min/max
- Wargear options legal
- Leader/bodyguard attachments valid
- Unit datasheet compliance

### 4. Game Mode Rules
**Matched Play:**
- Rule of 3 (max 3 of same datasheet, except Battleline/Dedicated Transports)
- Points limit adherence
- Detachment rules

**Crusade:**
- Order of Battle limits
- Supply limit
- Crusade card validation

**Open Play:**
- Minimal restrictions
- Points suggested but not enforced

### 5. Enhancements/Relics
- Max number per list
- Faction restrictions
- Character eligibility
- No duplicates

## Implementation

<task>
**Step 1: Parse List Data**
- Extract faction, detachment, points limit
- Normalize unit names
- Structure wargear and enhancements

**Step 2: Fetch Reference Data**
Use Query Wahapedia task to get:
- Unit datasheets and points
- Detachment rules
- Faction-specific rules
- Wargear costs

**Step 3: Calculate Points**
For each unit:
- Base unit cost
- Wargear upgrades
- Model count modifiers
- Apply discounts

Aggregate:
- Total points
- Points breakdown by unit
- Verify against limit

**Step 4: Validate Force Organization**
- Count units in each slot
- Check min/max requirements
- Verify HQ and Troops minimums
- Enforce slot limits

**Step 5: Check Detachment Rules**
- Faction keyword compliance
- Detachment-specific restrictions
- Enhancement/stratagem eligibility
- Special detachment rules

**Step 6: Validate Units**
For each unit:
- Legal for faction
- Unit size valid
- Wargear options allowed
- Leader attachments valid
- Keywords match requirements

**Step 7: Game Mode Checks**
Apply mode-specific rules:
- **Matched Play**: Rule of 3, points limit
- **Crusade**: Supply/OOB limits
- **Open Play**: Minimal validation

**Step 8: Generate Results**
- Categorize errors by severity
- Provide actionable suggestions
- Calculate force org breakdown
- Summary of compliance status
</task>

## Error Examples

**Critical Errors:**
```json
{
  "type": "points",
  "severity": "critical",
  "message": "Army exceeds points limit: 2050/2000",
  "suggestion": "Remove 50 points worth of units or wargear"
}
```

**Warnings:**
```json
{
  "type": "force_org",
  "severity": "warning",
  "message": "Only 1 HQ unit (2 recommended)",
  "suggestion": "Add another HQ for more command points"
}
```

**Info:**
```json
{
  "type": "optimization",
  "severity": "info",
  "message": "Intercessors are Battleline - exempt from Rule of 3",
  "suggestion": null
}
```

## Output Examples

**Valid List:**
```json
{
  "valid": true,
  "total_points": 1998,
  "points_breakdown": {
    "units": 1850,
    "wargear": 98,
    "enhancements": 50
  },
  "errors": [],
  "warnings": [],
  "force_organization": {
    "HQ": "2/2",
    "Troops": "3/6",
    "Elites": "2/6",
    "Heavy_Support": "1/3"
  }
}
```

**Invalid List:**
```json
{
  "valid": false,
  "total_points": 2075,
  "errors": [
    {
      "type": "points",
      "severity": "critical",
      "message": "Exceeds 2000 points by 75",
      "suggestion": "Remove wargear or reduce unit size"
    },
    {
      "type": "force_org",
      "severity": "critical",
      "message": "No HQ units (minimum 1 required)",
      "suggestion": "Add a Captain, Lieutenant, or other HQ"
    }
  ]
}
```

## Strict vs Lenient Mode

**Strict Mode** (default for Matched Play):
- All rules enforced
- Points must be exact
- Force org strictly followed
- Wargear options validated

**Lenient Mode** (for casual/narrative):
- Points within 5% tolerance
- Force org warnings only
- Wargear suggestions not errors
- Rule of 3 advisory

## Notes

- Points costs change with FAQ updates - cache invalidation important
- Detachment rules vary significantly - dynamic validation needed
- Some rules are subjective (e.g., "counts as")
- Provide helpful messages, not just "invalid"
- Link to Wahapedia sources for disputed rules

## Dependencies

- Query Wahapedia task (for unit data and rules)
- JSON parsing and manipulation
- Mathematical calculations
- String matching for unit names

## Future Enhancements

- Point efficiency scoring
- Alternative suggestions (swap X for Y)
- FAQ/errata integration
- Visual list validation UI
- Export to common formats (BattleScribe, etc.)

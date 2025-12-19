# Build Army List Workflow

Interactive step-by-step army list construction with validation, meta analysis, and competitive optimization.

## Activation

This workflow is triggered by Tacticus (Army List Builder) agent when user selects **[BL] Build List**.

## Overview

Guides users through building a competitive, legal Warhammer 40k army list with:
- Faction and detachment selection
- Unit-by-unit construction
- Real-time points tracking
- Meta analysis and suggestions
- Validation and optimization
- Save to persistent storage

## Prerequisites

- Query Wahapedia task (for unit data)
- Fetch Tournament Data task (for meta analysis)
- Validate Army List task (for validation)
- Tacticus sidecar folder (for saving)

## Workflow Steps

### Step 1: Initialize List

**Prompt user for:**
- Points limit (1000/2000/3000 or custom)
- Game mode (Matched Play, Crusade, Open Play)
- Faction preference (or load from sidecar memory)

**Execute:**
- Load user's past lists from `tacticus-sidecar/lists.md`
- Load faction preferences from `tacticus-sidecar/memories.md`
- Initialize empty list structure:
  ```json
  {
    "faction": null,
    "detachment": null,
    "points_limit": 2000,
    "game_mode": "matched-play",
    "units": [],
    "total_points": 0
  }
  ```

**Present:**
- Welcome message with points limit
- User's faction history (if any)
- Recommended starting factions based on meta

**Output:** Initialized list object

---

### Step 2: Select Faction & Detachment

**Query Wahapedia:**
- Get list of all factions
- Get faction abilities
- Get available detachments per faction

**Present to user:**
- Faction selection (with brief descriptions)
- Highlight user's previously used factions
- Show current meta standings (via Fetch Tournament Data)

**After faction selection:**
- Query detachments for chosen faction
- Explain each detachment's playstyle
- Show tournament popularity of each detachment

**User selects detachment**

**Execute:**
- Update list object with faction and detachment
- Fetch detachment rules from Wahapedia
- Note faction preference in memories

**Output:** List with faction and detachment set

---

### Step 3: Add Units (Iterative)

**Display current state:**
- Points used / points limit
- Force organization slots filled
- Current units in list

**Present force org slots:**
```
Available Slots:
[HQ] Add HQ unit (0/2 filled)
[TR] Add Troops (0/6 filled)
[EL] Add Elites (0/6 filled)
[FA] Add Fast Attack (0/3 filled)
[HS] Add Heavy Support (0/3 filled)
[FL] Add Flyer (0/2 filled)
[DT] Add Dedicated Transport

[V] Validate list
[M] Get meta suggestions
[D] Done adding units
```

**When user selects slot (e.g., [HQ]):**

1. **Query Wahapedia** for units in that slot for the faction
2. **Fetch Tournament Data** for unit popularity
3. **Present units** with:
   - Name
   - Points cost
   - Brief role description
   - Tournament inclusion rate (if available)
   - Meta tier (S/A/B/C based on win correlation)

**User selects unit:**

1. **Configure unit:**
   - Unit size (min/max)
   - Wargear options
   - Leader attachments (if applicable)
   - Calculate points

2. **Show meta insights:**
   - "This unit appears in 73% of winning lists"
   - "Commonly paired with: [Unit X]"
   - "Win correlation: High (+0.62)"

3. **Add to list**

**Real-time validation:**
- Check points don't exceed limit
- Verify force org compliance
- Warn about Rule of 3 violations
- Show synergy opportunities

**Loop until user selects [D] Done**

**Output:** Populated list with units

---

### Step 4: Validate & Optimize

**Execute Validate Army List task:**
```yaml
validate-army-list:
  list_data: {current list}
  game_mode: {user's game mode}
  strict_mode: true
```

**Present validation results:**
- ✅ Valid or ❌ Invalid
- Points total and breakdown
- Force organization status
- Any errors or warnings

**If errors exist:**
- Show each error with suggestion
- Allow user to:
  - [F] Fix errors (return to Step 3)
  - [I] Ignore warnings (continue)
  - [C] Cancel and start over

**If valid:**

**Execute Fetch Tournament Data** for full list analysis:
- Overall list archetype classification
- Compare to winning lists
- Identify missing synergies
- Suggest optimizations

**Present optimization suggestions:**
```
List Analysis:
- Archetype: Mechanized Infantry
- Similar lists: 52% win rate in tournaments
- Strong against: Necrons, Tyranids
- Weak against: Eldar, Tau

Optimization Suggestions:
1. Add anti-tank: Consider Ballistus Dreadnought (+185pts)
2. Unit synergy: Your Intercessors benefit from Captain rerolls
3. Meta pick: Lieutenants are highly popular and effective

[A] Apply suggestion #1
[K] Keep current list
[O] Show more options
```

**User decides:** Accept optimizations or keep current

**Output:** Final validated list

---

### Step 5: Analyze Synergies

**Analyze unit interactions:**
- Buff/debuff chains
- Aura overlaps
- Strategic synergies
- Counter-play options

**Present synergy analysis:**
```
Unit Synergies:
⚔️ Captain + Intercessors: Reroll hits (high value)
🛡️ Ancient + Infantry: 6+ ignore wounds on death
🎯 Eliminators + Phobos units: Stealth deployment synergy

Tactical Recommendations:
- Deploy Captain within 6" of Intercessors for max efficiency
- Ancient works best near objective-holding Troops
- Consider Phobos detachment for stealth synergy

Missing Synergies:
- No anti-tank for heavy armor
- Limited screening units
- Psychic defense weak
```

**Output:** Synergy report

---

### Step 6: Generate Final List & Save

**Generate formatted army list:**
```markdown
# [Faction Name] - [Detachment] (2000pts)

## HQ (200pts)
- Captain with Master-Crafted Bolt Rifle (110pts)
- Lieutenant with Combi-Weapon (90pts)

## Troops (450pts)
- Intercessor Squad x10 with Bolt Rifles (180pts)
- Intercessor Squad x5 with Auto Bolt Rifles (135pts)
- Scout Squad x5 with Bolters (135pts)

[Continue for all slots...]

## Total: 1998/2000 points

## Meta Analysis
- Win Rate: ~52% (similar lists)
- Tournament Tier: A-tier
- Popular Matchup: Strong vs infantry-heavy armies

## Synergy Summary
[Key synergies from Step 5]

## Notes
- Built with Warhammer Veteran
- Data from: Wahapedia, 40k Event Tracker, Stat Check
- Generated: {date}
```

**Save to tacticus-sidecar:**
- `lists.md` - append full list
- `memories.md` - update faction preferences and patterns

**Present completion:**
```
✅ Army List Complete!

📋 List saved to tacticus-sidecar/lists.md
📊 {total_points}/{points_limit} points
✅ Legal for {game_mode}
🎯 Estimated win rate: ~52%

[E] Export list (copy to clipboard)
[S] Share insights with Lorekeeper (learn faction lore)
[T] Test against rules scenarios with Arbitrator
[X] Exit workflow
```

**User options:**
- Export formatted list
- Transition to other agents
- Exit

**Output:** Saved, validated, optimized army list

---

## Error Handling

**Wahapedia unavailable:**
- Use cached data if available
- Warn user data may be outdated
- Continue with reduced functionality

**Tournament data unavailable:**
- Skip meta analysis
- Provide basic list without competitive insights
- Note limitation to user

**Validation failures:**
- Always allow user to save invalid lists (with warning)
- Mark as "Work in Progress"
- Suggest fixes

## Data Flow

```
User Input (faction, points)
    ↓
Query Wahapedia (unit data)
    ↓
User Selection (units)
    ↓
Fetch Tournament Data (meta insights)
    ↓
Validate Army List (check legality)
    ↓
Save to Sidecar (persistence)
    ↓
Output (formatted list + analysis)
```

## Integration Points

**Tasks Used:**
- `query-wahapedia` - Unit data, rules, detachments
- `fetch-tournament-data` - Meta analysis, win rates
- `validate-army-list` - Legality checking

**Agents Involved:**
- **Tacticus** - Primary agent running this workflow
- **Lorekeeper** - Optional transition for lore context
- **Arbitrator** - Optional transition for rule questions

**Sidecar Files:**
- `tacticus-sidecar/lists.md` - Saved army lists
- `tacticus-sidecar/memories.md` - Faction preferences

## Future Enhancements

- Import from BattleScribe XML
- Export to TTS (Tabletop Simulator)
- Matchup analysis against specific factions
- Point efficiency scoring
- Alternative list suggestions
- Budget-conscious list building (start collecting boxes)

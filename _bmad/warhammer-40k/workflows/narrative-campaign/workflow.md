---
name: Narrative Campaign
description: Create and run narrative Crusade campaigns with story-driven missions and army progression
web_bundle: false
---

# Narrative Campaign Workflow

**Goal:** Design, run, and chronicle narrative Crusade campaigns with rich storytelling and meaningful progression.

**Your Role:** Campaign master weaving engaging narratives while tracking mechanical progression, balancing drama with clear record-keeping.

## WORKFLOW ARCHITECTURE

### Core Principles

- **Narrative First:** Story emerges from gameplay - let battles shape the tale
- **Player Agency:** Choices matter - player decisions drive outcomes
- **Meaningful Progression:** Every battle changes something
- **Collaborative Storytelling:** Campaign master and players build together

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read entire step file before execution
- **ALWAYS** follow the exact instructions in the step file
- **ALWAYS** halt at menus and wait for user input
- **NEVER** create mental todo lists from future steps

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read config from {project-root}/_bmad/warhammer-40k/module.yaml and resolve:

- `user_name`, `preferred_faction`, `hobby_focus`

### 2. Agent Context Loading

Load Chronicler sidecar files:
- `{project-root}/_bmad/warhammer-40k/agents/chronicler-sidecar/memories.md`
- `{project-root}/_bmad/warhammer-40k/agents/chronicler-sidecar/campaigns.md`
- `{project-root}/_bmad/warhammer-40k/agents/chronicler-sidecar/battles.md`

### 3. Present Campaign Options

**NARRATIVE CAMPAIGN WORKFLOW**

*In the grim darkness of the far future, there is only war...*

**What would you like to do?**

1. **[NC] New Campaign** - Create a fresh narrative campaign
2. **[RC] Resume Campaign** - Continue an existing campaign
3. **[RB] Record Battle** - Log a battle result
4. **[GM] Generate Mission** - Create a narrative mission
5. **[TP] Track Progression** - Update army Crusade cards

*Select an option to begin...*

---

## STEP 1: CAMPAIGN CREATION [NC]

### 1.1 Campaign Framework

**Campaign Type Selection:**

1. **[CR] Crusade** - Official 10th Edition Crusade rules
2. **[TC] Tree Campaign** - Branching narrative with set paths
3. **[MC] Map Campaign** - Territory control across locations
4. **[CC] Custom Campaign** - Freeform narrative

### 1.2 Campaign Details

Gather from user:

- **Campaign Name:** [Evocative title]
- **Setting:** [Planet/sector/system]
- **Timeframe:** [M41/M42, specific events]
- **Central Conflict:** [What are forces fighting over?]
- **Estimated Length:** [Number of battles planned]

### 1.3 Participating Forces

For each player:
- **Player Name:**
- **Faction:**
- **Army Name:** [Custom force name]
- **Starting Supply Limit:** [Crusade PL or points]
- **Starting Requisition:** [Per Crusade rules]
- **Narrative Hook:** [Why is this force here?]

### 1.4 Narrative Framework

Create story elements:

**The Stakes:**
[What happens if each side wins?]

**Key Locations:**
1. [Location 1] - [Significance]
2. [Location 2] - [Significance]
3. [Location 3] - [Significance]

**Narrative Threads:**
1. [Thread 1] - Potential plot developments
2. [Thread 2] - Character arcs
3. [Thread 3] - Mysteries to explore

**Campaign Victory Conditions:**
[How is the campaign won?]

### 1.5 Save Campaign

Save to `{project-root}/_bmad/warhammer-40k/agents/chronicler-sidecar/campaigns.md`:

```markdown
# Campaign: {Name}

## Overview
- **Status:** Active
- **Started:** {Date}
- **Setting:** {Location}
- **Type:** {Crusade/Tree/Map/Custom}

## Participants
### {Player 1}
- **Army:** {Name}
- **Faction:** {Faction}
- **Supply Limit:** {PL}
- **Requisition:** {RP}
- **Narrative:** {Hook}

### {Player 2}
...

## Narrative Framework
### Stakes
{Description}

### Key Locations
1. {Location}: {Significance}

### Story Threads
1. {Thread}: {Status}

## Battle History
(Battles will be logged here)

## Current State
{Summary of campaign situation}
```

---

## STEP 2: MISSION GENERATION [GM]

### 2.1 Mission Context

Ask user:
- Which campaign is this for?
- What was the outcome of the previous battle?
- Any specific narrative beats to include?

### 2.2 Generate Mission

Based on campaign state, create:

**MISSION: {Evocative Name}**

**Narrative Setup:**
*{2-3 paragraphs setting the scene, referencing past events}*

**The Battlefield:**
- **Location:** {Where this takes place}
- **Environment:** {Terrain features, weather, hazards}
- **Deployment:** {Zones and special deployment rules}

**Primary Objectives:**
1. {Objective 1} - {VP value}
2. {Objective 2} - {VP value}
3. {Objective 3} - {VP value}

**Secondary Objectives:**
- {Standard secondaries or custom}

**Narrative Objectives:** (No VP, story rewards)
- {Narrative goal 1}: If achieved, {consequence}
- {Narrative goal 2}: If achieved, {consequence}

**Special Rules:**
1. {Rule 1}: {Effect}
2. {Rule 2}: {Effect}

**Twists:** (Optional dramatic moments)
- End of Round 2: {Event}
- If {condition}: {Event}

**Aftermath:**
- **If Attacker Wins:** {Narrative consequence}
- **If Defender Wins:** {Narrative consequence}
- **If Draw:** {Narrative consequence}

---

## STEP 3: BATTLE RECORDING [RB]

### 3.1 Battle Details

Gather:
- **Campaign:** {Which campaign}
- **Battle Number:** {Sequence}
- **Mission:** {Mission name}
- **Date Played:** {Real-world date}

### 3.2 Participants & Outcome

- **Player 1:** {Name} playing {Army} at {PL/Points}
- **Player 2:** {Name} playing {Army} at {PL/Points}
- **Victor:** {Winner}
- **Score:** {Final score}
- **Margin:** {Close/Decisive/Crushing}

### 3.3 Battle Honors & Casualties

For each player:

**{Player} Results:**
- **Marked for Greatness:** {Unit}
- **Experience Gained:** {XP per unit}
- **Battle Honors Earned:** {New honors}
- **Casualties:**
  - {Unit}: {Destroyed/Out of Action}
  - Battle Scars: {Any scars gained}
- **Requisition Earned:** {RP}

### 3.4 Narrative Summary

Write battle report:

*{1-2 paragraphs describing key moments}*

**Turning Point:**
{The decisive moment}

**Heroes:**
{Units/characters who distinguished themselves}

**Fallen:**
{Notable casualties and their last stands}

### 3.5 Save Battle

Append to `{project-root}/_bmad/warhammer-40k/agents/chronicler-sidecar/battles.md`:

```markdown
## Battle {N}: {Title}
**Campaign:** {Name}
**Date:** {Date}
**Mission:** {Mission}

### Forces
- **{Player 1}:** {Army} ({PL})
- **{Player 2}:** {Army} ({PL})

### Result
- **Victor:** {Winner}
- **Score:** {Score}
- **Margin:** {Margin}

### Honors & Casualties
(Details)

### Narrative
{Battle report}

### Campaign Impact
{How this changes the story}
```

Update campaign state in campaigns.md.

---

## STEP 4: PROGRESSION TRACKING [TP]

### 4.1 Select Army

Which army to update:
- Load from campaign participants

### 4.2 Crusade Card Updates

For each unit that gained XP:

**{Unit Name}**
- **Current XP:** {Total}
- **Rank:** {Raw/Blooded/Battle-hardened/Heroic/Legendary}
- **Battle Honors:**
  - {Honor 1}
  - {Honor 2}
- **Battle Scars:**
  - {Scar 1}
- **Crusade Points:** {Total}
- **Equipment:** {Relics/upgrades}

### 4.3 Requisition Spending

Available RP: {Total}

**Options:**
1. **Increase Supply Limit** (1 RP) - Add 5 PL
2. **Fresh Recruits** (1 RP) - Replace destroyed unit
3. **Rearm and Resupply** (1 RP) - Remove Battle Scar
4. **Repair and Recuperate** (1 RP) - Return Out of Action unit
5. **Relic** (1 RP) - Give unit a Crusade Relic
6. **Specialist Reinforcements** (1 RP) - Add unit with XP

### 4.4 Save Progression

Update campaign file with new army state.

---

## CROSS-AGENT INTEGRATION

### With Tacticus
- Import army lists for campaigns
- Validate list changes after progression

### With Lorekeeper
- Enrich narrative with faction lore
- Research historical parallels for story beats

### With Brushmaster
- Track which units are painted
- Bonus narrative rewards for fully painted armies

### With Artisan
- Conversion ideas for veteran units
- Trophy/honor modifications for heroes

---

## MENU (Available Throughout)

- **[ST] Status** - Show campaign overview
- **[BL] Battle Log** - Review past battles
- **[AR] Army Roster** - View Crusade cards
- **[NR] Narrative Recap** - Story so far summary
- **[GM] Generate Mission** - Create next battle
- **[SAVE]** - Save all progress
- **[EXIT]** - Exit workflow (progress auto-saved)

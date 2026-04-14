---
name: warhammer-40k-build-army-list
description: Guided workflow to build tournament-legal Warhammer 40K army lists. Use when the user says "build me a list", "create an army list", or Tacticus triggers the build workflow.
---

# Build Army List Workflow

Build competitive, tournament-legal Warhammer 40K army lists with mandatory validation gates. This workflow is used by the Tacticus agent and enforces deterministic data queries at every step.

## Prerequisites

These skills MUST be available and used throughout:
- `warhammer-40k-army-data` — for all unit/points/faction data
- `warhammer-40k-validate-list` — for validation gates before output
- `warhammer-40k-paint-data` — if paint scheme sections are included

## Step 1: Gather Requirements

Ask the user:
1. **Faction:** Which army?
2. **Points Level:** 500 / 1000 / 2000 / Custom?
3. **Detachment:** Which detachment rules?
4. **Playstyle:** Competitive meta / Casual / Narrative / Specific theme?
5. **Constraints:** Must-have units, budget limits, models already owned?

Confirm all inputs before proceeding.

## Step 2: Load Faction Data

**DETERMINISTIC — no memory allowed.**

1. Use `warhammer-40k-army-data` to read `_bmad/_config/custom/warhammer-40k/data/datasheets/{faction}.compact.json`
2. If cheatsheet exists: read `army-lists/{faction}/*.cheatsheet.json` for reference lists
3. Read `_bmad-output/warhammer-40k/agents/tacticus-sidecar/validation-rules.yaml` for detachment rules and hard rules
4. Check `_bmad-output/warhammer-40k/shared/hallucination-registry.yaml` for faction-specific patterns

If any data file is missing, inform the user and offer to web search for current data.

## Step 3: Build 2000pt List First

**MANDATORY ORDER: Always build 2000pt first, then scale down.**

1. Select units from datasheet data — cite points from the file
2. Show math for every selection: `"X models x Ypts = Zpts [Source: {faction}.compact.json]"`
3. Assign leaders to bodyguard units — verify `leads` array in datasheet
4. Assign enhancements — verify eligibility (no Epic Heroes, check detachment rules)
5. Running total after each unit added

## Step 4: Run Validation Gates

**USE `warhammer-40k-validate-list` skill — do NOT validate from memory.**

Run all 7 gates. If any fail, fix before proceeding:
1. Points Total (hard cap)
2. Rule of Three
3. Epic Hero Uniqueness
4. Enhancement Eligibility
5. Unit Sizes
6. Leader Attachments
7. Faction Abilities warnings

## Step 5: Scale Down

Create 1000pt and 500pt variants by removing units proportionally:
- 1000pt: remove ~half the army, keep core synergies
- 500pt: keep only essential units, max 1 enhancement
- Re-run validation gates for each size

## Step 6: Model Assembly Guide

**MANDATORY — every list must include this.**

For each points level, create:

| Model | Qty | Loadout | Notes |
|-------|-----|---------|-------|
| [exact model] | [count] | [exact weapon names from datasheet] | [build notes] |

Then add:
- **Shopping List Summary** with GW product names (verify via web search, mark [UNVERIFIED] if from memory)
- **Total Model Count** per points level
- **Magnetization Recommendations** for multi-loadout units

## Step 7: Save

Save the completed list to `_bmad-output/warhammer-40k/agents/tacticus-sidecar/lists.md` and offer to create a cheatsheet JSON.

## Anti-Hallucination Checkpoints

At each step, verify:
- [ ] All points come from datasheet files, not memory
- [ ] All wargear exists in the unit's datasheet weapons array
- [ ] No Epic Heroes have enhancements
- [ ] Leader attachments verified against `leads` array
- [ ] Math shown and verified by re-adding
- [ ] Sources cited for every factual claim

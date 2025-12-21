---
name: Build Army List
description: Build tournament-legal Warhammer 40k army lists with validation gates
agent: tacticus
---

# Build Army List Workflow

**Purpose:** Build competitive, tournament-legal Warhammer 40k army lists with mandatory validation gates to prevent Rule of Three violations and other legality issues.

---

## Step 1: Load Rules Knowledge Base

**CRITICAL FIRST STEP - DO NOT SKIP**

<step id="load-rules-kb">

**Action:**
- Read `{project-root}/_bmad/warhammer-40k/agents/tacticus-sidecar/rules-validated.md`
- Review all verified rules, especially:
  - Rule of Three (max 3 units per datasheet)
  - Faction-specific unit availability
  - Points values
  - Detachment rules
  - Enhancement limits

**Validation:**
- ✅ Rules KB loaded and reviewed
- ✅ Aware of past mistakes to avoid

**Output:**
Confirm: "Rules KB loaded. Ready to build legal lists."

</step>

---

## Step 2: Gather Requirements

<step id="gather-requirements">

**Ask the user:**

1. **Faction:** Which army are you building?
2. **Points Level:** 500 / 1000 / 2000 / Custom?
3. **Detachment:** Which detachment rules?
4. **Playstyle:** Competitive meta / Casual / Narrative / Specific theme?
5. **Constraints:** Any must-have units or restrictions?

**Validation:**
- ✅ All requirements gathered
- ✅ User confirmed inputs

**Output:**
Summary of requirements for user confirmation.

</step>

---

## Step 3: Pre-Build Validation Planning

<step id="pre-build-validation">

**BEFORE drafting the list, calculate legal constraints:**

1. **Rule of Three Check:**
   - Identify which units will be used
   - Calculate maximum legal count per datasheet (max 3 units)
   - Document any Battleline exceptions

2. **Points Budget:**
   - Total points available
   - Mandatory units (HQ, etc.)
   - Remaining points for flex units

3. **Detachment Compliance:**
   - Enhancement limits (usually max 2, max 1 per character)
   - Required unit types
   - Epic Hero limits (1 per named character)

**Validation Checklist:**
- [ ] Rule of Three constraints documented
- [ ] Points budget calculated
- [ ] Detachment rules reviewed
- [ ] Epic Hero limits noted

**Output:**
"Legal constraints calculated. Maximum [X] units of [datasheet]. [Y] points remaining after mandatory units."

</step>

---

## Step 4: Draft Army List

<step id="draft-list">

**Build the army list within validated constraints:**

1. **Start with core units** (HQ, Troops/Battleline)
2. **Add synergy units** (support, buffs, combos)
3. **Fill remaining points** (flex slots, screening, fire support)

**As you build, actively track:**
- Unit count by datasheet name (ensure ≤3 for non-Battleline)
- Running points total
- Enhancement allocation (max 1 per character)

**Format:**
```
| Unit | Models | Role | Points |
|------|--------|------|--------|
| [Name] | [Count] | [Battlefield role] | [Cost] |
```

**Validation:**
- ✅ No datasheet appears >3 times (except Battleline/Transports)
- ✅ Points total matches target ±10pts
- ✅ All enhancements legal (max 1 per character)
- ✅ All Epic Heroes unique (max 1 each)

**Output:**
Complete army list with unit breakdown and points total.

</step>

---

## Step 5: Legal Compliance Validation

<step id="validate-legality">

**MANDATORY VALIDATION GATE - DO NOT SKIP**

**Run through the validation checklist:**

1. **Rule of Three:**
   - Count units by exact datasheet name
   - Verify ≤3 units per datasheet (except Battleline/Transports)
   - ❌ FAIL if any datasheet appears >3 times

2. **Points Total:**
   - Verify exact points match target
   - Account for all wargear, enhancements, upgrades

3. **Detachment Rules:**
   - Verify all units legal for chosen detachment
   - Check enhancement limits and eligibility

4. **Epic Heroes:**
   - Verify only 1 of each named character

5. **Wargear Legality:**
   - Cross-check against Wahapedia datasheets
   - Verify all loadouts are legal per unit

**CRITICAL:**
If ANY validation fails, return to Step 4 and rebuild.

**Output:**
"✅ LIST VALIDATED - Tournament legal" OR "❌ VALIDATION FAILED - [specific issue]"

</step>

---

## Step 6: Tactical Analysis

<step id="tactical-analysis">

**Analyze the validated list:**

1. **Strengths:** What does this list do well?
2. **Weaknesses:** What are the vulnerabilities?
3. **Deployment Strategy:** How to deploy for maximum effect?
4. **Win Conditions:** How does this list win games?
5. **Matchup Analysis:** Good/bad matchups vs common armies

**Output:**
Tactical breakdown with deployment guide and win conditions.

</step>

---

## Step 7: Save to Database

<step id="save-list">

**If user approves the list:**

1. **Save to lists.md:**
   - Add to `{project-root}/_bmad/warhammer-40k/agents/tacticus-sidecar/lists.md`
   - Include: faction, points, date, strategy notes

2. **Update memories.md:**
   - Document any new preferences learned
   - Add to user's playstyle patterns

**Validation:**
- ✅ List saved to database
- ✅ Memories updated

**Output:**
"Army list '[Name]' saved to database. Total lists: [count]"

</step>

---

## Step 8: Self-Correction (If Errors Found)

<step id="self-correction">

**If user corrects a mistake during this workflow:**

1. **Update rules-validated.md:**
   - Add ❌ ERROR entry documenting what went wrong
   - Add ✅ CORRECTED entry with the fix
   - Update validation checklist if needed

2. **Document lesson learned:**
   - What assumption was wrong?
   - How to prevent this in the future?

**Output:**
"Rules KB updated with correction. This mistake won't happen again."

</step>

---

## Success Criteria

**Workflow complete when:**
- ✅ List is tournament-legal (all validation gates passed)
- ✅ User approved the list
- ✅ List saved to database
- ✅ Tactical analysis provided

**Failure modes:**
- ❌ Validation gate failed → Return to Step 4
- ❌ User rejected list → Return to Step 4 with feedback
- ❌ Rule violation discovered → Update rules KB, return to Step 3

---

## Notes

**Why this workflow exists:**
- Prevents Rule of Three violations by validating BEFORE finalizing
- Ensures tournament legality through mandatory validation gates
- Documents mistakes in rules KB for future prevention
- Provides consistent, repeatable list-building process

**When to use:**
- Building new army lists from scratch
- Scaling existing lists up/down (500pt → 1000pt → 2000pt)
- Converting narrative lists to matched play

**When NOT to use:**
- Quick validation of existing list (use 'analyze-list' prompt instead)
- Unit lookup (use 'unit-search' prompt instead)

---

*Version: 1.0*
*Last Updated: 2025-12-21*
*Maintained by: Tacticus Agent*

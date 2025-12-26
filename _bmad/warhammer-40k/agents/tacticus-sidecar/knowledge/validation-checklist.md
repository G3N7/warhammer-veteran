# Tacticus Validation Checklist

**Purpose:** Mandatory validation gates that MUST pass before presenting any army list to user.
**Philosophy:** Legal first, optimized second. Show work. Verify twice.

---

## GATE 1: PRE-BUILD VALIDATION (BLOCKING)

**STOP. Do not build ANY list until ALL checks pass:**

### 1.1 Edition Verification
- [ ] Confirmed game system edition (40k = 10th, AoS = 4th)
- [ ] All data sources tagged with current edition
- [ ] No outdated cache entries being used

### 1.2 Faction Data Loaded
- [ ] Loaded `processed/{faction-id}/datasheets.json`
- [ ] Loaded `processed/{faction-id}/rules.json`
- [ ] Loaded `processed/{faction-id}/stratagems.json`
- [ ] Cross-referenced `rules-validated.md` for known corrections

### 1.3 Detachment Rules Loaded
- [ ] Detachment ability documented
- [ ] ALL enhancements listed with costs
- [ ] Enhancement restrictions noted (1 per character, eligible keywords)

### 1.4 Points Limit Acknowledged
- [ ] Target points confirmed: _____ pts
- [ ] HARD CAP understood (not "approximately")
- [ ] Under is legal, over is ILLEGAL

---

## GATE 2: UNIT SELECTION VALIDATION (PER UNIT)

**For EACH unit added to list:**

### 2.1 Datasheet Verification
- [ ] Unit exists in faction datasheets.json
- [ ] Unit role confirmed (HQ/Troops/Elites/etc.)
- [ ] Points cost verified from CSV (not memory)

### 2.2 Composition Check
- [ ] Unit size is legal (check min/max from datasheet)
- [ ] Pack Leader/Sergeant/Champion accounted for (if applicable)
- [ ] Heavy weapon limits respected (X per Y models)

### 2.3 Wargear Verification
- [ ] Each model's wargear exists in datasheet options
- [ ] Pack Leader wargear is Pack Leader-legal
- [ ] Regular model wargear is regular-model-legal
- [ ] No 9th edition wargear on 10th edition datasheets

---

## GATE 3: ARMY COMPOSITION VALIDATION (BLOCKING)

**After selecting all units, BEFORE calculating points:**

### 3.1 Rule of Three Check
```
DATASHEET COUNT TABLE (fill in):
| Datasheet Name | Count | Legal? |
|----------------|-------|--------|
| [unit 1]       | X     | ≤3? ✓/✗ |
| [unit 2]       | X     | ≤3? ✓/✗ |
...
```
- [ ] No non-Battleline/Transport datasheet appears >3 times
- [ ] If violation found: STOP and reduce before proceeding

### 3.2 Epic Hero Check
- [ ] Each named character appears at most ONCE
- [ ] List all Epic Heroes: ________________

### 3.3 Enhancement Check
- [ ] Max 1 enhancement per character
- [ ] Enhancement keywords match character keywords
- [ ] Total enhancement count ≤ army limit

### 3.4 Leader Attachment Check
- [ ] Each leader can legally join their assigned unit
- [ ] Leader keywords match unit keywords
- [ ] No unit has multiple leaders (unless rules allow)

---

## GATE 4: POINTS CALCULATION (SHOW ALL WORK)

**MANDATORY: Display calculation for EVERY unit**

### 4.1 Points Calculation Table
```
POINTS BREAKDOWN (fill in for EVERY unit):
| Unit | Models | PPM | Subtotal | Wargear | Unit Total |
|------|--------|-----|----------|---------|------------|
| [1]  | X      | Xpt | X × X    | +0      | XXX pts    |
| [2]  | X      | Xpt | X × X    | +0      | XXX pts    |
...
| SUBTOTAL UNITS: | | | | | XXXX pts |
```

### 4.2 Enhancement Points
```
| Enhancement | Cost | Character |
|-------------|------|-----------|
| [name]      | Xpt  | [who]     |
...
| SUBTOTAL ENHANCEMENTS: | XXX pts |
```

### 4.3 Total Verification
```
VERIFICATION:
- Unit subtotal:        XXXX pts
- Enhancement subtotal: XXX pts
- GRAND TOTAL:          XXXX pts
- Points limit:         XXXX pts
- Remaining:            XXX pts
- LEGAL? [YES/NO]
```

### 4.4 Re-Add Verification
**Add units again from scratch to verify:**
```
VERIFICATION RE-COUNT:
Unit 1: ___ + Unit 2: ___ + Unit 3: ___ + ... = ____
Enhancements: ___ + ___ = ___
TOTAL: ____

MATCHES ORIGINAL? [YES/NO]
```

---

## GATE 5: SELF-REVIEW (ADVERSARIAL)

**MANDATORY: Find potential issues with your own list**

### 5.1 Common Mistake Patterns
Check against known error patterns from `rules-validated.md`:

- [ ] **Wargear edition error:** Am I using wargear that was removed in 10th edition?
- [ ] **Pack Leader omission:** Did I forget to specify Pack Leader loadout?
- [ ] **Points overage:** Am I over the limit by even 1 point?
- [ ] **Rule of Three:** Did I count correctly?
- [ ] **Enhancement stacking:** Did I give same character multiple enhancements?

### 5.2 Find 3 Potential Issues
**List AT LEAST 3 things that could be wrong:**
1. ________________________________
2. ________________________________
3. ________________________________

**For each issue identified:**
- Verify if actually a problem
- If yes: FIX before presenting to user
- If no: Document why it's actually fine

### 5.3 Cross-Reference Mistake Log
Check `rules-validated.md` Mistake Log section:
- [ ] Reviewed all past mistakes
- [ ] Verified none of those patterns appear in current list

---

## GATE 6: KEYWORD ACCURACY CHECK (NEW - v2.0)

**Purpose:** Verify faction-specific keywords are correctly applied to units.

### 6.1 SYNAPSE Keyword Check (Tyranids)
**CRITICAL:** Only specific units have the SYNAPSE keyword. Most monsters do NOT.
```
SYNAPSE VERIFICATION:
| Unit | Has SYNAPSE? | Source |
|------|--------------|--------|
| Hive Tyrant | ✅ YES | Datasheet |
| Winged Hive Tyrant | ✅ YES | Datasheet |
| Exocrine | ❌ NO | Datasheet - must stay in Synapse aura |
| Tyrannofex | ❌ NO | Datasheet - must stay in Synapse aura |
| Carnifex | ❌ NO | Datasheet - must stay in Synapse aura |
| Barbgaunts | ❌ NO | Datasheet - benefits from Synapse |
```
- [ ] All units marked with correct SYNAPSE status
- [ ] Tactics mention Synapse bubble positioning for non-SYNAPSE units

### 6.2 Other Critical Keywords
- [ ] BATTLELINE units correctly identified
- [ ] LEADER units can actually lead their attached unit
- [ ] DEEP STRIKE units correctly identified
- [ ] TRANSPORT capacity correctly stated

---

## GATE 7: FULL STAT VALIDATION (REVISED - v2.1)

**Purpose:** Verify ALL unit stats match datasheets, not just movement.

### 7.1 Complete Stat Verification Table
**For EVERY unit in the list, verify ALL stats:**
```
FULL STAT VERIFICATION:
| Unit | M | T | Sv | W | Ld | OC | Invuln | Source | Verified? |
|------|---|---|----|----|----|----|--------|--------|-----------|
| [unit] | X" | X | X+ | X | X+ | X | X+/- | Wahapedia | ✓/✗ |
```
- [ ] ALL stat values verified against datasheet
- [ ] Movement (M) matches datasheet exactly
- [ ] Toughness (T) matches datasheet exactly
- [ ] Save (Sv) matches datasheet exactly
- [ ] Wounds (W) matches datasheet exactly
- [ ] Leadership (Ld) matches datasheet exactly
- [ ] Objective Control (OC) matches datasheet exactly
- [ ] Invulnerable save noted if applicable (or "-" if none)

### 7.2 Stat Verification Process
1. Load unit datasheet from processed/{faction}/datasheets.json
2. If stat not in local data, fetch from Wahapedia
3. Cross-reference every stat mentioned in prose against table
4. Flag any mismatches immediately

### 7.3 Ability Claims Consistency
**Verify abilities mentioned in Strengths/Tactics exist:**
- [ ] "Deep Strike available" → Unit actually has Deep Strike keyword
- [ ] "Can take enhancement X" → Character is eligible
- [ ] Aura ranges match actual ability text

### 7.4 Strengths vs Weaknesses Coherence
**Check for contradictions:**
- [ ] If Strength says "fast screening" → Weakness shouldn't say "slow army"
- [ ] If Weakness says "no Deep Strike" → Verify unit actually lacks it
- [ ] Movement weaknesses clarify WHICH units are slow

---

## GATE 8: SECTION CROSS-REFERENCE (NEW - v2.0)

**Purpose:** Verify all document sections reference the same army composition.

### 8.1 Table vs Prose Unit Count
```
UNIT COUNT VERIFICATION:
| Section | Unit Count | Units Listed |
|---------|------------|--------------|
| Army Table | X models | [list] |
| Strengths | mentions X | [check each] |
| Weaknesses | mentions X | [check each] |
| Tactics | mentions X | [check each] |
| Model Breakdown | X models | [list] |
```
- [ ] All sections reference same unit list
- [ ] No "phantom units" mentioned in prose but not in table
- [ ] No units in table missing from tactics section

### 8.2 Points Totals Match
- [ ] Table total matches stated total in prose
- [ ] "Model count" in prose matches actual table count
- [ ] Wound totals calculated correctly (Models × Wounds per model)

### 8.3 Tactics Reference Correct Units
For each tactic mentioned:
- [ ] Unit referenced exists in army list table
- [ ] Ability referenced exists on that unit's datasheet
- [ ] Synergy partners both exist in the list

---

## GATE 9: FINAL PRESENTATION

**Only after ALL 8 gates pass:**

### 9.1 Present List with Confidence Indicators
```
VALIDATION STATUS:
✅ Edition verified: 10th Edition
✅ Rule of Three: PASS (max X of any datasheet)
✅ Points: XXXX/XXXX (X pts remaining)
✅ Epic Heroes: X unique characters
✅ Enhancements: X/X (legal allocation)
✅ Self-review: X issues checked, 0 found
✅ Keywords: All faction keywords verified
✅ Consistency: Prose matches tables
✅ Cross-reference: All sections aligned
```

### 9.2 Cite Data Sources
- Points source: Wahapedia CSV (last updated: DATE)
- Wargear source: processed/{faction}/datasheets.json
- Corrections applied: rules-validated.md (if any)

---

## QUICK REFERENCE: CRITICAL MATH ERRORS TO AVOID

### Points Per Model (PPM) Gotchas
- Wolf Guard Terminators: **34pts** (not 38, not 40)
- Always multiply: Models × PPM = Unit cost
- Wargear is usually INCLUDED (no add-ons for most 10th ed units)

### Unit Size Gotchas
- Some units: 5 OR 10 only (not 6, 7, 8, 9)
- Check datasheet for exact legal sizes
- "5-10 models" means 5, 6, 7, 8, 9, OR 10

### Enhancement Gotchas
- Cost is FLAT (not per model)
- Only eligible characters can take them
- 1 per character MAXIMUM

---

## VALIDATION FAILURE PROTOCOL

**If ANY gate fails:**

1. **STOP** - Do not present incomplete/illegal list
2. **IDENTIFY** - Which specific check failed
3. **FIX** - Modify list to pass validation
4. **RE-RUN** - Start from Gate 1 again
5. **DOCUMENT** - If new error pattern, add to rules-validated.md

**Never present a list that failed validation with "close enough" disclaimer.**

---

*Version: 1.0*
*Created: 2025-12-24*
*Maintained by: Tacticus Agent*

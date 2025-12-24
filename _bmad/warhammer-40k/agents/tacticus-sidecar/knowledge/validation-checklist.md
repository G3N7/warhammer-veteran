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

## GATE 6: FINAL PRESENTATION

**Only after ALL gates pass:**

### 6.1 Present List with Confidence Indicators
```
VALIDATION STATUS:
✅ Edition verified: 10th Edition
✅ Rule of Three: PASS (max X of any datasheet)
✅ Points: XXXX/XXXX (X pts remaining)
✅ Epic Heroes: X unique characters
✅ Enhancements: X/X (legal allocation)
✅ Self-review: X issues checked, 0 found
```

### 6.2 Cite Data Sources
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

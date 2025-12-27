# Tacticus - Validated Warhammer 40k Rules Knowledge Base

**Purpose:** Persistent, self-correcting rules knowledge that prevents repeated mistakes across sessions.

**Update Protocol:**
- ✅ Add new verified rules with source + date
- ❌ Document mistakes and user corrections
- 🔄 Update when rules change (new edition, FAQ, errata)

---

## CRITICAL: Current Edition Enforcement

**WARHAMMER 40,000: 10TH EDITION (CURRENT)**
**Last Verified:** 2025-12-24
**Source:** [Goonhammer 10th Edition Hub](https://www.goonhammer.com/warhammer-40k-10th-edition/)

**EDITION VALIDATION PROTOCOL:**
- ✅ ALL datasheets MUST be marked "10TH EDITION - VERIFIED [DATE]"
- ✅ ALL WebFetch/WebSearch queries MUST include "10th edition"
- ✅ ALL cached rules MUST verify edition tag before use
- ❌ REJECT any cache entries from 9th/8th/7th editions without re-verification
- 🔄 If cache missing edition tag, mark as OUTDATED and re-fetch

**WHY THIS MATTERS:**
- **Edition changes remove/add wargear:** 10th Ed Wolf Guard Terminators lost thunder hammers/chainfists
- **Edition changes stats:** Weapon profiles change between editions
- **Edition changes unit composition:** Rules for Pack Leaders, Sergeants, etc. vary
- **Points values change:** MFM updates quarterly, but edition changes are major

**PREVENTION CHECKLIST:**
1. Before using cached datasheet: Verify edition tag present and correct
2. Before WebFetch/WebSearch: Include "10th edition" in query
3. After fetching new data: Tag with "10TH EDITION - VERIFIED [DATE]"
4. When edition changes (e.g., 11th Ed in 2026): Mark ALL cache as 🔄 OUTDATED

**AGE OF SIGMAR: 4TH EDITION (CURRENT)**
**Last Verified:** 2025-12-24
**Source:** [Goonhammer AoS 4th Edition](https://www.goonhammer.com/age-of-sigmar-new-edition-4th-explained/)

---

## Core Matched Play Rules

### Rule of Three ✅ VERIFIED
**Source:** Warhammer 40k 10th Edition Matched Play Rules
**Last Verified:** 2025-12-21
**Verification Method:** Wahapedia cross-reference + user correction

**THE RULE:**
Maximum 3 units with the same datasheet in matched play armies (except Battleline and Dedicated Transports).

**Validation History:**
- ❌ **2025-12-21 ERROR:** Built 2000pt list with 6x Wolf Guard Terminators units (VIOLATION)
  - **What went wrong:** Built 40-Terminator concept without validating unit count limits
  - **User correction:** "you can't have more than 3 of a given unit type"
  - **Lesson learned:** ALWAYS check Rule of Three BEFORE building lists, not after

- ✅ **2025-12-21 CORRECTED:** Verified via Wahapedia - max 3 units per datasheet applies to ALL non-Battleline/Transport units

**Application to Space Wolves:**
- Wolf Guard Terminators: MAX 3 units per army
- Legal configurations:
  - 3x 10-man = 30 Terminators (1,020pts)
  - 3x 5-man = 15 Terminators (510pts)
  - 2x 10-man + 1x 5-man = 25 Terminators (850pts)
  - 1x 10-man + 2x 5-man = 20 Terminators (680pts)

**CRITICAL VALIDATION STEP:**
Before building ANY list, count units by datasheet name and verify ≤ 3 units.

---

### Space Wolves Terminator Datasheet Availability ✅ VERIFIED
**Source:** Wahapedia Space Wolves faction page
**Last Verified:** 2025-12-21
**Verification Method:** Direct Wahapedia search + WebFetch validation

**AVAILABLE TO SPACE WOLVES:**
- ✅ **Wolf Guard Terminators** (Space Wolves-specific datasheet)

**NOT AVAILABLE TO SPACE WOLVES:**
- ❌ **Terminator Squad** (generic Space Marines only)
- ❌ **Terminator Assault Squad** (generic Space Marines only)
- ❌ **Deathwing Terminators** (Dark Angels only)
- ❌ **Deathwatch Terminators** (Deathwatch only)

**Validation History:**
- ❌ **2025-12-21 ASSUMPTION:** Thought there might be workarounds by using different Terminator datasheets
- ✅ **2025-12-21 VERIFIED:** Space Wolves have ONLY "Wolf Guard Terminators" - no mixing allowed

**Rule of Three Impact:**
- Only ONE Terminator datasheet available
- No loophole to exceed 30 Terminators by mixing types
- Hard cap: 30 Terminators maximum in any Space Wolves matched play army

---

### Wolf Guard Terminators Points Values ✅ VERIFIED
**Source:** Munitorum Field Manual December 2025
**Last Verified:** 2025-12-21

**POINTS:**
- 34pts per model (regardless of wargear)
- 5-man squad: 170pts
- 10-man squad: 340pts

**Unit Size Options:**
- Legal: 5 models OR 10 models
- Illegal: Any other size (6, 7, 8, 9, etc.)

---

### Wolf Guard Terminators Wargear Rules ✅ VERIFIED (10TH EDITION)
**Source:** Wolf Guard Terminators Datasheet (Wahapedia) + WebFetch validation
**Last Verified:** 2025-12-24
**Verification Method:** WebFetch + User correction + Mistake log

**WARGEAR STRUCTURE (10TH EDITION - CRITICAL CHANGES):**
- **Default:** Storm bolter + master-crafted power weapon (S5, AP-2, D2)
- **Pack Leader (1 per unit - REQUIRED):** Can replace BOTH weapons with twin lightning claws OR relic greataxe (both melee only)
- **Heavy Weapons (1 per 5 models):** Can replace BOTH weapons with assault cannon + power fist OR cyclone missile launcher + power fist
- **Regular Models:** Can replace storm bolter with storm shield (4++ invuln, lose shooting). KEEP master-crafted power weapon.

**❌ REMOVED IN 10TH EDITION (CRITICAL):**
- Thunder hammers NOT available to regular models
- Chainfists NOT available to regular models
- Power fists NOT available to regular models (only heavy weapon models get them)

**LEGAL 10-MAN SQUAD EXAMPLE:**
- 1x Pack Leader: Twin lightning claws (melee only, no ranged)
- 2x Heavy weapon models: Assault cannon + power fist
- 7x Regular Terminators: Storm shield + master-crafted power weapon (S5 AP-2 D2)

**CRITICAL RULES:**
- Twin lightning claws = **PACK LEADER ONLY** (1 per unit maximum)
- Regular models CANNOT take thunder hammers/chainfists/power fists in 10th Edition
- Master-crafted power weapon is S5 (weaker than old editions) but Lethal Hits compensates

**VALIDATION HISTORY:**
- ❌ **2025-12-23 ERROR:** Built army list using thunder hammers on regular Terminators (ILLEGAL in 10th Ed)
  - **What went wrong:** Used outdated wargear from previous edition/kit
  - **User correction:** Questioned if S5 power weapons were competitive, discovered 10th Ed removed thunder hammers
  - **Lesson learned:** ALWAYS verify datasheet wargear matches current edition, especially after kit/rules updates

**Validation History:**
- ❌ **2025-12-22 ERROR:** Stated any model could take twin lightning claws
  - **User correction:** "twin claw is only able to be equiped by the pack leader and the pack leader is only 1 per unit/squad"
  - **What went wrong:** Did not verify Pack Leader restriction on datasheet
  - **Lesson learned:** Always check model type restrictions (Pack Leader vs regular models)
- ✅ **2025-12-22 CORRECTED:** Twin claws restricted to Pack Leader only (1 per unit)

---

### Enhancement Eligibility ✅ VERIFIED (CRITICAL)
**Source:** Warhammer 40k 10th Edition Core Rules - Matched Play
**Last Verified:** 2025-12-27
**Verification Method:** User correction

**THE RULE:**
**Enhancements can ONLY be given to CHARACTER models that do NOT have the EPIC HERO keyword.**

**EPIC HERO = NO ENHANCEMENTS:**
- ❌ Logan Grimnar (Epic Hero) - CANNOT take enhancements
- ❌ Arjac Rockfist (Epic Hero) - CANNOT take enhancements
- ❌ Bjorn the Fell-Handed (Epic Hero) - CANNOT take enhancements
- ❌ Roboute Guilliman (Epic Hero) - CANNOT take enhancements
- ❌ ANY named character (Epic Hero) - CANNOT take enhancements

**ENHANCEMENT-ELIGIBLE CHARACTERS (Generic):**
- ✅ Wolf Guard Battle Leader (generic) - CAN take enhancements
- ✅ Primaris Captain (generic) - CAN take enhancements
- ✅ Primaris Librarian (generic) - CAN take enhancements
- ✅ Wolf Priest (generic) - CAN take enhancements
- ✅ Any CHARACTER without EPIC HERO keyword - CAN take enhancements

**Validation History:**
- ❌ **2025-12-27 ERROR:** Assigned enhancements to Logan Grimnar and Arjac Rockfist
  - **What went wrong:** Did not know Epic Heroes cannot take Enhancements
  - **User correction:** "named characters are allowed to have enhancements, they cannot"
  - **Lesson learned:** Epic Hero keyword = NO enhancements, ever

**Prevention:** Before assigning ANY enhancement, check if target has EPIC HERO keyword. If yes, STOP.

---

### Saga of the Beastslayer Detachment ✅ VERIFIED
**Source:** Wahapedia Space Wolves Detachment Rules
**Last Verified:** 2025-12-21

**DETACHMENT ABILITY:**
Units from this detachment gain **Lethal Hits** when targeting:
- Characters
- Monsters
- Vehicles

**ENHANCEMENTS (Max 1 per Character, NOT Epic Heroes):**
- **Blade of the Slayer** (25pts): Precision + enhanced damage vs big targets
- **Hunter's Instincts** (20pts): Re-roll wound rolls vs Characters/Monsters/Vehicles
- **The Pelt of Balewolf** (15pts): Stealth
- **Black Death** (15pts): Devastating Wounds

**LEGAL ENHANCEMENT ALLOCATION:**
- ✅ Wolf Guard Battle Leader gets Blade of Slayer (25pts)
- ✅ Primaris Captain gets Hunter's Instincts (20pts)
- ❌ Logan Grimnar CANNOT take enhancements (Epic Hero)
- ❌ Arjac Rockfist CANNOT take enhancements (Epic Hero)
- ❌ Cannot give both enhancements to same Character
- ❌ Cannot give more than 1 enhancement per Character

---

## Unit-Specific Rules

### Logan Grimnar ✅ VERIFIED
**Source:** Wahapedia Space Marines Epic Heroes
**Points:** 110pts
**Can Lead:** Wolf Guard Terminators (Terminator keyword)
**Epic Hero:** Only 1 per army

---

### Arjac Rockfist ✅ VERIFIED
**Source:** Wahapedia Space Marines Epic Heroes
**Points:** 105pts (Updated Dec 2025 - was 95pts)
**Can Lead:** Wolf Guard Terminators (Terminator keyword)
**Epic Hero:** Only 1 per army

---

### Bjorn the Fell-Handed ✅ VERIFIED
**Source:** Wahapedia Space Marines Epic Heroes
**Points:** 160pts (Updated Dec 2025 - was 170pts)
**Special Ability:** Ancient Tactician - Gain 1CP at start of each Command phase
**Epic Hero:** Only 1 per army

---

### Venerable Dreadnought ✅ VERIFIED
**Source:** Wahapedia Space Marines Units
**Points:** 130pts (Updated Dec 2025 - was 140pts)
**Space Wolves Access:** ✅ Yes (all Space Marines datasheets available)
**Aura:** Fervour of the Ancients - +1 to Advance/Charge rolls for SPACE WOLVES units within 6"
**Critical for:** Making 9" Deep Strike charges easier (becomes 8" with aura)

---

### Fenrisian Wolves ✅ VERIFIED
**Source:** Wahapedia Space Wolves Units
**Points:** 8pts per model
**Unit Sizes:** 5 or 10 models
**Role:** Screening, cheap objective holders
**NOT Battleline:** Subject to Rule of Three (max 3 units)

---

## Validation Checklist (Use BEFORE Building Lists)

**PRE-BUILD VALIDATION:**
- [ ] Count units by datasheet name
- [ ] Verify no datasheet appears >3 times (except Battleline/Transports)
- [ ] Check Epic Heroes (max 1 of each named character)
- [ ] Verify enhancements (max 1 per CHARACTER, NEVER on Epic Heroes)
- [ ] Confirm points total matches mission size (500/1000/2000)
- [ ] Check detachment rules compliance

**POST-BUILD VALIDATION:**
- [ ] Re-count Rule of Three compliance
- [ ] Verify leader attachments are legal (correct keywords)
- [ ] Confirm wargear is legal per datasheet
- [ ] Double-check points math
- [ ] Review for any TO-specific restrictions (if applicable)

---

## Mistake Log & Corrections

### 2025-12-27: Epic Hero Enhancement Error (CRITICAL)
**Mistake:** Assigned Enhancements to Logan Grimnar and Arjac Rockfist in Space Wolves army list
**User Correction:** "named characters are allowed to have enhancements, they cannot"
**Root Cause:**
- Did not have the core Matched Play rule documented: "Epic Heroes CANNOT take Enhancements"
- Validation checklist said "eligible models" but never defined eligibility
- Knowledge base explicitly (and incorrectly) stated Logan and Arjac could take enhancements

**Fix Applied:**
- ✅ Added "Enhancement Eligibility" section to Core Matched Play Rules (line 155)
- ✅ Updated Saga of the Beastslayer examples to show legal allocation (generic characters only)
- ✅ Updated validation checklist: "NEVER on Epic Heroes"
- ✅ Documented mistake in log with prevention steps

**What I Needed to Know Ahead of Time:**
1. The 10th Edition Matched Play rule: "Enhancements can ONLY be given to CHARACTER models that do NOT have the EPIC HERO keyword"
2. How to identify Epic Heroes: Any named/unique character has the EPIC HERO keyword
3. Enhancement eligibility should have been a pre-build validation gate

**Prevention:**
- Before assigning ANY enhancement, explicitly check: Does this CHARACTER have the EPIC HERO keyword?
- If EPIC HERO = YES → CANNOT take enhancements
- If EPIC HERO = NO (generic character) → CAN take enhancements
- Add EPIC HERO check to datasheet loading/verification step

---

### 2025-12-21: Rule of Three Violation
**Mistake:** Built 6x Wolf Guard Terminator units in 2000pt list
**User Correction:** "you can't have more than 3 of a given unit type"
**Root Cause:** Did not validate matched play rules before building concept
**Fix Applied:**
- Added Rule of Three to validated knowledge base
- Added pre-build validation checklist
- Updated critical_actions to load rules KB first

**Prevention:** Always check this KB BEFORE building lists, not after user correction.

### 2025-12-21: Incorrect GW Store URL Year Suffixes
**Mistake:** Generated URLs like `roboute-guilliman-2023` when actual URL is `Roboute-Guilliman-Ultramarines-Primarch-2020`
**User Correction:** "you seem to have gotten a bunch of the urls wrong. You consistantly get the year at the end of the url wrong"
**Root Cause:** Cannot reliably guess URL patterns without fetching actual pages
**Fix Applied:**
- **DO NOT construct direct product URLs manually**
- Use warhammer.com search URLs with pre-filled queries
- Format: `https://www.warhammer.com/en-US/plp?search=Unit%20Name` (URL-encoded spaces as %20)
- Example: `https://www.warhammer.com/en-US/plp?search=Roboute%20Guilliman`

**Prevention:** Always use search URLs with `/plp?search=`, never direct product URLs. User provided correct URL structure.

### 2025-12-24: Wolf Guard Terminators Thunder Hammer Error (10th Edition Wargear Changes)
**Mistake:** Built entire 2000pt army list using thunder hammers + storm shields on regular Wolf Guard Terminators
**User Correction:** "is that different than a thunder hammer" → discovered S5 master-crafted power weapons, questioned competitiveness
**Root Cause:**
- Cached datasheet had outdated wargear options from previous edition
- Did not verify 10th Edition kit/datasheet changes (GW removed thunder hammers from new 2025 kit)
- WebFetch initially failed to extract complete datasheet from Wahapedia (JavaScript-rendered content)

**Fix Applied:**
- ✅ Updated datasheet-cache.md with correct 10th Edition wargear
- ✅ Updated rules-validated.md with mistake log and validation history
- ✅ Added damage calculations showing S5 master-crafted power weapons deal ~20 damage vs T10 (Lethal Hits compensates)
- ✅ Added warning to army list document explaining 10th Ed changes
- ✅ Verified via WebSearch that new 2025 kit contains ZERO thunder hammers

**Key Learning:**
- **10th Edition changed Wolf Guard Terminators significantly:**
  - Regular models: Can ONLY swap storm bolter → storm shield
  - Regular models: CANNOT take thunder hammers/chainfists/power fists (REMOVED)
  - Regular models: Keep master-crafted power weapon (S5 AP-2 D2)
  - Pack Leaders: Can take twin claws OR relic greataxe (both replace BOTH weapons)
  - Heavy weapon models: Get assault cannon/cyclone + power fist (1 per 5 models)

**Why S5 Master-Crafted Power Weapons Are Still Competitive:**
- **Lethal Hits (Beastslayer detachment):** 6s to hit auto-wound vs Characters/Monsters/Vehicles
- **Volume compensates:** 7 shield models × 3 attacks = 21 attacks = ~3.5 auto-wounds from crits alone
- **Verified math:** Arjac's 10-man deals ~20 damage vs T10 Dreadnought in one activation
  - Arjac: 7.6 damage (S12 melee + Hunter's Instincts rerolls)
  - 2x Assault cannons: 3.3 damage (Devastating Wounds)
  - 2x Power fists: 3.3 damage (S10 AP-2 D2)
  - 7x Master-crafted power weapons: 5.25 damage (Lethal Hits makes S5 viable!)
  - Pack Leader twin claws: 0.8 damage
- **Local play:** Can model as hammers/axes (thematic) and call them "master-crafted power weapons" for rules

**Prevention:**
- ALWAYS WebFetch current datasheet when building lists for units not recently verified
- Check "Last Verified" date in cache - if >30 days, re-verify wargear options
- When WebFetch fails (JavaScript rendering), use WebSearch for "unit name wargear options 10th edition" + cross-reference community forums
- Mark cache entries with edition number (e.g., "10TH EDITION - VERIFIED DEC 2025")
- **ENFORCE EDITION VALIDATION:** Verify edition tag on ALL cached data before use

### 2025-12-24: Edition Enforcement Added (Root Cause Analysis)
**Why This Error Happened:**
- Datasheet cache had NO edition validation
- Agent assumed cached data was current without checking edition
- 10th Edition made significant wargear changes vs 9th Edition
- No system in place to detect outdated cache entries

**Fix Applied:**
- ✅ Added "CRITICAL: Current Edition Enforcement" section to rules-validated.md
- ✅ Updated agent critical_actions with edition validation protocol
- ✅ Marked all cached datasheets with "10TH EDITION - VERIFIED DEC 2025"
- ✅ Added checklist: verify edition tag before using cache, include "10th edition" in searches
- ✅ Added 🔄 OUTDATED tag protocol for when editions change

**Future-Proofing:**
- When 11th Edition releases (rumored Summer 2026), mark ALL cache as 🔄 OUTDATED
- Update critical_actions with new edition number
- Re-verify ALL datasheets against new edition rules
- Document edition-specific changes in mistake log

---

## Rule Update Protocol

**When rules change (new edition, FAQ, errata, MFM):**
1. Mark outdated rules with 🔄 OUTDATED tag
2. Add new verified rule with updated date
3. Document what changed and why
4. Archive old rule in "Historical Rules" section if needed

**When user corrects a mistake:**
1. Add ❌ ERROR entry under relevant rule
2. Document what went wrong
3. Add ✅ CORRECTED entry with fix
4. Update validation checklist if needed

---

## Army List Documentation Standard

**When to Offer Full Explanation:**
After building ANY initial army list, always ask user: "Want me to generate a full tactical reference document for this list? I can also create 500pt and 1000pt scaled versions if you want all three points levels."

**Full Tactical Reference Format:**

### Section 1: Army Lists (Required)
For each points level (500/1000/2000):
- **List table:** Unit | Models | Role | Points
- **Tactical Overview:** Key strengths, weaknesses, how this differs from other points levels
- **How to Play:** 5-step tactical guide specific to this list

### Section 2: Full Model List (2000pt only)
- Breakdown by unit type (Characters, Terminators, Infantry, etc.)
- Total model count and wound count
- Firepower and melee output summary
- **IMPORTANT:** Only include ONCE, deduplicated

### Section 3: Weapon Loadouts & Options (Required)
- Loadout options table for each unit type
- Squad compositions for EACH squad at EACH points level
- Wargear choices explained with tactical reasoning

### Section 4: Unit Details (Required)
For EVERY unit in the army:
- Stats table (M/T/Sv/W/Ld/OC/Points)
- Wargear listing
- Special rules and abilities
- "Why Take This Unit" tactical explanation

### Section 5: Rules Reference (Required)
- Wahapedia link for EVERY unit
- Detachment rules with Stratagems and Enhancements
- Faction rules (Oath of Moment, etc.)

### Section 6: Painting Reference (Required)
- Official GW purchase links for EVERY unit
- Prices in USD
- Notes on box contents (models per box, build options)

### Section 7: 3D Printing Guide (Optional)
- Exact component counts for printing
- Arm pair combinations
- Total model requirements

**What NOT to Include:**
- ❌ Legality verification (stays in Tacticus memory)
- ❌ Lore explanations (user can ask Lorekeeper)
- ❌ Duplicate sections (consolidate model counts)
- ❌ Quick reference stats if already in Rules Reference

**Workflow:**
1. Build initial list at requested points level
2. Show list table + quick tactical summary
3. Ask: "Want full tactical reference document? (includes weapon loadouts, rules links, painting reference, and tactical guide)"
4. If yes, ask: "Want me to include 500pt and 1000pt scaled versions too?"
5. Generate document following format above

---

---

## List Building Protocol ✅ REQUIRED
**When to Use:** Before building ANY army list (initial or iterations)
**Last Updated:** 2025-12-22

**STEP-BY-STEP PROTOCOL:**

1. **Load Faction Army Rules**
   - URL: `https://wahapedia.ru/wh40k10ed/factions/{faction-name}/`
   - Extract: Faction abilities, army-wide special rules, available detachments
   - Example: `https://wahapedia.ru/wh40k10ed/factions/space-marines/space-wolves`

2. **Load Detachment Rules** (chosen detachment)
   - URL: `https://wahapedia.ru/wh40k10ed/factions/{faction-name}/#{Detachment-Name}`
   - Extract: Detachment ability, ALL Enhancements (with costs), Stratagems, restrictions
   - Example: `https://wahapedia.ru/wh40k10ed/factions/space-marines/space-wolves#Saga-of-the-Beastslayer`
   - **CRITICAL:** Enhancements are ALWAYS in the detachment rules section

3. **Load Unit Datasheets** (for each unit in planned list)
   - URL: `https://wahapedia.ru/wh40k10ed/factions/{faction-name}/{Unit-Name}`
   - Extract: Stats, wargear options, points costs, special rules, unit size options
   - Ask user for wargear structure if WebFetch cannot extract details

4. **Build List** (with full context loaded)
   - Validate Rule of Three compliance
   - Verify points totals
   - Check enhancement restrictions (max 1 per character)
   - Confirm wargear legality per datasheet

5. **Include Wahapedia Links** (in final document)
   - Link to faction rules in Rules Reference section
   - Link to detachment rules (with enhancements clearly marked)
   - Link to EVERY unit datasheet
   - Format: `[Unit Name](https://wahapedia.ru/wh40k10ed/factions/{faction}/{Unit})`

**WHY THIS MATTERS:**
- Prevents building lists with invalid enhancements (don't exist or wrong cost)
- Ensures all detachment abilities and Stratagems are referenced
- Provides user with clickable links to verify all rules
- Loads full context BEFORE making list decisions

**EXAMPLE WORKFLOW:**

```
User: "Build me a 2000pt Space Wolves list with Saga of the Beastslayer"

Step 1: Load https://wahapedia.ru/wh40k10ed/factions/space-marines/space-wolves
        → Extract Oath of Moment, Space Wolves faction rules

Step 2: Load https://wahapedia.ru/wh40k10ed/factions/space-marines/space-wolves#Saga-of-the-Beastslayer
        → Extract Lethal Hits ability
        → Extract ALL 4 Enhancements:
          - Blade of the Slayer (25pts)
          - Hunter's Instincts (20pts)
          - The Pelt of Balewolf (15pts)
          - Black Death (15pts)

Step 3: Load datasheets for Wolf Guard Terminators, Logan Grimnar, etc.
        → Extract wargear, points, restrictions

Step 4: Build list with enhancements from Step 2, units from Step 3

Step 5: Include all Wahapedia links in final document
```

---

## Universal Datasheet Wargear Pattern ✅ VALIDATED
**Source:** Cross-faction datasheet analysis
**Last Updated:** 2025-12-23
**Status:** User validated

**PATTERN:**
Most unit datasheets follow this structure:
1. **Special Models (varies per unit):** Sergeant/Pack Leader/Boss Nob/Champion - unique wargear options
   - Usually 1 per unit, but could be different (datasheet explicitly states quantity)
2. **Heavy/Special Weapons (X per Y models):** Limited special weapons
   - Example: "For every 10 models, 1 can take..." or "1 per 5 models can take..."
3. **Regular Models:** Standard wargear with swap options available to all non-special models

**CRITICAL PROTOCOL - PACK LEADER AUTO-INCLUSION:**
**When building ANY army list, ALWAYS account for Pack Leaders/Sergeants/Champions if they exist on the datasheet:**
- ✅ Include Pack Leader in unit composition (1 per unit unless stated otherwise)
- ✅ Assign wargear to Pack Leader (usually upgraded melee weapon)
- ✅ Document Pack Leader loadout in weapon loadouts section
- ✅ Count Pack Leader in model breakdowns
- ✅ Account for Pack Leader in 3D printing guides

**Example - Space Wolves Blood Claws (10 models):**
- ❌ WRONG: "10x Blood Claws: Chainsword + Bolt pistol"
- ✅ CORRECT: "1x Pack Leader: Power weapon + Bolt pistol | 9x Blood Claws: Chainsword + Bolt pistol"

**Why This Matters:**
- Pack Leaders often have better wargear options (power weapons, special melee weapons)
- Failing to account for them = inaccurate army lists
- User expects Pack Leaders to be included if datasheet has them

**VALIDATED EXAMPLES:**

**Wolf Guard Terminators (Space Wolves):**
- ✅ Pack Leader (1 per unit): Twin lightning claws OR standard weapons
- ✅ Heavy Weapons (1 per 5 models): Assault cannon OR Cyclone missile launcher
- ✅ Regular Models: Storm bolter + power weapon (swap options)

**Immortals (Necrons):**
- ❌ NO special models - all identical
- ❌ NO heavy weapon slots
- ✅ Regular Models: Gauss blaster OR tesla carbine (squad-wide, all must match)

**Ork Boyz (Orks):**
- ✅ Boss Nob (1 per unit): Power klaw OR kombi-weapon options (unique to Boss Nob)
- ✅ Heavy Weapons (1 per 10 models): Big shoota OR rokkit launcha
- ✅ Regular Models: Slugga + choppa OR shoota (any number can swap)

**PATTERN VARIANCE:**
- NOT all units have special models (e.g., Necron Immortals are uniform)
- Heavy weapon ratios vary: "1 per 5", "1 per 10", or none
- Some squads require uniform loadouts (Immortals), others allow mixing (Boyz)

**CRITICAL LEARNING:**
- **ALWAYS read the datasheet explicitly** - don't assume pattern
- Special model restrictions (Sergeant, Pack Leader, Boss Nob) are ALWAYS stated on datasheet
- Heavy weapon limits are ALWAYS explicitly stated (e.g., "1 per 5 models")
- WebFetch cannot extract datasheet details from Wahapedia (returns JavaScript/navigation only)

**KNOWN VALID WAHAPEDIA URLS:**
- Faction lists: `https://wahapedia.ru/wh40k10ed/factions/{faction-name}/`
- Unit datasheets: `https://wahapedia.ru/wh40k10ed/factions/{faction-name}/{Unit-Name}`
- Examples:
  - `https://wahapedia.ru/wh40k10ed/factions/space-marines/`
  - `https://wahapedia.ru/wh40k10ed/factions/space-marines/Wolf-Guard-Terminators`
  - `https://wahapedia.ru/wh40k10ed/factions/necrons/Immortals`
  - `https://wahapedia.ru/wh40k10ed/factions/orks/Boyz`

**ACTION REQUIRED:**
When building lists for new unit types:
1. Ask user for datasheet wargear structure if uncertain
2. Do NOT assume pattern from other units
3. User will provide correct wargear rules or better links

---

## Points Limit Enforcement ✅ VERIFIED
**Source:** Warhammer 40k 10th Edition Matched Play Rules
**Last Verified:** 2025-12-23

**THE RULE:**
Points limits are HARD CAPS in matched play:
- 500pt games: Maximum 500pts (not 501, not 510)
- 1000pt games: Maximum 1000pts
- 2000pt games: Maximum 2000pts

**CRITICAL:**
- Going over by even 1 point = ILLEGAL list
- "Close enough" is not tournament legal
- Better to be under than over

**Validation History:**
- ❌ **2025-12-23 ERROR:** Recommended 1,010pt list for 1000pt game
  - **What went wrong:** Prioritized "maximizing enhancement value" over legality
  - **User correction:** "i feel like the rules of warhammer are 1000 points or under"
  - **Lesson learned:** Points limits are STRICT. Never exceed. Legal first, optimized second.

- ✅ **2025-12-23 CORRECTED:** Stayed at exactly 1,000pts by optimizing unit selection instead

**VALIDATION STEP:**
Before finalizing ANY list, verify total points ≤ mission size limit.

---

### 2025-12-26: Tyranid SYNAPSE Keyword Errors
**Mistake:** Listed Exocrine, Tyrannofex, Carnifex, and Barbgaunts as having the SYNAPSE keyword
**User Correction:** User reviewed army list and found inconsistencies - these units do NOT have SYNAPSE
**Root Cause:**
- Agent assumed all large Tyranid monsters have SYNAPSE
- Did not verify keyword presence on actual datasheets
- SYNAPSE is only on specific SYNAPSE CREATURE keyword units

**Fix Applied:**
- ✅ Added "⚠️ Note: Does NOT have SYNAPSE keyword" to each datasheet entry
- ✅ Updated Full Model Breakdown to clarify SYNAPSE status
- ✅ Added GATE 6: Keyword Accuracy Check to validation-checklist.md
- ✅ Added CONSISTENCY - KEYWORDS critical action to agent YAML

**Tyranid SYNAPSE Providers (VERIFIED):**
- ✅ Hive Tyrant (has SYNAPSE keyword)
- ✅ Winged Hive Tyrant (has SYNAPSE keyword)
- ✅ Tervigon, Neurothrope, Broodlord, etc. (specific units only)

**Tyranid NON-SYNAPSE Creatures (VERIFIED):**
- ❌ Exocrine (no SYNAPSE - must stay in Synapse aura)
- ❌ Tyrannofex (no SYNAPSE - must stay in Synapse aura)
- ❌ Carnifex (no SYNAPSE - must stay in Synapse aura)
- ❌ Barbgaunts (no SYNAPSE - benefits from Synapse)
- ❌ Termagants (no SYNAPSE - benefits from Synapse)

**Prevention:** ALWAYS check unit keywords on datasheet, never assume. Add keyword verification step.

---

### 2025-12-26: Points Budget Violations (Tyranids List)
**Mistake:** Created army lists that exceeded points limits:
- 500pt list was 515pts (15 over!)
- 1000pt list was 1,025pts (25 over!)
- 2000pt list was 2,035pts (35 over!)

**Root Cause:**
- Added units without recalculating total
- Did not verify total against points limit before presenting
- Gate 4 (Points Calculation) was not properly enforced

**Fix Applied:**
- ✅ Recalculated all three lists to be under budget
- ✅ 500pt now 480pts, 1000pt now 965pts, 2000pt now 1,975pts
- ✅ Emphasized "HARD CAP" nature of points limits in protocols

**Prevention:** Re-add all units before presenting. Points limit is HARD CAP. Under is legal, over is ILLEGAL.

---

### 2025-12-26: Internal Document Consistency Failures (Space Wolves List)
**Mistake:** Multiple inconsistencies between prose sections:
- 500pt list claimed "No Deep Strike" when Wolf Guard Terminators have Deep Strike
- Bjorn listed with "9" move" when actual M=8"
- Strengths mentioned "12" move wolves" but tactics said "grind forward slowly"
- 2000pt model count in prose didn't match actual table

**Root Cause:**
- Wrote Strengths/Weaknesses/Tactics sections without cross-referencing
- Used movement values from memory instead of datasheets
- Deep Strike keyword not verified against unit datasheet

**Fix Applied:**
- ✅ Changed "No Deep Strike" → "Deep Strike available but inadvisable"
- ✅ Corrected Bjorn movement to 8" (actual datasheet value)
- ✅ Clarified which units are slow (Terminators 5") vs fast (wolves 12")
- ✅ Added GATE 7: Internal Consistency Check to validation-checklist.md
- ✅ Added GATE 8: Section Cross-Reference to validation-checklist.md

**Prevention:**
- After completing any section, cross-reference stats against datasheets
- Verify Strengths don't contradict Weaknesses
- Ensure movement values match actual unit profiles
- Check all keyword claims (Deep Strike, SYNAPSE, etc.) against datasheets

---

---

### 2025-12-26: Space Wolves Points Corrections (MFM December 2025)
**Mistake:** Multiple unit points were outdated after December 2025 MFM update
**User Correction:** User verified via New Recruit app that Arjac was 105pts, not 95pts
**Root Cause:**
- Cached points values from earlier MFM version
- No automated refresh of points data
- BSData/Wahapedia not being checked regularly

**Corrections Applied:**
| Unit | Old Points | New Points | Delta |
|------|------------|------------|-------|
| Arjac Rockfist | 95pts | 105pts | +10pts |
| Bjorn the Fell-Handed | 170pts | 160pts | -10pts |
| Venerable Dreadnought | 140pts | 130pts | -10pts |
| Blood Claws (10) | 140pts | 135pts | -5pts |
| Grey Hunters (10) | 140pts | 165pts | +25pts |

**Data Sources Verified:**
- Wahapedia (primary): https://wahapedia.ru/wh40k10ed/factions/space-marines/
- BSData GitHub: https://github.com/BSData/wh40k-10e
- New Recruit app (user verification)

**Prevention:**
- Created Wahapedia scraper script: `_bmad/warhammer-40k/scripts/scrape-wahapedia.py`
- Points in PriceTag divs can be extracted programmatically
- Check points against Wahapedia before building lists
- Refresh data monthly or after MFM updates

---

*Last Updated: 2025-12-26*
*Maintained by: Tacticus Agent*
*Version: 1.6*

---

## Competitive Meta Tracking ✅ ACTIVE
**Purpose:** Cache tournament meta data to reduce web searches - only query for deltas/changes
**Last Meta Update:** 2025-12-23
**Next Scheduled Update:** 2026-01-15 (or when user requests refresh)

### December 2025 Meta Snapshot

**Balance Dataslate:** December 2025 (pre-Christmas release)
**Philosophy:** "Light-touch" - game in healthy spot, mostly points tweaks

**S-Tier Armies (Tournament Winners):**
1. **Astra Militarum** - Won Rise of Empire GT (Dec 19), consistent top finishes
2. **Space Marines** (Ultramarines, Dark Angels, Black Templars) - Multiple wins
3. **Drukhari** - Everwinter GT placement, avoided nerfs
4. **Chaos Daemons** - S-Tier rated, flexible
5. **Death Guard** - Multiple December top finishes (despite points nerfs)

**A-Tier (Strong):**
- T'au Empire (won King of Blades Dec 18, but win rate crashed - no buffs given)
- Necrons (early December strong showings)
- Thousand Sons (competitive)
- Imperial Knights (some nerfs applied)
- Adepta Sororitas (top finish Everwinter, but hit with big points nerfs)

**December Dataslate Major Changes:**
- ❌ **Aeldari NERFED HARD:** Skyborne Sanctuary + Swift as the Wind ability changes
- ❌ **AdMech:** Big points increases
- ❌ **Adepta Sororitas:** Points nerfs across board
- ❌ **Raven Guard:** Points + ability nerfs
- ❌ **Death Guard:** Points adjustments
- ❌ **Black Templars:** Points increases (still competitive)
- 😢 **T'au + Genestealer Cults:** Left untouched despite needing help

**Top Tournament Results (December 2025):**
- Rise of Empire GT (Dec 19): Astra Militarum, Dark Angels, Death Guard
- King of Blades (Dec 18): T'au Empire, Aeldari
- Everwinter GT (Dec 10): Adepta Sororitas, T'au, Drukhari

**Sources:**
- Stat Check Meta Dashboard: https://www.stat-check.com/the-meta
- Goonhammer Q4 2025 Balance Update: https://www.goonhammer.com/40k-the-q4-2025-balance-update-overview/
- Frontline Gaming Winter 2025 Balance: https://frontlinegaming.org/2025/12/10/warhammer-40k-winter-2025-balance-update-every-faction-touched-no-meta-left-behind/
- Spikey Bits Tournament Lists: https://spikeybits.com/army-lists/

**Meta Refresh Protocol:**
- Check monthly (mid-month after potential balance updates)
- Search query: "Warhammer 40k 10th edition meta [current month] [current year] tournament"
- Store deltas only (what changed since last update)

---

## Durability Rankings by Faction ✅ VALIDATED
**Purpose:** Persistent durability analysis to guide tank-heavy/durable army building
**Last Updated:** 2025-12-23
**Next Scheduled Update:** 2026-06-15 (bi-annual: June + December after balance dataslates)
**Verification Method:** Wahapedia processed data + tournament meta + web research

### S-TIER DURABILITY (Competitive + Tank-Heavy)

**1. ASTRA MILITARUM** ⭐ Tournament Winner
- **Max Toughness:** T13 (15+ Baneblade/Macharius variants)
- **Core Durability:** Leman Russ spam (T11, 2+ save, 13W)
- **Meta Status:** S-Tier, won Rise of Empire GT (Dec 19, 2025)
- **Synergies:** Lord Solar Leontus (CP farming), Grizzled Company detachment
- **Why S-Tier:** Most T13 units in game + active tournament success + accessible durability
- **User Alignment:** Matches castle strategy + vehicle-heavy preference (has "Imperial Hammer" list)

**2. IMPERIAL KNIGHTS** 🛡️ Universal Invulns
- **Max Toughness:** T13 (Acastus Porphyrion/Asterius, W30)
- **Core Durability:** ALL units have 4+/5+ invulnerable saves (built-in)
- **Meta Status:** A-Tier (some nerfs applied December dataslate)
- **Synergies:** Pure invuln faction - no conditional mechanics needed
- **Why S-Tier:** Only faction with universal invulns + consistent T11-T13 across roster
- **Playstyle:** Elite, low model count (3-6 Knights at 2000pts)

**3. TYRANIDS** 🦖 Monster Supremacy
- **Max Toughness:** T14 (Hierophant - highest in game)
- **Core Durability:** Monster swarm (T11-T12 with 2+ armor, inv4 on key units)
- **Meta Status:** Mid-tier (not featured in December S-Tier)
- **Synergies:** 2 FNP stratagems + 2 invuln stratagems (most defensive density)
- **Why S-Tier:** Highest raw T value + monster layering + stratagem depth
- **Playstyle:** Monster-heavy lists (Norn Emissary, Tyrannofex, Tervigon spam)

---

### A-TIER DURABILITY (Elite Armor Specialists)

**4. NECRONS** 🤖 Invuln Specialists
- **Max Toughness:** T13 (Tomb Citadel, Gauss Pylon fortifications)
- **Core Durability:** Widest invuln distribution (C'tan T11/inv4, constructs T12/inv5)
- **Meta Status:** A-Tier (early December strong showings)
- **Synergies:** Reanimation protocols + vehicle invuln stacking
- **Playstyle:** C'tan + Ghost Ark + Doomsday Ark spam (all have inv4/5)

**5. DEATH GUARD** ☠️ Nurgle's Chosen
- **Max Toughness:** T14 (Mastodon super-heavy transport)
- **Core Durability:** Mortarion T12/inv4, daemon princes, plague marines
- **Meta Status:** S-Tier (multiple December top finishes despite points nerfs)
- **Synergies:** Army-wide Nurgle durability + FNP stratagems
- **Playstyle:** Mortarion + daemon engines + plague marine spam

**6. ADEPTUS CUSTODES** 🛡️ Golden Elite
- **Max Toughness:** T12 (Coronus, Orion, Ares gunships)
- **Core Durability:** Entire army has 2+/3+ armor + 4+/5+ invulns (elite quality)
- **Meta Status:** Mid-tier
- **Synergies:** T6 infantry with 2+/inv4 (3W per model) + durable vehicles
- **Playstyle:** Elite, low model count (30-40 models at 2000pts)

---

### B-TIER DURABILITY (Competitive but Lower T Ceiling)

**7. SPACE MARINES** (Ultramarines/Dark Angels/Black Templars)
- **Max Toughness:** T10 (Redemptor Dreadnought), T9 (Ballistus)
- **Core Durability:** Dreadnought-heavy castles with character auras
- **Meta Status:** S-Tier (Adepticon 2025 winner, Dallas Open winner)
- **Synergies:** Gladius Task Force (Combat Doctrines), character buffs
- **User Alignment:** Has "Sons of Guilliman" Dreadnought castle list

**8. ADEPTA SORORITAS**
- **Max Toughness:** T10 (Castigator, Exorcist)
- **Core Durability:** Shield of Faith (FNP 5+ vs mortals), Army of Faith detachment
- **Meta Status:** A-Tier early December, NERFED HARD (points increases)
- **Synergies:** Ignore modifiers + -1 to hit stratagems

**9. ADEPTUS MECHANICUS**
- **Max Toughness:** T11 (Skorpius Disintegrator)
- **Core Durability:** 1 FNP stratagem + 3 invuln stratagems (most defensive options)
- **Meta Status:** A-Tier (big points increases December dataslate)
- **Synergies:** Data-Psalm Conclave (4+ invuln + FNP 4+ vs mortals stacking)

---

### KEY INSIGHTS (December 2025)

**Toughness Meta Gap:**
- Competitive play shows gap between T7-T9
- T10+ is premium durability tier
- T13-T14 units define fortress armies (AM, Knights, Tyranids)

**Invulns > Raw Toughness:**
- Imperial Knights prove universal invulns outperform raw T alone
- Necrons/Custodes combine high T + invulns for layered defense
- AP-4+ weapons punish armies without invuln saves

**S-Tier ≠ Most Tanky:**
- Drukhari (S-Tier) relies on speed/mobility, not durability
- Tournament success = durability + firepower + CP generation
- Astra Militarum wins by combining all three

**Meta Shifts to Watch:**
- GW balance philosophy: "Light-touch" tweaks (mostly points)
- Tank-heavy armies avoided major nerfs (AM, Knights stable)
- Infantry-heavy armies hit harder (Sororitas, AdMech points increases)

---

### DURABILITY REFRESH PROTOCOL

**When to Update (Bi-Annual):**
1. **June Update:** After Q2 balance dataslate (mid-year adjustments)
2. **December Update:** After Q4 balance dataslate (pre-Christmas release)

**What to Track:**
- Max Toughness values (if new units released)
- Tournament meta shifts (S-Tier → A-Tier movements)
- Points changes affecting tank/monster spam viability
- New detachment rules granting defensive bonuses
- Errata/FAQ changes to invuln/FNP mechanics

**Search Queries:**
- "Warhammer 40k 10th edition most durable armies [month] [year] tournament"
- "Warhammer 40k toughness tier list [year]"
- "Warhammer 40k tank meta [year] balance dataslate"

**Data Sources:**
- Wahapedia processed datasheets (toughness values, saves, wounds)
- Stat Check Meta Dashboard (win rates, appearance rates)
- Goonhammer balance updates (detailed analysis)
- Spikey Bits tournament results (winning lists)

---

## Ultramarines Gladius Task Force ✅ VERIFIED
**Source:** Wahapedia Ultramarines + Tournament Data
**Last Verified:** 2025-12-21
**Verification Method:** Adepticon 2025 + Dallas Open winning lists

**GLADIUS TASK FORCE DETACHMENT:**
- **Combat Doctrines:** Choose one per Command phase (each once per game)
  - Devastator: Units shoot after Advancing
  - Tactical: Units shoot + charge after Falling Back
  - Assault: Units charge after Advancing

**ENHANCEMENTS (Max 2 per army, max 1 per character):**
- **Artificer Armour** (10pts): 2+ save + Feel No Pain 5+
- **The Honour Vehement** (15pts): +1 Attack/Strength (+2 in Assault Doctrine)
- **Fire Discipline** (cost unknown): Sustained Hits 1, crit on 5+ in Devastator
- **Adept of the Codex** (cost unknown): Unit counts as in Tactical Doctrine

**VERIFIED POINTS COSTS:**
- Roboute Guilliman: 345pts
- Marneus Calgar: 210pts (includes 2x Victrix Honour Guard)
- Captain in Gravis Armour: 90pts
- Lieutenant: 70pts
- Ballistus Dreadnought: 140pts
- Redemptor Dreadnought: ~200pts (estimated)
- Intercessor Squad (10 models): 80pts
- Assault Intercessor Squad (10 models): 90pts
- Infernus Squad (10 models): ~85pts (estimated)
- Infernus Squad (5 models): ~45pts (estimated)

**ADEPTICON 2025 WINNING LIST (Conan Jennings):**
- Roboute Guilliman (345) + Marneus Calgar (210) + Captain Gravis (90) + Lieutenant (70)
- 3x Ballistus Dreadnought (420pts total)
- 2x Vindicator (370pts total)
- Intercessor support troops
- **Result:** Won Adepticon 2025 + Dallas Open 2025 (undefeated)

---

## Wahapedia CSV Data Integration ✅ IMPLEMENTED
**Last Updated:** 2025-12-22
**Status:** Active - Auto-refresh weekly

**PURPOSE:**
Integration of official Wahapedia CSV data exports to eliminate manual datasheet lookups and ensure points/wargear accuracy.

**DATA HIERARCHY:**
1. **Wahapedia CSVs:** Official source of truth for stats, points, wargear
2. **rules-validated.md:** User corrections, mistake logs, learned patterns
3. **When conflicts exist:** rules-validated.md overrides CSV (user has corrected an error)

**LOADING PROTOCOL:**
1. On agent activation: Check CSV age (auto-refresh if >7 days old)
2. Load core-rules.json + factions-index.json on startup
3. On faction request: Load faction-specific datasheets/rules/stratagems
4. Cross-reference rules-validated.md for known corrections

**CSV FILES USED:**
- `Datasheets.csv`: Unit profiles (id, name, faction_id, role, loadout, transport, points)
- `Datasheets_wargear.csv`: Equipment options with costs (datasheet_id, wargear_id, cost)
- `Datasheets_models.csv`: Individual model stats (M, T, SV, W, LD, OC)
- `Wargear_list.csv`: Weapon/equipment profiles (range, A, BS_WS, S, AP, D, abilities)
- `Abilities.csv`: Unit and faction abilities (id, name, type, description)
- `Stratagems.csv`: Detachment stratagems (id, name, CP_cost, description, detachment)
- `Factions.csv`: Faction index (id, name)

**PROCESSED FILES STRUCTURE:**
```
_bmad/warhammer-40k/data/
├── wahapedia-10ed/              # Raw CSVs (auto-downloaded weekly)
│   └── last_update.csv          # Timestamp for refresh checks
└── processed/                   # Agent-optimized JSON
    ├── core-rules.json          # Core abilities (lore trimmed)
    ├── factions-index.json      # Faction list
    └── {faction-id}/            # Per-faction data
        ├── datasheets.json      # Full unit stats + wargear
        ├── rules.json           # Faction abilities
        └── stratagems.json      # Detachment stratagems
```

**EXAMPLE USAGE:**
```
User: "Build a Space Wolves 2000pt list"

Agent:
1. Load processed/SM/datasheets.json (Space Marines includes Space Wolves)
2. Filter for Space Wolves units (faction_id match)
3. Query units where role in ['HQ', 'Troops', 'Elites', 'Heavy Support']
4. Cross-check rules-validated.md for Pack Leader wargear restriction (known override)
5. Build list using CSV points + rules-validated corrections
```

**BENEFITS:**
- ✅ No more "ask user for datasheet details" workarounds
- ✅ Perfect wargear validation (Pack Leader restrictions from CSV)
- ✅ Instant points accuracy (always current)
- ✅ Offline capability (CSVs cached locally)
- ✅ Weekly auto-refresh ensures rules updates (errata, FAQs, points changes)

**MANUAL REFRESH:**
Use the `refresh-data` menu trigger to force download + reprocess if needed.

---

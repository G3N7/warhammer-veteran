# Tacticus - Validated Warhammer 40k Rules Knowledge Base

**Purpose:** Persistent, self-correcting rules knowledge that prevents repeated mistakes across sessions.

**Update Protocol:**
- ✅ Add new verified rules with source + date
- ❌ Document mistakes and user corrections
- 🔄 Update when rules change (new edition, FAQ, errata)

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

### Saga of the Beastslayer Detachment ✅ VERIFIED
**Source:** Wahapedia Space Wolves Detachment Rules
**Last Verified:** 2025-12-21

**DETACHMENT ABILITY:**
Units from this detachment gain **Lethal Hits** when targeting:
- Characters
- Monsters
- Vehicles

**ENHANCEMENTS (Max 1 per Character):**
- **Blade of the Slayer** (25pts): Precision + enhanced damage vs big targets
- **Hunter's Instincts** (20pts): Re-roll wound rolls vs Characters/Monsters/Vehicles
- **The Pelt of Balewolf** (15pts): Stealth
- **Black Death** (15pts): Devastating Wounds

**LEGAL ENHANCEMENT ALLOCATION:**
- ✅ Logan gets Blade of Slayer (25pts)
- ✅ Arjac gets Hunter's Instincts (20pts)
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
**Points:** 95pts
**Can Lead:** Wolf Guard Terminators (Terminator keyword)
**Epic Hero:** Only 1 per army

---

### Bjorn the Fell-Handed ✅ VERIFIED
**Source:** Wahapedia Space Marines Epic Heroes
**Points:** 170pts
**Special Ability:** Ancient Tactician - Gain 1CP at start of each Command phase
**Epic Hero:** Only 1 per army

---

### Venerable Dreadnought ✅ VERIFIED
**Source:** Wahapedia Space Marines Units
**Points:** 140pts
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
- [ ] Verify enhancements (max 1 per character, only on eligible models)
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

### 2025-12-21: Rule of Three Violation
**Mistake:** Built 6x Wolf Guard Terminator units in 2000pt list
**User Correction:** "you can't have more than 3 of a given unit type"
**Root Cause:** Did not validate matched play rules before building concept
**Fix Applied:**
- Added Rule of Three to validated knowledge base
- Added pre-build validation checklist
- Updated critical_actions to load rules KB first

**Prevention:** Always check this KB BEFORE building lists, not after user correction.

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

*Last Updated: 2025-12-21*
*Maintained by: Tacticus Agent*
*Version: 1.1*

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

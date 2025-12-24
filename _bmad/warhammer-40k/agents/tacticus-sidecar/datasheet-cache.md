# Tacticus - Datasheet Cache

**Purpose:** Local cache of frequently-used datasheets to avoid repeated web fetches
**Last Updated:** 2025-12-23
**Format:** Concise, LLM-optimized datasheet summaries

---

## Schema

Each cached datasheet contains:
- **Unit Composition:** Model types (Pack Leader, special weapons, regular models)
- **Wargear Options:** By model type (Pack Leader vs regular)
- **Unit Size:** Min/Max models
- **Points:** Cost per model
- **Stats:** M/T/Sv/W/Ld/OC
- **Special Rules:** Abilities (concise)
- **Source:** Wahapedia URL
- **Last Verified:** Date

---

## Space Wolves Units

### Blood Claws
**Source:** https://wahapedia.ru/wh40k10ed/factions/space-marines/Blood-Claws
**Last Verified:** 2025-12-23 (applied to Ultramarines Sergeant audit)
**Faction:** Space Marines (Space Wolves)
**Role:** Battleline

**UNIT COMPOSITION:**
- 1x Blood Claw Pack Leader
- 4-9x Blood Claws
- **Unit Size:** 5-10 models

**STATS:**
- M: 6" | T: 4 | Sv: 3+ | W: 2 | Ld: 6+ | OC: 2

**POINTS:**
- 14pts per model

**WARGEAR (Default):**
- Every model: Bolt pistol + Astartes chainsword

**WARGEAR OPTIONS:**
- **Pack Leader (1 per unit):**
  - Can swap Astartes chainsword for: **Power weapon** (recommended)
  - Can swap bolt pistol for: Plasma pistol (optional)
- **Regular models:**
  - Standard loadout (no swaps typical)

**RECOMMENDED LOADOUT:**
- **Pack Leader:** Power weapon + Bolt pistol
- **9x Regular Blood Claws:** Astartes chainsword + Bolt pistol

**SPECIAL RULES:**
- **Berserk Charge:** Extra attacks when charging
- **Headstrong:** Leadership penalties

**STATUS:** ✅ COMPLETE (validated pattern for Codex Sergeants)

---

### Grey Hunters
**Source:** https://wahapedia.ru/wh40k10ed/factions/space-marines/Grey-Hunters
**Last Verified:** 2025-12-23 (validated via Ultramarines Sergeant audit)
**Faction:** Space Marines (Space Wolves)
**Role:** Battleline

**UNIT COMPOSITION:**
- 1x Grey Hunter Pack Leader
- 4-9x Grey Hunters
- **Unit Size:** 5-10 models

**STATS:**
- M: 6" | T: 4 | Sv: 3+ | W: 2 | Ld: 6+ | OC: 2

**POINTS:**
- 14pts per model

**WARGEAR (Default):**
- Every model: Boltgun + Bolt pistol + Astartes chainsword

**WARGEAR OPTIONS:**
- **Pack Leader (1 per unit):**
  - Can swap Astartes chainsword for: **Power weapon** (recommended) OR Power fist
  - Can swap bolt pistol for: Plasma pistol (optional)
- **Regular models:**
  - Standard loadout (no swaps typical)

**RECOMMENDED LOADOUT:**
- **Pack Leader:** Power weapon + Boltgun + Bolt pistol
- **9x Regular Grey Hunters:** Boltgun + Bolt pistol + Astartes chainsword

**SPECIAL RULES:**
- Versatile troops (shooting + melee)

**STATUS:** ✅ COMPLETE (pattern confirms Codex Sergeant equivalence)

---

### Wolf Guard Terminators ✅ VERIFIED
**Source:** https://wahapedia.ru/wh40k10ed/factions/space-marines/Wolf-Guard-Terminators
**Last Verified:** 2025-12-22 (user corrected twin claws restriction)
**Faction:** Space Marines (Space Wolves)
**Role:** Elites

**UNIT COMPOSITION:**
- 1x Wolf Guard Pack Leader
- 4 or 9x Wolf Guard Terminators
- **Unit Size:** 5 or 10 models

**STATS:**
- M: 5" | T: 5 | Sv: 2+/4++ | W: 3 | Ld: 6+ | OC: 1

**POINTS:**
- 34pts per model (all wargear included)

**WARGEAR (Default):**
- Every model: Storm bolter + **master-crafted power weapon** (S5, AP-2, D2)

**WARGEAR OPTIONS (10TH EDITION - VERIFIED DEC 2025):**
- **Pack Leader (1 per unit - REQUIRED):**
  - Can replace BOTH weapons with: **Twin lightning claws** (S User, AP-2, D1, Twin-linked, melee only)
  - Can replace BOTH weapons with: **Relic greataxe** (melee only, stats TBD)
- **Heavy Weapons (1 per 5 models):**
  - Can replace storm bolter + master-crafted power weapon with: **Assault cannon + Power fist** (Heavy 6, S6 AP-1 D1 Devastating Wounds + S10 AP-2 D2 melee)
  - Can replace storm bolter + master-crafted power weapon with: **Cyclone missile launcher + Power fist** (Heavy 2, S9 AP-2 D3 + S10 AP-2 D2 melee)
- **Regular models:**
  - Can replace storm bolter with: **Storm shield** (4++ invuln, lose shooting)
  - ❌ **REMOVED IN 10TH EDITION:** Thunder hammers, chainfists, and power fists are NOT available to regular models
  - ✅ All regular models keep master-crafted power weapon (S5 AP-2 D2)

**SPECIAL RULES:**
- Deep Strike
- Terminator armor (2+/4++)
- Can be led by Logan Grimnar or Arjac Rockfist

**CRITICAL RESTRICTION:**
- Twin lightning claws = **PACK LEADER ONLY** (1 per unit max)

---

## Datasheet Request Queue

**STATUS:** All pending requests resolved ✅

**COMPLETED (2025-12-23):**
1. ✅ Blood Claws Pack Leader wargear - verified via Ultramarines Sergeant audit
2. ✅ Grey Hunters unit composition - confirmed Pack Leader + wargear options

---

## Cache Update Protocol

**When to Add New Datasheets:**
- User asks for specific unit details that aren't cached
- Building new army list for faction with uncached units
- Datasheet updates from errata/FAQ/MFM require refresh

**Cache Verification:**
- ⚠️ INCOMPLETE = missing wargear details, ask user for clarification
- ✅ COMPLETE = full composition + wargear + special rules documented
- 🔄 OUTDATED = rules changed, needs refresh (mark date + what changed)

---

*Maintained by: Tacticus Agent*
*Version: 1.1*
*Last Updated: 2025-12-23*

# 10th Edition Phase Sequence

**Edition:** Warhammer 40,000 10th Edition
**Last Updated:** December 2024

## Turn Structure Overview

```
BATTLE ROUND
├── Player Turn (Active Player)
│   ├── 1. Command Phase
│   ├── 2. Movement Phase
│   ├── 3. Shooting Phase
│   ├── 4. Charge Phase
│   └── 5. Fight Phase
└── Player Turn (Other Player)
    └── (Same structure)
```

---

## 1. COMMAND PHASE

### Step Order
1. **Command** - Gain CP (1 per turn, +1 if Warlord alive)
2. **Battle-shock** - Test units below half strength
3. **Start of Command Phase abilities** - Resolve in active player's order

### Battle-shock Tests
- Units below Starting Strength take test
- Roll 2D6, compare to Leadership
- Fail = Battle-shocked until next Command Phase
- Battle-shocked effects:
  - Cannot use Stratagems on unit
  - OC becomes 0
  - Cannot be selected for Heroic Intervention

### Timing Window: "Start of Command Phase"
Abilities that trigger here resolve BEFORE Battle-shock tests.

---

## 2. MOVEMENT PHASE

### Step Order
1. **Start of Movement Phase abilities**
2. **Move units** (any order)
3. **End of Movement Phase abilities**

### Movement Types

| Type | Distance | Restrictions |
|------|----------|--------------|
| Normal Move | Up to M" | Cannot move within Engagement Range |
| Advance | M" + D6" | Cannot shoot (except Assault), cannot charge |
| Fall Back | Up to M" | Cannot shoot (unless Pistol), cannot charge |
| Remain Stationary | 0" | Counts as having moved 0" |

### Reinforcements
- Arrive at end of Movement Phase
- Set up more than 9" from enemy models
- Count as having made Normal Move

### Key Rules
- **Engagement Range:** 1" horizontally, 5" vertically
- **Unit Coherency:** 2" (or 1" vertically) from another model
- **Transports:** Embark before moving OR disembark then move

---

## 3. SHOOTING PHASE

### Step Order
1. **Start of Shooting Phase abilities**
2. **Select unit to shoot**
3. **Select targets**
4. **Make ranged attacks** (roll hit, wound, save, damage)
5. **Repeat for other units**
6. **End of Shooting Phase abilities**

### Shooting Sequence (Per Unit)
1. Select shooting unit
2. Select weapons to fire
3. Select targets for each weapon
4. Roll hit rolls (modifiers apply)
5. Roll wound rolls
6. Allocate attacks to models
7. Roll saving throws
8. Inflict damage

### Key Modifiers
| Modifier | Effect |
|----------|--------|
| Heavy | -1 to hit if unit moved |
| Assault | Can shoot after Advance |
| Rapid Fire | Double shots at half range |
| Melta | +D6 damage at half range |
| Torrent | Auto-hit |
| Blast | +1 attack per 5 models in target |

### Line of Sight
- True line of sight from shooting model
- Any part of target model = visible
- Cover: +1 to save if benefit applies

---

## 4. CHARGE PHASE

### Step Order
1. **Start of Charge Phase abilities**
2. **Select unit to charge**
3. **Declare targets**
4. **Overwatch** (if opponent uses stratagem)
5. **Roll charge** (2D6")
6. **Charge move** (must end within Engagement Range of all targets)
7. **Repeat for other units**
8. **Heroic Interventions**
9. **End of Charge Phase abilities**

### Charge Requirements
- Cannot charge if: Advanced, Fell Back, arrived from Reserves this turn (unless special rule)
- Must declare ALL targets before rolling
- Must reach ALL declared targets or charge fails

### Heroic Intervention
- At end of Charge Phase
- Eligible: Character within 6" of enemy
- Move up to 3" toward closest enemy
- Must end closer to enemy
- Cannot do if Battle-shocked

---

## 5. FIGHT PHASE

### Step Order
1. **Start of Fight Phase abilities**
2. **Fights First units** (alternate, starting with active player)
3. **Remaining Eligible units** (alternate, starting with active player)
4. **End of Fight Phase abilities**

### Fight Sequence (Per Unit)
1. **Pile In** - 3" toward closest enemy
2. **Make Attacks** - Allocate, roll, resolve
3. **Consolidate** - 3" toward closest enemy

### Fights First
Units with this ability (or that charged) fight before normal units.

If multiple Fights First:
1. Active player picks first
2. Alternate

### Fights Last
Must fight after all other eligible units have fought.

---

## Critical Timing Windows

### "At the start of X phase"
- Resolve BEFORE any normal phase actions
- Active player chooses order of their abilities

### "At the end of X phase"
- Resolve AFTER all normal phase actions complete
- Before moving to next phase

### "When X happens"
- Interrupt normal sequence
- Resolve immediately when triggered

### "Once per phase"
- Can only use ability one time during that phase
- Resets at start of next occurrence of that phase

---

## Common Disputes

### Q: Can I shoot into combat?
**A:** Yes, but only with Pistols. Other weapons cannot target units in Engagement Range.

### Q: When does a model die?
**A:** When it loses its last wound. Resolve all damage from an attack before removing models.

### Q: Can I Fall Back and charge?
**A:** No, unless a special rule allows it.

### Q: Do auras affect the model with the aura?
**A:** Check wording. "Other friendly units" = no. "Friendly units" = yes.

### Q: Can I re-roll a re-roll?
**A:** No. You can never re-roll a die more than once.

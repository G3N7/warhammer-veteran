# Design Paint Scheme Workflow

Interactive paint scheme designer with lore validation, budget optimization, and personalized recommendations.

## Activation

This workflow is triggered by Brushmaster (Painting Guide) agent when user selects **[DPS] Design Paint Scheme**.

## Overview

Collaborative paint scheme design that considers:
- User's painting skill and style
- Current paint collection and budget
- Lore accuracy requirements
- Color theory and aesthetics
- Practical application steps

**Multi-Agent Feature:** Integrates with Lorekeeper agent for faction color validation.

## Prerequisites

- Query Wahapedia task (for faction info)
- Brushmaster sidecar folder (for saving schemes)
- Lorekeeper agent (for lore validation)
- Access to painting technique knowledge

## Workflow Steps

### Step 0: Import Army Context (Optional)

**Check for linked army list:**
```
Checking if you're coming from Tacticus with an army list...
```

**If army list linked:**
- Load army list from `tacticus-sidecar/lists.md`
- Extract faction, points, unit counts
- Calculate total models to paint
- Identify unit types (infantry, vehicles, characters)

**Display army context:**
```
I see you're painting:
- Faction: {faction}
- Points: {points}
- Total Models: ~{count} (estimated)
- Unit Breakdown:
  - {count} Infantry
  - {count} Characters
  - {count} Vehicles

This helps me design a scheme optimized for your army size!
```

**If no army list:**
- Skip to Step 1
- Continue with standard workflow

**Benefits:**
- Auto-calculate painting time estimates
- Suggest batch painting order
- Tailor complexity to army size
- Link paint scheme to specific project

**Output:** Army context (if available)

---

### Step 1: Gather Painting Preferences

**Greet user:**
```
Welcome to the Paint Scheme Designer!

I'll help you create a personalized color scheme for your army that matches
your skill level, budget, and preferences. Let's start with some questions.
```

**Ask about painting goals:**
- What quality level are you aiming for?
  - **Speed Paint** - Fast tabletop standard (3-5 paints)
  - **Tabletop Standard** - Good looking at arm's length (5-8 paints)
  - **Display Quality** - Contest/showcase level (10+ paints)

**Determine skill level:**
- How experienced are you with miniature painting?
  - **Beginner** - New to the hobby or first army
  - **Intermediate** - Painted a few units, comfortable with basics
  - **Advanced** - Experienced with advanced techniques

**Identify preferred techniques:**
Present techniques with brief explanations:
- ✓ Drybrushing (fast highlights)
- ✓ Layering (smooth color transitions)
- ✓ Contrast Paints (one-coat shading)
- ✓ Washes/Shades (easy depth)
- ✓ Edge Highlighting (crisp definition)
- ✓ Wet Blending (smooth gradients - advanced)
- ✓ NMM (Non-Metallic Metal - advanced)
- ✓ OSL (Object Source Lighting - advanced)

User selects techniques they're comfortable with or want to learn.

**Load preferences:**
- Check `brushmaster-sidecar/techniques.md` for past preferences
- Suggest based on skill level if new user

**Output:** User preference profile

---

### Step 1.5: Select Paint Set Preset (NEW - Optional Fast Track)

**Offer common paint set presets:**
```
Do you have one of these common paint sets? I can design using only those paints!
```

**Paint Set Presets:**

**[AP] Army Painter Mega Paint Set (54 colors)**
- Includes: Full color range, metallics, washes
- Perfect for: Any scheme, beginner-friendly
- **Auto-loads:** All 54 colors from set

**[APS] Army Painter Speedpaints Set**
- Includes: 24 Speedpaints + primers
- Perfect for: Fast batch painting, one-coat schemes
- **Auto-loads:** Speedpaint range

**[CE] Citadel Essentials Set**
- Includes: ~20 core paints + shades
- Perfect for: Standard Games Workshop schemes
- **Auto-loads:** Citadel starter colors

**[VP] Vallejo Game Color Basic Set**
- Includes: 16 basic colors
- Perfect for: Traditional painting techniques
- **Auto-loads:** Vallejo basics

**[CI] Custom Inventory**
- **Continue to Step 2:** Manual paint entry

**If preset selected:**
- Load complete paint inventory for that set
- Skip Step 2 (inventory already known)
- Jump to Step 3 (budget)
- **Fast-track benefit:** Saves 5-10 minutes of workflow time

**Preset Inventory Database:**

```yaml
Army Painter Mega Set:
  base_colors:
    - Matt Black, Matt White, Pure Red, Electric Blue, etc. (54 total)
  metallics:
    - Plate Mail Metal, Greedy Gold, Weapon Bronze
  washes:
    - Dark Tone, Strong Tone, Soft Tone
  primers:
    - Compatible with all Army Painter sprays

Army Painter Speedpaints:
  speedpaints:
    - Holy White, Zealot Yellow, Grim Black, etc. (24 colors)
  technique:
    - One-coat painting over light primer

Citadel Essentials:
  base:
    - Abaddon Black, Corax White, Mephiston Red, etc.
  shade:
    - Agrax Earthshade, Nuln Oil, Reikland Fleshshade
  layer:
    - Evil Sunz Scarlet, Calgar Blue, etc.
```

**Benefits:**
- Instant paint inventory
- Guaranteed scheme compatibility
- Eliminates manual entry errors
- Optimizes for what user actually owns
- Common beginner purchase = fast onboarding

**Output:** Paint inventory (if preset selected) OR continue to Step 2

---

### Step 2: Inventory Current Paints

**Ask about paint collection:**
```
Let's see what paints you already have. This helps me recommend schemes
using what you own and minimize new purchases.
```

**Paint inventory options:**
- [F] Full inventory (list all paints)
- [B] Basics only (list primary/secondary colors, metallics, washes)
- [N] None / Start fresh
- [L] Load from previous schemes

**If user provides inventory:**
- Parse paint brands (Citadel, Vallejo, Army Painter, etc.)
- Categorize by type (base, layer, contrast, wash, metallic)
- Note special paints (technical, effects)

**Example input:**
```
I have:
- Citadel: Leadbelcher, Agrax Earthshade, Nuln Oil
- Vallejo: Black, White, Red
- Army Painter: Speedpaints starter set
```

**Parse and confirm:**
```
Got it! You have:
- 2 metallics (Leadbelcher)
- 2 washes (Agrax, Nuln Oil)
- 3 base colors (Black, White, Red)
- Speedpaints set (~12 contrast paints)

Paint Collection Size: Small (~17 paints)
```

**Save inventory** to `brushmaster-sidecar/techniques.md`

**Output:** Paint inventory profile

---

### Step 3: Budget & Purchase Willingness

**Ask about new paint budget:**
```
How many new paints are you willing to buy for this scheme?
```

Options:
- **0** - Use only what I have
- **1-3** - Minimal purchases (fill gaps)
- **4-6** - Moderate purchases (complete scheme)
- **7-10** - Full investment (premium scheme)
- **Unlimited** - Best possible scheme, cost no object

**Brand preferences:**
- Preferred brand? (Citadel/Vallejo/Army Painter/No preference)
- Budget per paint? ($4-8 typical range)

**Calculate budget:**
```
Budget Summary:
- Willing to buy: 4-6 paints
- Preferred brand: Citadel
- Estimated cost: $24-48
```

**Output:** Budget constraints

---

### Step 4: Color Palette Constraints

**Ask about complexity:**
```
How many total paints should your scheme use?
(More paints = more visual interest but longer painting time)
```

Options:
- **Minimal (3-4)** - Fast, simple schemes
- **Standard (5-7)** - Balanced detail and speed
- **Detailed (8-10)** - Rich, layered schemes
- **Complex (11+)** - Maximum visual impact

**Complexity preference:**
- **Simple** - 2-3 colors max per model area
- **Moderate** - Highlight/shade variations
- **Complex** - Multiple layers, glazes, effects

**Match to skill level:**
- Warn if complexity exceeds skill level
- Suggest appropriate range

**Output:** Palette constraints (total paints, complexity)

---

### Step 5: Faction & Lore Accuracy Check

**Identify faction:**
```
What faction/army are you painting?
```

**Query Wahapedia** for faction info via `query-wahapedia`:
```yaml
query: "{faction_name} color scheme"
category: "factions"
```

**MULTI-AGENT COLLABORATION:**

**Call Lorekeeper agent** for canonical colors:
```
🔄 Consulting Lorekeeper for faction lore...

[Execute: Load Lorekeeper agent context]
[Query: "What are the canonical color schemes for {faction_name}?"]
```

**Lorekeeper provides:**
- Official faction colors from codex
- Notable sub-factions and their schemes
- Lore reasoning for color choices
- Historical context for heraldry

**Example Lorekeeper response:**
```
📜 Lorekeeper reporting:

Ultramarines (Space Marines):
- Primary: Ultramarine Blue (Macragge Blue)
- Secondary: White/Bone (Ceramite White)
- Trim: Gold (Retributor Armor)
- Details: Red (Mephiston Red)

Lore: Colors represent honor and nobility of Macragge. Blue symbolizes
Guilliman's strategic brilliance, gold shows veteran status, white for purity.

Common Variants:
- Scions of Guilliman: Lighter blue, more white
- Veteran squads: Additional gold trim
- Honour Guard: White helmets
```

**Ask user about lore accuracy:**
```
📜 Lorekeeper has identified the canonical scheme above.

How important is lore accuracy?
[S] Strict - Follow canon exactly
[F] Flexible - Inspired by canon, some changes okay
[C] Custom - Original scheme (note: may not "read" as this faction)
```

**If Flexible or Custom:**
```
Which lore elements do you want to preserve?
- [ ] Primary color (blue)
- [ ] Trim color (gold)
- [ ] Faction iconography colors
- [ ] None - completely custom
```

**Output:** Faction info + lore accuracy requirements

---

### Step 6: Generate Paint Scheme

**Synthesize all constraints:**
- Skill level + techniques
- Paint inventory
- Budget (paints to buy)
- Palette size
- Lore requirements

**Design algorithm:**

1. **Start with lore colors** (if strict/flexible)
2. **Map to user's existing paints** (minimize purchases)
3. **Fill gaps with budget purchases**
4. **Suggest alternatives** from user's collection
5. **Apply color theory** (complementary, analogous)
6. **Match to skill level** (complexity check)
7. **Generate 3-TIER SCHEME** (Speed/Standard/Advanced)

---

## 🎨 3-TIER SCHEME APPROACH (FORMALIZED)

**CRITICAL: All paint schemes MUST provide three tiers of complexity**

This allows beginners to start fast and grow their skills progressively.

### **TIER 1: SPEED PAINT** (Beginner Start Here)
**Goal:** Tabletop ready FAST - 30-45min per model
- Base colors only
- Washes for automatic shading
- Minimal highlighting (optional)
- Perfect for: Batch painting troops, getting army on table quickly

**Techniques:**
- Basecoating
- Washing/shading
- (Optional) Drybrushing for quick highlights

**Time Estimate:** Calculate based on army size from Step 0
- Example: 30 models × 40min = 20 hours total

### **TIER 2: STANDARD** (Add When Comfortable)
**Goal:** Great tabletop quality - 45-75min per model
- Everything from Tier 1
- PLUS: Edge highlighting
- PLUS: Layering on armor
- Perfect for: Once user has painted 5-10 models and wants more

**Techniques:**
- All Tier 1 techniques
- Edge highlighting (THE technique for crisp models)
- Layering for smooth transitions
- (Optional) Glazing for color shifts

**Time Estimate:** +15-30min per model over Tier 1

### **TIER 3: ADVANCED** (Future You / Characters)
**Goal:** Display quality - 90-120+ min per model
- Everything from Tier 2
- PLUS: Smooth blending
- PLUS: Advanced effects (NMM, OSL, battle damage)
- PLUS: Freehand details
- Perfect for: Characters, centerpiece models, showcase pieces

**Techniques:**
- All Tier 1 + 2 techniques
- Wet blending
- NMM (Non-Metallic Metal)
- OSL (Object Source Lighting)
- Battle damage/weathering
- Freehand iconography

**Time Estimate:** 2-4+ hours per model

---

## Scheme Presentation Format

**Generate scheme in this structure:**
```markdown
# Paint Scheme: Ultramarines (Lore-Flexible)

## Color Palette (6 paints - 2 to buy)

### PRIMARY: Armor
- **Base:** Macragge Blue (BUY - Citadel)
- **Shade:** Nuln Oil (HAVE ✓)
- **Highlight:** Calgar Blue (BUY - Citadel) OR use White mix

### SECONDARY: Trim
- **Base:** Retributor Armor (SUBSTITUTE: Use Leadbelcher + Brown wash)
- **Shade:** Agrax Earthshade (HAVE ✓)

### DETAILS: Cloth & Accents
- **Red Details:** Use your Vallejo Red (HAVE ✓)
- **White/Bone:** Use your Vallejo White (HAVE ✓)

## Shopping List (2 paints = ~$8)
1. Citadel Macragge Blue (Base) - $4.55
2. Citadel Calgar Blue (Layer) - $4.55
Total: ~$9.10

## Application Guide

### Step 1: Prime
- Black or Grey Sphex primer

### Step 2: Armor (Blue)
1. Base coat: Macragge Blue (2 thin coats)
2. Shade: Nuln Oil in recesses only
3. Layer: Macragge Blue on raised areas
4. Highlight: Calgar Blue on edges

### Step 3: Trim (Gold)
1. Base: Leadbelcher (your metallic)
2. Wash: Agrax Earthshade (creates bronze/gold tone)
3. Highlight: Leadbelcher on raised edges

### Step 4: Details
- Cloth/Parchment: White + Agrax = bone color
- Wax seals: Vallejo Red
- Lenses: Red + White dot

### Step 5: Base
- (Recommendations based on preference)

## Techniques Used
✓ Basecoating (beginner friendly)
✓ Shade washing (easy depth)
✓ Edge highlighting (tabletop standard)

## Time Estimate
~45-60 minutes per infantry model (tabletop quality)

## Lore Accuracy
📜 Based on canonical Ultramarines scheme with budget-friendly substitutions.
- Primary blue: ✓ Lore accurate
- Trim: ~80% accurate (bronze tone vs pure gold)
- Details: ✓ Lore accurate

Lorekeeper notes: "Close enough to 'read' as Ultramarines at tabletop
distance. The bronze trim actually evokes younger companies."
```

**Include Painting Roadmap (if army list linked from Step 0):**
```markdown
## 🎯 Your Painting Roadmap

### Phase 1: Speed Paint Your Army (Tier 1)
Paint these first to get tabletop-ready quickly:
- All {count} Troops units (Intercessors, Infiltrators, etc.)
- {count} Fast Attack / Heavy Support units
**Goal:** Fully painted army in ~{hours} hours total
**Batch painting:** Do 5-10 models at once for efficiency

### Phase 2: Level Up (Add Tier 2)
Go back and upgrade quality:
- Add edge highlights to {count} troops
- Practice on "safe" models before characters
**Goal:** Learn edge highlighting on forgiving models

### Phase 3: Showcase Characters (Tier 3)
Paint your centerpieces last:
- HQ Characters (Captain, Librarian, etc.)
- Elite units or special models
- Dreadnoughts / Vehicles
**Goal:** Display-worthy showcase pieces
```

**Present alternatives:**
```
Want to see alternatives?
[A] All new paints (no constraints)
[B] Budget scheme (0 new paints, use what you have)
[C] Custom colors (move away from lore)
```

**Output:** Complete 3-tier paint scheme with roadmap

---

### Step 7: Visual Examples & References

**Provide reference guidance:**
```
Visual References for This Scheme:

📸 Official Examples:
- Games Workshop: Ultramarines Painting Guide
- Warhammer TV: "How to Paint Ultramarines"
- 'Eavy Metal: Codex Ultramarines showcase

🎨 Community Examples:
- Search: "Ultramarines Macragge Blue tutorial"
- Reddit r/Warhammer40k: Ultramarines showcase tag
- Instagram: #ultramarines #spacemarines

🖌️ Color Swatch Preview:
Imagine: Deep blue armor, darker blue recesses, lighter blue edges,
bronze-gold trim, white details. Clean, regal, military aesthetic.
```

**Test model recommendation:**
```
💡 Recommended Test Model:
Paint one Intercessor or Tactical Marine first to verify:
- Color balance (blue vs gold ratio)
- Highlight visibility
- Technique comfort level

This prevents committing to a scheme you don't enjoy!
```

**Tabletop appearance:**
```
Expected Tabletop Look:
From 3 feet away, your army will:
- "Read" clearly as Ultramarines
- Blue will dominate (70% coverage)
- Gold trim will provide visual "pop"
- Unit cohesion from consistent scheme

Army Coherence: This scheme works across all unit types (infantry,
vehicles, characters) with minor variations for rank/role.
```

**Output:** Reference guidance and expectations

---

### Step 8: Save Scheme

**Generate scheme file:**

Filename: `{faction}_{date}_scheme.md`

Example: `ultramarines_2025-12-18_scheme.md`

**Save to:** `brushmaster-sidecar/schemes/ultramarines_2025-12-18_scheme.md`

Content:
```markdown
# Ultramarines Paint Scheme
Created: 2025-12-18
Quality Level: Tabletop Standard
Skill Level: Beginner-Intermediate

## User Preferences
- Techniques: Basecoating, Washing, Edge Highlighting
- Paint Count: 6 total (2 to buy)
- Budget: $9.10
- Lore Accuracy: Flexible

## Color Palette
[Full scheme from Step 6]

## Paint Inventory Snapshot
[Paints owned at time of creation]

## Application Steps
[Step-by-step from Step 6]

## Lorekeeper Notes
[Lore validation from Step 5]

## Test Results
[Leave blank for user to add notes after test model]
```

**Update sidecar files:**
- `brushmaster-sidecar/projects.md` - Add to active projects
- `brushmaster-sidecar/techniques.md` - Update paint inventory

**OPTIONAL: Create Unified Project (if army list linked):**

Ask user:
```
Would you like me to create a unified hobby project to track your painting progress?

This will link your army list + paint scheme and let you:
- Track models painted over time
- Log painting sessions with notes
- See progress toward completion
- Resume project anytime with "continue my {project_name}"

[Y] Yes, create project
[N] No, just save the scheme
```

If Yes:
- Execute `track-project-progress` task:
  ```yaml
  project_name: "{faction} {points}pt Army"
  project_type: "painting"
  action: "create"
  linked_army_list: "{path to army list}"
  linked_paint_scheme: "{path to this scheme}"
  ```
- Display project created message
- Show how to resume project

**Present completion:**
```
✅ Paint Scheme Saved!

📁 Saved to: brushmaster-sidecar/schemes/ultramarines_2025-12-18_scheme.md
💰 Shopping list: 2 paints ($9.10)
📜 Lore validated by Lorekeeper
🎨 Ready to paint!

Next Steps:
[S] Show shopping list again
[T] Get painting tutorial for specific technique
[L] Learn more lore (transition to Lorekeeper)
[X] Exit workflow
```

**User options:**
- Review shopping list
- Request technique tutorial (trigger Brushmaster prompts)
- Explore lore (transition to Lorekeeper agent)
- Exit

**Output:** Saved scheme + next action options

---

## Multi-Agent Collaboration

**Calling Lorekeeper:**

The workflow uses **agent-to-agent communication** in Step 5:

```
[Pause current workflow]
[Execute: Load Lorekeeper agent]
[Provide context: faction, user's lore accuracy preference]
[Query: Canonical colors, sub-faction variants, lore reasoning]
[Receive: Lorekeeper's response]
[Resume workflow with lore data]
```

**Benefits:**
- Authoritative lore information
- Historical context for colors
- Sub-faction variants
- Richer narrative for user's scheme

---

## Error Handling

**Lorekeeper unavailable:**
- Fall back to Wahapedia query for basic faction colors
- Warn user lore validation is limited
- Offer to revisit later

**No paints in inventory:**
- Assume complete beginner
- Recommend starter paint sets
- Provide budget-conscious schemes

**Budget too restrictive:**
- Show minimum viable scheme
- Explain trade-offs
- Offer to revisit with higher budget

**Faction not found:**
- Ask for clarification
- Suggest closest match
- Offer custom color scheme (non-lore)

## Data Flow

```
User Input (preferences, inventory, faction)
    ↓
Query Wahapedia (faction data)
    ↓
Call Lorekeeper Agent (lore validation)
    ↓
Generate Scheme (synthesis)
    ↓
Save to Sidecar (persistence)
    ↓
Output (complete scheme + references)
```

## Integration Points

**Tasks Used:**
- `query-wahapedia` - Faction info and base colors

**Agents Involved:**
- **Brushmaster** - Primary agent running this workflow
- **Lorekeeper** - Lore validation and color justification (called in Step 5)

**Sidecar Files:**
- `brushmaster-sidecar/schemes/{faction}_{date}_scheme.md` - Saved schemes
- `brushmaster-sidecar/projects.md` - Active painting projects
- `brushmaster-sidecar/techniques.md` - Paint inventory and preferences

## Future Enhancements

- Image generation (AI mockup of scheme)
- Color palette visualizer
- Paint compatibility checker
- Batch scheme generation (whole army roles)
- Community scheme database
- Track actual painting time vs estimates

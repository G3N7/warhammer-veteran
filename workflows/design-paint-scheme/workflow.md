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

**Generate scheme:**
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

**Present alternatives:**
```
Want to see alternatives?
[A] All new paints (no constraints)
[B] Budget scheme (0 new paints, use what you have)
[C] Custom colors (move away from lore)
```

**Output:** Complete paint scheme with rationale

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

---
name: warhammer-40k-design-paint-scheme
description: Guided workflow to design paint schemes with lore validation and paint inventory lookup. Use when the user says "design a paint scheme", "help me pick colors", or Brushmaster triggers the design workflow.
---

# Design Paint Scheme Workflow

Interactive paint scheme designer with lore validation, budget optimization, and 3-tier complexity (Speed/Standard/Advanced).

## Prerequisites

These skills MUST be available and used throughout:
- `warhammer-40k-paint-data` — for ALL paint name lookups (never from memory)
- `warhammer-40k-army-data` — for army context and faction data

## Step 1: Import Army Context (Optional)

Check if the user has an army list to reference:
1. Read `_bmad-output/warhammer-40k/agents/tacticus-sidecar/lists.md` for saved lists
2. If linked: extract faction, points, unit counts, model types
3. Calculate total models to paint and display breakdown

## Step 2: Gather Preferences

Ask the user:
1. **Faction/Unit:** What are we painting?
2. **Skill Level:** Beginner / Intermediate / Advanced?
3. **Style:** Lore-accurate / Custom / Speed paint?
4. **Budget:** Use existing collection / Buy new / Mix?
5. **Time:** Speed batch / Standard quality / Competition level?

## Step 3: Load Paint Inventory

**DETERMINISTIC — no paint names from memory.**

1. Use `warhammer-40k-paint-data` to read:
   - `_bmad/_config/custom/warhammer-40k/data/paints/army-painter-warpaints.json`
   - `_bmad/_config/custom/warhammer-40k/data/paints/army-painter-speedpaints.json`
2. Check user's Brushmaster sidecar for existing schemes:
   - `_bmad-output/warhammer-40k/agents/brushmaster-sidecar/schemes/`

## Step 4: Lore Color Check

If lore-accurate style requested:
1. Use `warhammer-40k-army-data` to check faction data
2. Check `_bmad-output/warhammer-40k/shared/retcon-registry.yaml` for lore changes
3. Note canonical faction colors with sources
4. Flag any lore-inaccurate choices

## Step 5: Generate 3-Tier Scheme

Design three complexity levels:

### Speed Tier (Beginner/Batch)
- Primer + 2-3 speedpaints + 1 drybrush + basing
- Target: 15-30 min per model
- All paint names from inventory JSON with hex codes

### Standard Tier (Intermediate)
- Base coat + wash + layer + edge highlight + details
- Target: 45-90 min per model
- Full paint list with alternatives

### Advanced Tier (Competition)
- Multiple highlight stages + glazing + OSL/NMM if applicable
- Target: 2+ hours per model
- Complete technique descriptions

For each tier, include:
- **Color swatches**: Paint name + hex code from JSON
- **Application order**: Step-by-step sequence
- **Paint list**: Exact names from inventory, mark any [UNVERIFIED]

## Step 6: Save Scheme

Save to `_bmad-output/warhammer-40k/agents/brushmaster-sidecar/schemes/{faction}_{date}_scheme.md`

## Anti-Hallucination Checkpoints

- [ ] Every paint name verified against JSON inventory
- [ ] Hex codes included for all colors
- [ ] Lore accuracy checked against retcon registry
- [ ] No discontinued paint range names (Warpaints → Warpaints Fanatic)
- [ ] Sources cited for all factual claims

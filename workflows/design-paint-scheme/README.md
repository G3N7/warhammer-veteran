# Design Paint Scheme Workflow

## Purpose
Interactive paint scheme designer that considers user's painting style preferences, paint collection, budget, and lore accuracy. Collaborates with Lorekeeper agent for faction color validation.

## Trigger
DPS (from Brushmaster agent menu - needs to be added)

## Workflow Steps
1. **Gather Painting Preferences**
   - Ask about painting style (speed paint/tabletop/display quality)
   - Determine skill level (beginner/intermediate/advanced)
   - Identify preferred techniques (drybrushing/layering/contrast paints/etc.)

2. **Inventory Current Paints**
   - Ask what paints user currently owns (brands, colors)
   - Identify paint collection size
   - Note any special paints (metallics, washes, contrast)

3. **Budget & Purchase Willingness**
   - How many new paints willing to buy? (0/1-3/4-6/unlimited)
   - Budget constraints
   - Brand preferences

4. **Color Palette Constraints**
   - Total number of paints to use in scheme (3/5/7/10+)
   - Complexity preference (simple/moderate/complex)

5. **Faction & Lore Accuracy Check**
   - Identify faction/army being painted
   - **Consult Lorekeeper agent** for canonical color schemes
   - Ask user: strict lore accuracy vs custom scheme?
   - If custom: note what lore elements to preserve

6. **Generate Paint Scheme**
   - Design color palette based on all inputs
   - Provide specific paint recommendations (with alternatives)
   - Show application guide (base/shade/highlight for each area)
   - Include lore reasoning for colors

7. **Visual Examples & References**
   - Suggest visual references
   - Describe expected tabletop appearance
   - Provide test model recommendations

8. **Save Scheme**
   - Save complete scheme to brushmaster-sidecar
   - Include paint list, techniques, lore notes

## Inputs
- User painting preferences and skill level
- Current paint inventory
- Budget and purchase willingness
- Desired complexity and color count
- Faction and lore accuracy requirements

## Outputs
- Complete paint scheme with specific color recommendations
- Step-by-step application guide
- Shopping list (if new paints needed)
- Lore-accurate color justification
- Saved scheme to brushmaster-sidecar/schemes/

## Special Features
- **Multi-agent collaboration:** Calls Lorekeeper for faction color validation
- **Budget optimization:** Recommends schemes within paint count constraints
- **Paint substitution:** Suggests alternatives from user's existing collection
- **Lore flexibility:** Balances canon accuracy with creative freedom

## Implementation Status
Placeholder - Full workflow to be created using create-workflow workflow

## Notes
This workflow requires integration with Lorekeeper agent for lore accuracy checks. The workflow should use Party Mode or agent-to-agent communication to validate faction colors.

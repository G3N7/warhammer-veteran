# Convert Paint Colors Workflow

## Metadata
- **ID:** convert-paint-colors
- **Name:** Paint Color Conversion
- **Description:** Convert paint colors between brands (Army Painter, Citadel, Vallejo, etc.) using hex color matching
- **Agent:** Brushmaster
- **Category:** Hobby Utility

---

## Purpose

Convert paint recommendations from Army Painter (the default) to other major miniature paint brands. Uses hex color codes from the paint inventory to find the closest matches.

---

## Step 1: Identify Conversion Direction

**Action:** Determine what paints need to be converted and to which brand.

**Ask User:**
- What colors do you need to convert?
- Which paint brand do you want to convert TO?

**Common Conversion Targets:**
- **Citadel (Games Workshop)** - Most widely available, GW store compatibility
- **Vallejo Game Color** - Great value, dropper bottles
- **Vallejo Model Color** - More muted/realistic tones
- **Scale75** - Premium quality, artist-grade
- **AK Interactive** - Weathering specialists
- **Reaper** - Budget-friendly, wide range

---

## Step 2: Load Source Colors

**Action:** Read the Army Painter color inventories to get exact hex codes.

**Reference Files:**
- `{project-root}/data/paints/army-painter-warpaints.json`
- `{project-root}/data/paints/army-painter-speedpaints.json`

**Extract for each paint:**
- Paint name
- Hex code
- Category (base, layer, metallic, wash, effect)
- Usage notes

---

## Step 3: Research Target Brand Equivalents

**Action:** For each source color, find the closest match in the target brand.

**Matching Priority:**
1. **Exact hex match** - Same color value (rare but ideal)
2. **Near hex match** - Within ~10% color difference
3. **Functional match** - Same role in painting (e.g., both are "skin wash")
4. **Closest available** - Best approximation with notes on differences

**Web Search Pattern:**
- "[Army Painter Color] to Citadel equivalent"
- "[Target Brand] color chart hex codes"
- "Miniature paint conversion chart [Target Brand]"

---

## Step 4: Generate Conversion Table

**Action:** Create a formatted conversion table with visual color references.

**Output Format:**

```markdown
# Paint Conversion: Army Painter → [Target Brand]

## Conversion Table

| Army Painter | Hex | [Target Brand] Equivalent | Hex | Match Quality |
|--------------|-----|---------------------------|-----|---------------|
| Matt White (#FFFFFF) | #FFFFFF | White Scar | #FFFFFF | Exact |
| Greedy Gold (#FFD700) | #FFD700 | Retributor Armour | #B5802A | Near (darker) |

## Notes

### Differences to Expect
- [Note any systematic differences between brands]
- [Coverage, consistency, bottle type differences]

### Colors with No Good Match
- [List any problematic conversions]
- [Suggest mixing alternatives]
```

---

## Step 5: Provide Purchasing Guidance

**Action:** Give practical advice for acquiring the converted paints.

**Include:**
- Where to buy the target brand
- Cost comparison (Army Painter vs target brand)
- Any starter sets that cover multiple needed colors
- Which colors are "must-have" vs "nice-to-have" for mixing

---

## Output Deliverable

A markdown file with:
1. Complete conversion table with hex codes
2. Visual color swatches (hex codes inline)
3. Match quality ratings
4. Notes on differences
5. Purchasing recommendations

**Save Location:** `{project-root}/_bmad/warhammer-40k/agents/brushmaster-sidecar/conversions/[source]-to-[target].md`

---

## Integration

This workflow can be triggered from:
- Brushmaster agent menu
- Design Paint Scheme workflow (when user prefers different brand)
- Any painting tutorial (when user asks for alternatives)

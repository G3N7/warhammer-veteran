# Cross-Agent Validation Workflow

**Purpose:** Independent verification of agent output to catch hallucinations, stale data, and cross-agent inconsistencies.

**Trigger:** Run after any agent produces substantive output (army list, rules ruling, lore answer, paint scheme).

---

## When to Use This Workflow

- After Tacticus builds or modifies an army list
- After Arbitrator makes a complex ruling
- When any agent's output will be saved to a file
- When user explicitly requests verification
- Before tournament-critical decisions

---

## Step 1: Identify Claims to Verify

Scan the agent's output for:

| Claim Type | How to Verify | Priority |
|-----------|---------------|----------|
| Points values | Check datasheet cache, verify math | BLOCKING |
| Unit stats (M/T/Sv/W) | Check datasheet cache | BLOCKING |
| Wargear options | Check datasheet cache weapons arrays | BLOCKING |
| Leader attachments | Check cache.leads arrays | BLOCKING |
| Enhancement names | Check validation-rules.yaml detachments | BLOCKING |
| Enhancement eligibility | Verify CHARACTER keyword, not EPIC HERO | BLOCKING |
| Rule of Three | Count units by datasheet name | BLOCKING |
| Detachment rules text | Check Wahapedia or validation-rules.yaml | HIGH |
| Faction ability text | Check validation-rules.yaml faction_abilities | HIGH |
| Rules citations | Verify Wahapedia section exists | HIGH |
| Lore claims | Check for [UNVERIFIED] tag presence | MEDIUM |
| Paint names | Check paint DB JSON files | MEDIUM |
| Product recommendations | Web search to verify product exists | LOW |

---

## Step 2: Source Verification

For each claim identified in Step 1:

### Points/Stats/Wargear (BLOCKING)
1. Load datasheet cache: `{faction}.compact.json`
2. For each unit: compare output value vs cache value
3. If mismatch: **FLAG AS ERROR** with correct value from cache
4. If cache missing: run `--add-unit` to populate, then verify

### Enhancement/Detachment Rules (BLOCKING)
1. Check validation-rules.yaml → detachments section
2. Verify enhancement name exists for the specified detachment
3. Verify enhancement is assigned to generic CHARACTER (not EPIC HERO)
4. If not found in validation-rules.yaml: web search Wahapedia

### Rules Citations (HIGH)
1. Check if cited Wahapedia section exists
2. Verify quoted text matches (if quote provided)
3. Check FAQ registry for any overrides

### Lore/Creative Content (MEDIUM)
1. Verify [UNVERIFIED] tags present on training-data claims
2. Check for edition-specific context (is this 10th Ed lore?)
3. Flag any claims presented as fact without citation

---

## Step 3: Math Verification

For army lists specifically:

1. **Re-add all points from scratch** (independent of original calculation)
2. **Compare totals** - must match within 0pts
3. **Verify against limit** - must be ≤ game size cap
4. **Check Rule of Three** - count each datasheet independently
5. **Verify enhancement count** - max 1 at 1000pts, max 3 at 2000pts

---

## Step 4: Consistency Check

Cross-reference different sections of the output:

- [ ] Every unit in prose sections exists in the army table
- [ ] Model counts in tactics match army table quantities
- [ ] Abilities claimed in tactics exist on unit datasheets
- [ ] Keywords claimed exist on unit datasheets
- [ ] Assembly guide loadouts match army table loadouts
- [ ] Points in assembly summary match army table

---

## Step 5: Freshness Audit

Check data freshness:

- [ ] Datasheet cache: less than 30 days old?
- [ ] Knowledge base files: have `<!-- VERIFIED: -->` header?
- [ ] Meta claims: dated and qualified ("as of [date]")?
- [ ] FAQ citations: include date?

---

## Step 6: Report

Generate a verification report:

```
## VERIFICATION REPORT
**Agent:** [which agent produced the output]
**Date:** [today]
**Data Sources Checked:** [list of caches/files/web searches used]

### BLOCKING Issues (MUST FIX)
- [ ] [Issue description + correct value]

### HIGH Priority Issues
- [ ] [Issue description]

### MEDIUM Priority Issues
- [ ] [Issue description]

### Freshness Warnings
- [ ] [Stale data identified]

### VERDICT: ✅ VERIFIED / ⚠️ NEEDS FIXES / ❌ BLOCKED
```

---

## Integration Points

This workflow can be triggered:
1. **Manually:** User says "verify this" or "audit this"
2. **By Tacticus:** After `[AL] Analyze List` or `[VL] Validate List`
3. **By any agent:** When saving output to a file
4. **In party mode:** Any agent can call for verification of another agent's claims

# Warhammer 40K Agent System — Improvement Plan

**Created:** 2026-04-14
**Status:** In Progress
**Last Updated:** 2026-04-14

## Problem Statement

The BMAD v6.3.0 upgrade broke the Warhammer 40K agent system:

1. **Deleted agent files**: The installer removed `_bmad/warhammer-40k/agents/*.agent.yaml` (full instructions) and `*.yaml` (compact) from the working tree. Only compact copies survive at `_bmad/_config/custom/warhammer-40k/agents/*.yaml` (165 lines vs 585 lines original).
2. **Broken command wrappers**: `.claude/commands/warhammer-40k/agents/*.md` reference `@_bmad/warhammer-40k/agents/{name}.agent.yaml` which no longer exist.
3. **Deleted shared resources**: Hallucination registry, retcon registry, army registry, shared instructions — all deleted from working tree.
4. **No deterministic data skills**: Agents hallucinate unit stats, points, leader attachments instead of querying the actual `army-lists/` data files.
5. **Not registered in manifest**: Warhammer agents missing from `_bmad/_config/agent-manifest.csv`.
6. **Wrong format**: Agents are commands (`.claude/commands/`) instead of skills (`.claude/skills/`) like other BMAD agents.

## Architecture Decision: Skills over Commands

BMAD agents now use the **skill pattern**:
```
.claude/skills/{skill-name}/
  SKILL.md              # Full agent definition + persona + instructions
  bmad-skill-manifest.yaml  # Metadata for discovery
```

Warhammer agents will be migrated from commands → skills to match.

## Implementation Phases

### Phase 1: Deterministic Data Skills ✅ HIGHEST IMPACT
> Agents hallucinate because they have no tool to query real data. Fix this first.

- [x] **1.1** Create `warhammer-40k:army-data` skill — deterministic lookup of:
  - Army list index (what lists exist, factions, points)
  - Unit stats from cheatsheet JSON files
  - Validation rules from `tacticus-sidecar/validation-rules.yaml`
  - Leader attachment legality
  - Points costs
- [x] **1.2** Create `warhammer-40k:paint-data` skill — deterministic lookup of:
  - Paint inventory (Army Painter Warpaints + Speedpaints JSON)
  - Color schemes from brushmaster sidecar
  - Hex codes and paint categories
- [x] **1.3** Restore shared registries to a non-deleted location:
  - `hallucination-registry.yaml` → `_bmad-output/warhammer-40k/shared/`
  - `retcon-registry.yaml` → `_bmad-output/warhammer-40k/shared/`
  - `army-registry.yaml` → `_bmad-output/warhammer-40k/shared/`
  - `user-profile.yaml` → `_bmad-output/warhammer-40k/shared/`

### Phase 2: Migrate Agents to Skill Format
> Convert all 6 agents from broken commands to proper BMAD skills.

- [x] **2.1** Create skill files for each agent:
  - `.claude/skills/warhammer-40k-agents-tacticus/SKILL.md`
  - `.claude/skills/warhammer-40k-agents-arbitrator/SKILL.md`
  - `.claude/skills/warhammer-40k-agents-brushmaster/SKILL.md`
  - `.claude/skills/warhammer-40k-agents-lorekeeper/SKILL.md`
  - `.claude/skills/warhammer-40k-agents-chronicler/SKILL.md`
  - `.claude/skills/warhammer-40k-agents-artisan/SKILL.md`
  - Each gets a `bmad-skill-manifest.yaml`
- [x] **2.2** Port critical content from `.agent.yaml` (git history) into SKILL.md:
  - Anti-hallucination preamble (accuracy-first instructions)
  - Domain-specific validation rules
  - Sidecar loading instructions
  - Menu system (capabilities table linking to skills)
  - Prompt templates
- [x] **2.3** Each agent SKILL.md must reference deterministic skills:
  - Tacticus → `warhammer-40k:army-data` for all unit/points queries
  - Brushmaster → `warhammer-40k:paint-data` for paint lookups
  - Arbitrator → `warhammer-40k:army-data` for rules verification
  - All agents → shared registries for hallucination/retcon checks

### Phase 3: Register in Manifest & Clean Up
> Make agents discoverable by the BMAD system.

- [x] **3.1** Add all 6 agents to `_bmad/_config/agent-manifest.csv`
- [x] **3.2** Remove broken command wrappers from `.claude/commands/warhammer-40k/`
- [x] **3.3** Update `CLAUDE.md` to reflect new file locations
- [ ] **3.4** Clean up git: stage deletions of old `_bmad/warhammer-40k/` files

### Phase 4: Improve Agent Instructions
> Incorporate lessons from hallucination history into skill definitions.

- [x] **4.1** Embed the 13 documented hallucination patterns directly into relevant agent skills
- [x] **4.2** Embed the 5 retcon entries into Lorekeeper skill
- [x] **4.3** Add `STOP AND QUERY` directives — when an agent needs unit data, it MUST use the army-data skill rather than generating from memory
- [x] **4.4** Simplify shared instructions — moved into per-agent skills with only what each agent needs

### Phase 5: Future Enhancements (Backlog)
> Not blocking, but valuable.

- [ ] **5.1** Create `warhammer-40k:wahapedia-cache` skill to manage cached web lookups
- [ ] **5.2** Wire up New Recruit MCP server with credentials flow
- [ ] **5.3** Create workflow skills (Build Army List, Design Paint Scheme) as proper BMAD skills
- [ ] **5.4** Add more cheatsheet JSON files for non-Space-Wolves factions
- [ ] **5.5** Create `warhammer-40k:validate-list` skill wrapping validation-rules.yaml

## Key Files Reference

| Purpose | Location |
|---------|----------|
| Army lists (source of truth) | `army-lists/{faction}/*.md` |
| Cheatsheet JSON | `army-lists/{faction}/*.cheatsheet.json` |
| Agent sidecars | `_bmad-output/warhammer-40k/agents/{name}-sidecar/` |
| Shared registries | `_bmad-output/warhammer-40k/shared/` |
| Agent skills | `.claude/skills/warhammer-40k-agents-{name}/` |
| Data skills | `.claude/skills/warhammer-40k-army-data/` |
| Paint data | `_bmad-output/warhammer-40k/agents/brushmaster-sidecar/` |
| Validation rules | `_bmad-output/warhammer-40k/agents/tacticus-sidecar/validation-rules.yaml` |
| Agent manifest | `_bmad/_config/agent-manifest.csv` |

## Progress Log

| Date | Phase | Items | Notes |
|------|-------|-------|-------|
| 2026-04-14 | Research | Complete | Full audit of all agents, data, history |
| 2026-04-14 | Phase 1.1 | DONE | Created `warhammer-40k-army-data` skill |
| 2026-04-14 | Phase 1.2 | DONE | Created `warhammer-40k-paint-data` skill |
| 2026-04-14 | Phase 1.3 | DONE | Restored all 4 shared registries to `_bmad-output/warhammer-40k/shared/` |
| 2026-04-14 | Phase 2.1 | DONE | Created all 6 agent skills in `.claude/skills/` |
| 2026-04-14 | Phase 2.2 | DONE | Ported anti-hallucination rules, principles, prompt templates |
| 2026-04-14 | Phase 2.3 | DONE | Each agent references deterministic data skills |
| 2026-04-14 | Phase 3.1 | DONE | Added all 6 agents to `agent-manifest.csv` |
| 2026-04-14 | Phase 3.2 | DONE | Removed broken command wrappers |
| 2026-04-14 | Phase 3.3 | DONE | Updated `CLAUDE.md` with new file locations |
| 2026-04-14 | Phase 4.1 | DONE | Embedded 13 hallucination patterns into relevant agent skills |
| 2026-04-14 | Phase 4.2 | DONE | Embedded 5 retcon entries into Lorekeeper skill |
| 2026-04-14 | Phase 4.3 | DONE | Added STOP AND QUERY directive tables to all 6 agents |
| 2026-04-14 | Phase 4.4 | DONE | Shared instructions folded into per-agent skills |

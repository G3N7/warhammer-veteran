# Warhammer Veteran - Phase 2 Enhancement Plan

**Created:** 2025-12-19
**Status:** In Progress
**Priority:** P1 - High Value Quick Wins

---

## Overview

Based on user testing session with Tacticus → Brushmaster workflow, identified improvements for better project continuity and user experience.

---

## Requirements Discovered

### 1. Persistent Project Tracking
**User Request:** "Create essentially a journal so we can always pickup where we left off"

**Gap:** No unified project tracking across agents (army list + paint scheme + progress)

**Solution:** Track Project Progress task

### 2. Paint Set Presets
**User Need:** "I bought the army painter starter set, can the scheme only use those"

**Gap:** Generic paint inventory step, not optimized for common paint sets

**Solution:** Add preset paint collections to Design Paint Scheme workflow

### 3. Tiered Skill Building
**User Profile:** "Beginner with ambition so I will want to build"

**Success:** Brushmaster created 3-tier approach (Speed → Standard → Advanced)

**Solution:** Document as best practice, formalize in workflow

### 4. Session Retrospective
**User Request:** "Extract new requirements from both conversations"

**Gap:** No systematic way to analyze sessions for improvements

**Solution:** New workflow for requirement extraction

---

## Phase 2 Implementation Tasks

### ✅ Task 1: Create Track Project Progress Task
**File:** `tasks/track-project-progress.md`
**Purpose:** Unified project file linking army list + paint scheme + painting progress
**Features:**
- Create project file with all linked data
- Session logging
- Progress tracking (models completed, time spent)
- Resume project context
- Milestone tracking

**Status:** ⬜ Not Started

---

### ✅ Task 2: Update Design Paint Scheme Workflow
**File:** `workflows/design-paint-scheme/workflow.md`
**Enhancements:**
- Add Step 1.5: Paint Set Presets (Army Painter, Citadel, Vallejo)
- Formalize 3-tier complexity approach (Speed/Standard/Advanced)
- Add Step 0: Import army list data (if available from Tacticus)
- Auto-calculate total models to paint
- Suggest batch painting order

**Status:** ⬜ Not Started

---

### ✅ Task 3: Create Session Retrospective Workflow
**File:** `workflows/session-retrospective/workflow.md`
**Purpose:** Extract learnings and requirements from completed sessions
**Features:**
- Analyze conversation history
- Identify user preferences
- Note workflow gaps
- Generate improvement suggestions
- Update agent memories

**Status:** ⬜ Not Started

---

### ✅ Task 4: Update Brushmaster Agent
**File:** `agents/brushmaster.yaml`
**Changes:**
- Add menu trigger for Track Project Progress
- Add menu trigger for Session Retrospective
- Update embedded prompts to reference tiered complexity

**Status:** ⬜ Not Started

---

### ✅ Task 5: Update Documentation
**Files:** `README.md`, `TODO.md`, `TESTING.md`
**Changes:**
- Document new Track Project Progress task
- Document Session Retrospective workflow
- Update feature list
- Move Phase 2 items to completed

**Status:** ⬜ Not Started

---

## Success Criteria

- [ ] User can resume "Ultramarines project" and see army list + paint scheme + progress
- [ ] Design Paint Scheme offers "Army Painter Starter Set" preset
- [ ] All painting guides offer 3-tier complexity
- [ ] Session Retrospective can analyze conversations and extract requirements
- [ ] All changes committed with proper git messages
- [ ] Documentation updated

---

## Implementation Order

1. Track Project Progress task (highest user value)
2. Update Design Paint Scheme workflow (user's immediate need)
3. Session Retrospective workflow (meta-improvement)
4. Update Brushmaster agent (integration)
5. Update documentation (finalize)

---

## Git Commit Strategy

Commit after each task completion:
1. "Add Track Project Progress task for unified project tracking"
2. "Enhance Design Paint Scheme workflow with presets and tiers"
3. "Add Session Retrospective workflow for requirement extraction"
4. "Update Brushmaster agent with new workflow triggers"
5. "Update Phase 2 documentation and feature list"

---

## Notes

- Keep commits focused and atomic
- Test each enhancement before committing
- Update TESTING.md with validation steps
- User wants token management - commit frequently

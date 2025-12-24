---
name: Paint Project
description: Guide a complete painting project from color scheme design through completion tracking
web_bundle: false
---

# Paint Project Workflow

**Goal:** Create and track a complete miniature painting project, from concept to completion.

**Your Role:** Collaborative hobby mentor guiding users through painting projects with practical advice and encouragement.

## WORKFLOW ARCHITECTURE

### Core Principles

- **User-Driven Pace:** Adapt to user's skill level and available time
- **Practical Focus:** Provide actionable steps, not just theory
- **Progress Celebration:** Acknowledge milestones and improvements
- **Cross-Agent Integration:** Connect with Tacticus for army lists, Artisan for basing

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read entire step file before execution
- **ALWAYS** follow the exact instructions in the step file
- **ALWAYS** halt at menus and wait for user input
- **NEVER** create mental todo lists from future steps

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read config from {project-root}/_bmad/warhammer-40k/module.yaml and resolve:

- `user_name`, `preferred_faction`, `hobby_focus`

### 2. Agent Context Loading

Load Brushmaster sidecar files for user preferences:
- `{project-root}/_bmad/warhammer-40k/agents/brushmaster-sidecar/memories.md`
- `{project-root}/_bmad/warhammer-40k/agents/brushmaster-sidecar/projects.md`

### 3. Present Project Options

**PAINT PROJECT WORKFLOW**

Welcome! Let's create a painting project together.

**What would you like to paint?**

1. **[SA] Single Army** - Plan painting for an entire army list
2. **[SU] Single Unit** - Focus on one unit or squad
3. **[SM] Single Model** - Paint a character or centerpiece model
4. **[RP] Resume Project** - Continue an existing project

*Select an option to begin...*

---

## STEP 1: PROJECT DEFINITION

Based on user selection:

### For Single Army [SA]
1. Ask: "Do you have an army list already, or should we check with Tacticus?"
2. If list exists: Load it from tacticus-sidecar/lists.md
3. If no list: Recommend consulting Tacticus first, or proceed with general faction painting
4. Identify: Total model count, unit types, centerpiece models

### For Single Unit [SU] or Single Model [SM]
1. Ask: "What model(s) are you painting?"
2. Ask: "What's your experience level with this type of model?"
3. Ask: "Do you have a deadline or is this a leisure project?"

### Project Parameters
Document:
- **Project Name:** [User-provided or auto-generated]
- **Models:** [List of models/units]
- **Skill Level:** [Beginner/Intermediate/Advanced]
- **Timeline:** [Deadline or open-ended]
- **Priority:** [Tabletop ready / Display quality / Competition]

---

## STEP 2: COLOR SCHEME DESIGN

### 2.1 Scheme Exploration

**Options:**

1. **[OS] Official Scheme** - Use a canon faction color scheme
2. **[CS] Custom Scheme** - Design a unique color palette
3. **[ES] Existing Scheme** - Use a scheme already in schemes/ folder

### 2.2 For Official Scheme [OS]
1. Search Wahapedia for faction paint guides
2. Present 2-3 official sub-faction variants
3. List required paints by brand (Citadel, Vallejo, Army Painter)

### 2.3 For Custom Scheme [CS]
Apply color theory principles:
1. **Primary Color:** Main armor/body color
2. **Secondary Color:** Trim, weapons, details (complementary or analogous)
3. **Accent Color:** Eyes, energy effects, spot details (high contrast)
4. **Metal Choice:** Gold, silver, bronze, or NMM approach

Suggest paint names and provide mixing recipes if needed.

### 2.4 Document Scheme

Save to `{project-root}/_bmad/warhammer-40k/agents/brushmaster-sidecar/schemes/{project-name}.md`:

```markdown
# Color Scheme: {Project Name}

## Palette
- **Primary:** [Color] - [Paint name]
- **Secondary:** [Color] - [Paint name]
- **Accent:** [Color] - [Paint name]
- **Metals:** [Type] - [Paint name]

## Recipe
### [Area 1]
1. Base: [Paint]
2. Shade: [Paint]
3. Layer: [Paint]
4. Highlight: [Paint]

### [Area 2]
...
```

---

## STEP 3: PAINTING PLAN

### 3.1 Technique Selection

Based on skill level and priority:

**Beginner / Tabletop Ready:**
- Base coat → Wash → Drybrush → Details
- Estimated time per infantry model: 20-30 min

**Intermediate / Quality Tabletop:**
- Base coat → Wash → Layering → Edge highlights → Details
- Estimated time per infantry model: 45-60 min

**Advanced / Display:**
- Zenithal prime → Glazes → Blending → NMM/OSL → Weathering
- Estimated time per infantry model: 2-4 hours

### 3.2 Batch Planning

For armies/units, recommend batch painting strategy:
1. Group models by similar colors
2. Assembly line by step (all base coats, then all washes, etc.)
3. Identify leader/special models for extra attention

### 3.3 Materials Checklist

Generate shopping list:
- [ ] Paints needed (with alternatives)
- [ ] Brushes required
- [ ] Other supplies (washes, primers, varnish)

---

## STEP 4: PROGRESS TRACKING

### 4.1 Create Project Tracker

Save to `{project-root}/_bmad/warhammer-40k/agents/brushmaster-sidecar/projects.md`:

```markdown
## Project: {Name}
**Started:** {Date}
**Target:** {Deadline or "Open"}
**Status:** In Progress

### Models
| Model | Status | Notes |
|-------|--------|-------|
| [Name] | [ ] Primed / [ ] Base / [ ] Shaded / [ ] Detailed / [ ] Based / [ ] Done | |

### Session Log
- {Date}: Started project, completed priming
```

### 4.2 Session Updates

When user returns with `[RP] Resume Project`:
1. Load project from projects.md
2. Show current status
3. Ask: "What did you work on since last time?"
4. Update tracker
5. Suggest next steps

### 4.3 Completion

When project complete:
1. Celebrate the achievement!
2. Ask for lessons learned
3. Update techniques.md with new skills
4. Archive project as completed
5. Suggest: "Want to share with Tacticus to link this paint job to your army list?"

---

## CROSS-AGENT INTEGRATION

### With Tacticus
- Import army lists for painting projects
- Link painted status to list tracking

### With Artisan
- Coordinate basing themes
- Conversion work before painting

### With Chronicler
- Track painted armies for campaigns
- Crusade unit appearance bonuses

---

## MENU (Available Throughout)

- **[ST] Status** - Show current project progress
- **[UP] Update** - Log painting session progress
- **[SC] Scheme** - View/modify color scheme
- **[TIP] Quick Tip** - Get painting advice for current step
- **[SAVE]** - Save all progress to sidecar files
- **[EXIT]** - Exit workflow (progress auto-saved)

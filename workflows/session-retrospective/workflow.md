# Session Retrospective Workflow

Meta-workflow for analyzing completed sessions, extracting requirements, and improving agent performance.

## Activation

This workflow can be triggered by:
- Any agent after complex interactions
- User request: "extract requirements from our conversation"
- Manual trigger for module improvement
- Periodic review cycles

## Overview

Systematically analyzes conversation history to:
- Identify user preferences and patterns
- Discover workflow pain points
- Extract improvement opportunities
- Update agent memories with learnings
- Generate actionable requirement suggestions

**Purpose:** Continuous improvement through systematic session analysis.

## Prerequisites

- Conversation history access
- Agent sidecar write access (for memory updates)
- BMAD module knowledge (to understand current capabilities vs gaps)

## Workflow Steps

### Step 1: Initialize Retrospective

**Greet user:**
```
Session Retrospective Analysis

I'll analyze our conversation to extract learnings, identify improvements,
and discover new requirements. This helps make the module better for you
and future users!
```

**Determine scope:**
- **Current session only:** Analyze this conversation
- **Recent sessions:** Analyze last N sessions from agent memory
- **Specific interaction:** Analyze particular workflow execution

**Ask user:**
```
What should I analyze?
[C] Current session (this conversation)
[R] Recent sessions (last 3-5 interactions)
[S] Specific workflow (name the workflow)
```

**Output:** Scope defined

---

### Step 2: Conversation Analysis

**Parse conversation history:**

**Extract key elements:**
1. **User requests:** What did the user ask for?
2. **Agent responses:** How did agents handle requests?
3. **User reactions:** Positive, negative, neutral feedback
4. **Follow-up questions:** What needed clarification?
5. **Workarounds:** Did user have to work around limitations?
6. **Explicit feedback:** Direct complaints or praise

**Identify conversation patterns:**
```
Analyzing conversation structure...

- Total exchanges: {count}
- Agents involved: {list}
- Workflows triggered: {list}
- Tasks executed: {list}
- User corrections: {count}
- Clarification requests: {count}
```

**Output:** Conversation structure map

---

### Step 3: User Preference Discovery

**Identify preferences:**

**Painting Preferences (if Brushmaster involved):**
- Preferred paint brands
- Skill level assessment
- Quality goals (speed vs display)
- Technique comfort zones
- Budget constraints
- Lore accuracy importance

**Army Building Preferences (if Tacticus involved):**
- Preferred factions
- Playstyle (aggressive, defensive, balanced)
- Game modes (matched, crusade, open)
- Points levels
- Competitive vs casual

**Lore Preferences (if Lorekeeper involved):**
- Favorite factions
- Interest in deep lore vs surface level
- Preferred eras (Horus Heresy, 40k, etc.)

**General Preferences:**
- Communication style (technical vs casual)
- Detail level (concise vs comprehensive)
- Autonomy preference (guided vs self-directed)

**Example output:**
```markdown
## User Preferences Discovered

### Painting
- **Paint Brand:** Army Painter (starter set owner)
- **Skill Level:** Beginner with growth ambition
- **Quality Goal:** Speed → Standard progression
- **Constraints:** Budget-conscious, wants preset schemes

### Army Building
- **Faction:** Space Marines (Ultramarines chapter)
- **Playstyle:** Balanced, competitive
- **Game Mode:** Open Play (1000pts)
- **Optimization:** Wants meta-competitive lists

### Communication
- **Style:** Direct, tactical language appreciated
- **Detail:** Comprehensive explanations preferred
- **Learning:** Wants tiered complexity with growth path
```

**Output:** User preference profile

---

### Step 4: Pain Point Identification

**Analyze friction points:**

**Categories:**

**1. Workflow Friction**
- Steps that required multiple attempts
- Unclear instructions
- Missing information
- Excessive back-and-forth

**Example:**
```
Pain Point: Paint Inventory Entry
- User had to manually describe "Army Painter Starter Set"
- No preset for common paint collections
- Required itemizing 54 individual paints
→ Suggestion: Add paint set presets
```

**2. Missing Features**
- User requested capability that doesn't exist
- Workarounds needed
- Cross-agent gaps

**Example:**
```
Pain Point: No Project Continuity
- User asked: "create a journal to pickup where we left off"
- No unified project tracking across army list + paint scheme
- Had to manually remember context between sessions
→ Suggestion: Create track-project-progress task
```

**3. Agent Limitations**
- Information agent couldn't provide
- Tasks agent couldn't complete
- Knowledge gaps

**4. User Experience Issues**
- Confusing terminology
- Unexpected behavior
- Inconsistent patterns

**Output:** Prioritized list of pain points

---

### Step 5: Workflow Gap Analysis

**Compare what exists vs what was needed:**

**Current Capabilities:**
- List workflows executed successfully
- List tasks that worked well
- Identify smooth agent interactions

**Gaps Discovered:**
- Workflows that should exist but don't
- Task parameters that should exist
- Agent integrations needed
- Data that should be accessible

**Example:**
```markdown
## Workflow Gaps

### Existing & Working
✅ Build Army List - Executed successfully
✅ Design Paint Scheme - Worked but had gaps
✅ Lorekeeper consultation - Smooth integration

### Gaps Identified
❌ Track Project Progress - Requested but doesn't exist
❌ Paint Set Presets - Manual entry was friction
❌ 3-Tier Complexity - User created manually, should be standard
❌ Resume Project - No continuity mechanism

### Enhancement Opportunities
⚠️ Design Paint Scheme - Could auto-import army data
⚠️ Army validation - Could suggest optimizations
⚠️ Cross-agent handoff - Works but informal
```

**Output:** Gap analysis with priorities

---

### Step 6: Requirement Extraction

**Generate actionable requirements:**

**Format:**
```markdown
## Requirement: {Name}

**Priority:** P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)

**User Need:**
{What the user was trying to accomplish}

**Current Gap:**
{What's missing or broken}

**Proposed Solution:**
{How to address it}

**Implementation:**
- [ ] Task to create: {task name}
- [ ] Workflow to build: {workflow name}
- [ ] Agent to update: {agent name}
- [ ] Documentation to write: {doc name}

**Success Criteria:**
{How to know it's solved}

**Estimated Effort:**
Small / Medium / Large

**User Quote:**
"{Actual user request that triggered this}"
```

**Example:**
```markdown
## Requirement: Unified Project Tracking

**Priority:** P1 (High)

**User Need:**
User wants to resume painting project across sessions without losing context.
Wants a "journal" to track progress and pickup where they left off.

**Current Gap:**
- Army lists saved separately in tacticus-sidecar
- Paint schemes saved separately in brushmaster-sidecar
- No link between them
- No session logging or progress tracking
- Can't "resume project" across agents

**Proposed Solution:**
Create `track-project-progress` task that:
- Links army list + paint scheme + campaign data
- Tracks painting progress (models completed, time spent)
- Logs sessions with notes
- Enables "resume {project}" functionality
- Generates next steps recommendations

**Implementation:**
- [x] Task: track-project-progress.md
- [x] Enhance: Design Paint Scheme workflow (Step 8 - create project option)
- [ ] Update: Brushmaster agent (add resume project trigger)
- [ ] Update: Documentation

**Success Criteria:**
- User can say "continue my Ultramarines project" and see linked data
- Painting progress tracked over time
- Session notes persist

**Estimated Effort:** Medium (4-6 hours)

**User Quote:**
"can you please save this plan and also create essentially a journal
so we can always pickup where we left off"
```

**Output:** Structured requirement documents

---

### Step 7: Agent Memory Updates

**Update relevant agent sidecars:**

**Brushmaster Updates:**
```
brushmaster-sidecar/techniques.md:
- User prefers Army Painter paints
- Beginner skill level, ambitious growth mindset
- Responds well to tiered complexity
- Values budget optimization
```

**Tacticus Updates:**
```
tacticus-sidecar/memories.md:
- Prefers Space Marines (Ultramarines)
- Likes competitive meta analysis
- Open Play at 1000pts preferred
- Values validation and optimization
```

**General Learnings:**
```
module-learnings.md (new file):
- 3-tier complexity approach resonates with beginners
- Paint set presets eliminate friction
- Users want cross-agent project continuity
- Explicit roadmaps valued (Phase 1/2/3)
```

**Output:** Updated agent memories

---

### Step 8: Generate Improvement Report

**Create comprehensive report:**

Filename: `session-retrospective-{date}.md`
Location: `{w40k_output_folder}/retrospectives/`

**Report structure:**
```markdown
# Session Retrospective - {Date}

## Session Summary
- Agents involved: {list}
- Workflows executed: {list}
- Tasks used: {list}
- Duration: {time}

## User Profile
{Preferences discovered - from Step 3}

## Pain Points Identified
{Prioritized list - from Step 4}

## Workflow Gaps
{Gap analysis - from Step 5}

## Requirements Extracted
{Detailed requirements - from Step 6}

## Recommendations

### Immediate (P0-P1)
1. {Requirement 1}
2. {Requirement 2}

### Near-term (P2)
1. {Requirement 3}

### Future (P3)
1. {Requirement 4}

## Agent Memory Updates
{What was saved to sidecars}

## Success Metrics
If these requirements are implemented:
- User friction reduced by {estimate}
- Workflow completion time improved by {estimate}
- User satisfaction increased

## Next Steps
[ ] Implement P0 requirements
[ ] Review with module maintainers
[ ] Update TODO.md roadmap
[ ] Test with real users
```

**Output:** Saved retrospective report

---

### Step 9: Present Findings

**Display summary to user:**
```
✅ Session Retrospective Complete!

📊 Analysis Summary:
- {count} user preferences discovered
- {count} pain points identified
- {count} workflow gaps found
- {count} requirements extracted

🎯 Top Priorities:

1. {Requirement 1} - {Brief description}
   Impact: High | Effort: {estimate}

2. {Requirement 2} - {Brief description}
   Impact: High | Effort: {estimate}

3. {Requirement 3} - {Brief description}
   Impact: Medium | Effort: {estimate}

📁 Full report saved to:
{w40k_output_folder}/retrospectives/session-retrospective-{date}.md

Would you like me to:
[I] Implement high-priority requirements now
[R] Review detailed report
[E] Export requirements to GitHub issues
[X] Exit

Your feedback helps improve this module for everyone!
```

**User options:**
- Trigger implementation of specific requirements
- Review full retrospective document
- Export to external tracking (GitHub, Jira, etc.)
- Exit

**Output:** User-friendly summary + action options

---

## Integration Points

**Tasks Used:**
- None (pure analysis workflow)

**Agents Involved:**
- All agents (for memory updates)
- Triggered by any agent

**Files Created:**
- `{w40k_output_folder}/retrospectives/session-retrospective-{date}.md`
- Updates to `*-sidecar/memories.md` files
- Optional: `module-learnings.md` for cross-session patterns

**Outputs to:**
- Retrospective reports (for review)
- Agent memories (for personalization)
- TODO.md updates (for roadmap)
- GitHub issues (if enabled)

---

## Error Handling

**No conversation history:**
- Use current session only
- Warn that analysis may be limited

**Agent sidecars not writable:**
- Save retrospective report
- Skip memory updates
- Warn user

**Complex multi-session analysis:**
- Limit to manageable scope
- Prioritize recent sessions
- Focus on actionable insights

---

## Use Cases

### Use Case 1: Post-Workflow Improvement
User completes Design Paint Scheme workflow.
Agent triggers retrospective to identify friction.
Discovers paint set preset need.
Creates requirement for next version.

### Use Case 2: User-Requested Analysis
User says: "extract requirements from our conversation"
Workflow analyzes entire session.
Identifies unified project tracking need.
Generates detailed requirement documents.

### Use Case 3: Periodic Review
Module maintainer runs retrospective monthly.
Analyzes aggregate patterns across users.
Prioritizes most common pain points.
Updates module roadmap.

---

## Future Enhancements

- Automated pattern detection across multiple users
- Machine learning for requirement prioritization
- GitHub issue auto-creation
- Sentiment analysis for user satisfaction tracking
- A/B testing workflow variations
- Performance metrics (time to completion, user corrections)

---

## Notes

- This is a meta-workflow (improves the module itself)
- Can be run by any agent or standalone
- Retrospective reports are valuable historical records
- User preferences improve agent personalization over time
- Continuous improvement mindset built into module

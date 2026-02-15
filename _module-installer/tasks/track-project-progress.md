# Track Project Progress Task

## Purpose
Creates and maintains unified hobby project files that link army lists, paint schemes, campaign data, and progress tracking. Enables "resume project" functionality and provides progress visibility across painting sessions, campaigns, and army building.

## Usage

**From Agents:**
```yaml
- action: Execute task track-project-progress with project_name="Ultramarines 1000pt Army"
```

**From Workflows:**
```yaml
Execute: track-project-progress
Parameters:
  project_name: "Ultramarines 1000pt Army"
  project_type: "painting" # or "campaign", "army-building", "combined"
  action: "create" # or "update", "resume", "complete"
```

## Inputs

- `project_name` (required): Name of the hobby project
- `project_type` (required): Type - "painting", "campaign", "army-building", "combined"
- `action` (required): "create", "update", "resume", "complete"
- `linked_army_list` (optional): Path to army list file
- `linked_paint_scheme` (optional): Path to paint scheme file
- `linked_campaign` (optional): Path to campaign file
- `session_notes` (optional): Notes for current session
- `models_completed` (optional): Number of models painted this session
- `time_spent` (optional): Time spent this session (minutes)

## Outputs

Returns project data:
- `success`: Boolean indicating if operation succeeded
- `project_file_path`: Path to unified project file
- `project_data`: Complete project information
  - `project_name`: Project name
  - `created_date`: When project started
  - `last_updated`: Most recent session
  - `project_type`: Type of project
  - `status`: "planning", "in-progress", "completed"
  - `linked_files`: Paths to related files
  - `progress`: Progress tracking data
  - `sessions`: Array of session logs
  - `milestones`: Key achievements
  - `next_steps`: Recommended actions

## Project Types

### Painting Project
Tracks painting progress for an army:
- Total models to paint (from army list)
- Models completed
- Time spent painting
- Techniques learned
- Paint inventory used
- Quality tier achieved (Speed/Standard/Advanced)

### Campaign Project
Tracks narrative campaign:
- Battles fought
- Win/loss record
- Army progression (Crusade)
- Story developments
- Character developments

### Army Building Project
Tracks list development:
- Iterations of army list
- Playtesting results
- Meta analysis over time
- Tournament performance

### Combined Project
Links all aspects:
- Army list + Paint scheme + Campaign
- Full hobby project tracking

## Implementation

<task>
**Step 1: Parse Action**
- Determine action type (create/update/resume/complete)
- Validate required parameters
- Check if project already exists

**Step 2: Initialize or Load Project**

**If action = "create":**
- Generate project file path: `{w40k_output_folder}/projects/{project_name_slug}.md`
- Create project directory if needed
- Initialize project structure

**If action = "update" or "resume":**
- Load existing project file
- Parse current state
- Prepare for updates

**If action = "complete":**
- Load project
- Mark as completed
- Generate final summary

**Step 3: Link Related Files**

Check for and link:
- **Army List:** Search `tacticus-sidecar/lists.md` for matching faction/points
- **Paint Scheme:** Search `brushmaster-sidecar/schemes/` for matching faction
- **Campaign:** Search `chronicler-sidecar/campaigns.md` for matching army

Create relationships between files.

**Step 4: Calculate Progress**

**For Painting Projects:**
- Count total models from army list (if linked)
- Calculate completion percentage
- Estimate time remaining based on average time per model
- Identify next batch to paint

**For Campaign Projects:**
- Count battles fought
- Calculate win rate
- Track experience earned
- Note upcoming missions

**For Army Building:**
- Count list iterations
- Track point value changes
- Note meta shifts

**Step 5: Session Logging**

If session_notes provided:
- Create session entry with timestamp
- Log models completed, time spent, notes
- Update running totals
- Calculate session efficiency (models per hour)

**Step 6: Milestone Detection**

Check for milestones:
- 25% complete
- 50% complete
- 75% complete
- First unit finished
- First character painted
- Army fully painted
- Campaign victory
- Tournament placement

**Step 7: Generate Next Steps**

Based on project state, recommend:
- **Painting:** "Paint 5 Intercessors next (Tier 1)"
- **Campaign:** "Schedule next battle: Mission 3"
- **Army Building:** "Playtest against Necrons to validate anti-tank"

**Step 8: Write Project File**

Format:
```markdown
# {Project Name}

**Type:** {project_type}
**Status:** {status}
**Created:** {date}
**Last Updated:** {date}

## Links
- Army List: [path or "none"]
- Paint Scheme: [path or "none"]
- Campaign: [path or "none"]

## Progress
- Total Models: {count}
- Models Painted: {count} ({percentage}%)
- Time Spent: {hours} hours
- Average Time Per Model: {minutes} minutes
- Estimated Time Remaining: {hours} hours

## Current Status
{Auto-generated summary}

## Next Steps
1. {recommended action}
2. {recommended action}
3. {recommended action}

## Milestones
- [x] Project started ({date})
- [x] First model painted ({date})
- [ ] 25% complete
- [ ] 50% complete
- [ ] First unit complete
- [ ] Army complete

## Session Log

### Session {N} - {date}
**Time Spent:** {minutes} min
**Models Completed:** {count}
**Notes:** {session_notes}

{Previous sessions...}

## Notes
{User notes, observations, learnings}
```

**Step 9: Update Agent Sidecars**

If project links to agent data:
- Update `brushmaster-sidecar/projects.md` with painting project
- Update `tacticus-sidecar/memories.md` with army building notes
- Update `chronicler-sidecar/campaigns.md` with campaign links

**Step 10: Return Project Data**

Return structured data with:
- Project file path
- Current progress summary
- Next steps
- Session summary (if update)
</task>

## Error Handling

- **Project not found (resume/update):** Return error, suggest creating new project
- **Invalid action:** Return error with valid actions
- **No linked files found:** Continue without links, note in project file
- **File write failure:** Retry, return error if persistent

## Project File Location

- **Path:** `{w40k_output_folder}/projects/{project_name_slug}.md`
- **Format:** Markdown with YAML frontmatter (optional)
- **Naming:** Lowercase, hyphens for spaces (e.g., "ultramarines-1000pt-army.md")

## Resume Project Workflow

When user says "continue my Ultramarines project":
1. Execute with `action: "resume"`
2. Load project file
3. Display current status
4. Show next steps
5. Ask user what they want to do:
   - Update painting progress
   - Review army list
   - Plan next session
   - View full project details

## Example Queries

**Create New Painting Project:**
```yaml
project_name: "Ultramarines 1000pt Army"
project_type: "painting"
action: "create"
linked_army_list: "tacticus-sidecar/lists.md#ultramarines-gladius-995pts"
linked_paint_scheme: "brushmaster-sidecar/schemes/ultramarines_2025-12-19_scheme.md"
```

**Update After Painting Session:**
```yaml
project_name: "Ultramarines 1000pt Army"
action: "update"
session_notes: "Painted 5 Intercessors to Tier 1 completion. Edge highlighting is getting easier!"
models_completed: 5
time_spent: 180
```

**Resume Project:**
```yaml
project_name: "Ultramarines 1000pt Army"
action: "resume"
```

**Complete Project:**
```yaml
project_name: "Ultramarines 1000pt Army"
action: "complete"
session_notes: "Army fully painted! Ready for the tabletop."
```

## Output Examples

**Create Response:**
```json
{
  "success": true,
  "project_file_path": "/output/projects/ultramarines-1000pt-army.md",
  "project_data": {
    "project_name": "Ultramarines 1000pt Army",
    "status": "in-progress",
    "progress": {
      "total_models": 35,
      "painted": 0,
      "percentage": 0
    },
    "next_steps": [
      "Prime 5 Intercessors with Matt Black",
      "Paint first test model (Tier 1)",
      "Batch paint remaining 4"
    ]
  }
}
```

**Update Response:**
```json
{
  "success": true,
  "session_summary": {
    "models_painted": 5,
    "time_spent": "3 hours",
    "new_total": "5/35 models (14%)",
    "milestone_reached": "First unit started!"
  },
  "next_steps": [
    "Paint remaining 5 Intercessors from first unit",
    "Practice edge highlighting on hidden areas",
    "Consider moving to Tier 2 on next character"
  ]
}
```

## Notes

- Projects persist across agent sessions
- Multiple projects can exist simultaneously
- Project files are human-readable markdown
- Can be edited manually by user
- Agents should check for active projects when loading
- "Resume project" is a powerful UX feature for continuity

## Dependencies

- File system access (for project files)
- Read access to agent sidecars (for linked data)
- Date/time handling for session tracking
- Basic math for progress calculations

## Future Enhancements

- Project templates for common army sizes
- Visual progress bars (ASCII art)
- Export project summary as image/PDF
- Sync with external tools (BattleScribe, painting trackers)
- Multi-user project sharing
- Photo attachments for painted models

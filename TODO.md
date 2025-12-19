# Warhammer Veteran Development Roadmap

## Phase 1: Core Implementation (MVP) ✅ COMPLETE

### Workflows - High Priority

- [x] **Implement Build Army List Workflow** ✅
  - Use: `workflow create-workflow`
  - Input: workflows/build-army-list/README.md
  - Features: Faction selection, unit addition, points validation, meta analysis
  - Priority: **CRITICAL** - Core competitive player feature
  - **Status:** COMPLETE

- [x] **Implement Design Paint Scheme Workflow** ✅
  - Use: `workflow create-workflow`
  - Input: workflows/design-paint-scheme/README.md
  - Features: Paint inventory, budget constraints, Lorekeeper integration
  - Priority: **HIGH** - Multi-agent collaboration showcase
  - **Status:** COMPLETE + Phase 2 enhancements

### Tasks - High Priority

- [x] **Create Query Wahapedia Task** ✅
  - Centralized data retrieval from https://wahapedia.ru/
  - Used by: Tacticus, Arbitrator, Lorekeeper
  - Features: Caching, error handling, data parsing
  - Priority: **CRITICAL** - Foundational for all agents
  - **Status:** COMPLETE

- [x] **Create Fetch Tournament Data Task** ✅
  - Aggregate data from 5 tournament sources
  - Implement caching with timestamp tracking
  - Respect tournament_cache_days config setting
  - Priority: **HIGH** - Enables meta analysis
  - **Status:** COMPLETE

- [x] **Create Validate Army List Task** ✅
  - Points calculation logic
  - Detachment rules validation
  - Force organization checking
  - Priority: **HIGH** - Required for Build Army List workflow
  - **Status:** COMPLETE

### Integration & Testing

- [ ] Test Tacticus agent with Build Army List workflow
- [ ] Test Brushmaster agent with Design Paint Scheme workflow
- [ ] Verify Wahapedia query task works across all agents
- [ ] Test tournament data fetching and caching
- [ ] Validate army list validation logic
- [ ] Test multi-agent collaboration (Brushmaster → Lorekeeper)

### Configuration Validation

- [ ] Test installer questions flow
- [ ] Verify config.yaml generation
- [ ] Test all config values are accessible to agents
- [ ] Validate cache paths are created on-demand

## Phase 2: Enhanced Features 🎯 IN PROGRESS

### ✅ Completed Phase 2 Features

- [x] **Track Project Progress Task** ✅
  - Unified project files linking army lists, paint schemes, campaigns
  - Session logging with time tracking
  - Progress calculation and milestone detection
  - Resume project functionality
  - **Status:** COMPLETE

- [x] **Enhanced Design Paint Scheme Workflow** ✅
  - Paint set presets (Army Painter, Citadel, Vallejo)
  - 3-tier complexity system (Speed/Standard/Advanced)
  - Army list integration with auto model counting
  - Painting roadmap generation
  - Project creation integration
  - **Status:** COMPLETE

- [x] **Session Retrospective Workflow** ✅
  - Conversation analysis for requirement extraction
  - User preference discovery
  - Pain point identification
  - Workflow gap analysis
  - Agent memory updates
  - **Status:** COMPLETE

- [x] **Brushmaster Agent Enhancements** ✅
  - Track Project menu triggers
  - Resume Project functionality
  - Integration with track-project-progress task
  - **Status:** COMPLETE

### 🔄 In Progress / Planned

### Additional Agent Enhancements

- [ ] Add more embedded prompts to existing agents based on usage patterns
- [ ] Implement advanced meta analysis features (tier lists, matchup predictions)
- [ ] Enhance Lorekeeper with timeline visualization
- [x] Add Brushmaster paint collection inventory tracking ✅ (via project tracking)
- [ ] Enhance Chronicler with automated battle report generation
- [ ] Add Artisan budget tracking and spending analytics

### Workflow Expansions

- [ ] Create "Analyze Matchup" workflow (Tacticus)
- [ ] Create "Generate Lore Narrative" workflow (Lorekeeper)
- [ ] Create "Plan Campaign Arc" workflow (Chronicler)
- [ ] Create "Collection Roadmap" workflow (Artisan)

### Data & Caching Improvements

- [ ] Implement smart cache invalidation
- [ ] Add offline mode support
- [ ] Create data export features
- [ ] Build tournament data analytics dashboard

## Phase 3: Polish and Launch

### Testing

- [ ] Unit test all workflow steps
- [ ] Integration test agent-to-agent communication
- [ ] Test installer in completely clean project
- [ ] Test with sample Wahapedia data
- [ ] Load test tournament data aggregation
- [ ] Test sidecar memory persistence across sessions
- [ ] Verify all agent menu commands work
- [ ] Test Party Mode integration

### Documentation Expansion

- [ ] Add workflow-specific documentation
- [ ] Create agent usage examples for each specialist
- [ ] Write troubleshooting guide (common issues)
- [ ] Add FAQ section
- [ ] Create video walkthrough (optional)
- [ ] Document data source API dependencies

### Performance & Optimization

- [ ] Optimize Wahapedia query caching
- [ ] Reduce tournament data fetch times
- [ ] Implement lazy-loading for agent prompts
- [ ] Profile and optimize workflow execution

### Release Preparation

- [ ] Version bump to 1.0.0
- [ ] Create comprehensive release notes
- [ ] Tag release in Git repository
- [ ] Create GitHub/GitLab releases
- [ ] Publish to BMAD module registry (if applicable)
- [ ] Announce to Warhammer 40k community

## Phase 4: Post-MVP Expansion

### Age of Sigmar Support

- [ ] Create AoS versions of all 6 agents
- [ ] Adapt workflows for AoS army building
- [ ] Integrate AoS tournament data sources
- [ ] Update installer to support both game systems

### Advanced Features

- [ ] AI-powered meta prediction
- [ ] Community army list sharing platform
- [ ] Paint scheme gallery with voting
- [ ] Tournament result predictions
- [ ] Automated battle reports with narrative generation

## Quick Commands

### Create New Workflow
```bash
workflow create-workflow
```

### Test Module Installation
```bash
bmad install warhammer-40k
```

### Run Agents
```bash
agent tacticus      # Army List Builder
agent arbitrator    # Rules Judge
agent lorekeeper    # Lore Master
agent brushmaster   # Painting Guide
agent chronicler    # Campaign Manager
agent artisan       # Hobby Advisor
```

### Test Workflows
```bash
agent tacticus
BL  # Build List

agent brushmaster
DPS  # Design Paint Scheme
```

## Development Notes

### Important Considerations

- **Wahapedia Dependency**: Module relies on Wahapedia structure remaining stable. Implement robust error handling for data retrieval.
- **Tournament Data**: 5 different sources with different formats. Need adapter pattern for unified data structure.
- **Multi-Agent Communication**: Design Paint Scheme workflow calls Lorekeeper - ensure agent-to-agent communication works smoothly.
- **Caching Strategy**: Balance between data freshness and performance. User-configurable cache duration is key.
- **Sidecar Memory**: All agents track state across sessions. Test persistence thoroughly.

### Dependencies

- **BMAD Version**: 6.0.0-alpha or higher
- **External APIs**:
  - Wahapedia.ru (rules and unit data)
  - 40k Event Tracker API (if available)
  - Stat Check API (if available)
- **Optional Integrations**:
  - Image generation for paint scheme visualization
  - PDF generation for army list export

### Module Structure Reference

```
warhammer-40k/
├── agents/          # ✅ Created - 6 YAML files with sidecar folders
├── workflows/       # ✅ Plans created - needs implementation
├── tasks/           # ⚠️  Needs implementation
├── templates/       # ✅ Created (empty, ready for shared templates)
├── data/            # ✅ Created (empty, ready for static data)
├── _module-installer/  # ✅ Configured
├── README.md        # ✅ Complete
└── module.yaml      # ✅ Complete
```

## Completion Criteria

The module is MVP-complete when:

- [x] All 6 agents created with YAML configuration
- [ ] Both Phase 1 workflows implemented (Build Army List, Design Paint Scheme)
- [ ] All 3 tasks implemented (Query Wahapedia, Fetch Tournament Data, Validate Army List)
- [ ] Installation works smoothly in clean project
- [ ] Documentation covers all features
- [ ] Sample usage produces expected results
- [ ] Multi-agent collaboration works (Brushmaster → Lorekeeper)

The module is production-ready when:

- [ ] All Phase 1 and Phase 2 items complete
- [ ] Phase 3 testing complete
- [ ] Performance optimized
- [ ] Documentation comprehensive
- [ ] Community feedback incorporated

---

**Created:** 2025-12-18
**Last Updated:** 2025-12-18
**Status:** Planning Complete - Ready for Implementation

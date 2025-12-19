# Warhammer Veteran - Product Vision & Roadmap

**Created:** 2025-12-19
**Status:** Vision Definition Phase

---

## Product Vision

**Warhammer-as-a-Service Platform**
- SaaS platform for Warhammer 40k players
- Persistent user data (armies, paint schemes, lore, campaigns)
- Multi-user platform with freemium monetization
- AI agents as premium add-ons

---

## Technical Architecture Decisions

### Phase 1: MVP (Current)
- **Deployment:** GitHub Pages (static site)
- **Data Persistence:** Browser localStorage
- **Target:** Single-user, local-first experience
- **Tech Stack:** Static HTML/JS/CSS + BMAD agents

### Phase 2: SaaS Transition
- **Deployment:** Web application
- **Backend:** MongoDB database
- **Auth:** User accounts & authentication
- **Multi-tenant:** Separate user data per account

---

## Monetization Strategy

**Freemium Model:**

### Free Tier
- Basic army list building
- Paint scheme designer (limited)
- Static content access
- localStorage persistence only

### Premium Tier (Paid Add-ons)
- **AI Agents as Add-ons:**
  - Tacticus (Army Builder) - $X/month
  - Brushmaster (Painting) - $Y/month
  - Lorekeeper (Lore) - $Z/month
  - Full Agent Suite - $Bundle/month
- Cloud persistence (MongoDB)
- Project tracking & analytics
- Priority support

### Potential Pricing Models
- Monthly subscription per agent
- Bundle discount for all agents
- Per-army pricing (alternative)
- Annual subscription discount

---

## MVP User Journey

**Ideal First Experience:**

1. **Sign Up** (optional for MVP with localStorage)
2. **Build Army List**
   - Use Tacticus to create competitive list
   - Validate points and legality
   - Get meta analysis
3. **Design Paint Scheme**
   - Use Brushmaster for personalized scheme
   - 3-tier complexity guidance
   - Paint set preset optimization
4. **Store Forever**
   - localStorage (MVP)
   - Cloud sync (Phase 2)
5. **Optional Conversion:**
   - Free trial of premium agents
   - Convert to paid for cloud persistence + full features

---

## Data Persistence Requirements

### Critical User Data
Must persist across sessions:

1. **Army Lists** (from Tacticus)
   - Faction, detachment, units, points
   - Validation status
   - Creation date, last modified
   - Meta analysis snapshots

2. **Paint Schemes** (from Brushmaster)
   - Faction/chapter
   - Color palette with specific paints
   - 3-tier instructions (Speed/Standard/Advanced)
   - Painting roadmap
   - Test model notes

3. **Projects** (from Track Project Progress)
   - Linked army list + paint scheme
   - Session logs (models painted, time spent)
   - Progress tracking (%, milestones)
   - User notes per session

4. **Lore Content** (from Lorekeeper)
   - Faction explorations
   - Character deep-dives
   - Timeline notes
   - Custom narratives

5. **Campaigns** (from Chronicler)
   - Crusade campaign data
   - Battle records
   - Army progression
   - Narrative developments

6. **Hobby Plans** (from Artisan)
   - Conversion guides
   - Basing schemes
   - Collection roadmaps
   - Tool recommendations

### User Preferences
- Preferred factions
- Paint brands owned
- Skill level
- Game mode preferences
- Communication style

---

## Next Brainstorming Session Topics

**To Explore:**

1. **Productization Features**
   - What features make this a compelling product vs free tools?
   - Unique value propositions
   - Competitive moats

2. **Data Architecture**
   - localStorage schema design
   - MongoDB migration strategy
   - Import/export formats (BattleScribe compatibility?)

3. **Monetization Details**
   - Pricing per agent
   - Bundle pricing
   - Trial period length
   - Conversion tactics

4. **Go-to-Market Strategy**
   - Target audience segments
   - Marketing channels
   - Community building
   - Content marketing

5. **Competitive Analysis**
   - BattleScribe (free, army lists only)
   - Wahapedia (free, reference only)
   - Paid alternatives?
   - How to differentiate?

6. **Feature Prioritization**
   - What ships in MVP?
   - What's Phase 2 (SaaS)?
   - What's Phase 3 (mobile/advanced)?

---

## Architecture Notes

### localStorage Schema (MVP)
```javascript
{
  "user_preferences": {
    "factions": [],
    "paint_brands": [],
    "skill_level": "beginner"
  },
  "army_lists": [
    {
      "id": "uuid",
      "created": "ISO date",
      "faction": "Space Marines",
      "points": 1000,
      "units": [...],
      "validated": true
    }
  ],
  "paint_schemes": [
    {
      "id": "uuid",
      "faction": "Ultramarines",
      "paints": [...],
      "tiers": {...}
    }
  ],
  "projects": [
    {
      "id": "uuid",
      "army_list_id": "ref",
      "paint_scheme_id": "ref",
      "progress": {...}
    }
  ]
}
```

### MongoDB Schema (Phase 2)
```javascript
// Users collection
{
  "_id": ObjectId,
  "email": "user@example.com",
  "subscription_tier": "free|premium",
  "active_agents": ["tacticus", "brushmaster"],
  "created_at": Date
}

// ArmyLists collection
{
  "_id": ObjectId,
  "user_id": ObjectId (ref),
  "faction": "Space Marines",
  "points": 1000,
  "units": [...],
  "created_at": Date,
  "updated_at": Date
}

// Similar for paint_schemes, projects, etc.
```

---

## Product Differentiation Ideas

**Brainstorming Needed:**
- AI-powered recommendations (meta shifts, paint combos)
- Social features (share armies, schemes, vote on community schemes)
- Integration with other tools (BattleScribe import, Tabletop Simulator export)
- Premium content (exclusive paint schemes, lore expansions)
- Tournament integration (submit lists to events, track results)
- Photo gallery (upload painted models, track progress visually)
- Community marketplace (buy/sell custom schemes, conversions)

---

## Open Questions for Next Session

1. Should free tier have AI agents at all, or is it just static tools?
2. What's the conversion funnel? (Free → Trial → Paid)
3. How to handle Wahapedia dependency? (Cache locally? API?)
4. Export formats for portability? (JSON, PDF, BattleScribe XML?)
5. Social/community features priority?
6. Mobile-first or desktop-first?
7. Offline-first architecture?

---

## Action Items

**Before Next Session:**
- [ ] Research localStorage size limits (5-10MB typical)
- [ ] Design localStorage schema for all 6 agents
- [ ] Prototype GitHub Pages deployment
- [ ] Research BattleScribe file format (for import/export)
- [ ] Competitive analysis (pricing, features)
- [ ] User persona development
- [ ] Sketch wireframes for web UI

---

## Context for Future Sessions

**Resume Brainstorming With:**
"We're productizing Warhammer Veteran as a freemium SaaS platform. MVP uses GitHub Pages + localStorage. Phase 2 transitions to MongoDB backend. AI agents are premium add-ons. Need to brainstorm: productization features, data architecture, monetization details, go-to-market strategy."

**Key Files to Reference:**
- This document (PRODUCT-VISION.md)
- PHASE-2-PLAN.md (technical implementation)
- README.md (current features)
- TODO.md (development roadmap)

---

**Next Steps:** Continue brainstorming session with Progressive Technique Flow to generate concrete ideas for productization, persistence architecture, and monetization strategy.

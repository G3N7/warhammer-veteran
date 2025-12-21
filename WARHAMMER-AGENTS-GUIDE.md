# Warhammer Veteran Agents - Quick Reference

## ✅ Installation Complete!

Your Warhammer 40k agents are now properly installed and accessible from the Claude window!

## 🎯 Available Agents

### 1. **⚔️ Tacticus** - Army List Builder & Competitive Strategist
**Command:** `/tacticus`
- Build competitive army lists
- Analyze unit synergies
- Check tournament meta data
- Validate points and legality

### 2. **⚖️ Arbitrator** - Rules Judge & Dispute Resolver
**Command:** `/arbitrator`
- Resolve rules disputes
- Clarify complex interactions
- Phase sequencing help
- Wahapedia citations

### 3. **📜 Lorekeeper** - Lore Master & Narrative Historian
**Command:** `/lorekeeper`
- Faction history deep-dives
- Character backgrounds
- Timeline exploration
- Narrative context

### 4. **🎨 Brushmaster** - Painting Guide & Hobby Mentor
**Command:** `/brushmaster`
- Paint scheme design
- Step-by-step tutorials
- Color recommendations
- Technique breakdowns

### 5. **📖 Chronicler** - Campaign Manager & Narrative Coordinator
**Command:** `/chronicler`
- Crusade campaign tracking
- Battle recording
- Narrative mission generation
- Campaign progression

### 6. **🔨 Artisan** - Hobby Advisor & Conversion Specialist
**Command:** `/artisan`
- Conversion guides
- Basing design
- Collection planning
- Tool recommendations

## 🚀 How to Use

### From the Normal Claude Window:
Simply type the slash command for any agent:
```
/tacticus
```

### From Chat:
You can also invoke them using the Skill tool or by mentioning them by name.

## 📂 Agent Locations

- **Command Wrappers:** `.claude/commands/warhammer-40k/agents/`
- **Agent Files:** `_bmad/warhammer-40k/agents/`
- **Sidecar Memory:** `_bmad/warhammer-40k/agents/{agent-name}-sidecar/`

## 💾 Persistent Memory

Each agent has its own sidecar folder where it stores:
- Session memories
- Past projects/lists/campaigns
- Learned preferences
- Historical data

All agents will remember your previous conversations and build on past interactions!

## 🎨 Example Usage

**Building an Army List:**
```
/tacticus
"Help me build a 2000pt Space Marines list focused on melee"
```

**Painting Help:**
```
/brushmaster
"I want to paint Ultramarines but with a grimdark style"
```

**Rules Question:**
```
/arbitrator
"Can I use Overwatch against a unit charging from deepstrike?"
```

## 🔧 Troubleshooting

If an agent doesn't load:
1. Make sure you're in the `/workspaces/warhammer-veteran` directory
2. Check that the files exist in `_bmad/warhammer-40k/agents/`
3. Try reloading your Claude window

## 🎯 Next Steps

Your agents are ready to use! The module structure is complete with:
- ✅ All 6 agents installed
- ✅ Command wrappers created
- ✅ Sidecar memory folders set up
- ✅ Proper BMAD module structure

For the Emperor! 🦅

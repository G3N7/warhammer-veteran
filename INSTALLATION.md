# Warhammer Veteran - Installation Guide

## For Users (NPM Installation)

Once published to NPM, users can install the module with:

```bash
npm install @bmad-modules/warhammer-veteran
```

Then configure their BMAD project to load the module.

## For Developers (Local Testing)

### Method 1: Direct Agent Usage

To test the module locally during development:

1. **Create or navigate to a BMAD project:**
   ```bash
   mkdir my-warhammer-project
   cd my-warhammer-project
   npx bmad-method@alpha install  # Install BMAD Core if not already done
   ```

2. **Copy module files to your project:**
   ```bash
   # From the warhammer-veteran directory:
   cp -r agents/* /path/to/my-warhammer-project/.bmad/agents/
   cp -r tasks/* /path/to/my-warhammer-project/.bmad/tasks/
   cp -r workflows/* /path/to/my-warhammer-project/.bmad/workflows/
   ```

3. **Use the agents:**
   You can now use the agents in your BMAD project. The agents will be available
   via their names (Tacticus, Arbitrator, Lorekeeper, etc.)

### Method 2: Symlink for Development

Create symbolic links to avoid copying files repeatedly:

```bash
cd my-warhammer-project/.bmad
ln -s /workspaces/warhammer-veteran/agents/* agents/
ln -s /workspaces/warhammer-veteran/tasks/* tasks/
ln -s /workspaces/warhammer-veteran/workflows/* workflows/
```

Now any changes to the module files are immediately reflected in your test project.

### Method 3: NPM Link (For Package Testing)

Test the module as an NPM package without publishing:

```bash
# In the warhammer-veteran directory:
npm link

# In your BMAD project:
npm link @bmad-modules/warhammer-veteran
```

## Module Structure

The module includes:

- **6 Agents:** Tacticus, Arbitrator, Lorekeeper, Brushmaster, Chronicler, Artisan
- **3 Tasks:** Query Wahapedia, Fetch Tournament Data, Validate Army List
- **2 Workflows:** Build Army List, Design Paint Scheme
- **Sidecar Memory:** Persistent storage for each agent

## Configuration

After installation, configure the module with these settings:

- `w40k_output_folder`: Where to save generated content
- `default_game_mode`: matched-play, crusade, or open-play
- `tournament_cache_days`: How often to refresh meta data (1/7/30)
- `meta_detail_level`: minimal, standard, or detailed

## Testing the Module

Run the validation script to verify the module structure:

```bash
./test-module.sh
```

This checks:
- Module configuration (module.yaml)
- Agent YAML files (6 agents)
- Task files (3 tasks)
- Workflow files (2 workflows)
- Sidecar folder structure (6 sidecars)

## First Steps After Installation

1. **Try Tacticus (Army List Builder):**
   - Load the Tacticus agent
   - Use `[BL] Build List` to create an army list
   - Follow the 6-step interactive workflow

2. **Try Brushmaster (Painting Guide):**
   - Load the Brushmaster agent
   - Use `[DPS] Design Paint Scheme` for a personalized paint scheme
   - Experience multi-agent collaboration with Lorekeeper

3. **Explore Other Agents:**
   - Arbitrator for rules questions
   - Lorekeeper for lore deep-dives
   - Chronicler for campaign management
   - Artisan for hobby advice

## Troubleshooting

### Module not found
- Ensure you've copied the files to the correct BMAD directories
- Check that agent YAML files are in `.bmad/agents/`
- Verify tasks are in `.bmad/tasks/`
- Confirm workflows are in `.bmad/workflows/`

### Workflow triggers not working
- Check that workflow paths use `{module-root}` in agent YAMLs
- Verify workflow.md files exist in workflow directories
- Ensure README.md accompanies each workflow

### Sidecar memory not persisting
- Check that sidecar folders exist (e.g., `agents/tacticus-sidecar/`)
- Verify folder permissions allow writing
- Look for `lists.md`, `memories.md`, etc. in sidecar folders

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/yourusername/warhammer-veteran/issues
- See CONTRIBUTING.md for development guidelines
- See TESTING.md for validation procedures

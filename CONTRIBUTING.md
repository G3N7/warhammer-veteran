# Contributing to Warhammer Veteran

Thanks for your interest in contributing to the Warhammer Veteran BMAD module!

## Development Setup

### Prerequisites

- BMAD Method v6.0.0-alpha or higher
- Node.js (for npm packaging)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/warhammer-veteran.git
   cd warhammer-veteran
   ```

2. Install BMAD (if not already installed):
   ```bash
   npx bmad-method@alpha install
   ```

3. The `_bmad/` folder in your development environment contains BMAD core tools for building the module - it's gitignored and not part of the module itself.

## Project Structure

This repository contains only the Warhammer Veteran module files. The `_bmad/` folder is for development only and should not be committed.

**What's in the repo:**
- `agents/` - Agent YAML files and sidecar folders
- `workflows/` - Workflow plans and implementations
- `tasks/` - Shared utility tasks
- `module.yaml` - Module configuration
- `README.md`, `TODO.md` - Documentation

**What's NOT in the repo (gitignored):**
- `_bmad/` - BMAD core (development only)
- `_bmad-output/` - Build outputs
- `node_modules/` - NPM dependencies
- Agent sidecar memory contents (user data)

## Development Workflow

### Implementing Workflows

Use the BMAD create-workflow tool:
```bash
workflow create-workflow
```

Select the workflow folder (e.g., `workflows/build-army-list/`) and follow the prompts.

### Implementing Tasks

Create task files in the `tasks/` directory following BMAD task patterns.

### Testing Your Changes

1. Test installation in a clean project:
   ```bash
   cd /path/to/test-project
   bmad install /path/to/warhammer-veteran
   ```

2. Load agents and test commands:
   ```bash
   agent tacticus
   CH  # Chat
   BL  # Build List
   ```

3. Test workflows:
   ```bash
   agent brushmaster
   DPS  # Design Paint Scheme
   ```

## Pull Request Guidelines

1. **Follow the roadmap**: Check TODO.md for prioritized tasks
2. **Test thoroughly**: Ensure all agents and workflows function
3. **Update documentation**: Keep README.md and TODO.md current
4. **Clear commits**: Use descriptive commit messages
5. **One feature per PR**: Keep changes focused

## Code Style

- Follow existing YAML formatting for agents
- Use clear, descriptive names for prompts and workflows
- Add comments for complex logic
- Keep agent personas consistent

## Areas Needing Contribution

See [TODO.md](TODO.md) for the full roadmap. High-priority items:

### Phase 1 (MVP)
- [ ] Query Wahapedia task implementation
- [ ] Fetch Tournament Data task implementation
- [ ] Validate Army List task implementation
- [ ] Build Army List workflow implementation
- [ ] Design Paint Scheme workflow implementation

### Phase 2
- [ ] Enhanced agent prompts
- [ ] Additional workflow expansions
- [ ] Data caching improvements

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Documentation improvements
- Questions about contributing

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

# New Recruit MCP Server

MCP (Model Context Protocol) server for integrating with [New Recruit](https://www.newrecruit.eu) - the Warhammer 40k army list builder and tournament platform.

## Features

- **Test Connection** - Verify your New Recruit credentials
- **Browse Game Systems** - List all supported game systems
- **Browse Tournaments** - Search and view tournament details
- **Fetch Player Lists** - Get army lists submitted by any player
- **Fetch Tournament Lists** - Get all lists from a tournament
- **Local Army Management** - List and read local markdown army lists
- **Export for New Recruit** - Convert local markdown lists to plain text format
- **Import from New Recruit** - Import tournament lists and save as markdown

## Installation

### 1. Install Dependencies

```bash
cd mcp-servers/newrecruit
npm install
```

### 2. Build the Server

```bash
npm run build
```

### 3. Configure Credentials

Create a `.env` file with your New Recruit credentials:

```bash
cp .env.example .env
# Edit .env with your credentials
```

Or set environment variables:
```bash
export NR_LOGIN=your_username
export NR_PASSWORD=your_password
```

### 4. Configure Claude Code

Add the MCP server to your Claude Code settings.

**Option A: Global configuration** - Edit `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "newrecruit": {
      "command": "node",
      "args": ["/absolute/path/to/warhammer-veteran/mcp-servers/newrecruit/dist/index.js"],
      "env": {
        "NR_LOGIN": "your_username",
        "NR_PASSWORD": "your_password"
      }
    }
  }
}
```

**Option B: Project-specific** - Create `.claude/settings.local.json` in your project:

```json
{
  "mcpServers": {
    "newrecruit": {
      "command": "node",
      "args": ["./mcp-servers/newrecruit/dist/index.js"],
      "env": {
        "NR_LOGIN": "${NR_LOGIN}",
        "NR_PASSWORD": "${NR_PASSWORD}"
      }
    }
  }
}
```

Then set the environment variables before running Claude Code:
```bash
export NR_LOGIN=your_username
export NR_PASSWORD=your_password
```

A sample configuration is provided in `claude-mcp-config.json` that you can copy.

## Available Tools

### New Recruit API Tools

| Tool | Description |
|------|-------------|
| `nr_test_connection` | Test API authentication |
| `nr_list_systems` | List all game systems |
| `nr_list_tournaments` | List tournaments (optionally filtered by system) |
| `nr_get_tournament` | Get tournament details |
| `nr_get_player_lists` | Get army lists for a player |
| `nr_get_tournament_lists` | Get all lists from a tournament |
| `nr_import_list` | Import a list and save as markdown |

### Local Army List Tools

| Tool | Description |
|------|-------------|
| `local_list_armies` | List all local markdown army lists |
| `local_get_army` | Read a specific army list |
| `local_export_for_nr` | Convert markdown list to plain text for NR |

## Usage Examples

### Test Your Connection
```
Use the nr_test_connection tool to verify credentials
```

### Browse Warhammer 40k Tournaments
```
Use nr_list_systems to find the 40k system ID, then nr_list_tournaments with that ID
```

### Get Tournament Lists
```
Use nr_get_tournament_lists with tournament_id "12345" to see all submitted lists
```

### Export Your List
```
Use local_export_for_nr with file_path "tau-empire/patient-hunter-kauyon-gunline.md"
```

### Import a Tournament Winner's List
```
Use nr_import_list with tournament_id, player_name, output_faction, and output_filename
```

## Development

```bash
# Run in development mode (with tsx)
npm run dev

# Build for production
npm run build

# Run built version
npm start
```

## API Notes

New Recruit uses HTTP header-based authentication:
- `NR-Login`: Your username
- `NR-Password`: Your password

All API endpoints use POST requests to `https://www.newrecruit.eu/api/`.

## License

MIT - Part of the Warhammer Veteran BMAD module.

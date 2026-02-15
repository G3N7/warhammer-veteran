#!/usr/bin/env node
/**
 * New Recruit MCP Server
 * Provides tools for syncing army lists with newrecruit.eu
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema, ListResourcesRequestSchema, ReadResourceRequestSchema, } from '@modelcontextprotocol/sdk/types.js';
import { NewRecruitClient } from './newrecruit-client.js';
import { scanArmyLists, parseMarkdownArmyList, toPlainTextFormat, toRosterFormat, getListSummary, } from './army-list-converter.js';
import { readFile, writeFile } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
// Get project root (assumes MCP server is in mcp-servers/newrecruit/)
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = join(__dirname, '..', '..', '..');
const ARMY_LISTS_DIR = join(PROJECT_ROOT, 'army-lists');
// Initialize credentials from environment
function getCredentials() {
    const login = process.env.NR_LOGIN;
    const password = process.env.NR_PASSWORD;
    if (!login || !password) {
        return null;
    }
    return { login, password };
}
// Tool definitions
const TOOLS = [
    {
        name: 'nr_test_connection',
        description: 'Test the connection to New Recruit API with current credentials',
        inputSchema: {
            type: 'object',
            properties: {},
            required: [],
        },
    },
    {
        name: 'nr_list_systems',
        description: 'List all available game systems on New Recruit',
        inputSchema: {
            type: 'object',
            properties: {},
            required: [],
        },
    },
    {
        name: 'nr_list_tournaments',
        description: 'List tournaments from New Recruit, optionally filtered by game system',
        inputSchema: {
            type: 'object',
            properties: {
                game_system_id: {
                    type: 'number',
                    description: 'Optional game system ID to filter tournaments',
                },
            },
            required: [],
        },
    },
    {
        name: 'nr_get_tournament',
        description: 'Get detailed information about a specific tournament including rounds and players',
        inputSchema: {
            type: 'object',
            properties: {
                tournament_id: {
                    type: 'string',
                    description: 'Tournament ID to fetch details for',
                },
            },
            required: ['tournament_id'],
        },
    },
    {
        name: 'nr_get_player_lists',
        description: 'Get all army lists submitted by a specific player',
        inputSchema: {
            type: 'object',
            properties: {
                player_name: {
                    type: 'string',
                    description: 'Player login name (case-insensitive)',
                },
            },
            required: ['player_name'],
        },
    },
    {
        name: 'nr_get_tournament_lists',
        description: 'Get all army lists from a specific tournament',
        inputSchema: {
            type: 'object',
            properties: {
                tournament_id: {
                    type: 'string',
                    description: 'Tournament ID to fetch lists from',
                },
            },
            required: ['tournament_id'],
        },
    },
    {
        name: 'local_list_armies',
        description: 'List all army lists stored locally in the army-lists directory',
        inputSchema: {
            type: 'object',
            properties: {},
            required: [],
        },
    },
    {
        name: 'local_get_army',
        description: 'Get a specific local army list by file path or name',
        inputSchema: {
            type: 'object',
            properties: {
                file_path: {
                    type: 'string',
                    description: 'Path to the army list file (relative to army-lists/ or absolute)',
                },
            },
            required: ['file_path'],
        },
    },
    {
        name: 'local_export_for_nr',
        description: 'Convert a local army list to plain text format suitable for New Recruit',
        inputSchema: {
            type: 'object',
            properties: {
                file_path: {
                    type: 'string',
                    description: 'Path to the army list file to export',
                },
                format: {
                    type: 'string',
                    enum: ['plain', 'roster'],
                    description: 'Export format: plain (simple text) or roster (Battlescribe-style)',
                },
            },
            required: ['file_path'],
        },
    },
    {
        name: 'nr_import_list',
        description: 'Import an army list from New Recruit and save it locally as markdown',
        inputSchema: {
            type: 'object',
            properties: {
                tournament_id: {
                    type: 'string',
                    description: 'Tournament ID to import from',
                },
                player_name: {
                    type: 'string',
                    description: 'Player name whose list to import',
                },
                output_faction: {
                    type: 'string',
                    description: 'Faction folder to save to (e.g., "space-marines", "tau-empire")',
                },
                output_filename: {
                    type: 'string',
                    description: 'Filename for the imported list (without .md extension)',
                },
            },
            required: ['tournament_id', 'player_name', 'output_faction', 'output_filename'],
        },
    },
];
// Create MCP server
const server = new Server({
    name: 'mcp-newrecruit',
    version: '1.0.0',
}, {
    capabilities: {
        tools: {},
        resources: {},
    },
});
// Handle tool listing
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools: TOOLS };
});
// Handle resource listing (local army lists)
server.setRequestHandler(ListResourcesRequestSchema, async () => {
    try {
        const lists = await scanArmyLists(ARMY_LISTS_DIR);
        return {
            resources: lists.map((list) => ({
                uri: `army-list://${list.filePath}`,
                name: list.name,
                description: getListSummary(list),
                mimeType: 'text/markdown',
            })),
        };
    }
    catch (error) {
        return { resources: [] };
    }
});
// Handle resource reading
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const uri = request.params.uri;
    if (uri.startsWith('army-list://')) {
        const filePath = uri.replace('army-list://', '');
        const content = await readFile(filePath, 'utf-8');
        return {
            contents: [
                {
                    uri,
                    mimeType: 'text/markdown',
                    text: content,
                },
            ],
        };
    }
    throw new Error(`Unknown resource: ${uri}`);
});
// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    // Helper to create text response
    const textResponse = (text) => ({
        content: [{ type: 'text', text }],
    });
    // Helper to get NR client
    const getClient = () => {
        const creds = getCredentials();
        if (!creds) {
            throw new Error('New Recruit credentials not configured. Set NR_LOGIN and NR_PASSWORD environment variables.');
        }
        return new NewRecruitClient(creds);
    };
    try {
        switch (name) {
            case 'nr_test_connection': {
                const client = getClient();
                const success = await client.testConnection();
                if (success) {
                    return textResponse('Successfully connected to New Recruit API!');
                }
                else {
                    return textResponse('Failed to connect to New Recruit API. Check your credentials.');
                }
            }
            case 'nr_list_systems': {
                const client = getClient();
                const systems = await client.getSystems();
                const formatted = systems
                    .map((s) => `- [${s.id}] ${s.name}`)
                    .join('\n');
                return textResponse(`Available game systems:\n${formatted}`);
            }
            case 'nr_list_tournaments': {
                const client = getClient();
                const gameSystemId = args.game_system_id;
                const tournaments = await client.getTournaments(gameSystemId);
                if (tournaments.length === 0) {
                    return textResponse('No tournaments found.');
                }
                const formatted = tournaments
                    .slice(0, 20) // Limit to 20 for readability
                    .map((t) => `- [${t.id}] ${t.name}${t.date ? ` (${t.date})` : ''}`)
                    .join('\n');
                return textResponse(`Recent tournaments (showing ${Math.min(20, tournaments.length)} of ${tournaments.length}):\n${formatted}`);
            }
            case 'nr_get_tournament': {
                const client = getClient();
                const tournamentId = args.tournament_id;
                const details = await client.getTournamentDetails(tournamentId);
                return textResponse(JSON.stringify(details, null, 2));
            }
            case 'nr_get_player_lists': {
                const client = getClient();
                const playerName = args.player_name;
                const reports = await client.getPlayerLists(playerName);
                if (reports.length === 0) {
                    return textResponse(`No lists found for player: ${playerName}`);
                }
                const formatted = reports
                    .map((r) => {
                    let info = `Tournament: ${r.tournament_name || r.tournament_id}`;
                    if (r.faction)
                        info += ` | Faction: ${r.faction}`;
                    if (r.ranking)
                        info += ` | Rank: ${r.ranking}`;
                    if (r.exported_list) {
                        info += `\nList:\n${r.exported_list.substring(0, 500)}${r.exported_list.length > 500 ? '...' : ''}`;
                    }
                    return info;
                })
                    .join('\n\n---\n\n');
                return textResponse(`Lists for ${playerName}:\n\n${formatted}`);
            }
            case 'nr_get_tournament_lists': {
                const client = getClient();
                const tournamentId = args.tournament_id;
                const reports = await client.getTournamentLists(tournamentId);
                if (reports.length === 0) {
                    return textResponse(`No lists found for tournament: ${tournamentId}`);
                }
                const formatted = reports
                    .map((r) => {
                    let info = `Player: ${r.player}`;
                    if (r.faction)
                        info += ` | Faction: ${r.faction}`;
                    if (r.ranking)
                        info += ` | Rank: ${r.ranking}`;
                    return info;
                })
                    .join('\n');
                return textResponse(`${reports.length} lists in tournament:\n${formatted}`);
            }
            case 'local_list_armies': {
                const lists = await scanArmyLists(ARMY_LISTS_DIR);
                if (lists.length === 0) {
                    return textResponse('No army lists found in army-lists/ directory.');
                }
                const formatted = lists.map((l) => `- ${getListSummary(l)}\n  File: ${l.filePath}`).join('\n');
                return textResponse(`Local army lists (${lists.length}):\n\n${formatted}`);
            }
            case 'local_get_army': {
                let filePath = args.file_path;
                // Handle relative paths
                if (!filePath.startsWith('/')) {
                    filePath = join(ARMY_LISTS_DIR, filePath);
                }
                const content = await readFile(filePath, 'utf-8');
                const parsed = parseMarkdownArmyList(content, filePath);
                return textResponse(`Army List: ${parsed.name}\n` +
                    `Faction: ${parsed.faction}\n` +
                    `Detachment: ${parsed.detachment}\n` +
                    `Points: ${parsed.pointsTotal}/${parsed.pointsLimit}\n` +
                    `Units: ${parsed.units.length}\n` +
                    `Enhancements: ${parsed.enhancements.length}\n\n` +
                    `---\n\n${content}`);
            }
            case 'local_export_for_nr': {
                let filePath = args.file_path;
                const format = args.format || 'plain';
                if (!filePath.startsWith('/')) {
                    filePath = join(ARMY_LISTS_DIR, filePath);
                }
                const content = await readFile(filePath, 'utf-8');
                const parsed = parseMarkdownArmyList(content, filePath);
                const exported = format === 'roster' ? toRosterFormat(parsed) : toPlainTextFormat(parsed);
                return textResponse(`Exported "${parsed.name}" in ${format} format:\n\n` +
                    `---\n${exported}\n---\n\n` +
                    `Copy the text between the --- markers to paste into New Recruit.`);
            }
            case 'nr_import_list': {
                const client = getClient();
                const { tournament_id, player_name, output_faction, output_filename } = args;
                // Fetch the list from New Recruit
                const reports = await client.getReports({
                    tournamentId: tournament_id,
                    player: player_name,
                });
                if (reports.length === 0) {
                    return textResponse(`No list found for player "${player_name}" in tournament ${tournament_id}`);
                }
                const report = reports[0];
                if (!report.exported_list) {
                    return textResponse(`Player "${player_name}" has no exported list in tournament ${tournament_id}`);
                }
                // Create basic markdown template with imported data
                const markdown = `# Imported: ${player_name}'s List

**Faction:** ${report.faction || 'Unknown'}
**Detachment:** Unknown
**Edition:** 10th Edition
**Points:** ${report.exported_list.match(/(\d+)\s*pts/)?.[1] || 'Unknown'}/2000
**Source:** New Recruit - Tournament ${tournament_id}
**Imported:** ${new Date().toISOString().split('T')[0]}

---

## Original List

\`\`\`
${report.exported_list}
\`\`\`

---

## Notes

- This list was imported from New Recruit tournament ${tournament_id}
- Player: ${player_name}
- Ranking: ${report.ranking || 'Unknown'}
- Review and convert to standard Warhammer Veteran format as needed

---

*Imported via MCP New Recruit Integration*
`;
                // Save to file
                const outputPath = join(ARMY_LISTS_DIR, output_faction, `${output_filename}.md`);
                try {
                    await writeFile(outputPath, markdown, 'utf-8');
                    return textResponse(`Successfully imported list to: ${outputPath}\n\n` +
                        `The list has been saved in a basic format. ` +
                        `Review and convert it to the full Warhammer Veteran army list format.`);
                }
                catch (err) {
                    return textResponse(`Failed to save imported list: ${err}\n\n` +
                        `Here is the imported content:\n\n${markdown}`);
                }
            }
            default:
                throw new Error(`Unknown tool: ${name}`);
        }
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return textResponse(`Error: ${message}`);
    }
});
// Start the server
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error('New Recruit MCP Server running on stdio');
}
main().catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
});
//# sourceMappingURL=index.js.map
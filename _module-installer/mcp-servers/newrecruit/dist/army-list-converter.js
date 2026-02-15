/**
 * Army List Converter
 * Converts between Warhammer Veteran markdown format and New Recruit formats
 */
import { readFile, readdir } from 'fs/promises';
import { join } from 'path';
/**
 * Parse a Warhammer Veteran markdown army list file
 */
export function parseMarkdownArmyList(markdown, filePath) {
    const lines = markdown.split('\n');
    // Extract header metadata
    const nameMatch = markdown.match(/^#\s+(.+?)(?:\s+-|$)/m);
    const factionMatch = markdown.match(/\*\*Faction:\*\*\s*(.+)/);
    const detachmentMatch = markdown.match(/\*\*Detachment:\*\*\s*(.+)/);
    const editionMatch = markdown.match(/\*\*Edition:\*\*\s*(.+)/);
    const pointsMatch = markdown.match(/\*\*Points:\*\*\s*(\d+)\s*\/\s*(\d+)/);
    const name = nameMatch?.[1]?.trim() || 'Unnamed List';
    const faction = factionMatch?.[1]?.trim() || 'Unknown';
    const detachment = detachmentMatch?.[1]?.trim() || 'Unknown';
    const edition = editionMatch?.[1]?.trim() || '10th Edition';
    const pointsTotal = pointsMatch ? parseInt(pointsMatch[1], 10) : 0;
    const pointsLimit = pointsMatch ? parseInt(pointsMatch[2], 10) : 2000;
    // Parse unit table
    const units = [];
    const enhancements = [];
    // Find the army list table section
    const tableMatch = markdown.match(/### Army List Table[\s\S]*?\|[\s\S]*?(?=\n###|\n---|\n##|$)/);
    if (tableMatch) {
        const tableSection = tableMatch[0];
        const tableLines = tableSection.split('\n').filter(line => line.startsWith('|'));
        // Skip header rows (first 2 lines are header and separator)
        for (let i = 2; i < tableLines.length; i++) {
            const line = tableLines[i];
            const cells = line.split('|').map(c => c.trim()).filter(c => c);
            if (cells.length >= 3) {
                const unitName = cells[0].replace(/\*\*/g, '').trim();
                const modelsStr = cells[1];
                const role = cells[2];
                const pointsStr = cells[3] || '0';
                // Skip category headers
                if (unitName.toUpperCase() === unitName && !unitName.includes('pts')) {
                    continue;
                }
                // Check if this is an enhancement
                if (role?.toLowerCase().includes('enhancement') || unitName.toLowerCase().includes('enhancement')) {
                    const enhancementName = unitName.replace(/^\*?Enhancement:?\*?\s*/i, '').trim();
                    const bearer = modelsStr || role || '';
                    const pts = parseInt(pointsStr.replace(/[^\d]/g, ''), 10) || 0;
                    enhancements.push({
                        name: enhancementName,
                        bearer: bearer,
                        points: pts,
                    });
                }
                else {
                    const models = parseInt(modelsStr, 10) || 1;
                    const pts = parseInt(pointsStr.replace(/[^\d]/g, ''), 10) || 0;
                    if (pts > 0) {
                        units.push({
                            name: unitName,
                            models,
                            role,
                            points: pts,
                        });
                    }
                }
            }
        }
    }
    return {
        name,
        faction,
        detachment,
        edition,
        pointsTotal,
        pointsLimit,
        units,
        enhancements,
        rawMarkdown: markdown,
        filePath,
    };
}
/**
 * Convert a parsed army list to plain text format (for New Recruit export)
 */
export function toPlainTextFormat(list) {
    const lines = [];
    lines.push(`${list.name}`);
    lines.push(`${list.faction} - ${list.detachment}`);
    lines.push(`${list.pointsTotal}pts / ${list.pointsLimit}pts`);
    lines.push('');
    lines.push('UNITS:');
    for (const unit of list.units) {
        const modelStr = unit.models > 1 ? ` (${unit.models})` : '';
        lines.push(`- ${unit.name}${modelStr}: ${unit.points}pts`);
    }
    if (list.enhancements.length > 0) {
        lines.push('');
        lines.push('ENHANCEMENTS:');
        for (const enh of list.enhancements) {
            lines.push(`- ${enh.name} on ${enh.bearer}: ${enh.points}pts`);
        }
    }
    return lines.join('\n');
}
/**
 * Convert a parsed army list to Battlescribe-style ROS format
 * (simplified - actual ROS is XML-based)
 */
export function toRosterFormat(list) {
    const lines = [];
    lines.push(`++ ${list.name} [${list.pointsTotal}pts] ++`);
    lines.push('');
    lines.push(`++ ${list.faction} - ${list.detachment} ++`);
    lines.push('');
    // Group by role
    const byRole = {};
    for (const unit of list.units) {
        const role = unit.role || 'Other';
        if (!byRole[role])
            byRole[role] = [];
        byRole[role].push(unit);
    }
    for (const [role, roleUnits] of Object.entries(byRole)) {
        lines.push(`+ ${role} +`);
        lines.push('');
        for (const unit of roleUnits) {
            lines.push(`${unit.name} [${unit.points}pts]`);
            if (unit.models > 1) {
                lines.push(`. ${unit.models} models`);
            }
        }
        lines.push('');
    }
    if (list.enhancements.length > 0) {
        lines.push('+ Enhancements +');
        lines.push('');
        for (const enh of list.enhancements) {
            lines.push(`${enh.name} [${enh.points}pts]: ${enh.bearer}`);
        }
    }
    lines.push('');
    lines.push(`++ Total: ${list.pointsTotal}pts ++`);
    return lines.join('\n');
}
/**
 * Parse a New Recruit exported list (plain text) back to structured format
 */
export function parseNewRecruitList(text) {
    const lines = text.split('\n').map(l => l.trim()).filter(l => l);
    // Try to extract faction and points from common formats
    let faction = 'Unknown';
    let pointsTotal = 0;
    // Look for faction line (usually near the top)
    for (const line of lines.slice(0, 5)) {
        if (line.includes(' - ') || line.match(/^(Space Marines|Aeldari|T'au|Orks|Necrons|Chaos|Tyranids|Imperial|Adeptus)/i)) {
            faction = line.split(' - ')[0].trim();
            break;
        }
    }
    // Look for points total
    const pointsMatch = text.match(/(\d+)\s*(?:pts|points)/i);
    if (pointsMatch) {
        pointsTotal = parseInt(pointsMatch[1], 10);
    }
    return {
        faction,
        pointsTotal,
        rawMarkdown: text,
    };
}
/**
 * Scan the army-lists directory and return all available lists
 */
export async function scanArmyLists(armyListsDir) {
    const lists = [];
    try {
        const factions = await readdir(armyListsDir, { withFileTypes: true });
        for (const faction of factions) {
            if (!faction.isDirectory())
                continue;
            const factionPath = join(armyListsDir, faction.name);
            const files = await readdir(factionPath);
            for (const file of files) {
                if (!file.endsWith('.md'))
                    continue;
                const filePath = join(factionPath, file);
                try {
                    const content = await readFile(filePath, 'utf-8');
                    const parsed = parseMarkdownArmyList(content, filePath);
                    lists.push(parsed);
                }
                catch (err) {
                    console.error(`Error parsing ${filePath}:`, err);
                }
            }
        }
    }
    catch (err) {
        console.error(`Error scanning army lists directory:`, err);
    }
    return lists;
}
/**
 * Get a summary of an army list for display
 */
export function getListSummary(list) {
    return `${list.name} (${list.faction} - ${list.detachment}) - ${list.pointsTotal}/${list.pointsLimit}pts, ${list.units.length} units`;
}
//# sourceMappingURL=army-list-converter.js.map
/**
 * Army List Converter
 * Converts between Warhammer Veteran markdown format and New Recruit formats
 */
export interface ParsedArmyList {
    name: string;
    faction: string;
    detachment: string;
    edition: string;
    pointsTotal: number;
    pointsLimit: number;
    units: ParsedUnit[];
    enhancements: ParsedEnhancement[];
    rawMarkdown: string;
    filePath?: string;
}
export interface ParsedUnit {
    name: string;
    models: number;
    role: string;
    points: number;
    wargear?: string[];
}
export interface ParsedEnhancement {
    name: string;
    bearer: string;
    points: number;
}
/**
 * Parse a Warhammer Veteran markdown army list file
 */
export declare function parseMarkdownArmyList(markdown: string, filePath?: string): ParsedArmyList;
/**
 * Convert a parsed army list to plain text format (for New Recruit export)
 */
export declare function toPlainTextFormat(list: ParsedArmyList): string;
/**
 * Convert a parsed army list to Battlescribe-style ROS format
 * (simplified - actual ROS is XML-based)
 */
export declare function toRosterFormat(list: ParsedArmyList): string;
/**
 * Parse a New Recruit exported list (plain text) back to structured format
 */
export declare function parseNewRecruitList(text: string): Partial<ParsedArmyList>;
/**
 * Scan the army-lists directory and return all available lists
 */
export declare function scanArmyLists(armyListsDir: string): Promise<ParsedArmyList[]>;
/**
 * Get a summary of an army list for display
 */
export declare function getListSummary(list: ParsedArmyList): string;
//# sourceMappingURL=army-list-converter.d.ts.map
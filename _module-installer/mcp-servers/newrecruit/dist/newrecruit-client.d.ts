/**
 * New Recruit API Client
 * Handles authentication and API calls to newrecruit.eu
 */
export interface NRCredentials {
    login: string;
    password: string;
}
export interface NRGameSystem {
    id: number;
    name: string;
}
export interface NRTournament {
    id: number;
    id_tourny?: string;
    name: string;
    date?: string;
    game_system?: string;
    location?: string;
    players_count?: number;
}
export interface NRTournamentDetails {
    id: number;
    name: string;
    date: string;
    rounds?: NRRound[];
    players?: NRPlayer[];
}
export interface NRRound {
    round_number: number;
    pairings: NRPairing[];
}
export interface NRPairing {
    player1: string;
    player2: string;
    score1?: number;
    score2?: number;
}
export interface NRPlayer {
    login: string;
    name?: string;
    faction?: string;
    score?: number;
    exported_list?: string;
}
export interface NRReport {
    id: number;
    tournament_id: number;
    tournament_name?: string;
    player: string;
    faction?: string;
    exported_list?: string;
    score?: number;
    ranking?: number;
}
export interface NRListSubmission {
    id_tournament: string;
    army_list: string;
    faction?: string;
}
export declare class NewRecruitClient {
    private baseUrl;
    private credentials;
    constructor(credentials: NRCredentials);
    private request;
    /**
     * Get list of available game systems
     */
    getSystems(): Promise<NRGameSystem[]>;
    /**
     * Get list of tournaments
     * @param gameSystemId - Optional game system ID to filter by
     */
    getTournaments(gameSystemId?: number): Promise<NRTournament[]>;
    /**
     * Get tournament details including rounds and players
     * @param tournamentId - Tournament ID or tourny ID
     */
    getTournamentDetails(tournamentId: string | number): Promise<NRTournamentDetails>;
    /**
     * Get player reports (with army lists)
     * @param options - Filter by tournament ID and/or player name
     */
    getReports(options: {
        tournamentId?: string | number;
        player?: string;
    }): Promise<NRReport[]>;
    /**
     * Get army lists for a specific player
     * @param playerName - Player login name (case-insensitive)
     */
    getPlayerLists(playerName: string): Promise<NRReport[]>;
    /**
     * Get all army lists from a tournament
     * @param tournamentId - Tournament ID
     */
    getTournamentLists(tournamentId: string | number): Promise<NRReport[]>;
    /**
     * Test authentication by fetching game systems
     */
    testConnection(): Promise<boolean>;
}
export declare const WH40K_SYSTEM_ID = 1;
//# sourceMappingURL=newrecruit-client.d.ts.map
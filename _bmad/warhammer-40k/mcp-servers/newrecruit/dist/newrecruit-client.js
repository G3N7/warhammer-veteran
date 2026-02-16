/**
 * New Recruit API Client
 * Handles authentication and API calls to newrecruit.eu
 */
export class NewRecruitClient {
    baseUrl = 'https://www.newrecruit.eu/api';
    credentials;
    constructor(credentials) {
        this.credentials = credentials;
    }
    async request(endpoint, body) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'NR-Login': this.credentials.login,
                'NR-Password': this.credentials.password,
            },
            body: body ? JSON.stringify(body) : undefined,
        });
        if (!response.ok) {
            const text = await response.text();
            throw new Error(`New Recruit API error (${response.status}): ${text}`);
        }
        const data = await response.json();
        // Check for API-level errors
        if (data.error) {
            throw new Error(`New Recruit API error: ${data.error}`);
        }
        if (data.message && data.message.includes('Wrong username/password')) {
            throw new Error('Authentication failed: Invalid NR_LOGIN or NR_PASSWORD credentials');
        }
        return data;
    }
    /**
     * Get list of available game systems
     */
    async getSystems() {
        return this.request('/systems');
    }
    /**
     * Get list of tournaments
     * @param gameSystemId - Optional game system ID to filter by
     */
    async getTournaments(gameSystemId) {
        const body = gameSystemId ? { id_game_system: gameSystemId } : undefined;
        return this.request('/tournaments', body);
    }
    /**
     * Get tournament details including rounds and players
     * @param tournamentId - Tournament ID or tourny ID
     */
    async getTournamentDetails(tournamentId) {
        return this.request('/tournament', {
            id_tournament: String(tournamentId),
        });
    }
    /**
     * Get player reports (with army lists)
     * @param options - Filter by tournament ID and/or player name
     */
    async getReports(options) {
        const body = {};
        if (options.tournamentId) {
            body.id_tournament = String(options.tournamentId);
        }
        if (options.player) {
            body.player = options.player;
        }
        if (Object.keys(body).length === 0) {
            throw new Error('At least one of tournamentId or player must be provided');
        }
        return this.request('/reports', body);
    }
    /**
     * Get army lists for a specific player
     * @param playerName - Player login name (case-insensitive)
     */
    async getPlayerLists(playerName) {
        return this.getReports({ player: playerName });
    }
    /**
     * Get all army lists from a tournament
     * @param tournamentId - Tournament ID
     */
    async getTournamentLists(tournamentId) {
        return this.getReports({ tournamentId });
    }
    /**
     * Test authentication by fetching game systems
     */
    async testConnection() {
        try {
            await this.getSystems();
            return true;
        }
        catch {
            return false;
        }
    }
}
// Warhammer 40k Game System ID (you may need to discover this dynamically)
export const WH40K_SYSTEM_ID = 1; // Placeholder - will be discovered via getSystems()
//# sourceMappingURL=newrecruit-client.js.map
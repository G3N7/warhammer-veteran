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

export class NewRecruitClient {
  private baseUrl = 'https://www.newrecruit.eu/api';
  private credentials: NRCredentials;

  constructor(credentials: NRCredentials) {
    this.credentials = credentials;
  }

  private async request<T>(endpoint: string, body?: object): Promise<T> {
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

    return data as T;
  }

  /**
   * Get list of available game systems
   */
  async getSystems(): Promise<NRGameSystem[]> {
    return this.request<NRGameSystem[]>('/systems');
  }

  /**
   * Get list of tournaments
   * @param gameSystemId - Optional game system ID to filter by
   */
  async getTournaments(gameSystemId?: number): Promise<NRTournament[]> {
    const body = gameSystemId ? { id_game_system: gameSystemId } : undefined;
    return this.request<NRTournament[]>('/tournaments', body);
  }

  /**
   * Get tournament details including rounds and players
   * @param tournamentId - Tournament ID or tourny ID
   */
  async getTournamentDetails(tournamentId: string | number): Promise<NRTournamentDetails> {
    return this.request<NRTournamentDetails>('/tournament', {
      id_tournament: String(tournamentId),
    });
  }

  /**
   * Get player reports (with army lists)
   * @param options - Filter by tournament ID and/or player name
   */
  async getReports(options: {
    tournamentId?: string | number;
    player?: string;
  }): Promise<NRReport[]> {
    const body: Record<string, string> = {};

    if (options.tournamentId) {
      body.id_tournament = String(options.tournamentId);
    }
    if (options.player) {
      body.player = options.player;
    }

    if (Object.keys(body).length === 0) {
      throw new Error('At least one of tournamentId or player must be provided');
    }

    return this.request<NRReport[]>('/reports', body);
  }

  /**
   * Get army lists for a specific player
   * @param playerName - Player login name (case-insensitive)
   */
  async getPlayerLists(playerName: string): Promise<NRReport[]> {
    return this.getReports({ player: playerName });
  }

  /**
   * Get all army lists from a tournament
   * @param tournamentId - Tournament ID
   */
  async getTournamentLists(tournamentId: string | number): Promise<NRReport[]> {
    return this.getReports({ tournamentId });
  }

  /**
   * Test authentication by fetching game systems
   */
  async testConnection(): Promise<boolean> {
    try {
      await this.getSystems();
      return true;
    } catch {
      return false;
    }
  }
}

// Warhammer 40k Game System ID (you may need to discover this dynamically)
export const WH40K_SYSTEM_ID = 1; // Placeholder - will be discovered via getSystems()

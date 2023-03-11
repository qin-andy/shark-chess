
/**
 * Mapping of a game result retrieved from DB
 * Represents a single game between two players
 */
export interface GameResult {
  matchupId: string,
  winningPlayer: string,  // TODO: could strict type this with union types.
  winningColor: string,
  endReason: string,
  moves: number,
  time: number,
  pgn: string,
  white: string,
  black: string,
  endingFEN: string,
}

/**
 * Mapping of player retrieved from DB
 * Stores info for a player's overall tourney performance
 */
export interface Player {
  name: string,
  id: number,
  elo: number,
  wins: number,
  losses: number,
  draws: number,
}

/** Wrapper for tourney data used by Cell components including UI state */
export interface CellData {
  x: number,
  y: number,
  players: Player[],
  games: GameResult[],
  highlighted: boolean,
  open: boolean,
}

/** Wrapper for game item used by game list components */
export interface GameItemData {
  game: GameResult,
  highlighted: boolean,
  open: boolean,
}
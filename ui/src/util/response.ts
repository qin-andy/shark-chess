import { parseJsonText } from "typescript";
import { GameResult, Player } from "../types";

/** 
 * Takes a json list of game results and transofmrs them into a list of
 *  GameResult  objects
 */
export const processGamesResponse = (data: any) => {
  let results: GameResult[] = [];
  for (let i = 0; i < data.length; i++) {
    let gameResultDict = data[i];
    let gameResult: GameResult = {
      matchupId: gameResultDict['Matchup ID'],
      winningPlayer: gameResultDict['Winning Player'],
      winningColor: gameResultDict['Winning Color'],
      endReason: gameResultDict['End Reason'],
      moves: gameResultDict['Moves'],
      time: gameResultDict['Time'],
      pgn: gameResultDict['PGN'],
      white: gameResultDict['White'],
      black: gameResultDict['Black'],
      endingFEN: gameResultDict['Ending FEN'],
    };
    results.push(gameResult);
  }
  return results;
}

export const processPlayerResponse = (data: any) => {
  let results: Player[] = [];
  for (let i = 0; i < data.length; i++) {
    let p = data[i];
    let player: Player = {
      name: p['Name'],
      id: p['ID'],
      elo: p['Elo'],
      wins: p['Wins'],
      losses: p['Losses'],
      draws: p['Draws'],
      thinkTime: p['Think Time'],
      totalMoves: p['Moves'],
      botCode: p['Bot Code'],
      botSettings: p['Bot Settings']
    }
    results.push(player);
  }
  return results;
}

// generates 2d array indexted by matchups
export const aggregateMatchups = (games: GameResult[], players: Player[]): GameResult[][][] => {
  // matches[white player id][black player id][game number]
  const matches: any = {};

  games.forEach((game) => {
    const players = game.matchupId.split(',');
    const white = players[0];
    const black = players[1];
    if (matches[white] == null) {
      matches[white] = {};
    }
    if (matches[white][black] == null) {
      matches[white][black] = [];
    }
    matches[white][black].push(game);
  });

  // fill mirror matches
  players.forEach((player, index) => {
    matches[index][index] = []
  });
  return matches;
}
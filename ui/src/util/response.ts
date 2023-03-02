import { parseJsonText } from "typescript";
import { GameResult, Player } from "../types";

/** 
 * Takes a json list of game results and transofmrs them into a list of
 *  GameResult  objects
 */
export const processGamesResponse = (data: any) => {
  let results: GameResult[] = [];
  for (let i = 0; i < data.length; i++) {
    let gameResultData = data[i];
    let gameResult: GameResult = {
      matchupId: gameResultData['Matchup ID'],
      winningPlayer: gameResultData['Winning Player'],
      winningColor: gameResultData['Winning Color'],
      endReason: gameResultData['End Reason'],
      moves: gameResultData['Moves'],
      time: gameResultData['Time'],
      pgn: gameResultData['PGN'],
      white: gameResultData['White'],
      black: gameResultData['Black'],
      endingFEN: gameResultData['Ending FEN'],
    };
    results.push(gameResult);
  }
  return results;
}

export const processPlayerResponse = (data: any) => {
  let results: Player[] = [];
  for (let i = 0; i < data.length; i++) {
    let playerData = data[i];
    let player: Player = {
      name: playerData['Name'],
      id: playerData['ID'],
      elo: playerData['Elo'],
      wins: playerData['Wins'],
      losses: playerData['Losses'],
      draws: playerData['Draws'],
    }
    results.push(player);
  }
  return results;
}

export const aggregateMatchups = (games: GameResult[], players: Player[]) => {
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
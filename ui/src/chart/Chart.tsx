import React, { useEffect, useState } from 'react';
import { GameResult, Player } from '../types';
import { aggregateMatchups, processGamesResponse, processPlayerResponse } from '../util/response';
import Cell from './Cell';

const Chart = () => {
  const [games, setGames] = useState<GameResult[]>();
  const [players, setPlayers] = useState<Player[]>();
  const [matchups, setMatchups] = useState<any>();
  const [ordering, setOrdering] = useState<number[]>([]);

  useEffect(() => {
    const dataset = 'nine'; // For testing directory

    fetch(`./results/${dataset}/games.json`)
      .then((response) => response.json())
      .then((json) => {
        let games = processGamesResponse(json);
        setGames(games);
        console.log(games);
      });

    fetch(`./results/${dataset}/players.json`)
      .then((response) => response.json())
      .then((json) => {
        let players = processPlayerResponse(json);
        setPlayers(players);
        console.log(players);
      });
  }, []);

  useEffect(() => {
    if (players && games) {
      const matchups = aggregateMatchups(games, players);
      setMatchups(matchups);
      let order = generateOrdering(players);
      console.log(order);
      setOrdering(order);
    }
  }, [games, players])


  const dimension = players == null ? 3 : players.length
  const chartStyle = {
    display: 'grid',
    gridTemplateRows: `repeat(${dimension}, 100px)`,
    gridTemplateColumns: `repeat(${dimension}, 100px)`,
  };

  const buildCells = () => { // TODO : refactor into static method
    if (players == null || matchups == null || ordering == null) return;

    const dimension = players.length
    const cells_y = []
    for (let i = 0; i < dimension; i++) {
      const cells_x = [];
      let x = ordering[i]

      for (let j = 0; j < dimension; j++) {
        let y = ordering[j]
        cells_x.push(
          <Cell 
            key={x + ',' + y}
            x={x} 
            y={y}
            players={players}
            games={matchups[x][y]}
          />
        )
      }
      cells_y.push(cells_x);
    }
    return cells_y;
  }

  return (
    <>
      <div style={chartStyle}>
        {buildCells()}
      </div>
    </>
  )
}

// Generates an array of player ids in order of ELO
const generateOrdering = (players: Player[]) => {
  players.sort((a, b) => {
    return a.elo - b.elo
  });
  return players.map((player) => {
    return player.id
  });
}

export default Chart;
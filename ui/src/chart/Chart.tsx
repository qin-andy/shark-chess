import React, { useEffect, useState } from 'react';
import { GameResult, Player } from '../types';
import { aggregateMatchups, processGamesResponse, processPlayerResponse } from '../util/response';
import Cell from './Cell';

const Chart = (props: {
  games: GameResult[] | undefined;
  players: Player[] | undefined;
}) => {
  const { players, games } = props;

  const [matchups, setMatchups] = useState<any>();
  const [ordering, setOrdering] = useState<number[]>([]);

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
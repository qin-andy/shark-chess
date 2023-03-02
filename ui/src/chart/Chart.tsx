import React, { useEffect, useState } from 'react';
import { GameResult, Player } from '../types';
import { dummyGames, dummyPlayers } from '../util/dummy';
import { aggregateMatchups, processGamesResponse, processPlayerResponse, summarizeMatch } from '../util/response';

const Chart = () => {
  const [games, setGames] = useState<GameResult[]>();
  const [players, setPlayers] = useState<Player[]>();
  const [matchups, setMatchups] = useState<any>();

  useEffect(() => {
    // let games = processGamesResponse(dummyGames);
    // let players = processPlayerResponse(dummyPlayers);
    // let games = processGamesResponse(JSON.parse('/results/big/games.json'));
    // let players = processPlayerResponse(JSON.parse('/results/big/players.json'));
    
    // setGames(games);
    // setPlayers(players);
    // setMatchups(matchups);

    fetch('./results/big/games.json')
      .then((response) => response.json())
      .then((json) => {
        let games = processGamesResponse(json);
        setGames(games);
        console.log(games);
      });

    fetch('./results/big/players.json')
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
    }
  }, [games, players])


  const dimension = players == null ? 3 : players.length
  const chartStyle = {
    display: 'grid',
    gridTemplateRows: `repeat(${dimension}, 150px)`,
    gridTemplateColumns: `repeat(${dimension}, 150px)`,
  };

  const buildCells = () => {
    if (players == null || matchups == null) return;

    const dimension = players.length
    const cells_y = []
    for (let y = 0; y < dimension; y++) {
      const cells_x = [];
      for (let x = 0; x < dimension; x++) {
        const matchSummary = summarizeMatch(matchups[x][y]);
        cells_x.push(
          <div style={{borderStyle: 'solid'}}>
            <p>
              ({x},{y})
            </p>
            <p>
                {matchups[x][y] == null ? '' 
                : matchups[x][y][0] == null ? 'x' :  matchups[x][y][0].white}
            </p>            
            <p>
                {matchups[x][y] == null ? '' 
                : matchups[x][y][0] == null ? 'x' :  matchups[x][y][0].black}
            </p>
            <p>
              {matchSummary[0]}/
              {matchSummary[1]}/
              {matchSummary[2]}
            </p>
          </div>
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

export default Chart;
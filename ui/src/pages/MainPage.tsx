import React, { useEffect, useState } from 'react';
import Chart from '../chart/Chart';
import PlayerList from '../player/PlayerList';
import { CellData, GameResult, Player } from '../types';
import { aggregateMatchups, processGamesResponse, processPlayerResponse } from '../util/response';

const MainPage = () => {
  const [playerData, setPlayerData] = useState<Player[]>();
  const [gameData, setGameData] = useState<GameResult[]>();
  const [matchups, setMatchups] = useState<any>();
  const [cellData, setCellData] = useState<CellData[][]>();

  useEffect(() => {
    // TODO: refactor this to a config file
    const dataset = 'manager'; // For testing directory

    // fetch(`./results/${dataset}/${dataset}_tourney.json`)
    //   .then((response) => response.json())
    //   .then((json) => {
    //     let games = processGamesResponse(json['Games']);
    //     setGameData(games);
    //     console.log(games);

    //     let players = processPlayerResponse(json['Players']);
    //     players?.sort((a, b) => {
    //       return b.elo - a.elo
    //     });
    //     setPlayerData(players);
    //     console.log(players);
    //   });

    // Hit FLask API
    fetch(`http://localhost:5000/tourney/${dataset}`)
      .then((response) => response.json())
      .then((json) => {
        let games = processGamesResponse(json['Games']);
        setGameData(games);
        console.log(games);

        let players = processPlayerResponse(json['Players']);
        players?.sort((a, b) => {
          return b.elo - a.elo
        });
        setPlayerData(players);
        console.log(players);
      });
  }, []);

  useEffect(() => {
    if (playerData && gameData) {
      const matchups = aggregateMatchups(gameData, playerData);
      setMatchups(matchups);
      let cd = populateCellData(gameData, playerData.slice().reverse(), matchups);
      setCellData(cd);
    }
  }, [gameData, playerData])

  /** Mutates the open attribute of [y,x] and disables open for all other cells */
  const openCell = (x_index: number, y_index: number) => {
    console.log('Opening' + x_index + ',' + y_index)
    if (!cellData) return;
    let newCellData = cellData.map((cellRow, y_col) => {
      let newCellRow = cellRow.map((cell, x_row) => {
        if ((y_col === y_index) && (x_row === x_index)) {
          cell.open = true;
        } else {
          cell.open = false
        }
        return cell;
      });
      return newCellRow;
    });
    setCellData(newCellData);
  }

  return (
    <>
      <Chart
       players={playerData} 
       games={gameData} 
       matchups={matchups} 
       cellData={cellData} 
       openCell={openCell}
      />
      <PlayerList players={playerData} games={gameData} />
    </>
  )
}

// Build cell data pre component
const populateCellData = (games?: GameResult[], players?: Player[], matchups?: GameResult[][][]) => {
  if (players == null || matchups == null) return [];

  const dimension = players.length
  const cells_y: CellData[][] = []
  for (let i = 0; i < dimension; i++) {
    const cells_x: CellData[] = [];
    let x = players[i].id; // TODO : conditional logic here is iff. what does x/y represnt here if not coords?

    for (let j = 0; j < dimension; j++) {
      let y = players[j].id
      cells_x.push({
        x, y, players,
        games: matchups[x][y],
        highlighted: false,
        open: false,
      });
    }
    cells_y.push(cells_x);
  }
  return cells_y;
}

export default MainPage;

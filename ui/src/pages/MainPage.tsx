import React, { useEffect, useState } from 'react';
import Chart from '../chart/Chart';
import PlayerList from '../player/PlayerList';
import { CellData, GameResult, Player } from '../types';
import { aggregateMatchups, processGamesResponse, processPlayerResponse } from '../util/response';

const MainPage = () => {
  const [currentPlayers, setCurrentPlayers] = useState<Player[]>();
  const [currentGames, setCurrentGames] = useState<GameResult[]>();
  const [matchups, setMatchups] = useState<any>();
  const [cellData, setCellData] = useState<CellData[][]>();

  useEffect(() => {
    // TODO: refactor this to a config file
    const dataset = 'manager'; // For testing directory

    // Hit Flask API
    fetch(`http://localhost:5000/tourney/${dataset}`)
      .then((response) => response.json())
      .then((json) => {
        let gameResults = processGamesResponse(json['Games']);
        setCurrentGames(gameResults);
        console.log(gameResults);

        let players = processPlayerResponse(json['Players']);

        // Ordering players is handled here.
        players?.sort((a, b) => {
          return b.elo - a.elo
        });
        setCurrentPlayers(players);
        console.log(players);
      });
  }, []);

  // Use Effect hook to sort games into matchups when gameData and playerData is populated
  useEffect(() => {
    if (currentPlayers && currentGames) {
      const matchups = aggregateMatchups(currentGames, currentPlayers);
      setMatchups(matchups);
      let cd = populateCellData(currentPlayers.slice().reverse(), matchups);
      setCellData(cd);
    }
  }, [currentGames, currentPlayers])

  // Mutually exclusive cell opening logic
  // Mutates the open attribute of [y,x] and disables open for all other cells
  const openCell = (x_index: number, y_index: number) => {
    console.log('Opening ' + x_index + ',' + y_index)
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

  // Toggles highlighting a cell or clearing all cells
  const highlightCell = (x_index: number, y_index: number) => {
    // This could be a one liner, but it's more explicit as an if else
    let clearing: boolean = false;
    if (x_index === -1 && y_index === -1) clearing = true;

    console.log('Highlighting ' + x_index + ',' + y_index)
    if (!cellData) return;
    let newCellData = cellData.map((cellRow, y_col) => {
      let newCellRow = cellRow.map((cell, x_row) => {
        if (clearing) cell.highlighted = false; // clearing case
        else if ((y_col === y_index) && (x_row === x_index)) { // default case
          cell.highlighted = true;
        }
        return cell;
      });
      return newCellRow;
    });
    setCellData(newCellData);
  }

  const highlightPlayerCells = (pid: number) => {
    console.log('Highlighting pid: ' + pid)
    if (!cellData) return;
    let newCellData = cellData.map((cellRow) => {
      let newCellRow = cellRow.map((cell) => {
        if ((pid === cell.x) || (pid === cell.y)) {
          cell.highlighted = true;
          console.log('highlighted ' + cell.x + ',' + cell.y)
        }
        else cell.highlighted = false

        return cell;
      });
      return newCellRow;
    });
    setCellData(newCellData);
  }

  return (
    <>
      <Chart
        players={currentPlayers}
        games={currentGames}
        matchups={matchups}
        cellData={cellData}
        openCell={openCell}
        highlightCell={highlightCell}
      />
      <PlayerList
        players={currentPlayers}
        games={currentGames}
        highlightCell={highlightCell}
        highlightPlayerCells={highlightPlayerCells}
      />
    </>
  )
}

// Build cell data pre component
const populateCellData = (players: Player[], matchups: GameResult[][][]) => {
  if (players == null || matchups == null) return [];

  const dimension = players.length
  const cells_y: CellData[][] = []
  for (let i = 0; i < dimension; i++) {
    const cells_x: CellData[] = [];
    let x = players[i].id; // TODO : conditional logic here is iff. what does x/y represnt here if not coords?

    for (let j = 0; j < dimension; j++) {
      let y = players[j].id
      cells_x.push({
        // TODO : X, Y DO NOT REPRESENT THE X Y COORDINATES. THEY REPRESENT THE PLAYER IDS. ?????
        x: x,
        y: y,
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

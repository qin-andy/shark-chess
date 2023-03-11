import React, { useEffect, useState } from 'react';
import { CellData, GameResult, Player } from '../types';
import { aggregateMatchups, processGamesResponse, processPlayerResponse } from '../util/response';
import Cell from './Cell';

const Chart = (props: {
  games: GameResult[] | undefined;
  players: Player[] | undefined;
  matchups: GameResult[][][] | undefined;
  cellData: CellData[][] | undefined;
  openCell: Function;
}) => {
  const { players, games, matchups, cellData, openCell } = props;
  const dimension = players == null ? 3 : players.length
  const chartStyle = {
    display: 'grid',
    gridTemplateRows: `repeat(${dimension}, 100px)`,
    gridTemplateColumns: `repeat(${dimension}, 100px)`,
  };

  // consolidate cell data in components
  const createCellComponents = (cellData?: CellData[][]) => {
    if (!cellData) return [];
    let components = []
    for (let y = 0; y < cellData.length; y++) {
      let y_row = [];
      for (let x = 0; x < cellData.length; x++) {
        let c = cellData[y][x];
        let element = (
          <Cell 
            key={c.x + ',' + c.y}
            x={x} // Note we're using the x, y coords from the iteration rather than CELL.X and CELL.Y.
            y={y}
            players={c.players}
            games={c.games}
            highlighted={c.highlighted}
            open={c.open}
            openCell={openCell}
          />
        )
        y_row.push(element);
      }
      components.push(y_row);
    }
    return components;
  }

  return (
    <>
      <div style={chartStyle}>
        {createCellComponents(cellData)}
      </div>
    </>
  )
}

export default Chart;
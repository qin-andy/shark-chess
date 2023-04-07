import React from 'react';
import { GameResult, Player } from '../types';
import PlayerSummary from './PlayerListItem';
import './PlayerList.css'

const PlayerList = (props: {
  games: GameResult[] | undefined;
  players: Player[] | undefined;
  highlightPlayerCells: Function;
  highlightCell: Function;
}) => {
  const { players, games, highlightPlayerCells, highlightCell } = props;

  return (
    <div className='player-list'>
      {players?.map((player, index) => {
        return <PlayerSummary
          player={player}
          key={index}
          highlightPlayerCells={highlightPlayerCells}
          highlightCell={highlightCell}
        />
      })}
    </div>
  )
}

export default PlayerList;
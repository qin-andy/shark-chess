import React from 'react';
import { GameResult, Player } from '../types';
import PlayerSummary from './PlayerListItem';
import './PlayerList.css'

const PlayerList = (props: {
  games: GameResult[] | undefined;
  players: Player[] | undefined;
}) => {
  const { players, games } = props;

  return (
    <div className='player-list'>
      {players?.map((player, index) => {
        return <PlayerSummary player={player} />
      })}
    </div>
  )
}

export default PlayerList;
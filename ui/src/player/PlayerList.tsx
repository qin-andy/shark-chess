import React from 'react';
import { GameResult, Player } from '../types';
import PlayerSummary from './PlayerListItem';
import './PlayerList.css'

const PlayerList = (props: {
  games: GameResult[] | undefined;
  players: Player[] | undefined;
}) => {
  const { players, games } = props;

  players?.sort((a, b) => { // TODO : refactor above with player ordering for the chart
    return b.elo - a.elo
  });

  return (
    <div className='player-list'>
      {/* <h1>PLAYERS</h1> */}
      {players?.map((player, index) => {
        return <PlayerSummary player={player} />
      })}
    </div>
  )
}

export default PlayerList;
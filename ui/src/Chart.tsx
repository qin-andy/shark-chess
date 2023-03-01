import React, { useEffect } from 'react';
import { dummyGames, dummyPlayers } from './util/dummy';
import { processGamesResponse, processPlayerResponse } from './util/response';

const Chart = () => {
  useEffect(() => {
    let games = processGamesResponse(dummyGames)
    let players = processPlayerResponse(dummyPlayers)
    console.table(players)
  }, []);

  return (
    <>
      <p>
        Chart!
      </p>
    </>
  )
}

export default Chart;
import React, { useEffect, useState } from 'react';
import Chart from '../chart/Chart';
import PlayerList from '../player/PlayerList';
import { GameResult, Player } from '../types';
import { processGamesResponse, processPlayerResponse } from '../util/response';

const MainPage = () => {
  const [playerData, setPlayerData] = useState<Player[]>();
  const [gameData, setGameData] = useState<GameResult[]>();

  useEffect(() => {
    const dataset = 'nine'; // For testing directory

    fetch(`./results/${dataset}/games.json`)
      .then((response) => response.json())
      .then((json) => {
        let games = processGamesResponse(json);
        setGameData(games);
        console.log(games);
      });

    fetch(`./results/${dataset}/players.json`)
      .then((response) => response.json())
      .then((json) => {
        let players = processPlayerResponse(json);
        setPlayerData(players);
        console.log(players);
      });
  }, []);

  return (
    <>
      <Chart players={playerData} games={gameData} />
      <PlayerList players={playerData} games={gameData} />
    </>
  )
}

export default MainPage;

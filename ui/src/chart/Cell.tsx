import React, { CSSProperties, useState } from 'react';
import { GameResult, Player } from '../types';

const Cell = (props: {
  x: number,
  y: number,
  players: Player[],
  games: GameResult[]
}) => {
  const [showList, setShowList] = useState(false);

  const handleClick = () => {
    setShowList(true)
  }

  const handleMouseLeave = () => {
    setShowList(false);
  }

  let { x, y, games, players } = props;
  let style: CSSProperties = {
    borderStyle: 'solid',
    position: 'relative'
  };

  // Mirror match case, show nothing
  if (x === y) {
    return (
      <div style={style}>
        <p>{x},{y}</p>
      </div>
    )
  }

  let wp = games[0].white;
  let bp = games[0].black;

  let [w, l, d] = summarizeMatch(games);
  let [r, g, b] = generateRGB(w, l, d);

  let new_style: CSSProperties = {...style, 
    backgroundColor: `rgb(${r},${g},${b})`
  };

  let listComponent = (
    <div
      style = {{
        position: 'absolute',
        backgroundColor: 'whitesmoke', 
        zIndex: 10,
        top: '10px',
        left: '120px',
        width: '300px',
        height: '400px',
        border: '3px solid',
        overflowY: 'auto'
      }}
    >
      <p>{wp} vs {bp}</p>
      <ul>
        {games.map((game, idx) => {
          return (
            <li key={idx} onClick={() => console.log(game.endingFEN)}>
              {game.winningPlayer} wins in {game.moves} moves
            </li>
          )
        })}
      </ul>
    </div>
  )

  return (
    <>
      <div 
        style={new_style}
        onClick={handleClick}
        onMouseLeave={handleMouseLeave}
      >
        {showList ? listComponent : null}
        <p>{x},{y}</p>
        <p>white: {wp}</p>
        <p>black: {bp}</p>
        <p>{w}/{l}/{d}</p>
      </div>
    </>
  )
}

const generateRGB = (w: number, l: number, d: number) => {
  let r = 0;
  let g = 0;
  let b = 0;

  let total = w + l + d;
  let max = 255;

  let w_ratio = w / total;
  let l_ratio = l / total; // L + ratio + you fell off + didn't ask
  let d_ratio = d / total;

  r = w_ratio * max;
  g = l_ratio * max;
  b = d_ratio * max;

  return [r, g, b];
}

const summarizeMatch = (results: GameResult[]) => {
  let wins = 0;
  let losses = 0;
  let draws = 0;
  results.forEach((result) => {
    if (result.winningColor == 'white') {
      wins += 1
    } else if (result.winningColor == 'black') {
      losses += 1
    } else {
      draws += 1
    }
  });
  return [wins, losses, draws]
}

export default Cell;

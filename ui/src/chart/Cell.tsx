import React, { CSSProperties, useState } from 'react';
import { GameResult, Player } from '../types';
import CellList from './CellList';

const Cell = (props: {
  x: number,
  y: number,
  players: Player[],
  games: GameResult[]
}) => {
  const [showList, setShowList] = useState(false);
  const [showListTimer, setShowListTimer] = useState<NodeJS.Timer>();

  const handleClick = () => {
    setShowList(!showList)
    // if (showListTimer) clearTimeout(showListTimer);
  }

  const handleHover = () => {
    // if (showListTimer) clearTimeout(showListTimer);
  }

  const handleMouseLeave = () => {
    // let timer = setTimeout(() => {
      // setShowList(false);
    // }, 1000)
    // setShowListTimer(timer);
  }

  let { x, y, games, players } = props;
  let style: CSSProperties = {
    border: ' 2px solid',
    borderRadius: '15px',
    position: 'relative',
    padding: '0px',
    margin: '0px', 

    fontSize: '14px',
    textAlign: 'center',
  };
  
  let playerDisplayStyle: CSSProperties = {
    // border: '3px solid',
    // borderRadius: '15px',
    margin: '2px',
  }

  // Mirror match case, show nothing
  if (x === y) {
    return (
      <div style={style}>
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

  return (
    <>
      <div 
        style={new_style}
        onClick={handleClick}
        onMouseEnter={handleHover}
        onMouseLeave={handleMouseLeave}
      >
        {showList ? <CellList wp={wp} bp={bp} games={games} /> : null}
        <p/>
        <p style={playerDisplayStyle}>{wp}</p>
        <p style={playerDisplayStyle}>{bp}</p>
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
  // Max ratio, set in order to make colors more pastel
  let max = 190; 

  let w_ratio = w / total;
  let l_ratio = l / total; // L + ratio + you fell off + didn't ask
  let d_ratio = d / total;

  r = l_ratio * max + 64; // LOSSES
  g = d_ratio * (max/2) + 127;  // DRAWS weighted less, seeing wins/losses is bigger
  b = w_ratio * max + 127; // WINS

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

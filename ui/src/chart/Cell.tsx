import React, { CSSProperties, useState } from 'react';
import { GameResult, Player } from '../types';
import CellList from './CellList';
import './Cell.css';

const Cell = (props: {
  x: number,
  y: number,
  players: Player[],
  games: GameResult[],
  highlighted: boolean,
  open: boolean,
  openCell: Function,
}) => {
  let { x, y, games, players, highlighted, open, openCell} = props;

  const [showList, setShowList] = useState(false);
  const [hover, setHover] = useState(false);

  const handleClick = () => {
    setShowList(!showList)
    let a = open ? openCell(-1, -1) : openCell(x, y); // hacky toggle
  }

  const handleHover = () => {
    setHover(true);
  }

  const handleUnhover = () => {
    setHover(false);
  }


  let playerDisplayStyle: CSSProperties = {
    margin: '2px',
  }

  // Mirror match case, show nothing
  if (x === y) {
    return (
      <div className='cell'>
      </div>
    )
  }

  let wp = games[0].white;
  let bp = games[0].black;

  let [w, l, d] = summarizeMatch(games);
  let [r, g, b] = generateRGB(w, l, d);
  if (open) {
    r -= 70;
    g -= 70;
    b -= 70;
  }

  if (hover) {
    r -= 30;
    g -= 30;
    b -= 30;
  }

  let new_style: CSSProperties = {
    backgroundColor: `rgb(${r},${g},${b})`
  };

  return (
    <>
      <div 
        className='cell'
        style={new_style}
      >
        {open ? <CellList wp={wp} bp={bp} games={games} /> : null}
        <div
          onClick={handleClick}
          onMouseEnter={handleHover}
          onMouseLeave={handleUnhover}
        >
          <p/>
          <p style={playerDisplayStyle}>{wp}</p>
          <p style={playerDisplayStyle}>{bp}</p>
          <p>{w}/{l}/{d}</p>
        </div>
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

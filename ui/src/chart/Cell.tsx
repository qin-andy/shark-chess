import React, { CSSProperties, useState } from 'react';
import { GameResult, Player } from '../types';
import CellList from './CellList';
import './Cell.css';

const Cell = (props: {
  x: number,
  y: number,
  games: GameResult[],
  highlighted: boolean,
  open: boolean,
  openCell: Function,
  highlightCell: Function,
}) => {
  let { x, y, games, highlighted, open, openCell, highlightCell } = props;

  const [showList, setShowList] = useState(false);
  const [hover, setHover] = useState(false);

  const handleClick = () => {
    setShowList(!showList)
    let a = open ? openCell(-1, -1) : openCell(x, y); // hacky toggle
  }

  const handleHover = () => {
    setHover(true);
    // highlightCell(x, y)
  }

  const handleUnhover = () => {
    setHover(false);
  }


  let playerDisplayStyle: CSSProperties = {
    margin: '2px',
  }

  // Empty match case, show nothing
  if (games === undefined || games.length === 0) {
    return (
      <div className='cell'>
      </div>
    )
  }

  let wp = games[0].white;
  let bp = games[0].black;

  let [w, l, d] = summarizeMatchup(games);
  let [r, g, b] = generateRGB(w, l, d);
  if (open) {
    r -= 70;
    g -= 70;
    b -= 70;
  }

  // highlighting logic
  if (hover) {
    r -= 20;
    g -= 20;
    b -= 20;
  }


  let new_style: CSSProperties = {
    backgroundColor: `rgb(${r},${g},${b})`
  };

  return (
    <>
      <div
        className={'cell ' + (highlighted ? 'cell-highlighted' : '')}
        style={new_style}
      >
        {open ? <CellList wp={wp} bp={bp} games={games} /> : null}
        <div
          onClick={handleClick}
          onMouseEnter={handleHover}
          onMouseLeave={handleUnhover}
        >
          <p />
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
  g = d_ratio * (max / 2) + 127;  // DRAWS weighted less, seeing wins/losses is bigger
  b = w_ratio * max + 127; // WINS

  return [r, g, b];
}

const summarizeMatchup = (results: GameResult[]) => {
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

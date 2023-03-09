import React, { CSSProperties } from 'react';
import { Player } from "../types"

const PlayerSummary = (props: {
  player: Player
}) => {
  const { player } = props;

  const {wins, losses, draws} = player;
  
  let [r, g, b] = generateRGB(wins, losses, draws); // TODO: refactor with Cell coloring

  let new_style: CSSProperties = {
    backgroundColor: `rgb(${r},${g},${b})`
  };

  return (
    <div className='player-list-item' style={new_style}>
      <p className='player-name'>{player.name}</p>
      <p className='player-elo'>{player.elo}</p>
      <p className='player-wld'>{wins}/{losses}/{draws}</p>
    </div>
  )
}

// TODO : refactor with cell coloring, should generate the same rgb
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

export default PlayerSummary;

import { useState, CSSProperties } from "react";
import { GameResult } from "../types";
import GamePreview from "./GamePreview";

const CellListItem = (props: {
  game: GameResult,
  open: boolean,
  highlighted: boolean,
  index: number,
  openGameItem: Function,
}) => {
  let { game, open, highlighted, index, openGameItem } = props;

  const [hover, setHover] = useState(false);
  const [clicked, setClicked] = useState(false);

  const onMouseEnter = () => { 
    openGameItem(index)
  }

  const onMouseLeave = () => {
    setHover(false)
    // setClicked(false);
  }

  const onMouseClick = () => {
    setClicked(!clicked);
    openGameItem(index);
    
  }

  // Coloring
  let bgColor = 'white';
  if (game.winningColor === 'black') bgColor = 'gray';
  else if (game.winningColor === 'white') bgColor = 'silver';

  let style: CSSProperties = { backgroundColor: bgColor };

  return (
    <div 
      className='cell-list-item'
      style={style}
      onClick={onMouseClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      {game.winningPlayer} wins in {game.moves} moves
      {open ? <GamePreview game={game} /> : null}
    </div>
  )
}

export default CellListItem;

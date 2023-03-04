import { useState, CSSProperties } from "react";
import { GameResult } from "../types";
import GamePreview from "./GamePreview";

const CellListItem = (props: {
  game: GameResult,
}) => {
  const [hover, setHover] = useState(false);
  const [clicked, setClicked] = useState(false);

  const onMouseEnter = () => { 
    setHover(true);
  }

  const onMouseLeave = () => {
    setHover(false)
    // setClicked(false);
  }

  const onMouseClick = () => {
    setClicked(!clicked);
  }

  let { game } = props;

  // Coloring
  let bgColor = 'white';
  if (game.winningColor === 'black') bgColor = 'gray';
  else if (game.winningColor === 'white') bgColor = 'silver';

  let style: CSSProperties = {
    border: 'solid 1px',
    backgroundColor: bgColor,

    display: 'flex', 
    flexDirection: 'column',
    alignItems: 'center',
  }

  return (
    <div 
      style={style} 
      onClick={onMouseClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      {game.winningPlayer} wins in {game.moves} moves
      {clicked ? <GamePreview game={game} /> : null}
    </div>
  )
}

export default CellListItem;

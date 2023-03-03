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
    setClicked(false);
  }

  const onMouseClick = () => {
    setClicked(!clicked);
  }

  let { game } = props;

  let style: CSSProperties = {
    border: 'solid 1px',
    backgroundColor: hover ? 'gray' : 'whitesmoke'
  }

  return (
    <div 
      style={style} 
      onClick={() => console.log(game.endingFEN)}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      onMouseDown={onMouseClick}
    >
      {game.winningPlayer} wins in {game.moves} moves
      {clicked ? <GamePreview game={game} /> : null}
    </div>
  )
}

export default CellListItem;

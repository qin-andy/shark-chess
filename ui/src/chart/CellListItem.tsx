import { useState, CSSProperties } from "react";
import { GameResult } from "../types";

const CellListItem = (props: {
  game: GameResult,
}) => {
  const [hover, setHover] = useState(false);

  const onMouseEnter = () => { 
    setHover(true);
  }

  const onMouseLeave = () => {
    setHover(false)
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
    >
      {game.winningPlayer} wins in {game.moves} moves
    </div>
  )
}

export default CellListItem;

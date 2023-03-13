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
    // openGameItem(index)
  }

  const onMouseLeave = () => {
    setHover(false)
    // setClicked(false);
  }

  const onMouseClick = () => {
    let a = clicked ? openGameItem(-1) : openGameItem(index); 
    setClicked(!clicked);
  }

  // Coloring
  let bgColor = 'silver'
  let textColor = 'black';
  if (game.winningColor === 'black') {
    bgColor = '#222222';
    textColor = 'white'
  }
  else if (game.winningColor === 'white') bgColor = '#EEEEEEE';

  let style: CSSProperties = { backgroundColor: bgColor, color: textColor };

  return (
    <div 
      className='cell-list-item'
      style={style}
      onClick={onMouseClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      
      {
        game.winningPlayer === 'None' ? 
          <><b>Draw</b> {game.moves} moves</>
          : <><b>{game.winningPlayer}</b> {game.moves} moves</>
      }
      {open ? <GamePreview game={game} /> : null}
    </div>
  )
}

export default CellListItem;

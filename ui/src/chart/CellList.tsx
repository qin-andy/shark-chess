import { CSSProperties } from "react";
import { GameResult } from "../types";
import CellListItem from "./CellListItem";

const CellList = (props: {
  wp: string,
  bp: string,
  games: GameResult[],
}) => {
  let {wp, bp, games} = props;

  let style: CSSProperties = {
    position: 'absolute',
    backgroundColor: 'whitesmoke', 
    zIndex: 10,
    top: '10px',
    left: '120px',
    width: '300px',
    height: '500px',
    border: '3px solid',
    overflowY: 'auto',
  };

  return (
    <div
      style={style}
    >
      <p>{wp} vs {bp}</p>
      {games.map((game, idx) => {
        return <CellListItem key={idx} game={game} />
      })}
    </div>
  )
}

export default CellList;
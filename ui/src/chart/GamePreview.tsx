import React, { CSSProperties, useEffect, useRef } from 'react';
import { GameResult } from '../types';
//@ts-ignore
import { Chessboard } from 'cm-chessboard';
import './chessboard.css';

const GamePreview = (props: {
  game: GameResult;
}) => {
  let { game } = props;
  const divRef = useRef(null);

  let style: CSSProperties = {
    position: 'relative',
    backgroundColor: 'whitesmoke', 
    zIndex: 20,
    top: '0px',
    left: '0px',
    width: '250px',
    height: '250px',
    border: '3px solid',
  }

  useEffect(() => {
    new Chessboard(divRef.current, {position: fen});
    console.log("Showing game preview");
  }, [])

  let fen = game.endingFEN;
  return (
    <div style={style} ref={divRef}>
    </div>
  )
}

export default GamePreview;
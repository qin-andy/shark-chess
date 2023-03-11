import React, { useEffect, useRef } from 'react';
import { GameResult } from '../types';
//@ts-ignore
import { Chessboard } from 'cm-chessboard';
import './chessboard.css';

const GamePreview = (props: {
  game: GameResult;
}) => {
  let { game } = props;
  const divRef = useRef(null);


  useEffect(() => {
    new Chessboard(divRef.current, {position: fen});
  }, [])

  let fen = game.endingFEN;
  return (
    <div className='game-preview' ref={divRef}>
    </div>
  )
}

export default GamePreview;
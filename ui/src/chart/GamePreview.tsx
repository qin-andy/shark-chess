import React, { useEffect, useRef, useState } from 'react';
import { GameResult } from '../types';
// @ts-ignore
import { Chessboard } from 'cm-chessboard';
// @ts-ignore 
import { CopyToClipboard } from 'react-copy-to-clipboard';

import './chessboard.css';

const GamePreview = (props: {
  game: GameResult;
}) => {
  let { game } = props;

  const [copied, setCopied] = useState(false);
  const divRef = useRef(null);

  useEffect(() => {
    new Chessboard(divRef.current, { position: fen });
  }, [])

  const onCopied = () => {
    setCopied(true);
  }

  let fen = game.endingFEN;
  return (
    <>
      <div className='game-preview'>
        <div ref={divRef} />
      </div>
      <CopyToClipboard className='copy-button' text={game.pgn} onCopy={onCopied}>
        <button>{copied ? 'Copied!' : 'Copy PGN'}</button>
      </CopyToClipboard>
    </>
  )
}

export default GamePreview;
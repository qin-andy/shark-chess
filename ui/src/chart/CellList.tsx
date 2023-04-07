import { GameItemData, GameResult } from '../types';
import CellListItem from './CellListItem';
import { useEffect, useState } from 'react';

const CellList = (props: {
  wp: string,
  bp: string,
  games: GameResult[],
}) => {
  let { wp, bp, games } = props;
  const [gameItemData, setGameItemData] = useState<GameItemData[]>([]);
  useEffect(() => {
    setGameItemData(buildCellListItemData(games));
  }, []);

  /** Builds initial UI data */
  const buildCellListItemData = (games: GameResult[]) => {
    let itemDataList = games.map((game) => {
      let data: GameItemData = {
        game: game,
        highlighted: false,
        open: false,
      }
      return data;
    });
    return itemDataList;
  }

  /** Callback to open a list item, prop drilled to children */
  const openGameItem = (index: number) => {
    let newGameItemData = gameItemData.map((itemData, idx) => {
      if (idx === index) {
        itemData.open = true;
      } else {
        itemData.open = false;
      }
      return itemData;
    });
    setGameItemData(newGameItemData);
  }

  /** Builds components from state data */
  const buildCellListItemComponents = (data: GameItemData[]) => {
    let items: JSX.Element[] = [];
    data.forEach((itemData, idx) => {
      let item = (
        <CellListItem
          key={idx}
          game={itemData.game}
          open={itemData.open}
          highlighted={itemData.highlighted}
          openGameItem={openGameItem}
          index={idx}
        />
      )
      items.push(item);
    });
    return items;
  }

  // Build components
  let items = buildCellListItemComponents(gameItemData);

  return (
    <div className="cell-list">
      <p className='cell-list-heading'>{wp} vs {bp}</p>
      {items}
      <p>Back to Top</p>
    </div>
  )
}




export default CellList;
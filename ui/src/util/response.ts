import { parseJsonText } from "typescript";
import { GameResult, Player } from "../types";

/** 
 * Takes a json list of game results and transofmrs them into a list of
 *  GameResult  objects
 */
export const processGamesResponse = (data: any) => {
  let results: GameResult[] = [];
  for (let i = 0; i < data.length; i++) {
    let gameResultData = data[i];
    let gameResult: GameResult = {
      matchupId: gameResultData['Matchup ID'],
      winningPlayer: gameResultData['Winning Player'],
      winningColor: gameResultData['Winning Color'],
      endReason: gameResultData['End Reason'],
      moves: gameResultData['Moves'],
      time: gameResultData['Time'],
      pgn: gameResultData['PGN'],
      white: gameResultData['White'],
      black: gameResultData['Black'],
      endingFEN: gameResultData['Ending FEN'],
    };
    results.push(gameResult);
  }
  return results;
}

export const processPlayerResponse = (data: any) => {
  let results: Player[] = [];
  for (let i = 0; i < data.length; i++) {
    let playerData = data[i];
    let player: Player = {
      name: playerData['Name'],
      id: playerData['ID'],
      elo: playerData['Elo'],
      wins: playerData['Wins'],
      losses: playerData['Losses'],
      draws: playerData['Draws'],
    }
    results.push(player);
  }
  return results;
}


let testGame = {
  "_id": {
    "$oid": "63fea94f2d056dff81a5ebf5"
  },
  "Matchup ID": "0,1",
  "Winning Player": "None",
  "Winning Color": "None",
  "End Reason": "INSUFFICIENT_MATERIAL",
  "Moves": 144,
  "Time": 0.1128475666046142,
  "PGN": "1. Nh3 c5 2. d3 a6 3. Kd2 f5 4. Ke3 Ra7 5. Kf4 b5 6. Kg5 a5 7. Ng1 Nf6 8. Be3\nKf7 9. Kh4 g6 10. Kg5 Ke6 11. c3 d5 12. Nf3 d4 13. Qb3+ Kd7 14. Kf4 Qc7+ 15.\nNe5+ Ke8 16. Kg5 dxc3 17. a4 c2 18. Qb4 Ba6 19. Bd2 bxa4 20. Qc4 Bc8 21. g3\nNbd7 22. Qa6 e6 23. Bb4 Be7 24. Ba3 Ne4+ 25. Kh6 c1=N 26. Kg7 Nxf2 27. Bh3 Kd8\n28. Kf7 Ng4 29. Rd1 Ndxe5+ 30. Kg7 Nf2 31. g4 h5 32. e4 hxg4 33. Rxc1 Bxa6 34.\nexf5 Bf6+ 35. Kxf6 Qe7+ 36. Kxe5 Qd7 37. Kf6 Bxd3 38. Rd1 Qh7 39. Re1 Nh1 40.\nBxc5 Rd7 41. Re2 gxh3 42. Rd2 Rf8+ 43. Bxf8 Nf2 44. Na3 Rf7+ 45. Kg5 Ng4 46.\nBb4 Ke8 47. Nb5 a3 48. Rc1 Bxf5 49. Rcd1 axb2 50. Re2 Rd7 51. Nd4 Rg7 52. Ra1\nKf7 53. Bf8 Qh8 54. Rxb2 Nh6 55. Ra4 Bd3 56. Rb1 Bc2 57. Rh1 Bd1 58. Rf1+ Kg8\n59. Kf6 Rd7+ 60. Kg5 Bg4 61. Kxg6 Bf5+ 62. Kg5 Bg4 63. Kg6 Rb7 64. Bxh6 Rc7 65.\nRd1 Rc4 66. Rxc4 a4 67. Ra1 Bh5+ 68. Kg5 a3 69. Nc2 Bf7 70. Rh4 Qd4 71. Rxh3\nQd3 72. Kf6 Qd7 73. Ke5 Qe7 74. Rd1 Qd6+ 75. Kf6 Kh7 76. Rc1 Qf8 77. Rf3 Qd8+\n78. Kxf7 Qa8 79. Rxa3 Qa6 80. Rd1 Qf1+ 81. Rxf1 Kxh6 82. Raa1 Kh7 83. Kf6 Kg8\n84. Na3 Kf8 85. Rac1 e5 86. Rf5 e4 87. Rf4 Kg8 88. Rc8+ Kh7 89. Rb8 e3 90. Rf3\nKh6 91. Kf7 Kh7 92. Rh8+ Kxh8 93. Rf1 Kh7 94. h4 Kh6 95. Rf2 Kh5 96. Kg8 exf2\n97. Kh7 Kxh4 98. Kh6 f1=B 99. Nb5 Kg3 100. Kh5 Kf2 101. Kh4 Bg2 102. Nc3 Kf1\n103. Kg3 Bh1 104. Kh2 Kf2 105. Nd5 Ke1 106. Kg3 Be4 107. Ne7 Bd5 108. Nf5 Bg8\n109. Nh4 Be6 110. Kh2 Bd5 111. Kg3 Bb7 112. Kg4 Bc6 113. Kg3 Bg2 114. Nf5 Ke2\n115. Ne3 Ke1 116. Nc4 Ke2 117. Ne5 Be4 118. Ng6 Bg2 119. Kf4 Bc6 120. Nh4 Ke1\n121. Kg3 Ba8 122. Kh3 Bh1 123. Kg3 Be4 124. Ng6 Bd3 125. Nf4 Bb5 126. Kf3 Ba4\n127. Nh5 Be8 128. Kg2 Ke2 129. Kg1 Ke1 130. Kh2 Bb5 131. Kg3 Ba6 132. Ng7 Bd3\n133. Kh4 Be4 134. Kg3 Ke2 135. Kh4 Bb7 136. Kg4 Bc6 137. Nh5 Bb5 138. Kf5 Bc4\n139. Kg4 Be6+ 140. Kf4 Bc4 141. Ng3+ Ke1 142. Kf3 Bf1 143. Nf5 Bg2+ 144. Kxg2 *",
  "White": "Suicide King",
  "Black": "Random",
  "Ending FEN": "8/8/8/5N2/8/8/6K1/4k3 b - - 0 144"
};


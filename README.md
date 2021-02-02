# Gomoku-AI

  This project has a simple interface, which displays the game board and the initial menu . <br>
  The player selects the position on which he/she wants to place the next piece . <br>
  The winner must place 5 consecutive pieces horizontaly, verticaly or diagonaly in order to win . <br>
  At the beginning, the user can choose the difficulty level of the AI from 1 to 3:
    - level 1 makes random corect moves in the neighbourhood of the position 
    - level 2 uses a weak heursitic function which can lead to a computer victory only if the player 
      does not play optimal ( has no defending strategy, or does not begin with a winning strategy ) 
    - level 3 has a balance of defending and improving its formations to the winning one
  
  Both level 2 and 3 uses minimax algorithm with a depth of 3 .
  The strong heuristic decides its value by computing a difference between computer's formations and human's formations, 
with a considerable advantage for those open at both ends and a larger dimmension . 
Here are the rules: https://en.wikipedia.org/wiki/Gomoku


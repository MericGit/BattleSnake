# BattleSnake - Lawrence Zhang

Simple BattleSnake coded in Python. Not the most efficient or elegant solution but should do alright.

The AI mainly uses A* To both stall, and find food as quick as possible. By mixing these two combinations the snake will be able to always be on the verge of starving, maximizing the time it can spend on the board.

Additionally the snake utilizes Flood Fill in order to attempt to always choose a more optimal solution that won't trap itself.

The snake also utilizes a simple search depth of 1 move to attempt to prevent head on collisions, or to be able to eliminate snakes within a few turns. 



Designed for Chicago-CSTA Battlesnake Competition


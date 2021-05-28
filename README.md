# BattleSnake - Lawrence Zhang

Simple BattleSnake coded in Python. Not the most efficient or elegant solution but should do alright.

The AI mainly uses A* To both stall, and find food as quick as possible. By mixing these two combinations the snake will be able to always be on the verge of starving, maximizing the time it can spend on the board.

Additionally the snake utilizes Flood Fill in order to attempt to always choose a more optimal solution that won't trap itself. Moving into a location which allows it to access fewer than 65% of the available board marks it as invalid. 

The snake also utilizes a simple search depth of 1 move to attempt to predict where the enemy snakes may move. This way it can attempt to avoid, or make head on collisions to kill and avoid snakes.

In cases where moves are all invalid, the snake follows a search heirarchy to determine the most optimal move. Each time a move check fails it loosens the restrictions. (I.E. First pass check --> must be valid --> Second pass --> Ignores floodfill req --> Third Pass ---> Ignores head on collision req --> Final pass --> Random Move)

![image](https://user-images.githubusercontent.com/41242144/120031860-ff215c80-bfbe-11eb-9de6-8cc1d5f4365b.png)
The snake has seen mild success, and is currently somewhere in the middle of the leaderboards. 



Designed for Chicago-CSTA Battlesnake Competition


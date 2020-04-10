# Path-Finding-Visualisation-with-Pygame
A path-finding visualisation program using Pygame
# Features
1. Pygame GUI
2. Placeable walls/obsticles in the gui
3. Placeable checkpoints for the pathfinding algorithm to follow
4. 4 different pathfind algorithms; Depth-first search, Breadth-first search, dijkstra and A*
5. Hotkeys to remove cirtain details from the gui
6. Adjustable speed of visualisation
7. Adjustable size of the grid by scrolling
## Depth-first Search
Rule of expansion - Expand most recently added node
Order of expansion - Up, Right, Down, Left
Acts like humans in perfect mazes and sometimes can be way faster than other algorithms
## Breadth-first search
Rule of expansion - Expand least recently added node
Acts like a wide net that covers every node that is closest in order
Always finds optimal route, however can be quite slow in long range searches
## Dijkstra
Rule of expansion - Expand node closest to starting node using g value
Because in this visualisation it can only move in 4 directions BFS and Dijkstra are identical in result but Dijkstra uses more computational power
## A Star
Rule of exspansion - Expand node with lowest f value, aka node that is close to the straightest diagonal path from the start node to end node put simply
Hueristic used is Manhanntan Distance

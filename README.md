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
# Depth-first Search
- Rule of expansion - Expand most recently added node
- Order of expansion - Up, Right, Down, Left
- Doesn't give the shortest route most of the time
- Acts like humans in perfect mazes and sometimes can be way faster than other algorithms

<img src="Media/DFS-Empty.gif" width="400">    <img src="Media/DFS-1.gif" width="400">    <img src="Media/DFS-2.gif" width="400">

- However even on the simplest mazes it can skip right past the end point

<img src="Media/DFS-3.gif" width="400">


# Breadth-first search
- Rule of expansion - Expand least recently added node
- Acts like a wide net that covers every node that is closest in order
- Always finds optimal route, however can be quite slow in long range searches

<img src="Media/BFS-Empty.gif" width="400">    <img src="Media/BFS-1.gif" width="400">    <img src="Media/BFS-2.gif" width="400">

# Dijkstra
- Rule of expansion - Expand node closest to starting node using g value
- Because in this visualisation it can only move in 4 directions BFS and Dijkstra are identical in result but Dijkstra uses more computational power

<img src="Media/Dijkstra-Empty.gif" width="400">    <img src="Media/Dijkstra-1.gif" width="400">    <img src="Media/Dijkstra-2.gif" width="400">

# A Star
- Rule of exspansion - Expand node with lowest f value, aka node that is close to the straightest diagonal path from the start node to end node put simply
- Hueristic used is Manhanntan Distance

<img src="Media/AStar-Empty.gif" width="400">    <img src="Media/AStar-1.gif" width="400">    <img src="Media/AStar-2.gif" width="400">

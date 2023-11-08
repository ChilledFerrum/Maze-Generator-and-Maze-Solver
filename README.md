# Maze Generator using Pygame in Python
![version](https://img.shields.io/badge/Version-v1.0.1-brightgreen)
![Pygame](https://custom-icon-badges.demolab.com/badge/Pygame-150458.svg?logo=pygame) <br/>
**Description:** <br/> This algorithm implements a maze with 3 different maze generation algorithms and solves it with 2 different maze solving algorithms. The user is able to change the parameters that change the output of the maze. The maze generation algorithms are, Iterative-Backtracking based on DFS, Breadth-First-Search and Disjoint-sets. The maze solving algorithms are based on the Iterative-backtracking or DFS algorithm and the Breadth-First-Search algorithm. <br/>
When running the program, every change is visualized using pygame. Most of the operations and functions are written in the Canvas.py and Maze.py files. <br/> <br/>
The program is finished but it is still unpolished, if any issue arises feel free to create a "New issue" in the issues tab.
<br/>
<br/>
**Parameters:** <br/>
The user can modify the following parameters based on their needs. The parameters are located in the Canvas.py file
 - rows = <Number of rows in the Maze (is Integer)> <br/>
 - cols = <Number of Colums in the Maze (is Integer)> <br/>
 - cellWidth = <The width of each cell in the Maze (is Integer) (The resolution of the maze is as follows Width: cols*cellWidth, Height: rows*cellwidth + UIoffset)> <br/>
 - FPS = <The tick speed of the maze generation algorithms (Is Integer)> <br/>
 - MazeSolver_TickSpeed = <The tick speed of the maze solving algorithms (Is Integer)> <br/>
 - use_BFS_Maze_Solver = <Write False to use the Iterative-Backtracking or DFS algorithm as the maze solver or True to use the BFS Maze Solver algorithm as the maze solver> <br/>
 - use_x_MazeGeneration_Algorithm = <Choose one of the 3 maze generation algorithms based on the below dictionary. (Read Comments if needed) (Is Integer)> <br/>

## Maze Generation Algorithms <br/>
### Maze Generation using Disjoint-sets
<img src="https://github.com/ChilledFerrum/Python/blob/ef7428b6ff01e8bdba71bd4b60553c889ff943ef/Maze%20Generator%20and%20Maze%20Solver/Assets/MazeGeneratorandMazeSolverDisjointSetsgen.gif" width="535" height="300"/> <br/>
### Maze Generation using DFS (Depth-First Search) 
<img src="https://github.com/ChilledFerrum/Python/blob/ef7428b6ff01e8bdba71bd4b60553c889ff943ef/Maze%20Generator%20and%20Maze%20Solver/Assets/MazeGeneratorandMazeSolverDFSgen.gif" width="535" height="300"/> <br/>
### Maze Generation using BFS (Breadth-First Search)
<img src="https://github.com/ChilledFerrum/Python/blob/ef7428b6ff01e8bdba71bd4b60553c889ff943ef/Maze%20Generator%20and%20Maze%20Solver/Assets/MazeGeneratorandMazeSolverBFSgen.gif" width="535" height="300"/> <br/>

## Requirements:
```
pip, pygame, python
```

## Compile:
```
> git clone 
> pip install pygame
> cd Maze Generator and Maze Solver
> python main.py
```
  
  

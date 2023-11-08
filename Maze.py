import random
# from collections import deque
from DisjointSet import Disjoint_set

"""
MIT License

Copyright (c) 2022 Dimitrios Mpouziotas

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE. 
"""

class Maze:
    def __init__(self, CanvasSize, rows, cols):
        # self.Maze is dictionary, saves {CellLocation: Walls} where walls is a list of booleans for north, east, south, west
        self.Maze = dict()
        # Reversing rows with columns due to a mistake within the code
        # Do not follow this
        self.rows = cols
        self.cols = rows

        self.MazeCompleted = False
        self.MazeSolved = False
        self.MazeTarget = (random.randint(0, self.rows - 1), self.cols - 1)

        self.grid = []
        self.start = (random.randint(0, self.rows - 1), 0)
        self.current = self.start
        self.OldCurrent = self.current

        # Visitor for Maze check if x Cell has been visited
        self.visited = dict()

        # Visitor for Maze Solver Iterative Backtracking DFS based method using stacks (LIFO - Last in First out)
        self.visitedSolver = dict()

        self.stack = []

        # Random Solver Function Variables
        self.randomSolverStack = []
        self.finalPath = []

        print("Maze Size:\nRows:", self.rows, "\nCols:", self.cols)

        # BFS Solver Function Variables
        self.BFSqueue = []

        # Disjoint Sets Variables
        self.doOnce1 = True
        self.S = Disjoint_set(self.rows * self.cols)
        self.E = []

        # A* Star
        self.openSet = []
        self.closedSet = []

    def createMaze(self):
        # Defines a Maze variable as Dictionary Where Each Cell variable/Location points to the information of each Wall
        for y in range(self.cols):
            for x in range(self.rows):
                newCell = (x, y)
                self.grid.append(newCell)
                self.Maze[(x, y)] = [True, True, True, True]
                self.visited.update({newCell: False})
                self.visitedSolver.update({newCell: False})

        currentCell = {self.current: True}
        # Update Current as Visited
        self.visitedSolver.update(currentCell)
        self.visited.update(currentCell)

        self.stack.append(self.current)

        # Init Random Solver Stack
        self.randomSolverStack.append(self.current)

        # Init A* Solver List
        self.openSet.append(self.current)

    # Converts Cell Value to Cell x and y
    def getXYLocation(self, val):
        x, y = list(self.Maze.keys())[val]
        return (x, y)

    def getValueLocation(self, x, y):
        for id, (xm, ym) in enumerate(self.Maze.keys()):
            if (xm, ym) == (x, y):
                return id

    def makeEdges(self):
        E = []
        for id, (x, y) in enumerate(self.Maze.keys()):
            neighbors = self.checkNeighbors(x, y)
            for neighbor in neighbors:
                E.append((id, self.getValueLocation(*neighbor)))
        return E

    def generateMaze_Disjoint_Sets_Method(self):

        if self.doOnce1:
            self.E = self.makeEdges()

        randomNeighbor = random.choice(self.E)
        self.E.remove(randomNeighbor)
        currentCell, neighborCell = randomNeighbor
        currentXY = self.getXYLocation(currentCell)
        neighborXY = self.getXYLocation(neighborCell)

        # current/neighbor-Cell is the count that leads to the X, Y location of the maze.
        # The current/neighbor-cells are used primarily to apply operations to the Disjoint set, such as Find and UNION
        u = self.S.find(currentCell)
        v = self.S.find(neighborCell)
        if u != v:
            self.S.union(u, v)
            self.removeWalls(currentXY, neighborXY)

        # If there are no other sets to UNION then maze is complete
        if self.S.numSets <= 1:
            self.MazeCompleted = True

    def generateMaze_LIFO_DFS_Method(self):
        self.OldCurrent = self.current
        [xCur, yCur] = self.current
        neighbors = self.checkNeighbors(xCur, yCur)
        if len(neighbors) > 0:
            next = random.choice(neighbors)
            cell = {next: True}

            self.visited.update(cell)
            self.stack.append(self.current)
            self.removeWalls(self.current, next)

            self.current = next

        elif len(self.stack) > 0:
            self.current = self.stack.pop()
        else:
            self.visited = {x: False for x in self.visited}
            self.current = self.start
            self.MazeCompleted = True

    def generateMaze_FIFO_BFS_Method(self):
        self.OldCurrent = self.current
        [xCur, yCur] = self.current
        neighbors = self.checkNeighbors(xCur, yCur)
        if len(neighbors) > 0:
            next = random.choice(neighbors)
            cell = {next: True}

            self.visited.update(cell)
            self.removeWalls(self.current, next)

            self.current = next
            self.BFSqueue.append(self.current)

        elif len(self.BFSqueue) > 0:
            self.current = self.BFSqueue.pop(0)
        else:
            self.visited = {x: False for x in self.visited}
            self.current = self.start
            self.MazeCompleted = True

    def solveMazeRandomNeighbor(self):
        self.OldCurrent = self.current
        [xCur, yCur] = self.current

        if self.current == self.MazeTarget:
            self.MazeSolved = True
        elif self.current == self.start:
            self.visited.update({self.current: self.getWallsXY(*self.current)})
            self.finalPath.append(self.current)

        ValidNeighbors = self.checkValidNeighbor(xCur, yCur)
        if not self.MazeSolved:
            if len(ValidNeighbors) > 0:
                next = random.choice(ValidNeighbors)
                Cell = {next: True}
                if not self.visited.get(next):
                    self.finalPath.append(next)

                # Save Next as Visited
                self.visited.update(Cell)
                # Save Current as visited
                self.visitedSolver.update({self.current: True})

                self.randomSolverStack.append(self.current)

                self.current = next

            elif len(self.randomSolverStack) > 0:
                self.finalPath.remove(self.current)
                self.current = self.randomSolverStack.pop()
            else:
                self.finalPath.append(self.MazeTarget)
                self.MazeSolved = True

    def getNorthWall(self, AtLoc):
        return self.Maze.get(AtLoc)[0]

    def getSouthWall(self, AtLoc):
        return self.Maze.get(AtLoc)[2]

    def getEastWall(self, AtLoc):
        return self.Maze.get(AtLoc)[1]

    def getWestWall(self, AtLoc):
        return self.Maze.get(AtLoc)[3]

    def removeWalls(self, Current, Next):

        [xOld, yOld] = Current
        [xCur, yCur] = Next

        x = xOld - xCur
        y = yOld - yCur
        # print("Location: ", Current, "\nWalls:", self.Maze.get(Current))

        # Going Right
        if x == -1:
            # REMOVE West wall of Next
            self.removeWestWall(xCur, yCur)

            # REMOVE East Wall of Current
            self.removeEastWall(xOld, yOld)
        # Going Left
        elif x == 1:
            # Remove East Wall of Next
            self.removeEastWall(xCur, yCur)

            # Remove West Wall of Current
            self.removeWestWall(xOld, yOld)
        # Going UP
        if y == 1:
            # Remove South Wall of Next
            self.removeSouthWall(xCur, yCur)

            # Remove North Wall of Current
            self.removeNorthWall(xOld, yOld)
        # Going Down
        elif y == -1:
            # Remove North Wall of Next
            self.removeNorthWall(xCur, yCur)

            # Remove South Wall of Current
            self.removeSouthWall(xOld, yOld)

    def checkValidNeighbor(self, x, y):
        RightCell = (x + 1, y)
        LeftCell = (x - 1, y)
        TopCell = (x, y - 1)
        BottomCell = (x, y + 1)

        AvailableNeighbors = []
        if not self.visited.get(RightCell) and self.Maze[(x, y)][1] is False and not (x + 1 > self.rows - 1):
            AvailableNeighbors.append(RightCell)
        if not self.visited.get(TopCell) and self.Maze[(x, y)][0] is False and not (y - 1 < 0):
            AvailableNeighbors.append(TopCell)
        if not self.visited.get(LeftCell) and self.Maze[(x, y)][3] is False and not (x - 1 < 0):
            AvailableNeighbors.append(LeftCell)
        if not self.visited.get(BottomCell) and self.Maze[(x, y)][2] is False and not (y + 1 > self.cols - 1):
            AvailableNeighbors.append(BottomCell)

        return AvailableNeighbors

    def removeNorthWall(self, x, y):
        wall = self.getWallsXY(x, y)
        wall[0] = False

        self.Maze[(x, y)] = wall

    def removeEastWall(self, x, y):
        wall = self.getWallsXY(x, y)
        wall[1] = False

        Cell = {(x, y): wall}
        self.Maze[(x, y)] = wall

    def removeSouthWall(self, x, y):
        wall = self.getWallsXY(x, y)
        wall[2] = False
        self.Maze[(x, y)] = wall

    def removeWestWall(self, x, y):
        wall = self.getWallsXY(x, y)
        wall[3] = False

        self.Maze[(x, y)] = wall

    def checkNeighbors(self, x, y):
        Neighbors = []
        # [C] is Current | [N] is Next

        #  [C] -> [N] Right     [N] <- [C] Left
        #
        #   [C]                 [N]
        #    |                   ^
        #    V        Bottom     |         Top
        #   [N]                 [C]
        RightCell = (x + 1, y)
        LeftCell = (x - 1, y)
        TopCell = (x, y - 1)
        BottomCell = (x, y + 1)

        # Check Right if Visited and not out of boundaries
        if not self.visited.get(RightCell) and not (x + 1 > self.rows - 1):
            Neighbors.append(RightCell)

        # Check Left if Visited and not out of boundaries
        if not self.visited.get(LeftCell) and not (x - 1 < 0):
            Neighbors.append(LeftCell)

        # Check Top if Visited and not out of boundaries
        if not self.visited.get(TopCell) and not (y - 1 < 0):
            Neighbors.append(TopCell)

        # Check Bottom if Visited and not out of boundaries
        if not self.visited.get(BottomCell) and not (y + 1 > self.cols - 1):
            Neighbors.append(BottomCell)

        # print("Available Neighbors:")
        # for x, y in Neighbors:
        #     print("(", f'{x},', f'{y}', ")\n")
        return Neighbors

    def Cell(self, x, y):
        self.x = x
        self.y = y

    # Returns a LIST of the Cell location data without the wall data
    def getMazeGrid(self):
        grid = []
        for x, y in self.Maze:
            grid.append((x, y))
        return grid

    # Returns a LIST of the Maze Wall data without the Cell Location data
    def getMazeWalls(self):
        walls = []
        for x, y in self.Maze:
            walls.append(self.Maze.get((x, y)))
        return walls

    # Returns a DICTIONARY of the entire Maze Structure {CellLocation: Walls}
    def getMaze(self):
        return self.Maze

    # Returns a LIST of the wall located at X and Y, with all its directions
    def getWallsXY(self, x, y):
        # walls =
        return self.Maze.get((x, y))

    # Returns the current processed Cell. Used to create, generate and solve the maze
    def getCurrent(self):
        return self.current

    def getOldCurrent(self):
        return self.OldCurrent

    def isMazeComplete(self):
        return self.MazeCompleted

    def getTarget(self):
        return self.MazeTarget

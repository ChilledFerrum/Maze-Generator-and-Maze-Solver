import math, pygame.display

from Maze import Maze
from BFSGraph import Node, Graph

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

rows = 15
cols = 15
cellWidth = 30
TrackerSize = cellWidth / math.log(rows * cols)  # I like My Math, it gives me an "Exponential crisis"
FPS = 120
MazeSolver_TickSpeed = 50

# By selecting False the default Maze Solving algorithm is Iterative Backtracking aka DFS.
# By selecting True the BFS algorithm will pause
use_BFS_Maze_Solver = False
use_x_MazeGeneration_Algorithm = 1
MazeGeneration_Algorithm = {
    # (BFS based maze generation, results in a more complex maze)
    1: "Breadth-First_Search",  # Maze Generation using queues and random neighbor selections

    # (normal Maze generation method based on DFS)
    2: "Depth-First-Search",  # Maze generation using stacks and random neighbor selections

    # Visualize
    3: "Disjoint-Sets"

}

Color = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),

    # Cyberpunk Color Palette:
    "BackgroundColor": (32, 14, 37),
    "TrackerPath": (0, 255, 159), # DOTS Using self.ColorGradient to color the tracker path dots instead  # Line 209 & 232
    "TrackerColor": (85, 109, 200), # Tracker Index background
    "WallColor": (230, 142, 54)
}
pygame.init()


class Canvas:
    def __init__(self):
        self.running = True
        self.fpsClock = pygame.time.Clock()

        self.ColorGradient = 0

        self.rows = rows
        self.cols = cols
        self.cellWidth = cellWidth

        # Width and Height of the Maze used for the Canvas
        W = self.cols * self.cellWidth
        H = self.rows * self.cellWidth

        # The Canvas Size (Width, Height)
        self.CanvasSize = (W, H)

        # Defining Maze Object to be created
        self.MyMaze = Maze(self.CanvasSize, self.rows, self.cols)

        # do Once Variable for Canvas Customizations
        self.doOnce = True
        self.doOnce2 = True
        self.doOnce3 = True

        # BFS Solving Algorithm Variables
        self.Graph = Graph()

        self.input_list = [] # Input Buffer

        # STYLE
        if self.cellWidth / 10 == 2:
            self.ExitImg = pygame.image.load("style/emergency-exit.png")
            self.iconSize = 32
        else:
            self.ExitImg = pygame.image.load("style/emergency-exit (1).png")
            self.iconSize = 64


        self.run()

    def runMaze(self):

        # Called to Indicate and animate the changes of the maze's current structure
        self.drawMaze()
        if self.ColorGradient + 5 < 255:
            self.ColorGradient += 5
        else:
            self.ColorGradient = 0
        # Maze Generation Process
        if not self.MyMaze.isMazeComplete():
            if self.doOnce3:
                print("Generating Maze")
                self.doOnce3 = False

            # Back-end maze generation algorithms using Queues and Stacks based on Random Neighboring exploration
            # with DFS and BFS based methods
            if MazeGeneration_Algorithm.get(use_x_MazeGeneration_Algorithm) == "Breadth-First_Search":
                self.MyMaze.generateMaze_FIFO_BFS_Method()

            elif MazeGeneration_Algorithm.get(use_x_MazeGeneration_Algorithm) == "Depth-First-Search":
                self.MyMaze.generateMaze_LIFO_DFS_Method()

            elif MazeGeneration_Algorithm.get(use_x_MazeGeneration_Algorithm) == "Disjoint-Sets":
                self.MyMaze.generateMaze_Disjoint_Sets_Method()

            else:
                print("Invalid Generation Algorithm")
                self.running = False
                return
        else:
            # NEXT OPERATIONS AFTER GENERATED MAZE
            if self.doOnce:
                print("Generating Maze - done")
                print("Final Maze Information:\n", self.MyMaze.Maze)

                print("Solving Maze")
                self.doOnce = False
                if use_BFS_Maze_Solver:
                    self.BreadthFirstSearch_CreateGraph()

            if not self.MyMaze.MazeSolved:
                if use_BFS_Maze_Solver:
                    # self.fpsClock.tick(MazeSolver_TickSpeed)
                    self.BreadthFirstSearch()
                    self.MyMaze.finalPath = self.getBFSPath()
                    self.drawMaze()
                else:
                    # self.fpsClock.tick(MazeSolver_TickSpeed)
                    # Use Random neighbor Indicator with Backtracking
                    self.MyMaze.solveMazeRandomNeighbor()
                    self.pathIndicator()


            elif self.doOnce2:
                # PRINT Final Path
                self.ColorGradient = 0
                for current in self.MyMaze.finalPath:
                    x, y = current
                    if self.ColorGradient + 5 < 255:
                        self.ColorGradient += 5
                    else:
                        self.ColorGradient = 0

                    if current == self.MyMaze.start:
                        print("Starting Cell: ", current, ":\n\tWalls:", self.MyMaze.getWallsXY(x, y))
                        self.drawFinalPathCell(current)
                    elif current == self.MyMaze.MazeTarget:
                        print("End Cell: ", current, ":\n\tWalls:", self.MyMaze.getWallsXY(x, y))
                        self.drawFinalPathCell(current)
                    else:
                        print("At Cell ", current, ":\n\tWalls:", self.MyMaze.getWallsXY(x, y))
                    # if Use_BFS_Maze_Solver:
                    self.drawFinalPathCell(current)
                self.doOnce2 = False
                print("\nSolving Maze - done")

    def drawMaze(self):
        grid = self.MyMaze.getMazeGrid()

        for (x, y) in grid:
            X = x * self.cellWidth
            Y = y * self.cellWidth

            # If North Wall is True then Draw North Line
            if self.MyMaze.getMaze()[(x, y)][0] is True:
                pygame.draw.line(self.screen, Color["WallColor"], (X, Y), (X + self.cellWidth, Y), 2)
            elif not self.MyMaze.MazeCompleted:
                self.removeNorthWall(x, y)

            # If East Wall is True then Draw East Line
            if self.MyMaze.getMaze()[(x, y)][1] is True:
                pygame.draw.line(self.screen, Color["WallColor"], (X + self.cellWidth, Y),
                                 (X + self.cellWidth, Y + self.cellWidth), 2)
            elif not self.MyMaze.MazeCompleted:
                self.removeEastWall(x, y)

            # If South Wall is True then Draw South Line
            if self.MyMaze.getMaze().get((x, y))[2] is True:
                pygame.draw.line(self.screen, Color["WallColor"], (X, Y + self.cellWidth),
                                 (X + self.cellWidth, Y + self.cellWidth), 2)
            elif not self.MyMaze.MazeCompleted:
                self.removeSouthWall(x, y)

            # If West Wall is True then Draw West Line
            if self.MyMaze.getMaze().get((x, y))[3] is True:
                pygame.draw.line(self.screen, Color["WallColor"], (X, Y), (X, Y + self.cellWidth), 2)
            else:
                self.removeWestWall(x, y)

            # DRAW TARGET LOCATION
            if (x, y) == self.MyMaze.getTarget():
                pygame.draw.rect(self.screen, Color["red"],
                                 (x * self.cellWidth + 2, y * self.cellWidth + 2, self.cellWidth - 2,
                                  self.cellWidth - 2), 0)
            # DRAW MAZE START LOCATION
            if (x, y) == self.MyMaze.start:
                pygame.draw.rect(self.screen, Color["green"],
                                 (x * self.cellWidth + 2, y * self.cellWidth + 2, self.cellWidth - 2,
                                  self.cellWidth - 2), 0)

        pygame.display.update()

    def pathIndicator(self):
        Current = self.MyMaze.getOldCurrent()
        Next = self.MyMaze.getCurrent()

        xCur, yCur = Current
        xNext, yNext = Next

        if self.MyMaze.isMazeComplete() and (xNext, yNext) != self.MyMaze.start:
            pygame.draw.rect(self.screen, Color["TrackerColor"], (
                xNext * self.cellWidth + 2, yNext * self.cellWidth + 2, self.cellWidth - 2, self.cellWidth - 2), 0)
        if Current != Next:
            pygame.draw.rect(self.screen, Color["BackgroundColor"],
                             (xCur * self.cellWidth + 2, yCur * self.cellWidth + 2, self.cellWidth - 2,
                              self.cellWidth - 2), 0)
        if self.MyMaze.OldCurrent == self.MyMaze.start:
            pygame.draw.rect(self.screen, Color["green"], (
                xCur * self.cellWidth + 2, yCur * self.cellWidth + 2, self.cellWidth - 2, self.cellWidth - 2), 0)
        if self.MyMaze.MazeCompleted:
            # Draws the Circles that result in the Final Path
            if self.MyMaze.visited.get(Next):
                pygame.draw.circle(self.screen, (self.ColorGradient//2, 0, 0),
                                   (xCur * self.cellWidth + self.cellWidth / 2,
                                    yCur * self.cellWidth + self.cellWidth / 2),
                                   TrackerSize, 0)
            if self.MyMaze.visitedSolver.get(Next):
                pygame.draw.rect(self.screen, Color["BackgroundColor"],
                                 (xCur * self.cellWidth + 2, yCur * self.cellWidth + 2, self.cellWidth - 2,
                                  self.cellWidth - 2), 0)

            if self.MyMaze.getCurrent() == self.MyMaze.getTarget():
                self.MyMaze.MazeSolved = True
                pygame.draw.rect(self.screen, Color["red"], (
                    xNext * self.cellWidth + 2, yNext * self.cellWidth + 2, self.cellWidth - 2, self.cellWidth - 2), 0)

            if self.MyMaze.getCurrent() == self.MyMaze.start and self.MyMaze.MazeSolved:
                pygame.draw.circle(self.screen, (self.ColorGradient / 2, 0, 0),
                                   (xNext * self.cellWidth + self.cellWidth / 2, yNext * self.cellWidth + self.cellWidth / 2),
                                   TrackerSize, 0)

        pygame.display.update()

    def drawFinalPathCell(self, current):
        x, y = current
        pygame.draw.circle(self.screen, (self.ColorGradient/2, 0, 0),
                       (x * self.cellWidth + self.cellWidth / 2, y * self.cellWidth + self.cellWidth / 2),
                           TrackerSize, 0)

    # gets The Breadth First Search final Path
    def getBFSPath(self):
        path = []
        end = self.Graph.getNode(self.MyMaze.MazeTarget)
        path.insert(0, end.location)

        next = self.Graph.getNode(end.location).parent

        while next != self.MyMaze.start:
            path.insert(0, next)
            next = self.Graph.getNode(next).parent

        path.insert(0, self.MyMaze.start)
        return path

    def BreadthFirstSearch(self):
        start = self.Graph.start
        self.MyMaze.finalPath.append(start.location)

        xS, yS = start.location
        startGrid = self.MyMaze.checkValidNeighbor(xS, yS)
        startNeighbors = dict()
        for neighbor in startGrid:
            xN, yN = neighbor
            startNeighbors = {neighbor: self.MyMaze.getWallsXY(xN, yN)}

        self.Graph.start.neighbors = startNeighbors
        end = self.Graph.end

        Q = [start]

        # Check Object IDs if they are the same
        # print("Start at", start.parent, " - ", start, "\nCurrent at", current.parent, " - ", current, "\nEnd at", end.parent, " - ", end)
        while Q is not len(Q) > 0:
            current = Q.pop(0)
            if current.location == end.location:
                return self.MyMaze.current
            Neighbors = self.Graph.getNode(current.location).Neighbors
            if len(Neighbors) > 0:
                for neighbor in Neighbors.keys():
                    # self.fpsClock.tick(MazeSolver_TickSpeed)
                    self.pathIndicator()
                    if not self.Graph.getNode(neighbor).visited:
                        self.Graph.getNode(neighbor).visited = True
                        self.Graph.getNode(neighbor).parent = current.location
                        self.Graph.getNode(neighbor).location = neighbor
                        Q.append(self.Graph.getNode(neighbor))
                        self.MyMaze.current = neighbor
            for event in pygame.event.get():
                if event.type == pygame.K_ESCAPE:
                    self.running = False
                    break

    # CREATE BFS GRAPH & EMBED TO THE MAZE
    def BreadthFirstSearch_CreateGraph(self):
        Grid = self.MyMaze.getMazeGrid()

        startNode = Node

        # DEFINE the Rest of the Graph
        for x, y in Grid:
            node = Node((x, y), self.MyMaze.getWallsXY(x, y), False)

            Neighbors = self.MyMaze.checkValidNeighbor(x, y)
            for Neighbor in Neighbors:
                xN, yN = Neighbor
                wall = self.MyMaze.getWallsXY(xN, yN)
                newNeighbor = {Neighbor: wall}
                node.addNeighbor(newNeighbor)

            self.Graph.graph.append(node)
            if (x, y) == self.MyMaze.MazeTarget:
                self.Graph.setEnd(node)
            elif (x, y) == self.MyMaze.start:
                self.Graph.setStart(node)
                startNode = node

        self.MyMaze.current = startNode.location


    def removeNorthWall(self, x, y):
        pygame.draw.line(self.screen, Color["BackgroundColor"], (x * self.cellWidth + 2, y * self.cellWidth),
                         (x * self.cellWidth + self.cellWidth - 1, y * self.cellWidth), 2)

    def removeSouthWall(self, x, y):
        pygame.draw.line(self.screen, Color["BackgroundColor"],
                         (x * self.cellWidth + 2, y * self.cellWidth + self.cellWidth),
                         (x * self.cellWidth + self.cellWidth - 1, y * self.cellWidth + self.cellWidth), 2)

    def removeWestWall(self, x, y):
        pygame.draw.line(self.screen, Color["BackgroundColor"], (x * self.cellWidth, y * self.cellWidth + 2),
                         (x * self.cellWidth, y * self.cellWidth + self.cellWidth - 1), 2)

    def removeEastWall(self, x, y):
        pygame.draw.line(self.screen, Color["BackgroundColor"],
                         (x * self.cellWidth + self.cellWidth, y * self.cellWidth + 2),
                         (x * self.cellWidth + self.cellWidth, y * self.cellWidth + self.cellWidth - 1), 2)

    def run(self):
        # Math for Icons
        y = math.fmod(75, self.iconSize)
        x = self.iconSize - 25

        self.MyMaze.createMaze()

        Gui_Size = (4, 100)


        CanvasSize = tuple(map(lambda i, j: i + j, self.CanvasSize, Gui_Size))
        self.screen = pygame.display.set_mode(CanvasSize)
        self.screen.fill(Color["BackgroundColor"])

        pygame.display.set_caption("Maze Generator")
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.K_ESCAPE, pygame.MOUSEBUTTONDOWN])
        while self.running:
            self.runMaze()
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CanvasSize[1] - 75 <= mouse[1] <= CanvasSize[1] - y and CanvasSize[0]/2 - 25 <= mouse[0] <= CanvasSize[0]/2 + x:
                        self.running = False


            # EXIT BUTTON LOCATION AND ICON
            if CanvasSize[1] - 75 <= mouse[1] <= CanvasSize[1] - y and CanvasSize[0]/2 - 25 <= mouse[0] <= CanvasSize[0]/2 + x:
                pygame.draw.rect(self.screen, Color["BackgroundColor"], [CanvasSize[0]/2 - 25, CanvasSize[1]-75, self.iconSize, self.iconSize])
                self.screen.blit(self.ExitImg, (CanvasSize[0] / 2 - 25, CanvasSize[1] - 75))
            else:
                self.screen.blit(self.ExitImg, (CanvasSize[0] / 2 - 25, CanvasSize[1] - 75))
            pygame.display.update()

            if self.MyMaze.isMazeComplete():
                self.fpsClock.tick(MazeSolver_TickSpeed)
            else:
                self.fpsClock.tick(FPS)

    def __del__(self):
        print("CLOSING MAZE")

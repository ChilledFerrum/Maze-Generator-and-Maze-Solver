class Graph:
    def __init__(self):
        self.graph = []
        self.start = None
        self.end = None

    def addNode(self, node):
        self.graph.append(node)

    def setStart(self, node):
        self.start = node

    def setEnd(self, node):
        self.end = node

    def getNode(self, Location):
        node = None
        for node in self.graph:
            if node.location == Location:
                return node
        return node


class Node:
    def __init__(self, Location, Walls, visited=False):
        self.location = Location
        self.parent = None
        self.Neighbors = dict()
        self.visited = visited

    def addNeighbor(self, neighbor):
        key = list(neighbor.keys())[0]
        val = list(neighbor.values())[0]
        self.Neighbors.update({key: val})

    def getVisited(self):
        return self.visited
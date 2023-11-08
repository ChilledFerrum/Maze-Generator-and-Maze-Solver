class Disjoint_set:
    def __init__(self, numElements):
        self.parent = [i for i in range(0, numElements)]
        self.size = [0] * numElements
        self.numSets = numElements

    # Recursive method to find the root of the first cell
    def find(self, element):
        # Using x to store the element instead of itself to avoid conflict with roots of each node
        x = element
        if self.parent[element] != x:
            x = self.find(self.parent[element])

        return x

    def union(self, element1, element2):
        root1 = self.find(element1)
        root2 = self.find(element2)

        if root1 == root2:
            return
        self.numSets -= 1
        if self.size[root2] > self.size[root1]:
            self.parent[root1] = root2

        self.parent[root2] = root1

        if self.size[root1] == self.size[root2]:
            self.size[root2] += 1

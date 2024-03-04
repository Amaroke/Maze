from cell import Cell


class UnionFind:
    """
    UnionFind data structure
    """

    def __init__(self, cells: Cell):
        self.parents = {cell: cell for cell in cells}

    def find(self, cell: Cell):
        """Find the representative of the set containing element"""
        if cell not in self.parents:
            raise KeyError(f"Element {cell} not found in UnionFind")
        if self.parents[cell] != cell:
            self.parents[cell] = self.find(self.parents[cell])
        return self.parents[cell]

    def union(self, cell1: Cell, cell2: Cell):
        """Union operation: merge sets containing cell1 and cell2, if they are different and the minimal element of the first set is less than the minimal element of the second set."""
        root1 = self.find(cell1)
        root2 = self.find(cell2)
        if root1 != root2:
            if root1 < root2:
                self.parents[root2] = root1
            else:
                self.parents[root1] = root2

    def number_of_classes(self):
        """Return the number of connected components"""
        return len({self.find(cell) for cell in self.parents})


def test():
    """Test all the methods of UnionFind"""
    uf = UnionFind([1, 2, 3])
    assert uf.number_of_classes() == 3
    assert uf.find(1) == 1
    assert uf.find(2) == 2
    assert uf.find(3) == 3
    uf.union(1, 2)
    assert uf.number_of_classes() == 2
    assert uf.find(2) == 1
    assert uf.find(1) == 1
    assert uf.find(3) == 3


if __name__ == "__main__":
    test()

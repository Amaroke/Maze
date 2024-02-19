class Cell:
    """
    Holds a Cell of the Maze
    """

    def __init__(self, i: int, j: int, width: int, height: int):
        """Create a cell"""
        self.i = i
        self.j = j
        self.width = width
        self.height = height
        self._neighbors = self._create_neighbors()

    def _create_neighbors(self) -> list:
        """Initiate the list of neighbors"""
        return [
            (self.i + i, self.j + j)
            for i in range(-1, 2)
            for j in range(-1, 2)
            if self._is_wall_valid(i, j)
        ]

    @property
    def neighbors(self) -> list:
        """Getter for the neighbors"""
        return self._neighbors

    def is_neighbor(self, other: "Cell") -> bool:
        """True if the `other` `Cell` is a neighbor of `self`"""
        return (other.i, other.j) in self.neighbors

    def _is_wall_valid(self, i: int, j: int) -> bool:
        """True if there's may be a wall between us and `Cell(self.i+i, self.j+j)`"""
        return (
            (i != 0 or j != 0)
            and (i == 0 or j == 0)
            and (self.i + i >= 0)
            and (self.j + j >= 0)
            and (self.i + i < self.width)
            and (self.j + j < self.height)
        )

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __lt__(self, other):
        if self.i < other.i:
            return True
        if self.i == other.i and self.j < other.j:
            return True
        return False

    def __hash__(self):
        return hash((self.i, self.j))

    def __repr__(self):
        return f"Cell({self.i}, {self.j}, {self.width}, {self.height})"

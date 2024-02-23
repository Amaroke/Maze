from random import randint
#from pyweb import pydom

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


class Graph:
    def __init__(self, maze):
        """Create a graph with all the cells."""
        self.list_of_summits = []
        self.list_of_edges = {}
        for cell in maze.cells:
            self.add_summits(cell)

    def add_summits(self, summit):
        """Add a summit in the graph.
        Each summit correspond to a cell."""
        self.list_of_summits.append(summit)
        self.list_of_edges[summit] = []

    def add_edge(self, summit1, summit2):
        """Add an edge between two cells.
        Used to represent the absence of a wall between to cell."""
        self.list_of_edges[summit1].append(summit2)
        self.list_of_edges[summit2].append(summit1)

    def neighbors(self, summit):
        return self.list_of_edges[summit]

    def predecessors(self, source):
        """
        Return the list of predecessors visited in the order of a thorough journey
        """
        pile = []
        predecessors = {source: None}
        pile.append(source)
        while pile:
            current = pile.pop()
            for neighbor in self.neighbors(current):
                if not neighbor in predecessors:
                    pile.append(neighbor)
                    predecessors[neighbor] = current
        return predecessors

    def build_path(self, source, destination, predecessors):
        """Find a path between source and destination.
        It is the solution of the maze."""
        if not destination in predecessors:
            return None
        path = [destination]
        current = destination
        while current != source:
            current = predecessors[current]
            path.append(current)
        path = path[::-1]
        return path


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


class Maze:
    """Holds a perfect random Maze generated by the Kruksal's algorithm"""

    def __init__(self, width: int, height: int):
        """
        Create the maze :
        -generate the perfect maze
        -create a graph linked to the maze
        -print the maze
        -solve the maze
        -print the solution
        """
        self.width = width
        self.height = height
        self.cells = self._init_cells()
        self.union_find = UnionFind(self.cells)
        self.graph = Graph(self)
        self.walls = self._init_walls()
        self.generate()
        self.path = []
        print(self.__repr__())
        self.entrance = self.cells[0]
        self.exit = self.cells[len(self.cells) - 1]
        self.path = self.solve()
        print(self.__repr__())

    def _init_cells(self) -> list:
        """initiate the cells"""
        return [
            Cell(i, j, self.width, self.height)
            for i in range(self.width)
            for j in range(self.height)
        ]

    def _init_walls(self) -> list:
        """initiate the walls: every pair of neighboring cells have a wall between them"""
        return [
            (cell_a, cell_b)
            for cell_a in self.cells
            for cell_b in self.cells
            if cell_a < cell_b and cell_a.is_neighbor(cell_b)
        ]

    def have_wall(self, i: int, j: int, x: int, y: int) -> bool:
        """True if there's a wall between Cell(i, j) and Cell(x, y)"""
        return (
            Cell(i, j, self.width, self.height),
            Cell(x, y, self.width, self.height),
        ) in self.walls or (
            Cell(x, y, self.width, self.height),
            Cell(i, j, self.width, self.height),
        ) in self.walls

    def _formatted_string(self) -> str:
        """Return the formatted_string used in the __repr__"""
        string = "+-" * self.width + "+\n"
        for j in range(self.height):
            string += "│{}"
            for i in range(self.width - 1):
                if self.have_wall(i, j, i + 1, j):
                    string += "│{}"
                else:
                    string += " {}"
            string += "|\n"
            if j < self.height - 1:
                for i in range(self.width):
                    if self.have_wall(i, j, i, j + 1):
                        string += "+-"
                    else:
                        string += "+ "
                string += "+\n"
        string += "+-" * self.width + "+\n"
        return string

    def generate_list(self):
        """Generate the list of the cells for the repr.
        A cell is represented with a space if it's not in the path
        or with an hashtag if it's in the path(=solution)."""
        list_solution = []
        for i in range(self.width):
            for j in range(self.height):
                if Cell(j, i, self.width, self.height) in self.path:
                    list_solution.append("#")
                else:
                    list_solution.append(" ")
        return list_solution

    def __repr__(self):
        return self._formatted_string().format(*self.generate_list())

    def generate(self):
        """Generate a perfect maze with the Kruskal algorithm"""
        while self.union_find.number_of_classes() > 1:
            index = randint(0, len(self.walls) - 1)
            wall = self.walls[index]
            if self.union_find.find(wall[0]) != self.union_find.find(wall[1]):
                self.union_find.union(wall[0], wall[1])
                self.graph.add_edge(wall[0], wall[1])
                self.walls.pop(index)

    def solve(self):
        """Find a path from the entrance to the exit.
        It uses a graph"""
        predecessors = self.graph.predecessors(self.entrance)
        return self.graph.build_path(self.entrance, self.exit, predecessors)

class Player:
    def __init__(self, max, walls):
        self.height = 0
        self.width = 0
        self.walls = walls
        self.max = max
    def move_right(self):
        if self.width<max:
            if (Cell(self.width, self.height, self.max, self.max),
                Cell(self.width+1, self.height, self.max, self.max)) not in self.walls:
                self.width +=1
    def move_left(self):
        if (Cell(self.width-1, self.height, self.max, self.max),
        Cell(self.width, self.height, self.max, self.max)) not in self.walls:
                self.width +=1
    def move_high(self):
        if self.height != 0:
            if (Cell(self.width, self.height-1, self.max, self.max),
            Cell(self.width, self.height, self.max, self.max)) not in self.walls:
                self.height -=1
    def move_down(self):
        if self.height<self.max:
            if (Cell(self.width, self.height, self.max, self.max),
            Cell(self.width, self.height+1, self.max, self.max)) not in self.walls:
                self.height +=1


class Game:
    def __init__(self, cote):
        self.maze = Maze(cote, cote)
        self.player = Player(cote, self.maze.walls)

    def solve(self):
        self.maze.solve()







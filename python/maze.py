from random import choice
from cell import Cell
from union_find import UnionFind
from graph import Graph


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
        self.cells = sorted(self._init_cells())
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
        for cell in self.cells:
            if cell in self.path:
                list_solution.append("#")
            else:
                list_solution.append(" ")
        return list_solution

    def __repr__(self):
        return self._formatted_string().format(*self.generate_list())

    def generate(self):
        """Generate a perfect maze with the Kruskal algorithm"""
        while self.union_find.number_of_classes() > 1:
            wall = choice(self.walls)
            if self.union_find.find(wall[0]) != self.union_find.find(wall[1]):
                self.union_find.union(wall[0], wall[1])
                self.graph.add_edge(wall[0], wall[1])
                self.walls.remove(wall)

    def solve(self):
        """Find a path from the entrance to the exit.
        It uses a graph"""
        predecessors = self.graph.predecessors(self.entrance)
        return self.graph.build_path(self.entrance, self.exit, predecessors)

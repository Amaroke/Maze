from maze import Maze
from cell import Cell


class Game:
    """Class with a maze instance and a player represented in x and y coordinates"""

    def __init__(self, width: int, height: int):
        self.maze = Maze(width, height)
        self.player = (0, 0)

    def display(self):
        """A : Il n'y a aucun mur
        B : Il y a un mur à droite et rien en dessous
        C : Il n'y a pas de murs à droite et un en dessous
        D : Il y a deux murs"""
        cells = ""
        for cell in self.maze.cells:
            if cell.j == self.maze.height:
                if cell.i == self.maze.width:
                    cells += "D"
                elif (
                    cell,
                    Cell(cell.i + 1, cell.j, self.maze.width, self.maze.height),
                ) in self.maze.walls:
                    cells += "D"
                elif (
                    cell,
                    Cell(cell.i + 1, cell.j, self.maze.width, self.maze.height),
                ) not in self.maze.walls:
                    cells += "C"
            elif cell.i == self.maze.width:
                if (
                    cell,
                    Cell(cell.i, cell.j + 1, self.maze.width, self.maze.height),
                ) in self.maze.walls:
                    cells += "D"
                elif (
                    cell,
                    Cell(cell.i, cell.j + 1, self.maze.width, self.maze.height),
                ) not in self.maze.walls:
                    cells += "B"
            else:
                if (
                    cell,
                    Cell(cell.i + 1, cell.j, self.maze.width, self.maze.height),
                ) not in self.maze.walls:
                    if (
                        cell,
                        Cell(cell.i, cell.j + 1, self.maze.width, self.maze.height),
                    ) not in self.maze.walls:
                        cells += "A"
                    else:
                        cells += "C"
                elif (
                    cell,
                    Cell(cell.i, cell.j + 1, self.maze.width, self.maze.height),
                ) not in self.maze.walls:
                    if (
                        cell,
                        Cell(cell.i + 1, cell.j, self.maze.width, self.maze.height),
                    ) not in self.maze.walls:
                        cells += "A"
                    else:
                        cells += "B"
                else:
                    cells += "D"
        return {
            "laby": cells,
            "pos_player": str(self.player),
            "taille": str(self.maze.width),
            "state": self.has_won(),
        }

    def move(self, direction: str):
        x, y = self.player
        if direction == "right":
            if x < self.maze.width:
                self.player = (x + 1, y)
        elif direction == "left":
            if x > 0:
                self.player = (x - 1, y)
        elif direction == "up":
            if y > 0:
                self.player = (x, y - 1)
        else:
            if y < self.maze.height:
                self.player = (x, y + 1)

    def has_won(self) -> bool:
        if self.player == (self.maze.width, self.maze.height):
            return True
        return False

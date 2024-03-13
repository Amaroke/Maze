from outils_sql import modifier
from maze import Maze
from cell import Cell
from time import time


class Game:
    """Class with a maze instance and a player represented in x and y coordinates"""

    def __init__(self, width: int, height: int):
        self.maze = Maze(width, height)
        self.player = (0, 0)
        self.start = time()
        self.mini_move = len(self.maze.path) - 1
        self.number_of_moves = 0
        self.pseudo = ""

    def display(self):
        """A : Il n'y a aucun mur
        B : Il y a un mur à droite et rien en dessous
        C : Il n'y a pas de murs à droite et un en dessous
        D : Il y a deux murs"""
        cells = ""
        solution = ""
        for cell in self.maze.path:
            solution += str(cell.i) + "," + str(cell.j) + ";"
        for cell in self.maze.cells:
            if cell.j == self.maze.height - 1:
                if cell.i == self.maze.width - 1:
                    cells += "D"
                elif (
                    cell,
                    Cell(cell.i + 1, cell.j, self.maze.width, self.maze.height),
                ) in self.maze.walls:
                    cells += "D"
                else:
                    cells += "C"
            elif cell.i == self.maze.width - 1:
                if (
                    cell,
                    Cell(cell.i, cell.j + 1, self.maze.width, self.maze.height),
                ) in self.maze.walls:
                    cells += "D"
                else:
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
            "maze": cells,
            "pos_player": self.player,
            "size": self.maze.width,
            "state": self.has_won(),
            "solution": solution,
        }

    def move(self, direction: str):
        x, y = self.player
        self.number_of_moves += 1
        if direction == "right":
            if (x + 1 < self.maze.width) and (
                (
                    Cell(x, y, self.maze.width, self.maze.height),
                    Cell(x + 1, y, self.maze.width, self.maze.height),
                )
                not in self.maze.walls
            ):
                self.player = (x + 1, y)
        elif direction == "left":
            if (x - 1 >= 0) and (
                (
                    Cell(x - 1, y, self.maze.width, self.maze.height),
                    Cell(x, y, self.maze.width, self.maze.height),
                )
                not in self.maze.walls
            ):
                self.player = (x - 1, y)
        elif direction == "up":
            if (y - 1 >= 0) and (
                (
                    Cell(x, y - 1, self.maze.width, self.maze.height),
                    Cell(x, y, self.maze.width, self.maze.height),
                )
                not in self.maze.walls
            ):
                self.player = (x, y - 1)
        elif direction == "down":
            if (y + 1 < self.maze.height) and (
                (
                    Cell(x, y, self.maze.width, self.maze.height),
                    Cell(x, y + 1, self.maze.width, self.maze.height),
                )
                not in self.maze.walls
            ):
                self.player = (x, y + 1)

    def has_won(self):
        if self.player == (self.maze.width - 1, self.maze.height - 1):
            elapsed = int(time() - self.start)
            score = (
                len(self.maze.cells)
                - (self.number_of_moves - self.mini_move)
                - elapsed // 5
            )
            modifier(
                """INSERT INTO results (Name, Score) VALUES (?, ?)""",
                (self.pseudo, score),
            )
            return (
                "You have won in "
                + str(elapsed // 60)
                + " minutes and "
                + str(elapsed % 60)
                + " seconds !\n Your number of move was "
                + str(self.number_of_moves)
                + " while the minimal was "
                + str(self.mini_move)
                + " !"
            )
        return "Keep playing"

    def restart(self, pseudo: str, width: str, height: str):
        if (width != "" or height != "") and width.isnumeric() and height.isnumeric():
            self.maze.width = int(width)
            self.maze.height = int(height)
        self.maze = Maze(self.maze.width, self.maze.height)
        self.player = (0, 0)
        self.start = time()
        self.number_of_moves = 0
        self.mini_move = len(self.maze.path) - 1
        self.pseudo = pseudo

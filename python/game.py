import sqlite3
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
            "laby": cells,
            "pos_player": self.player,
            "taille": self.maze.width,
            "state": self.has_won(),
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
            conn = sqlite3.connect("performances.db")
            conn.isolation_level = None
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO resultats (Name, Time, Nb_cells, Move_sup) VALUES (?, ?, ?, ?)""",
                (
                    self.pseudo,
                    elapsed,
                    self.maze.width * self.maze.height,
                    self.number_of_moves - self.mini_move,
                ),
            )
            conn.close()
            return (
                "Vous avez gagné ! \n Temps : "
                + str(elapsed // 60)
                + " minutes \n et "
                + str(elapsed % 60)
                + " secondes. \n Votre nombre de mouvements était "
                + str(self.number_of_moves)
                + " \nalors que le nombre minimal était "
                + str(self.mini_move)
            )
        return "Continuer à jouer !"

    def restart(self, pseudo: str, width: int, height: int):
        if width != "" or height != "":
            self.maze.width = int(width)
            self.maze.height = int(height)
        self.maze = Maze(self.maze.width, self.maze.height)
        self.player = (0, 0)
        self.start = time()
        self.number_of_moves = 0
        self.mini_move = len(self.maze.path) - 1
        self.pseudo = pseudo

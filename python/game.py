from maze import Maze


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
            if (cell, cell.neighbors[2]) not in self.maze.walls and (
                cell,
                cell.neighbors[3],
            ) not in self.maze.walls:
                cells += "A"
            elif (cell, cell.neighbors[2]) in self.maze.walls and (
                cell,
                cell.neighbors[3],
            ) not in self.maze.walls:
                cells += "B"
            elif (cell, cell.neighbors[2]) not in self.maze.walls and (
                cell,
                cell.neighbors[3],
            ) in self.maze.walls:
                cells += "C"
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
        if direction == "up":
            self.player = (x, y - 1)
        elif direction == "down":
            self.player = (x, y + 1)
        elif direction == "left":
            self.player = (x + 1, y)
        else:
            self.player = (x - 1, y)

    def has_won(self) -> bool:
        if self.player == (self.maze.width, self.maze.height):
            return True
        return False

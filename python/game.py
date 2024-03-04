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
        print(cells)

        return {
            "laby": cells,
            "pos_player": self.player,
            "taille": self.maze.width,
            "state": self.has_won(),
        }

    def move(self, direction: str):
        x, y = self.player
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

    def has_won(self) -> bool:
        if self.player == (self.maze.width, self.maze.height):
            return "Vous avez gagné !"
        return "Continuer à jouer !"


if __name__ == "__main__":
    game = Game(10, 10)
    game.display()

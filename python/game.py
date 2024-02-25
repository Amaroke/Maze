from maze import Maze


class Game:
    # Classe avec une instance de maze et un joueur représenté en coordonénées x et y
    def __init__(self, width: int, height: int):
        self.maze = Maze(width, height)
        self.player = (0, 0)

    # Méthode pour afficher le labyrinthe
    def display(self):
        # Doit renvoyer une chaîne de caractères représentant le labyrinthe avec le joueur à toi de voir comment tu veux faire passer ça pour ensuite facilement le traiter en JS (peut-être te renseigner sur le format json)
        return

    # Méthode pour déplacer le joueur
    def move(self, direction: str):
        return

    # Méthode pour vérifier si le joueur a gagné
    def has_won(self) -> bool:
        return

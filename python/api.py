# FORME DE BASE MODIFIE SELON CE QUE TU VEUX FAIRE ET TES FONCTIONS PYTHON

from flask import Flask, request, jsonify
from flask_cors import CORS
from game import Game

app = Flask(__name__)
CORS(
    app
)  # Ca c'est la sécurité des navigateurs comme je t'avais expliqué avec ça tu peux faire des requêtes depuis ton front-end sans problème
game = Game(10, 10)


@app.route("/display", methods=["GET"])
def display():
    return jsonify(game.display())


@app.route("/move", methods=["POST"])
def move():
    direction = request.json["direction"]
    game.move(direction)
    return jsonify(game.display())


@app.route("/has_won", methods=["GET"])
def has_won():
    return jsonify(game.has_won())


if __name__ == "__main__":
    app.run()

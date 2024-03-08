from flask import Flask, request, jsonify
from flask_cors import CORS
from game import Game
from outils_sql import modifier, lire

creation_sql = """CREATE TABLE IF NOT EXISTS resultats (
	"ID"	INTEGER,
	"Name"	TEXT,
	"Time"	INTEGER,
	"Nb_cells"	INTEGER,
	"Move_sup"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT)
);"""

ajout_sql = (
    """INSERT INTO resultats (Name, Time, Nb_cells, Move_sup) VALUES (?, ?, ?, ?)"""
)
modifier(creation_sql)

app = Flask(__name__)
CORS(app)

game = Game(20, 20)


@app.route("/display", methods=["GET"])
def display():
    return jsonify(game.display())


@app.route("/move", methods=["POST"])
def move():
    direction = request.json["direction"]
    game.move(direction)
    return jsonify()


@app.route("/restart", methods=["POST"])
def restart():
    game.restart()
    return jsonify()


if __name__ == "__main__":
    app.run(debug=True)

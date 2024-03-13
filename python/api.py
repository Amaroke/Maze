from flask import Flask, request, jsonify
from flask_cors import CORS
from game import Game
from outils_sql import modifier, lire

creation_sql = """CREATE TABLE IF NOT EXISTS results (
	"ID"	INTEGER,
	"Name"	TEXT,
	"Score"  INTEGER, 
	PRIMARY KEY("ID" AUTOINCREMENT)
);"""

modifier(creation_sql)

app = Flask(__name__)
CORS(app)

game = Game(3, 3)


@app.route("/display", methods=["GET"])
def display():
    return jsonify(game.display())


@app.route("/move", methods=["POST"])
def move():
    direction = request.json["direction"]
    game.move(direction)
    return jsonify()


@app.route("/scores", methods=["GET"])
def scores():
    return jsonify(lire("SELECT * FROM results", multiples=True))


@app.route("/restart", methods=["POST"])
def restart():
    game.restart(request.json["pseudo"], request.json["width"], request.json["height"])
    return jsonify()


if __name__ == "__main__":
    app.run(debug=True, port=5001)

from flask import Flask, request, jsonify
from flask_cors import CORS
from game import Game

app = Flask(__name__)
CORS(app)
game = Game(25, 25)


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
    app.run(debug=True)

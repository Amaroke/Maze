from flask import Flask, request, jsonify
from flask_cors import CORS
from game import Game

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


@app.route("/restart", methods=["POST"])
def restart():
    game.restart()
    return jsonify()


if __name__ == "__main__":
    app.run(debug=True)

let pseudo = localStorage.getItem("pseudo");

if (pseudo === null) {
    pseudo = prompt("Give your nick :");
    localStorage.setItem("pseudo", pseudo);
}

restart();

async function displayGame() {
    document.getElementById("scores").hidden = true;
    const response = await fetch("http://127.0.0.1:5000/display");
    const gameData = await response.json();
    const maze = splitMaze(gameData.maze, gameData.size);
    const solution = gameData.solution;

    var coordArray = solution.split(";");
    var coordinates = [];
    for (var i = 0; i < coordArray.length; i++) {
        var coordPair = coordArray[i].split(",");
        var x = parseFloat(coordPair[0]);
        var y = parseFloat(coordPair[1]);
        coordinates.push({ x, y });
    }

    displayState(gameData.state);

    let content = '';
    for (let i = 0; i < maze.length; i++) {
        const line = maze[i];

        for (let j = 0; j < line.length; j++) {
            const character = line[j];
            let isPlayer = false;
            let isSolution = false;
            let isEnd = false;
            if (gameData.pos_player[0] === j && gameData.pos_player[1] === i) {
                isPlayer = true;
            }
            if (j == maze[0].length - 1 && i == maze.length - 1) {
                isEnd = true;
            }
            if (coordinates.some(coord => coord.x === j && coord.y === i)) {
                isSolution = true;
            }
            content += generateDiv(character, isPlayer, isEnd, (isSolution && localStorage.getItem("solution")));

        }
        content += '<br>';
    }

    document.getElementById("gameDisplay").innerHTML = content;

    resizeCase(maze.length, maze[0].length);
}

async function displayState(state) {
    document.getElementById("playing").hidden = state[0] == 'Y';
    document.getElementById("gameStatus").innerText = state;
}

async function move(direction, gameData) {
    await fetch("http://127.0.0.1:5000/move", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ direction: direction, gameData: gameData }),
    });
    displayGame();
}

async function restart() {
    document.getElementById("scores").hidden = true;
    document.getElementById("gameDisplay").hidden = false;
    document.getElementById("gameStatus").hidden = false;
    document.getElementById("playing").hidden = false;
    document.getElementById("showScore").hidden = false;
    document.getElementById("showSolution").hidden = false;

    await fetch("http://127.0.0.1:5000/restart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ pseudo: pseudo, width: "", height: "" })
    });
    displayGame();
}

async function modifyPseudo() {
    pseudo = prompt("Give your new nick :");
    localStorage.setItem("pseudo", pseudo);
    restart();
}

async function showSolution() {
    localStorage.setItem("solution", localStorage.getItem("solution") === "true" ? "false" : "true");
    displayGame();
}

async function modifySize() {
    let width = prompt("Enter the width of the new maze :");
    let height = prompt("Enter the height of the new maze :");
    await fetch("http://127.0.0.1:5000/restart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ pseudo: pseudo, width: width, height: height })
    });
    restart();
}

async function showScore() {
    const response = await fetch("http://127.0.0.1:5000/scores");
    const scores = await response.json();
    let content = "<tr><th class='th_score'>Pseudo</th><th class='th_score'>Score</th></tr>";
    for (let i = 0; i < scores.length; i++) {
        const score = scores[i] + "";
        const values = score.split(",");
        content += `<tr><td class='td_score'>${values[1]}</td><td class='td_score'>${values[2]}</td></tr>`;
    }
    document.getElementById("scores").hidden = false;
    document.getElementById("scoreTable").innerHTML = content;
    document.getElementById("gameDisplay").hidden = true;
    document.getElementById("gameStatus").hidden = true;
    document.getElementById("playing").hidden = true;
    document.getElementById("showScore").hidden = true;
    document.getElementById("restart").hidden = false;
    document.getElementById("showSolution").hidden = true;
}


function splitMaze(laby, taille) {
    const tab = [];
    for (let i = 0; i < laby.length; i += parseInt(taille)) {
        tab.push(laby.substr(i, taille));
    }
    return tab;
}

function generateDiv(character, isPlayer, isEnd, isSolution) {
    let classes = "case" + character;
    if (isPlayer) {
        classes += " player";
    }
    if (isEnd) {
        classes += " end";
    }
    if (isSolution === "true") {
        classes += " solution";
    }
    return `<div class="${classes}"></div>`;
}

function resizeCase(width, height) {
    var cases = document.querySelectorAll('.gameDisplay > div');
    cases.forEach(function (caseElement) {
        caseElement.style.width = 100 / height + '%';
        caseElement.style.height = 100 / width + '%';
    });
}
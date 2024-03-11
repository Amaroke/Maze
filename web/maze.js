let pseudo = localStorage.getItem("pseudo");

if (pseudo === null) {
    pseudo = prompt("Entrez votre pseudo");
    localStorage.setItem("pseudo", pseudo);
}

restart();

async function displayGame() {
    document.getElementById("scores").hidden = true;
    const response = await fetch("http://127.0.0.1:5000/display");
    const gameData = await response.json();
    const laby = separerLaby(gameData.laby, gameData.taille);
    displayState(gameData.state);

    let contenuTableau = '';
    for (let i = 0; i < laby.length; i++) {
        const ligne = laby[i];

        for (let j = 0; j < ligne.length; j++) {
            const caractere = ligne[j];
            if (gameData.pos_player[0] === j && gameData.pos_player[1] === i) {
                contenuTableau += generateDiv(caractere, true, false);
            } else if (j == laby[0].length - 1 && i == laby.length - 1) {
                contenuTableau += generateDiv(caractere, false, true);
            } else {
                contenuTableau += generateDiv(caractere, false, false);
            }
        }
        contenuTableau += '<br>';
    }

    document.getElementById("gameDisplay").innerHTML = contenuTableau;

    resizeCase(laby.length, laby[0].length);
}

async function displayState(state) {
    document.getElementById("playing").hidden = state[0] == 'V';
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
    await fetch("http://127.0.0.1:5000/restart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ pseudo: pseudo, width: "", height: "" })
    });
    displayGame()
}

async function modifyPseudo() {
    pseudo = prompt("Entrez votre nouveau pseudo");
    localStorage.setItem("pseudo", pseudo);
    displayGame();
}

async function modifySize() {
    let width = prompt("Entrez la largeur du labyrinthe");
    let height = prompt("Entrez la hauteur du labyrinthe");
    await fetch("http://127.0.0.1:5000/restart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ pseudo: pseudo, width: width, height: height })
    });
    displayGame();
}

async function showScore() {
    const response = await fetch("http://127.0.0.1:5000/scores");
    const scores = await response.json();
    let contenuTableau = "";
    for (let i = 0; i < scores.length; i++) {
        const score = scores[i] + "";
        const values = score.split(",");
        contenuTableau += `<tr><td>${values[1]}</td><td>${values[2]}</td><td>${values[3]}</td><td>${values[4]}</td></tr>`;
    }
    document.getElementById("scores").hidden = false;
    document.getElementById("scoreTable").innerHTML += contenuTableau;
    document.getElementById("gameDisplay").hidden = true;
    document.getElementById("gameStatus").hidden = true;
    document.getElementById("playing").hidden = true;
    document.getElementById("showScore").hidden = true;
    document.getElementById("restart").hidden = false;
}


function separerLaby(laby, taille) {
    const tableauLignes = [];
    for (let i = 0; i < laby.length; i += parseInt(taille)) {
        tableauLignes.push(laby.substr(i, taille));
    }
    return tableauLignes;
}

function generateDiv(caractere, isPlayer, isEnd) {
    let classes = "case" + caractere;
    if (isPlayer) {
        classes += " player";
    } else if (isEnd) {
        classes += " end";
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


displayGame();
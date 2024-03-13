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
    const solution = gameData.solution;

    var coordArray = solution.split(";"); // Diviser la chaîne en un tableau de sous-chaînes

    var coordinates = []; // Initialiser un tableau vide pour stocker les coordonnées

    // Parcourir chaque sous-chaîne pour extraire les coordonnées
    for (var i = 0; i < coordArray.length; i++) {
        var coordPair = coordArray[i].split(","); // Diviser la sous-chaîne en un tableau de coordonnées
        var x = parseFloat(coordPair[0]); // Convertir la première partie en nombre flottant (x)
        var y = parseFloat(coordPair[1]); // Convertir la deuxième partie en nombre flottant (y) // Créer un objet contenant les coordonnées
        coordinates.push({ x, y }); // Ajouter l'objet au tableau des coordonnées
    }

    displayState(gameData.state);

    let contenuTableau = '';
    for (let i = 0; i < laby.length; i++) {
        const ligne = laby[i];

        for (let j = 0; j < ligne.length; j++) {
            const caractere = ligne[j];
            let isPlayer = false;
            let isSolution = false;
            let isEnd = false;
            if (gameData.pos_player[0] === j && gameData.pos_player[1] === i) {
                isPlayer = true;
            }
            if (j == laby[0].length - 1 && i == laby.length - 1) {
                isEnd = true;
            }
            if (coordinates.some(coord => coord.x === j && coord.y === i)) {
                isSolution = true;
            }
            contenuTableau += generateDiv(caractere, isPlayer, isEnd, (isSolution && localStorage.getItem("solution")));

        }
        contenuTableau += '<br>';
    }

    document.getElementById("gameDisplay").innerHTML = contenuTableau;

    resizeCase(laby.length, laby[0].length);
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
    pseudo = prompt("Entrez votre nouveau pseudo");
    localStorage.setItem("pseudo", pseudo);
    restart();
}

async function showSolution() {
    localStorage.setItem("solution", localStorage.getItem("solution") === "true" ? "false" : "true");
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
    restart();
}

async function showScore() {
    const response = await fetch("http://127.0.0.1:5000/scores");
    const scores = await response.json();
    let contenuTableau = "<tr><th class='th_score'>Pseudo</th><th class='th_score'>Score</th></tr>";
    for (let i = 0; i < scores.length; i++) {
        const score = scores[i] + "";
        const values = score.split(",");
        contenuTableau += `<tr><td class='td_score'>${values[1]}</td><td class='td_score'>${values[2]}</td></tr>`;
    }
    document.getElementById("scores").hidden = false;
    document.getElementById("scoreTable").innerHTML = contenuTableau;
    document.getElementById("gameDisplay").hidden = true;
    document.getElementById("gameStatus").hidden = true;
    document.getElementById("playing").hidden = true;
    document.getElementById("showScore").hidden = true;
    document.getElementById("restart").hidden = false;
    document.getElementById("showSolution").hidden = true;
}


function separerLaby(laby, taille) {
    const tableauLignes = [];
    for (let i = 0; i < laby.length; i += parseInt(taille)) {
        tableauLignes.push(laby.substr(i, taille));
    }
    return tableauLignes;
}

function generateDiv(caractere, isPlayer, isEnd, isSolution) {
    let classes = "case" + caractere;
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
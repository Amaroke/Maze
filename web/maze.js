async function displayGame() {
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
                contenuTableau += generateDiv(caractere, true);
            } else {
                contenuTableau += generateDiv(caractere, false);
            }
        }
        contenuTableau += '<br>';
    }

    document.getElementById("gameDisplay").innerHTML = contenuTableau;

    resizeCase(laby.length, laby[0].length);
}

async function displayState(state) {
    document.getElementById("playing").hidden = state[0] == 'V';
    document.getElementById("win").hidden = state[0] != 'V';
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
    await fetch("http://127.0.0.1:5000/restart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        }
    });
    displayGame()
}

function separerLaby(laby, taille) {
    const tableauLignes = [];
    for (let i = 0; i < laby.length; i += parseInt(taille)) {
        tableauLignes.push(laby.substr(i, taille));
    }
    return tableauLignes;
}

function generateDiv(caractere, isPlayer) {
    let classes = "case" + caractere;
    if (isPlayer) {
        classes += " player";
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
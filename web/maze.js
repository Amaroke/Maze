async function displayGame() {
    const response = await fetch("http://127.0.0.1:5000/display");
    const gameData = await response.json();

    const laby = await separerLaby(gameData.laby, gameData.taille);
    const state = gameData.state;
    const pos_player = gameData.pos_player;

    let laby_rotate = [];
    for (let i = 0; i < laby[0].length; i++) {
        let ligne = "";
        for (let j = 0; j < laby.length; j++) {
            ligne += laby[j][i];
        }
        laby_rotate.push(ligne);
    }

    let contenuTableau = '';
    for (let i = 0; i < laby.length; i++) {
        const ligne = laby[i];

        for (let j = 0; j < ligne.length; j++) {
            const caractere = ligne[j];
            if (pos_player[0] === j && pos_player[1] === i) {
                if (caractere === "A") {
                    contenuTableau += '<div class="caseA player"></div>';
                } else if (caractere === "B") {
                    contenuTableau += '<div class="caseB player"></div>';
                } else if (caractere === "C") {
                    contenuTableau += '<div class="caseC player"></div>';
                } else if (caractere === "D") {
                    contenuTableau += '<div class="caseD player"></div>';
                }
            }
            else {
                if (caractere === "A") {
                    contenuTableau += '<div class="caseA"></div>';
                } else if (caractere === "B") {
                    contenuTableau += '<div class="caseB"></div>';
                } else if (caractere === "C") {
                    contenuTableau += '<div class="caseC"></div>';
                } else if (caractere === "D") {
                    contenuTableau += '<div class="caseD"></div>';
                }
            }
        }
        contenuTableau += '<br>';
    }

    document.getElementById("gameDisplay").innerHTML = contenuTableau;
    document.getElementById("gameStatus").innerText = state;

    var cases = document.querySelectorAll('.gameDisplay > div');
    cases.forEach(function (caseElement) {
        caseElement.style.width = 100 / laby_rotate.length + '%';
        caseElement.style.height = 100 / laby_rotate.length + '%';
    });
}

async function separerLaby(laby, taille) {
    const tableauLignes = [];
    for (let i = 0; i < laby.length; i += parseInt(taille)) {
        tableauLignes.push(laby.substr(i, taille));
    }
    return tableauLignes;
}

async function move(direction, gameData) {
    const response = await fetch("http://127.0.0.1:5000/move", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ direction: direction, gameData: gameData }),
    });
    displayGame();
    // GERER LA REPONSE EN CAS DE WIN OU DERREUR EN GROS
}

displayGame();
async function displayGame() {
    const response = await fetch("http://127.0.0.1:5000/display");
    const gameData = await response.json();

    const laby = await separerLaby(gameData.laby, gameData.taille);
    const state = gameData.state;
    alert(laby)

    let contenuTableau = '<table class="maze">';
    for (let i = 0; i < laby.length; i++) {
        const ligne = laby[i];

        contenuTableau += '<tr>';
        for (let j = 0; j < ligne.length; j++) {
            const caractere = ligne[j];
            if (caractere === "A") {
                contenuTableau += '<td class="caseA">A</td>';
            } else if (caractere === "B") {
                contenuTableau += '<td class="caseB">B</td>';
            } else if (caractere === "c") {
                contenuTableau += '<td class="caseC">C</td>';
            } else if (caractere === "D") {
                contenuTableau += '<td class="caseD">D</td>';
            }
        }
        contenuTableau += '</tr>';
    }
    contenuTableau += '</table>';

    document.getElementById("gameDisplay").innerHTML = contenuTableau;
    document.getElementById("gameStatus").innerText = state;
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
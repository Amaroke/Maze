let gameData; // Déclarer la variable gameData à l'extérieur pour qu'elle soit accessible à plusieurs fonctions

async function displayGame() {
    const response = await fetch("http://127.0.0.1:5000/display");
    gameData = await response.json(); // Utiliser la variable gameData déclarée à l'extérieur
    document.getElementById("gameDisplay").innerText = JSON.stringify(gameData);
}

async function separerLaby(laby, taille) {
    const tableauLignes = [];
    for (let i = 0; i < laby.length; i += taille) {
        tableauLignes.push(laby.substr(i, taille));
    }
    return tableauLignes;
}

async function move(direction) {
    const response = await fetch("http://127.0.0.1:5000/move", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ direction: direction }),
    });

    gameData = await response.json();
    const laby = separerLaby(gameData.laby, gameData.taille); // Utiliser la variable laby déclarée localement
    const pos_player = gameData.pos_player;
    const state = gameData.state;

    let contenuTableau = '<table>';
    for (let i = 0; i < laby.length; i++) { // Utiliser le bon nom de variable ici (laby au lieu de tableauDeLignes)
        const ligne = laby[i];
        contenuTableau += '<tr>';
        for (let j = 0; j < ligne.length; j++) {
            const caractere = ligne[j];
            if (caractere === "A") {
                contenuTableau += '<td class="case00"></td>';
            } else if (caractere === "B") {
                contenuTableau += '<td class="case10"></td>';
            } else if (caractere === "c") {
                contenuTableau += '<td class="case01"></td>';
            } else if (caractere === "D") {
                contenuTableau += '<td class="case11"></td>';
            }
        }
        contenuTableau += '</tr>';
    }
    contenuTableau += '</table>';
    document.getElementById("gameDisplay").innerHTML = contenuTableau;
    if (state) {
        document.getElementById("gameStatus").innerText = "You have won!";
    } else {
        document.getElementById("gameStatus").innerText = "Keep playing...";
    }
}

displayGame();
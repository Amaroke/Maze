async function displayGame() {
    const response = await fetch("http://127.0.0.1:5000/display");
    const gameData = await response.json();
    document.getElementById("gameDisplay").innerText =
        JSON.stringify(gameData);
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
    const gameData = await response.json();
    laby = separerLaby(gameData.laby, gameData.taille)
    pos_player = gameData.pos_player
    state = gameData.state
    document.getElementById("gameDisplay").innerHTML = '<table>'
    for (let i = 0; i < tableauDeLignes.length; i++) {
        const ligne = tableauDeLignes[i];
        document.getElementById("gameDisplay").innerHTML = '<tr>'
        for (let j = 0; j < ligne.length; j++) {
            const caractere = ligne[j];
            if (caractere === "A") {
                document.getElementById("gameDisplay").innerHTML = '<td class="case00"></td>'
            }
            else if (caractere === "B") {
                document.getElementById("gameDisplay").innerHTML = '<td class="case10"></td>'
            }
            else if (caractere === "c") {
                document.getElementById("gameDisplay").innerHTML = '<td class="case01"></td>'
            }
            else if (caractere === "D") {
                document.getElementById("gameDisplay").innerHTML = '<td class="case11"></td>'
            }
        }
        document.getElementById("gameDisplay").innerHTML = '</tr>'
    }
    document.getElementById("gameDisplay").innerHTML = '</table>'
}
document.getElementById("gameDisplay").innerText =
    JSON.stringify(gameData);
//checkGameStatus();
if (state) {
    document.getElementById("gameStatus").innerText = "You have won!";
} else {
    document.getElementById("gameStatus").innerText = "Keep playing...";
}

/*
async function checkGameStatus() {
    const response = await fetch("http://127.0.0.1:5000/has_won");
    const status = await response.json();
    if (status) {
        document.getElementById("gameStatus").innerText = "You have won!";
    } else {
        document.getElementById("gameStatus").innerText = "Keep playing...";
    }
}
*/
displayGame();
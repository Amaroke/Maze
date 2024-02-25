async function displayGame() {
    const response = await fetch("http://127.0.0.1:5000/display");
    const gameData = await response.json();
    document.getElementById("gameDisplay").innerText =
        JSON.stringify(gameData);
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
    document.getElementById("gameDisplay").innerText =
        JSON.stringify(gameData);
    checkGameStatus();
}

async function checkGameStatus() {
    const response = await fetch("http://127.0.0.1:5000/has_won");
    const status = await response.json();
    if (status) {
        document.getElementById("gameStatus").innerText = "You have won!";
    } else {
        document.getElementById("gameStatus").innerText = "Keep playing...";
    }
}

displayGame();
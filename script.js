console.log("Welcome to Tic-Tac-Toe");
let turnSoundEffect = new Audio("ting.mp3");
// let gameOverSound = new Audio("")
let currentPlayerTurn = 'X';
let isGameCompleted = false;

// Function to switch player turn
const switchPlayerTurn = () => {
    return currentPlayerTurn === 'X' ? 'O' : 'X';
}

// Function to check for win
const checkForWin = () => {
    let boxTextElements = document.getElementsByClassName("boxtext");
    let winningCombinations = [
        [0, 1, 2, 5, 5, 0],
        [3, 4, 5, 5, 15, 0],
        [6, 7, 8, 5, 25, 0],
        [0, 3, 6, -5, 15, 90],
        [1, 4, 7, 5, 15, 90],
        [2, 5, 8, 15, 15, 90],
        [0, 4, 8, 5, 15, 45],
        [2, 4, 6, 5, 15, 135],
    ]
    winningCombinations.forEach(combination => {
        if ((boxTextElements[combination[0]].innerHTML === boxTextElements[combination[1]].innerHTML && boxTextElements[combination[2]].innerHTML === boxTextElements[combination[1]].innerHTML) && (boxTextElements[combination[1]].innerHTML !== "")) {
            document.querySelector('.info').innerText = boxTextElements[combination[0]].innerText + " Won";
            isGameCompleted = true;
            document.querySelector('.imgbox').getElementsByTagName('img')[0].style.width = "200px";
            document.querySelector(".line").style.width = "20vw";
            document.querySelector(".line").style.transform = `translate(${combination[3]}vw, ${combination[4]}vw) rotate(${combination[5]}deg)`
        }
    })
}

// Game logic

// Change the turn for in info class
let gameBoxes = Array.from(document.getElementsByClassName('box'));
gameBoxes.forEach(element => {
    let boxText = element.querySelector('.boxtext');
    element.addEventListener("click", () => {
        if (boxText.innerText === '') {
            boxText.innerText = currentPlayerTurn;
            currentPlayerTurn = switchPlayerTurn();
            turnSoundEffect.play();
            checkForWin();
            if (!isGameCompleted) {
                document.getElementsByClassName("info")[0].innerText = "Turn for " + currentPlayerTurn;
            }
        }
    })
});

// Add on click listener to reset button
let resetButton = document.getElementById("reset");
resetButton.addEventListener('click', () => {
    let boxTextElements = document.querySelectorAll('.boxtext');
    Array.from(boxTextElements).forEach(element => {
        element.innerText = ""
    })
    currentPlayerTurn = 'X';
    isGameCompleted = false;
    document.getElementsByClassName("info")[0].innerText = "Turn for " + currentPlayerTurn;
    document.querySelector('.imgbox').getElementsByTagName('img')[0].style.width = "0px";
    document.querySelector(".line").style.width = "0vw";
})

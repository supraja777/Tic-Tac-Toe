console.log("Welcome to Tic-Tac-Toe")
let audioturn = new Audio ("ting.mp3")
// let gameOver = new Audio ("")
let turn = 'X'
let isgameover = false

//Function to change the turn
const changeTurn = ()=>{
    return turn ==='X'? '0':'X';
}

//Function to check for win
const checkWin =()=>{
    let boxtext = document.getElementsByClassName("boxtext");
    let wins =[
        [0,1,2,5,5,0],
        [3,4,5,5,15,0],
        [6,7,8,5,25,0],
        [0,3,6,-5,15,90],
        [1,4,7,5,15,90],
        [2,5,8,15,15,90],
        [0,4,8,5,15,45],
        [2,4,6,5,15,135],
    ]
    wins.forEach(e=>{
        if ((boxtext[e[0]].innerHTML === boxtext[e[1]].innerHTML && boxtext[e[2]].innerHTML === boxtext[e[1]].innerHTML) && (boxtext[e[1]].innerHTML !== "")) {
            document.querySelector('.info').innerText = boxtext[e[0]].innerText + "Won";
            isgameover = true;
            document.querySelector('.imgbox').getElementsByTagName('img')[0].style.width = "200px";
            document.querySelector(".line").style.width = "20vw";
            document.querySelector(".line").style.transform = `translate(${e[3]}vw, ${e[4]}vw) rotate(${e[5]}deg)`
        }
    })
}

// Game logic



// change the turn for in info class
let boxes = Array.from(document.getElementsByClassName('box'));
boxes.forEach(element => {
    let boxText = element.querySelector('.boxtext');
    element.addEventListener("click",()=>{
        if (boxText.innerText === '') {
            boxText.innerText = turn;
            turn = changeTurn();
            audioturn.play();
            checkWin();
            if (!isgameover) {
                document.getElementsByClassName("info")[0].innerText = "Turn for " + turn;
            }
        }        
    })
});

// Add on click listener to reset button
let reset = document.getElementById("reset")
reset.addEventListener('click',()=>{
    let boxTexts = document.querySelectorAll('.boxtext');
    Array.from(boxTexts).forEach(element=>{
        element.innerText = ""
    })
    turn = 'X';
    isgameover = false;
    document.getElementsByClassName("info")[0].innerText = "Turn for " + turn;
    document.querySelector('.imgbox').getElementsByTagName('img')[0].style.width = "0px";
    document.querySelector(".line").style.width = "0vw";
})

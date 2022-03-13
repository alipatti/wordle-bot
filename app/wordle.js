var n_guesses = 0,
    cursor    = 0;

var mode = "headtohead"

const userBoard = document.querySelector(".board#user")
const botBoard = document.querySelector(".board#bot")
const wordInput = document.getElementById("wordInput")

function getTile(i, j, board="user") {
    return document.querySelector(`#${board} #tile_${i}${j}`)
}


function setTile(i, j, char, state="tbd", animate=true, board="user") {
    const tile = getTile(i,j, board=board)
    tile.innerText = char
    tile.setAttribute("state", state)
    if (animate) tile.setAttribute("animation", "pop")
}


document.onkeydown = (event) => {
    const keypress = event.key.toLowerCase()

    // check if game over
    if ((n_guesses > 6) | (mode != "headtohead")) return

    // check for backspace
    if ((keypress == "backspace") & (cursor != 0)) {
        setTile(n_guesses, cursor-1, "", state="empty", animate=false)
        cursor --
        return
    }

    // check if word is complete
    if (cursor == 5) {
        if (keypress == "enter") {
            // get word from board
            var word = ""
            for (j=0; j<5; j++)
                word += getTile(n_guesses, j).innerHTML

            getFlip(word).then(handleFlip)
        }
        return
    }

    // ensure keypress is a letter
    if (!keypress.match(/^[a-z]$/)) return

    setTile(n_guesses, cursor, keypress)

    cursor++
}



function revealTile(i, j, state) {
    const tile = getTile(i, j)
    const delay = j * 250

    setTimeout(
        () => tile.setAttribute("animation", "flip"),
        delay
    )

    setTimeout(
        () => tile.setAttribute("state", state),
        delay + 250
    )
}


async function getFlip(guess) {
    // TODO implement api

    if (guess == "toils")
        return { valid : false }

    const flips = [
        "correct",
        "present",
        "absent",
        "absent",
        "absent",
    ]

    return {
        valid : true,
        flip :  Array.from({length: 5}, () => flips[Math.random() * 5 | 0])
    }
}


function handleFlip(response) {

    if (!response.valid) {
        for (j=0; j<5; j++) {
            const tile = getTile(n_guesses, j)
            tile.setAttribute("animation", "shake")
        }
        return
    }

    // reveal tiles
    for (j=0; j<5; j++)
        revealTile(n_guesses, j, response.flip[j])

    cursor = 0
    n_guesses++ 
}


// reset animation state once tile animations end
document.onanimationend = (event) => {
    event.target.setAttribute("animation", "none")
}

function changeMode(checkbox) {
    if (checkbox.checked) mode = "challenge"
    else mode = "headtohead"

    userBoard.classList.toggle("hidden")
    wordInput.classList.toggle("hidden")
}

wordInput.onclick = () => {
    // send api request to server asking for bot's guesses
    // reveal the guesses on by one
}


/*
for bot:
 - two modes: 
   - user provides word, bot does it
     - bot 

   - play against the bot
     - user plays a game on the left
     - when done, bot plays
     - gives win/lose popup
*/
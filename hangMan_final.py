# ------------------------ LIBRARIES ------------------------
import random
import urllib.request
import keyboard
import os

# ------------------------ CONSTANTS ------------------------

# ------------------------ VARIABLES ------------------------
gameRunning = True
gameStarted = False
gameOver = False

hangMan_wordList = []
chosenWord = ""
hiddenWord = ""

chosenDif = 0
chancesLeft = 0
difList = [13, 10, 6, 4, 2, 1]

# ------------------------ FUNCTIONS ------------------------
#         ----------- Graphical Functions -----------
def GameCover():
    os.system("cls||clear")

    print("        ---------------------------------------------------------\n",
          "        =============== ** ================ ** ==================\n",
          "             |   |   /\\   |\\  |  /--\\  |\\    /|   /\\   |\\  |     \n",
          "             |---|  /--\\  | \\ | |  ___ | \\  / |  /--\\  | \\ |     \n",
          "             |   | /    \\ |  \\|  \\--/  |  \\/  | /    \\ |  \\|     \n",
          "        =============== ** ================ ** ==================\n",
          "        ---------------------------------------------------------\n\n\n",
          "                           Press SPACE to play                   \n",
          "                            Press ESC to exit                    \n")


def ChooseDif():
    global chosenDif
    global chancesLeft

    difChosen = False
    difIndex = ""

    while not difChosen:
        os.system("cls||clear")

        print("        ** WARNING: THIS DIFFICULTY WILL REMAIN UNTIL YOU RESTART THE GAME **\n",
              "                             --- Difficulty Options: ---  \n",
              "                                       Baby => 1          \n",
              "                                       Easy => 2          \n",
              "                                      Medium => 3         \n",
              "                                       Hard => 4          \n",
              "                                      Hellish => 5        \n",
              "                                Nightmare => 6  *DANGER*  \n")

        difIndex = input("What difficulty would you like? Write the number or the difficulty: ")

        if (difIndex[len(difIndex) - 1].isnumeric()):
            chosenDif = difList[ int(difIndex[len(difIndex) - 1]) - 1]
            difChosen = True
        else:
            if (("baby" in difIndex) or (difIndex[len(difIndex) - 1] == "b") or
                    (len(difIndex) >= 4 and difIndex[len(difIndex) - 4] == "b")):
                chosenDif = difList[0]
                difChosen = True
            elif (("easy" in difIndex) or (difIndex[len(difIndex) - 1] == "e") or
                  ( len(difIndex) >= 4 and difIndex[len(difIndex) - 4] == "e")):
                chosenDif = difList[1]
                difChosen = True
            elif (("med" in difIndex) or (difIndex[len(difIndex) - 1] == "m") or
                  (len(difIndex) >= 6 and difIndex[len(difIndex) - 6] == "m")):
                chosenDif = difList[2]
                difChosen = True
            elif ("ha" in difIndex) or (len(difIndex) >= 4 and difIndex[len(difIndex) - 4] == "h"
                                        and difIndex[len(difIndex) - 1] == "d"):
                chosenDif = difList[3]
                difChosen = True
            elif ("hell" in difIndex) or (len(difIndex) >= 7 and difIndex[len(difIndex) - 7] == "h"
                                          and difIndex[len(difIndex) - 1] == "h"):
                chosenDif = difList[4]
                difChosen = True
            elif (("night" in difIndex) or (difIndex[len(difIndex) - 1] == "n")
                  or (len(difIndex) >= 9 and difIndex[len(difIndex) - 9] == "n")):
                chosenDif = difList[5]
                difChosen = True


    chancesLeft = chosenDif

#         ----------- Backend Functions -----------

def MenuSelect():
    global gameRunning
    global gameStarted
    global gameOver

    while gameRunning and not gameStarted:
        if keyboard.is_pressed('E') or keyboard.is_pressed('Escape'):
            gameRunning = False

        elif keyboard.is_pressed('S') or keyboard.is_pressed('Space'):
            gameStarted = True
            gameOver = False
            print("Loading...")

def CreateWords():
    global hangMan_wordList

    MITWords = urllib.request.urlopen("https://www.mit.edu/~ecprice/wordlist.10000")
    allWords = MITWords.read().decode()
    fullWordList = allWords.splitlines()
    hangMan_wordList = [word for word in fullWordList if (word[0].islower() and len(word) >= 3)]

def ChooseHiddenWord():
    global chosenWord
    global hiddenWord

    hiddenWord = ""

    wordNum = random.randint(0, len(hangMan_wordList) - 1)
    chosenWord = hangMan_wordList[wordNum]

    for i in range(len(chosenWord)):
        hiddenWord += "*"

def GuessWord():
    global gameOver

    wordGuessed = input("(Careful, if you're wrong, you LOSE) What do you think the word is? ")
    if wordGuessed == chosenWord:
        global hiddenWord
        hiddenWord = wordGuessed
    elif wordGuessed == "nvm":
        print("Yea, that's what I thought.")
    else:
        global chancesLeft
        chancesLeft = 0
        gameOver = True

def GuessLetter():
    global gameOver

    print("Current word: " + hiddenWord)
    chr = "??"

    while len(chr) != 1:
        chr = (input("Please enter a letter, or write 'gg' to guess the word: ")).lower()
        if chr == "gg":
            GuessWord()
            chr = "?"
        elif len(chr) == 1:
            if chr == "~" or chr == "`":
                gameOver = True
            elif chr < "a" or chr > "z":
                chr = "??"
            else:
                CheckForLetter(chr)

def CheckForLetter(chr):
    global hiddenWord
    global chancesLeft

    rightLetter = False
    starList = list(hiddenWord)

    for i in range(len(chosenWord)):
        if chosenWord[i] == chr:
            rightLetter = True
            starList[i] = chr

    if not rightLetter:
        chancesLeft -= 1
        print("You have " + str(chancesLeft) + " chances left")

    hiddenWord = "".join(starList)

def CheckIfWin():
    global gameOver

    if "*" not in hiddenWord:
        print("Congrats! You got it right! The word was '" + chosenWord + "'\n")
        gameOver = True
    elif chancesLeft == 0:
        print("Oh, not quite right. The correct word was '" + chosenWord + "'\n")
        gameOver = True

def PlayAgain():
    global gameStarted
    global gameOver

    playAgain = (input("Would you like to play again (Yes / No)?")).lower()

    if playAgain[0] == "y" or playAgain[0] == "0":
        global chancesLeft

        gameOver = False
        chancesLeft = chosenDif

    elif playAgain[0] == "n" or playAgain == "1":
        gameStarted = False



#         ----------- Main Function -----------

def main():
    global gameRunning
    global gameOver

    while gameRunning:
        GameCover()
        MenuSelect()

        if gameStarted:
            ChooseDif()
            CreateWords()

            while gameStarted:
                ChooseHiddenWord()

                while not gameOver:
                    GuessLetter()
                    CheckIfWin()

                PlayAgain()

        else:
            print("Game ended")

main()

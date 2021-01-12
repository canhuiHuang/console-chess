import random
from Pieces import *
from Square import *
from VectorX import *
import copy

#Functions
def inputValidation(board): #Validates user input
    def isCmdValid(cmd):    #Also sets the formatting.
        newText = ""
        text = cmd.lower()

        if len(text) > 20 or len(text) < 5:
            print("Invalid Command or too long.")
            return "invalid"

        if (cmd[0] not in board.xLabel):
            print("Invalid Command.")
            return "invalid"
        else:
            newText += cmd[0]

        if (cmd[1] not in (board.yLabel)):
            print("Invalid Command.")
            return "invalid"
        else:
            newText += cmd[1]

        if (cmd[3] not in board.xLabel):
            print("Invalid Command.")
            return "invalid"
        else:
            newText += ' ' + cmd[3]
        if (cmd[4] not in (board.yLabel)): 
            print("Invalid Command.")
            return "invalid"
        else:
            newText += cmd[4]

        return newText

    userInput = "none"
    if (turn == 1):
        userInput = input(whiteInputPrompt)
    else:
        userInput = input(blackInputPrompt)
    userInput = isCmdValid(userInput)

    while (userInput == "invalid"):
        if (turn == 1):
            userInput = input(whiteInputPrompt)
        else:
            userInput = input(blackInputPrompt)
        userInput = isCmdValid(userInput)
    return userInput

def pair2Coord(pairString,board):        #Converts cmd to Coord in the grid. 
    r = -1
    c = -1

    for i in range(len(board.xLabel)):
        if (board.xLabel[i] == pairString[0]):
            c = i
    if (board.whitePerspective):
        r = 8 - int(pairString[1])
    else:
        r = int(pairString[1]) - 1

    return Cell(r,c)

def checkmate():
    if turn == 1:
        print("CHECKMATE. Black Wins!")
    else:
        print("CHECKMATE. White Wins!")

###############################################
turns = [1, -1]
turn = random.choice(turns) #1 for white, #-1 for black

chessBoard = Board(turn)
whiteInputPrompt = "White moves: "
blackInputPrompt = "Black moves: "
gameOver = False
###############################################

turn = 1
while (not gameOver):
    #Show Board
    chessBoard.showBoard(turn)
    print(chessBoard.grid[0][0].id)
    print(chessBoard.grid[0][0].graphic)
    print(chessBoard.grid[0][1].id)
    print(chessBoard.grid[0][1].graphic)

    #CheckState
    #0 - No Check
    #1 - On Check
    #2 - Checkmate
    #3 - Stalemate
    checkstate = chessBoard.checkStatus(turn)

    if checkstate == 0:
        #Check for Stalemate
        stalemate = True
        if turn == 1:
            if chessBoard.whiteKing.hasLegalMoves(chessBoard):
                checkstate = 0
            else:
                for piece in chessBoard.piecesWAlive:
                    if piece.hasLegalMoves(chessBoard):
                        checkstate = 0
                        stalemate = False
                        break
                if stalemate == True:
                    checkstate = 3
        else:
            if chessBoard.blackKing.hasLegalMoves(chessBoard):
                checkstate = 0
            else:
                for piece in chessBoard.piecesBAlive:
                    if piece.hasLegalMoves(chessBoard):
                        checkstate = 0
                        stalemate = False
                        break
                if stalemate == True:
                    checkstate = 3
        
        if checkstate == 0:
            #Input & Legal Move validation
            playerInput = inputValidation(chessBoard)
            pieceCoord = pair2Coord(playerInput[0] + playerInput[1], chessBoard)
            piece = chessBoard.grid[pieceCoord.r][pieceCoord.c]
            destinyCoord = pair2Coord(playerInput[3] + playerInput[4], chessBoard)

            pString = "white"
            if turn == -1:
                pString = "black"
            if piece.player != pString:
                print("Can't move that.")
            while (not piece.moveable(destinyCoord,chessBoard)) or (piece.player != pString):
                print("Can't do that.")
                playerInput = inputValidation(chessBoard)
                pieceCoord = pair2Coord(playerInput[0] + playerInput[1], chessBoard)
                piece = chessBoard.grid[pieceCoord.r][pieceCoord.c]
                destinyCoord = pair2Coord(playerInput[3] + playerInput[4], chessBoard)
                if piece.player != pString:
                    print("Can't move that.")
            
            piece.move(destinyCoord,chessBoard)
    
    elif checkstate == 2:
        checkmate()
        gameOver = True

    if checkstate == 3:
        print("STALEMATE")
        gameOver = True
    
    while checkstate == 1:
        print("CHECK")

        #Input & Legal Move validation
        playerInput = inputValidation(chessBoard)
        pieceCoord = pair2Coord(playerInput[0] + playerInput[1], chessBoard)
        piece = chessBoard.grid[pieceCoord.r][pieceCoord.c]
        destinyCoord = pair2Coord(playerInput[3] + playerInput[4], chessBoard)

        pString = "white"
        if turn == -1:
            pString = "black"
        if piece.player != pString:
            print("Can't move that.")
        while (not piece.moveable(destinyCoord,chessBoard)) or (piece.player != pString):
            print("Can't do that.")
            playerInput = inputValidation(chessBoard)
            pieceCoord = pair2Coord(playerInput[0] + playerInput[1], chessBoard)
            piece = chessBoard.grid[pieceCoord.r][pieceCoord.c]
            destinyCoord = pair2Coord(playerInput[3] + playerInput[4], chessBoard)

            if piece.player != pString:
                print("Can't move that.")

        #Fake Traslation on board & check for checks xd
        ghostBoard = copy.deepcopy(chessBoard)

        ghostBoard.grid[pieceCoord.r][pieceCoord.c].move(destinyCoord, ghostBoard)
        checkstate = ghostBoard.checkStatus(turn)

        if checkstate == 0:
            piece.move(destinyCoord,chessBoard)

    #Next turn  
    turn *= -1

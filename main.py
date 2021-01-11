import random
from Pieces import *
from Square import *
from VectorX import *
import copy

#Functions
def inputValidation(board):
    userInput = "none"
    if (turn == 1):
        userInput = input(whiteInputPrompt)
    else:
        userInput = input(blackInputPrompt)
    userInput = isCmdValid(userInput,board)

    while (userInput == "invalid"):
        if (turn == 1):
            userInput = input(whiteInputPrompt)
        else:
            userInput = input(blackInputPrompt)
        userInput = isCmdValid(userInput, board)
    return userInput

def checkmate():
    if turn == 1:
        print("Checkmate. Black Wins!")
    else:
        print("Checkmate. White Wins!")

def showBoard(board):
    print ("|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|")
    if board.whitePerspective and turn == -1:
        print("|   black   ", board.getCapturedPieces("black"),"          |")
    elif board.whitePerspective and turn == 1:
        print("|           ", board.getCapturedPieces("black"),"          |")
    elif (not board.whitePerspective and turn == 1):
        print("|   white   ", board.getCapturedPieces("white"),"          |")
    elif not board.whitePerspective and turn == -1:
        print("|           ", board.getCapturedPieces("white"),"          |")
    else:
        print("|                                                      |")
    print ("|______________________________________________________|")

    print ("  ", end = '')
    for i in range(8):
        print(" ", board.xLabel[i], " ", end = '')
    print()
    for r in range(8):
        print("  |‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|")
        print(board.yLabel[7 - r], "| ", end = '')
        for c in range(8):
            print(board.grid[r][c].piece.graphic,"| ", end = '')
        print()
    print("   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ")
    print ("  ", end = '')
    for i in range(8):
        print(" ", board.xLabel[i], " ", end = '')
    print()

    print ("|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|")
    if board.whitePerspective and turn == 1:
        print("|   white   ",board.getCapturedPieces("white"),"          |")
    elif board.whitePerspective and turn == -1:
        print("|           ",board.getCapturedPieces("white"),"          |")
    elif not board.whitePerspective and turn == -1:
        print("|   black   ",board.getCapturedPieces("black"),"          |")
    elif not board.whitePerspective and turn == 1:
        print("|           ",board.getCapturedPieces("black"),"          |")
    else:
        print("|                                                      |")
    print ("|______________________________________________________|")

def isCmdValid(cmd, board):    #Also sets the formatting.
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

###############################################
turns = [1, -1]
turn = random.choice(turns) #1 for white, #-1 for black

whiteInputPrompt = "White moves: "
blackInputPrompt = "Black moves: "
gameOver = False
###############################################

chessBoard = Board(turn)
print("despues del constructor")
print ("wKing: ", chessBoard.whiteKing.index.r,chessBoard.whiteKing.index.c)
print ("bKing: ", chessBoard.blackKing.index.r,chessBoard.blackKing.index.c)

turn = 1
while (not gameOver):
    #Show Board
    showBoard(chessBoard)

    #CheckState
    checkstate = chessBoard.checkStatus(turn)
    print(checkstate)

    if checkstate == 0:
        #Check for Stalemate
        draw = True
        if turn == 1:
            if chessBoard.whiteKing.hasLegalMoves(chessBoard):
                checkstate = 3
                draw = False
            else:
                for piece in chessBoard.piecesWAlive:
                    if piece.hasLegalMoves(chessBoard):
                        checkstate = 3
                        draw = False
        else:
            if chessBoard.blackKing.hasLegalMoves(chessBoard):
                checkstate = 3
                draw = False
            else:
                for piece in chessBoard.piecesBAlive:
                    if piece.hasLegalMoves(chessBoard):
                        checkstate = 3
                        draw = False
        
        if checkstate == 0:
            #Input & Legal Move validation
            playerInput = inputValidation(chessBoard)
            pieceCoord = pair2Coord(playerInput[0] + playerInput[1], chessBoard)
            piece = chessBoard.grid[pieceCoord.r][pieceCoord.c].piece
            destinyCoord = pair2Coord(playerInput[3] + playerInput[4], chessBoard)

            print(piece.player)
            pString = "white"
            if turn == -1:
                pString = "black"
            if piece.player != pString:
                print("Can't move opponent's piece.")
            while (not piece.moveable(destinyCoord,chessBoard)) or (piece.player != pString):
                playerInput = inputValidation(chessBoard)
                pieceCoord = pair2Coord(playerInput[0] + playerInput[1], chessBoard)
                piece = chessBoard.grid[pieceCoord.r][pieceCoord.c].piece
                destinyCoord = pair2Coord(playerInput[3] + playerInput[4], chessBoard)
                print(piece.player)
                if piece.player != pString:
                    print("Can't move opponent's piece.")
            
            piece.move(destinyCoord,chessBoard)
    
    elif checkstate == 2:
        print("CHECKMATE")
        checkmate()
        gameOver = True

    elif checkstate == 3:
        print("STALEMATE")
        gameOver = True
    
    while checkstate == 1:
        print("CHECK")

        #Input & Legal Move validation
        playerInput = inputValidation(chessBoard)
        pieceCoord = pair2Coord(playerInput[0] + playerInput[1], chessBoard)
        piece = chessBoard.grid[pieceCoord.r][pieceCoord.c].piece
        destinyCoord = pair2Coord(playerInput[3] + playerInput[4], chessBoard)

        pString = "white"
        if turn == -1:
            pString = "black"
        if piece.player != pString:
            print("Can't move opponent's piece.")
        while (not piece.moveable(destinyCoord,chessBoard)) or (piece.player != pString):
            playerInput = inputValidation(chessBoard)
            pieceCoord = pair2Coord(playerInput[0] + playerInput[1], chessBoard)
            piece = chessBoard.grid[pieceCoord.r][pieceCoord.c].piece
            destinyCoord = pair2Coord(playerInput[3] + playerInput[4], chessBoard)

            if piece.player != pString:
                print("Can't move opponent's piece.")

        #Fake Traslation on board & check for checks xd
        ghostBoard = copy.deepcopy(chessBoard)

        ghostBoard.grid[pieceCoord.r][pieceCoord.c].piece.move(destinyCoord, ghostBoard)
        checkstate = ghostBoard.checkStatus(turn)

        if checkstate == 0:
            piece.move(destinyCoord,chessBoard)

    #Next turn  
    turn *= -1

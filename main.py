import random
from Pieces import *
from Square import *
from VectorX import *

#Functions
def inputValidation():
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

def checkmate():
    if turn == 1:
        print("Checkmate. Black Wins!")
    else:
        print("Checkmate. White Wins!")

def checkOn(boardParameter):
    king = boardParameter.grid[boardParameter.whiteKingIndex.r][boardParameter.whiteKingIndex.c].piece
    if turn == -1:
        king = boardParameter.grid[boardParameter.blackKingIndex.r][boardParameter.blackKingIndex.c].piece

    attackers = king.isUnderAttacked(boardParameter.grid)
    print("White King Index: ", boardParameter.whiteKingIndex.r, boardParameter.whiteKingIndex.c)
    print("Black King Index: ", boardParameter.blackKingIndex.r, boardParameter.blackKingIndex.c)
    print("attackers: ", len(attackers))
    if len(attackers) > 0:
        if len(attackers) == 1: #Single Attack
            
            print(1)
            attacker = attackers[0]
            #Can attacker be captured?
            defenders = attacker.isUnderAttacked(boardParameter.grid)
            for defender in defenders:
                if defender.id[0] == "k":
                    if king.moveable(attacker.index, boardParameter):
                        return 1
                if not defender.amIPinnedTo(attacker.index, boardParameter.grid):
                    return 1
            print(2)
            
            #The reason amIPinned can be used is because the defender is attacking the Attacker, which means that it is LEGAL to move there,
            #So, the only thing else that needs to be checked is to see whether the defender is pinned or not.

            #Can the attack be blocked?
            sqrsBetweenAttackerNKing = attacker.shootRayTo(king.index,boardParameter.grid)
            ghostSqrs = sqrsBetweenAttackerNKing
            for sqr in ghostSqrs:
                sqr.player = attacker.player
                possibleBlockers = sqr.isUnderAttacked(boardParameter.grid)
                for blocker in possibleBlockers:
                    if not blocker.amIPinnedTo(sqr.index, boardParameter.grid):
                        return 1
            print(3)
            #Can King move?
            unitVector = DirectionalVector(1,1)
            for i in range(9):
                sqr = king.index + unitVector
                if not (sqr.r > 7 or sqr.c > 7):
                    if king.moveable(sqr,boardParameter):
                        return 1
            print(4)
            
            return 2
        
        elif len(attackers) == 2: #Double Attack
            print(69)
            #Can King move?
            unitVector = DirectionalVector(1,1)
            for i in range(9):
                sqr = king.index + unitVector
                if king.moveable(sqr,boardParameter):
                    return 1
            return 2
    else:
        return 0

def showBoard(board):
    print ("|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|")
    if whitePerspective and turn == -1:
        print("|   black   ",board.getCapturedPieces("black"),"|")
    elif (not whitePerspective and turn == 1):
        print("|   white   ",board.getCapturedPieces("white"),"|")
    else:
        print("|                                                      |")
    print ("|______________________________________________________|")

    print ("  ", end = '')
    for i in range(8):
        print(" ", xLabel[i], " ", end = '')
    print()
    for r in range(8):
        print("  |‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|")
        print(yLabel[7 - r], "| ", end = '')
        for c in range(8):
            print(board.grid[r][c].piece.graphic,"| ", end = '')
        print()
    print("   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ")
    print ("  ", end = '')
    for i in range(8):
        print(" ", xLabel[i], " ", end = '')
    print()

    print ("|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|")
    if whitePerspective and turn == 1:
        print("|   white   ",board.getCapturedPieces("white"),"|")
    elif not whitePerspective and turn == -1:
        print("|   black   ",board.getCapturedPieces("black"),"|")
    else:
        print("|                                                      |")
    print ("|______________________________________________________|")

def isCmdValid(cmd):    #Also sets the formatting.
    newText = ""
    text = cmd.lower()

    if len(text) > 20 or len(text) < 5:
        print("Invalid Command or too long.")
        return "invalid"

    if (cmd[0] not in xLabel):
        print("Invalid Command.")
        return "invalid"
    else:
        newText += cmd[0]

    if (cmd[1] not in (yLabel)):
        print("Invalid Command.")
        return "invalid"
    else:
        newText += cmd[1]

    if (cmd[3] not in xLabel):
        print("Invalid Command.")
        return "invalid"
    else:
        newText += ' ' + cmd[3]
    if (cmd[4] not in (yLabel)): 
        print("Invalid Command.")
        return "invalid"
    else:
        newText += cmd[4]

    return newText

def pair2Coord(pairString):        #Converts cmd to Coord in the grid. 
    r = -1
    c = -1

    for i in range(len(xLabel)):
        if (xLabel[i] == pairString[0]):
            c = i
    if (whitePerspective):
        r = 8 - int(pairString[1])
    else:
        r = int(pairString[1]) - 1

    return Cell(r,c)

def undo(pointA, pointB, board): #Can't untranslate castling
    board.grid[pointA.r][pointA.c].piece = board.grid[pointB.r][pointB.c].piece
    board.grid[pointB.r][pointB.c].piece = board.deadsQueue.pop(len(board.deadsQueue) - 1)

###############################################
turns = [1, -1]
turn = random.choice(turns) #1 for white, #-1 for black
bkI = Cell(-1,-1)
wkI = Cell(-1,-1)

whitePerspective = True
yLabel = ['1','2','3','4','5','6','7','8']
xLabel = ['a','b','c','d','e','f','g','h']

if (turn == -1):        #Flip Labels if perspective player is black.
    tempY = [None]*8
    for i in range(len(yLabel)):
        tempY[i] = yLabel[7 - i]
    yLabel = tempY

    tempX = [None]*8
    for i in range(len(xLabel)):
        tempX[i] = xLabel[7 - i]
    xLabel = tempX
    whitePerspective = False

whiteInputPrompt = "White moves: "
blackInputPrompt = "Black moves: "
gameOver = False
###############################################

#Create Empty 8x8 Board
grid = []
for r in range(8):
    tempRow = []
    for c in range(8):
        tempRow.append(Square(Cell(yLabel[r], xLabel[c]),Empty(Cell(yLabel[r], xLabel[c]), "0", "none", whitePerspective), False))
    grid.append(tempRow)
#Fill Board with pieces
player = "black"
if (turn == -1):
    player = "white"
grid[0][0].piece = Rook(Cell(0,0), "r1" + player[0], player, whitePerspective)
grid[0][1].piece = Knight(Cell(0,1), "n1" + player[0], player, whitePerspective)
grid[0][2].piece = Bishop(Cell(0,2), "b1" + player[0], player, whitePerspective)
if whitePerspective:
    grid[0][3].piece = Queen(Cell(0,3), "q" + player[0], player, whitePerspective)
    grid[0][4].piece = King(Cell(0,4), "k" + player[0], player, whitePerspective)
    bkI = grid[0][4].piece.index
    wkI = grid[7][4].piece.index
else:
    grid[0][3].piece = King(Cell(0,3), "k" + player[0], player, whitePerspective)
    grid[0][4].piece = Queen(Cell(0,4), "q" + player[0], player, whitePerspective)
    bkI = grid[0][3].piece.index
    wkI = grid[7][3].piece.index
grid[0][5].piece = Bishop(Cell(0,5), "b2" + player[0], player, whitePerspective)
grid[0][6].piece = Knight(Cell(0,6), "n2" + player[0], player, whitePerspective)
grid[0][7].piece = Rook(Cell(0,7), "r2" + player[0], player, whitePerspective)
for i in range(8):
    grid[1][i].piece = Pawn(Cell(1,i), "p" + str(i + 1) + player[0], player, whitePerspective)

if (player == "black"):
    player = "white"
else:
    player = "black"
grid[7][0].piece = Rook(Cell(7,0), "r1" + player[0], player, whitePerspective)
grid[7][1].piece = Knight(Cell(7,1), "n1" + player[0], player, whitePerspective)
grid[7][2].piece = Bishop(Cell(7,2), "b1" + player[0], player, whitePerspective)
if whitePerspective:
    grid[7][3].piece = Queen(Cell(7,3), "q" + player[0], player, whitePerspective)
    grid[7][4].piece = King(Cell(7,4), "k" + player[0], player, whitePerspective)
else:
    grid[7][3].piece = King(Cell(7,3), "k" + player[0], player, whitePerspective)
    grid[7][4].piece = Queen(Cell(7,4), "q" + player[0], player, whitePerspective)
grid[7][5].piece = Bishop(Cell(7,5), "b2" + player[0], player, whitePerspective)
grid[7][6].piece = Knight(Cell(7,6), "n2" + player[0], player, whitePerspective)
grid[7][7].piece = Rook(Cell(7,7), "r2" + player[0], player, whitePerspective)
for i in range(8):
    grid[6][i].piece = Pawn(Cell(6,i), "p" + str(i + 1) + player[0], player, whitePerspective)
board = Board(grid,"originalGrid",wkI,bkI)

turn = 1
while (not gameOver):
    #Show Board
    showBoard(board)

    #CheckState
    checkstate = board.checkStatus(turn)
    print(checkstate)

    while checkstate == 1:
        print("CHECK")

        #Input & Legal Move validation
        playerInput = inputValidation()
        pieceCoord = pair2Coord(playerInput[0] + playerInput[1])
        piece = board.grid[pieceCoord.r][pieceCoord.c].piece
        destinyCoord = pair2Coord(playerInput[3] + playerInput[4])

        pString = "white"
        if turn == -1:
            pString = "black"
        if piece.player != pString:
            print("Can't move opponent's piece.")
        while (not piece.moveable(destinyCoord,board)) or (piece.player != pString):
            playerInput = inputValidation()
            pieceCoord = pair2Coord(playerInput[0] + playerInput[1])
            piece = board.grid[pieceCoord.r][pieceCoord.c].piece
            destinyCoord = pair2Coord(playerInput[3] + playerInput[4])

            if piece.player != pString:
                print("Can't move opponent's piece.")

        #Fake Traslation on board & check for checks xd
        tempPointBPiece = board.grid[destinyCoord.r][destinyCoord.c].piece
        board.grid[destinyCoord.r][destinyCoord.c].piece = piece
        board.grid[pieceCoord.r][pieceCoord.c].piece = Empty(Cell(pieceCoord.r, pieceCoord.c), "0", "none", whitePerspective)

        print("before")
        checkstate = board.checkStatus(turn)
        print("after")

        board.grid[pieceCoord.r][pieceCoord.c].piece = piece
        board.grid[destinyCoord.r][destinyCoord.c].piece = tempPointBPiece

        if checkstate == 0:
            print("whats up")
            piece.move(destinyCoord,board)

    if checkstate == 0:
        #Input & Legal Move validation
        playerInput = inputValidation()
        pieceCoord = pair2Coord(playerInput[0] + playerInput[1])
        piece = board.grid[pieceCoord.r][pieceCoord.c].piece
        destinyCoord = pair2Coord(playerInput[3] + playerInput[4])

        print(piece.player)
        pString = "white"
        if turn == -1:
            pString = "black"
        if piece.player != pString:
            print("Can't move opponent's piece.")
        while (not piece.moveable(destinyCoord,board)) or (piece.player != pString):
            playerInput = inputValidation()
            pieceCoord = pair2Coord(playerInput[0] + playerInput[1])
            piece = board.grid[pieceCoord.r][pieceCoord.c].piece
            destinyCoord = pair2Coord(playerInput[3] + playerInput[4])
            print(piece.player)
            if piece.player != pString:
                print("Can't move opponent's piece.")
        
        piece.move(destinyCoord,board)
    
    elif checkstate == 2:
        print("CHECKMATE")
        checkmate()
        gameOver = True

    #Next turn  
    turn *= -1

import random
from Pieces import *
from Square import *
from VectorX import *

#Functions
def legalMoveValidation(userInput, board):
    legal = translate(pair2Coord(userInput[0] + userInput[1]),pair2Coord(userInput[3] + userInput[4]), board)
    newInput = ""
    if legal:
        return userInput
    while (not legal):
        if (turn == 1):
            newInput = input(whiteInputPrompt)
        else:
            newInput = input(blackInputPrompt)

        newInput = isCmdValid(newInput)
        while (newInput == "invalid"):
            if (turn == 1):
                newInput = input(whiteInputPrompt)
            else:
                newInput = input(blackInputPrompt)
            newInput = isCmdValid(newInput)

        legal = translate(pair2Coord(newInput[0] + newInput[1]),pair2Coord(newInput[3] + newInput[4]), board)
    return newInput

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

#CheckOn
def checkOn():
    king = grid[whiteKingIndex.r][whiteKingIndex.c].piece
    if turn == -1:
        king = grid[blackKingIndex.r][blackKingIndex.c].piece

    attackers = king.isUnderAttacked(grid)
    if len(attackers) > 0:
        if len(attackers) == 1: #Single Attack

            attacker = attackers[0]
            #Can attacker be captured?
            defenders = attacker.isUnderAttacked(grid)
            for defender in defenders:
                if not defender.amIPinnedTo(attacker.index, grid):
                    return 1
            
            #The reason amIPinned can be used is because the defender is attacking the Attacker, which means that it is LEGAL to move there,
            #So, the only thing else that needs to be checked is to see whether the defender is pinned or not.

            #Can the attack be blocked?
            sqrsBetweenAttackerNKing = attacker.shootRayTo(king.index,grid)
            ghostSqrs = sqrsBetweenAttackerNKing
            for sqr in ghostSqrs:
                sqr.piece.player = attacker.player
                possibleBlockers = sqr.isUnderAttacked(grid)
                for blocker in possibleBlockers:
                    if not blocker.amIPinnedTo(sqr.index, grid):
                        return 1

            #Can King move?
            unitVector = DirectionalVector(1,1)
            for i in range(9):
                sqr = king.index + unitVector
                if king.moveable(sqr,grid):
                    return 1
            
            return 2
        
        elif len(attackers) == 2: #Double Attack
            #Can King move?
            unitVector = DirectionalVector(1,1)
            for i in range(9):
                sqr = king.index + unitVector
                if king.moveable(sqr,grid):
                    return 1
            return 2
    else:
        return 0

def showBoard():
    print ("|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|")
    if whitePerspective and turn == -1:
        print("|        black                                         |")
    elif (not whitePerspective and turn == 1):
        print("|        white                                         |")
    else:
        print("|                                                      |")
    print ("|______________________________________________________|")

    print ("    ", end = '')
    for i in range(8):
        print(" ", xLabel[7 - i], " ", end = '')
    print()
    for r in range(8):
        print("   ","|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|")
        print(' ', yLabel[7 - r], "| ", end = '')
        for c in range(8):
            print(grid[r][c].piece.graphic,"| ", end = '')
        print()
    print("   "," ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ")
    print ("    ", end = '')
    for i in range(8):
        print(" ", xLabel[i], " ", end = '')
    print()

    print ("|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|")
    if whitePerspective and turn == 1:
        print("|       White                                          |")
    elif not whitePerspective and turn == -1:
        print("|       Black                                          |")
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

def translate(pointA, pointB, grid):
    if (turn == 1 and grid[pointA.r][pointA.c].piece.player == "white") or (turn == -1 and grid[pointA.r][pointA.c].piece.player == "black"):
        if grid[pointA.r][pointA.c].piece.moveable(pointB, grid):
            if grid[pointA.r][pointA.c].piece.move(pointB,grid):
                return True
            else:
                return False
        else:
            print("Can not perform the command. ")
            return False
    elif (grid[pointA.r][pointA.c].piece.player == "none"):
        print("No piece selected to move. ")
        return False
    else:
        print("Can't move opponent's piece. ")
        return False

###############################################
turns = [1, -1]
turn = random.choice(turns) #1 for white, #-1 for black
blackKingIndex = Cell(7,4)
whiteKingIndex = Cell(0,4)
deadPiecesQueue = []

whitePerspective = True
yLabel = ['1','2','3','4','5','6','7','8']
xLabel = ['a','b','c','d','e','f','g','h']

if (turn == -1):        #Flip Table if perspective player is black.
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
grid[0][3].piece = Queen(Cell(0,3), "q" + player[0], player, whitePerspective)
grid[0][4].piece = King(Cell(0,4), "k" + player[0], player, whitePerspective)
grid[0][5].piece = Bishop(Cell(0,5), "b2" + player[0], player, whitePerspective)
grid[0][6].piece = Knight(Cell(0,6), "n2" + player[0], player, whitePerspective)
grid[0][7].piece = Rook(Cell(0,7), "r2" + player[0], player, whitePerspective)
for i in range(8):
    grid[1][i].piece = Pawn(Cell(1,i), "p" + str(i + 1) + player[0], player, whitePerspective)

if (player == "black"):
    player = "white"
else:
    player = "black"
    whiteKingIndex = Cell(0,4)
    blackKingIndex = Cell(7,4)
grid[7][0].piece = Rook(Cell(7,0), "r1" + player[0], player, whitePerspective)
grid[7][1].piece = Knight(Cell(7,1), "n1" + player[0], player, whitePerspective)
grid[7][2].piece = Bishop(Cell(7,2), "b1" + player[0], player, whitePerspective)
grid[7][3].piece = Queen(Cell(7,3), "q" + player[0], player, whitePerspective)
grid[7][4].piece = King(Cell(7,4), "k" + player[0], player, whitePerspective)
grid[7][5].piece = Bishop(Cell(7,5), "b2" + player[0], player, whitePerspective)
grid[7][6].piece = Knight(Cell(7,6), "n2" + player[0], player, whitePerspective)
grid[7][7].piece = Rook(Cell(7,7), "r2" + player[0], player, whitePerspective)
for i in range(8):
    grid[6][i].piece = Pawn(Cell(6,i), "p" + str(i + 1) + player[0], player, whitePerspective)

turn = 1
#Show Board
showBoard()

while (not gameOver):
    #CheckState
    checkstate = checkOn()

    while checkstate == 1:
        ghostgrid = grid
        ghostDeadPiecesQueue = deadPiecesQueue

        playerInput = inputValidation()
        playerInput = legalMoveValidation(playerInput, ghostgrid)
        if translate(pair2Coord(playerInput[0] + playerInput[1]),pair2Coord(playerInput[3] + playerInput[4]), ghostgrid):
            translate(pair2Coord(playerInput[0] + playerInput[1]),pair2Coord(playerInput[3] + playerInput[4]), grid)
 

    while checkstate == 0:
        #Input Validation
        normalInput = inputValidation()



    #Legal Move Validation

    #Next turn    
    turn *= -1
        
    showBoard()

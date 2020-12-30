import random
from Pieces import *
from Square import *
from VectorX import *

#Functions
def showBoard():
    print ("|------------------------------------------------------|")
    if whitePerspective and turn == -1:
        print("|        black                                         |")
    elif (not whitePerspective and turn == 1):
        print("|        white                                         |")
    else:
        print("|                                                      |")
    print ("|------------------------------------------------------|")

    for r in range(8):
        print(' ', yLabel[7 - r],' ', end = '')
        for c in range(8):
            print('[', grid[r][c].piece.graphic,']', end = '')
        print()
    print ("     ", end = '')
    for i in range(8):
        print(' ', xLabel[i],'  ', end = '')
    print()

    print ("|------------------------------------------------------|")
    if whitePerspective and turn == 1:
        print("|       White                                          |")
    elif not whitePerspective and turn == -1:
        print("|       Black                                          |")
    else:
        print("|                                                      |")
    print ("|------------------------------------------------------|")

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
        if grid[pointA.r][pointA.c].piece.legalMove(pointB, grid):
            grid[pointA.r][pointA.c].piece.move(pointB,grid)
            return True
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

whitePerspective = True
yLabel = ['1','2','3','4','5','6','7','8']
xLabel = ['a','b','c','d','e','f','g','h']

whiteActiveThreatSquares = [[0]*8]*8
blackActiveThreatSquares = [[0]*8]*8
whitePassiveThreatSquares = [[0]*8]*8
blackPassiveThreatSquares = [[0]*8]*8

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
            tempRow.append(Square(Cell(yLabel[r], xLabel[c]),Empty(Cell(yLabel[r], xLabel[c]), 0, "none", whitePerspective), False))
    grid.append(tempRow)
#Fill Board with pieces
player = "black"
if (turn == -1):
    player = "white"
grid[0][0].piece = Rook(Cell(0,0), 1, player, whitePerspective)
grid[0][1].piece = Knight(Cell(0,1), 2, player, whitePerspective)
grid[0][2].piece = Bishop(Cell(0,2), 3, player, whitePerspective)
grid[0][3].piece = Queen(Cell(0,3), 4, player, whitePerspective)
grid[0][4].piece = King(Cell(0,4), 5, player, whitePerspective)
grid[0][5].piece = Bishop(Cell(0,5), 6, player, whitePerspective)
grid[0][6].piece = Knight(Cell(0,6), 7, player, whitePerspective)
grid[0][7].piece = Rook(Cell(0,7), 8, player, whitePerspective)
for i in range(8):
    grid[1][i].piece = Pawn(Cell(1,i), 9 + i, player, whitePerspective)

if (player == "black"):
    player = "white"
else:
    player = "black"
grid[7][0].piece = Rook(Cell(7,0), 20, player, whitePerspective)
grid[7][1].piece = Knight(Cell(7,1), 21, player, whitePerspective)
grid[7][2].piece = Bishop(Cell(7,2), 22, player, whitePerspective)
grid[7][3].piece = Queen(Cell(7,3), 23, player, whitePerspective)
grid[7][4].piece = King(Cell(7,4), 24, player, whitePerspective)
grid[7][5].piece = Bishop(Cell(7,5), 25, player, whitePerspective)
grid[7][6].piece = Knight(Cell(7,6), 26, player, whitePerspective)
grid[7][7].piece = Rook(Cell(7,7), 27, player, whitePerspective)
for i in range(8):
    grid[6][i].piece = Pawn(Cell(6,i), 28 + i, player, whitePerspective)

turn = 1
#Show Board
showBoard()

while (not gameOver):

    #Input Validation
    playerInput = "none"
    if (turn == 1):
        playerInput = input(whiteInputPrompt)
    else:
        playerInput = input(blackInputPrompt)
    playerInput = isCmdValid(playerInput)

    while (playerInput == "invalid"):
        if (turn == 1):
            playerInput = input(whiteInputPrompt)
        else:
            playerInput = input(blackInputPrompt)
        playerInput = isCmdValid(playerInput)

    #Legal Move Validation
    legal = translate(pair2Coord(playerInput[0] + playerInput[1]),pair2Coord(playerInput[3] + playerInput[4]), grid)
    while (not legal):
        if (turn == 1):
            playerInput = input(whiteInputPrompt)
        else:
            playerInput = input(blackInputPrompt)

        playerInput = isCmdValid(playerInput)
        while (playerInput == "invalid"):
            if (turn == 1):
                playerInput = input(whiteInputPrompt)
            else:
                playerInput = input(blackInputPrompt)

        legal = translate(pair2Coord(playerInput[0] + playerInput[1]),pair2Coord(playerInput[3] + playerInput[4]), grid)

    #Next turn    
    turn *= -1
        
    showBoard()



    

    




import random
from Pieces import *
from Square import *
from VectorX import *

#Functions
def showBoard():
    for r in range(8):
        print(' ', yLabel[7 - r],' ', end = '')
        for c in range(8):
            print('[', grid[r][c].piece.graphic,']', end = '')
        print()
    print ("     ", end = '')
    for i in range(8):
        print(' ', xLabel[i],' ', end = '')
    print()

def notation2Coord(codeString):        #Converts cmd to Coord in the grid. 
    r = -1
    c = -1

    for i in range(len(xLabel)):
        if (xLabel[i] == codeString[0]):
            c = i
    if (whitePerspective):
        r = 8 - codeString[1]
    else:
        r = codeString[1] - 1

    return Cell(r,c)

def translate(pointA, pointB):   #(Cell, Cell, )

    grid[pointB.r][pointB.c].piece.die()
    grid[pointB.r][pointB.c].piece = grid[pointA.r][pointA.c].piece
    grid[pointA.r][pointA.c].piece = Empty(Cell(pointA.r, pointA.c))



###############################################
turns = [1, -1]
turn = random.choice(turns) #1 for white, #-1 for black

whitePerspective = True
yLabel = [1,2,3,4,5,6,7,8]
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
            tempRow.append(Square(Cell(yLabel[r], xLabel[c]),Empty(Cell(yLabel[r], xLabel[c])), False))
    grid.append(tempRow)
#Fill Board with pieces
player = "black"
if (turn == -1):
    player = "white"
grid[0][0].piece = Rook(Cell(0,0), player)
grid[0][1].piece = Knight(Cell(0,1), player)
grid[0][2].piece = Bishop(Cell(0,2), player)
grid[0][3].piece = Queen(Cell(0,3), player)
grid[0][4].piece = King(Cell(0,4), player)
grid[0][5].piece = Bishop(Cell(0,5), player)
grid[0][6].piece = Knight(Cell(0,6), player)
grid[0][7].piece = Rook(Cell(0,7), player)
for i in range(8):
    grid[1][i].piece = Pawn(Cell(1,i), player)

if (player == "black"):
    player = "white"
else:
    player = "black"
grid[7][0].piece = Rook(Cell(7,0), player)
grid[7][1].piece = Knight(Cell(7,1), player)
grid[7][2].piece = Bishop(Cell(7,2), player)
grid[7][3].piece = Queen(Cell(7,3), player)
grid[7][4].piece = King(Cell(7,4), player)
grid[7][5].piece = Bishop(Cell(7,5), player)
grid[7][6].piece = Knight(Cell(7,6), player)
grid[7][7].piece = Rook(Cell(7,7), player)
for i in range(8):
    grid[6][i].piece = Pawn(Cell(6,i), player)

#Show Board
showBoard()

while (not gameOver):
    playerInput = "none"
    if (turn == 1):
        playerInput = input(whiteInputPrompt)
    else:
        playerInput = input(blackInputPrompt)

    translate(notation2Coord(playerInput[0] + playerInput[1]),notation2Coord(playerInput[3] + playerInput[4]))

    

    




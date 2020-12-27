import random
from Piece import *
from Square import *

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

def code2Coords(codeString):
    r = -1
    c = -1

    for i in range(len(xLabel)):
        if (xLabel[i] == codeString[0]):
            c = i
    if (whitePerspective):
        r = 8 - codeString[1]
    else:
        r = codeString[1] - 1

    return Vector2(r,c)

def translate(pointA, pointB):   #(Vector2, Vector2)

    grid[pointB.r][pointB.c].piece = grid[pointA.r][pointA.c].piece
    grid[pointA.r][pointA.c].piece = Empty("none")



###############################################
turns = [1, -1]
turn = random.choice(turns) #1 for white, #-1 for black

whitePerspective = True
yLabel = [1,2,3,4,5,6,7,8]
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
            tempRow.append(Square(Index(yLabel[r], xLabel[c]),Empty("none"), False))
    grid.append(tempRow)
#Fill Board with pieces
player = "black"
if (turn == -1):
    player = "white"
grid[0][0].piece = Rook(player)
grid[0][1].piece = Knight(player)
grid[0][2].piece = Bishop(player)
grid[0][3].piece = Queen(player)
grid[0][4].piece = King(player)
grid[0][5].piece = Bishop(player)
grid[0][6].piece = Knight(player)
grid[0][7].piece = Rook(player)
for i in range(8):
    grid[1][i].piece = Pawn(player)

if (player == "black"):
    player = "white"
else:
    player = "black"
grid[7][0].piece = Rook(player)
grid[7][1].piece = Knight(player)
grid[7][2].piece = Bishop(player)
grid[7][3].piece = Queen(player)
grid[7][4].piece = King(player)
grid[7][5].piece = Bishop(player)
grid[7][6].piece = Knight(player)
grid[7][7].piece = Rook(player)
for i in range(8):
    grid[6][i].piece = Pawn(player)

#Show Board
showBoard()

while (not gameOver):
    if (turn == 1):
        playerInput = input(whiteInputPrompt)
    else:
        playerInput = input(blackInputPrompt)

    




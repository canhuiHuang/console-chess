import random
from Pieces import *
from Square import *
from VectorX import *

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

# direction = directionalVector(-1,0)
# lista = grid[7][0].piece.shootRay(direction, grid)
# for var in lista:
#     print(var.id)

# lista = grid[7][0].piece.radar("threats", grid)
# print("tamano: ",len(lista))
# for var in lista:
#     print(var.id)

def f1():
    return 2

def f1():
    return 4

def f1():
    return 6

def test(a,b,c):
    return a+b+c

sofa = 1
sifa = 2
rera = 3

test(sofa,sifa,rera)
print(sofa,sifa,rera)



from Piece import Empty
from Square import Square
from Square import Index

grid = []
for r in range(8):
    tempRow = []
    for c in range(8):
        tempRow.append(Square(Index(r,c),Empty(), False))
        print(len(tempRow))
    grid.append(tempRow)

yLabel = [1,2,3,4,5,6,7,8]
xLabel = ['a','b','c','d','e','f','g','h']


print(len(grid))

for r in range(8):
    for c in range(8):
        print('[', grid[r][c].piece.graphic,']')


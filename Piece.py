from VectorX import * 

class Piece:
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        self.player = player    #ownership
        self.index = index
        self.id = id
        self.whitePerspective = whitePerspectiveBool

    def move(self, pointB, grid):
        #Move
        grid[pointB.r][pointB.c].piece =  self
        grid[pointB.r][pointB.c].piece.die()
        #Update index
        tempIndex = Cell(self.index.r, self.index.c)
        self.index = Cell(pointB.r,pointB.c)
        grid[tempIndex.r][tempIndex.c].piece = Empty(Cell(tempIndex.r, tempIndex.c), 0, "none", self.whitePerspective)

    def die(self):
        pass

class Empty(Piece):
    graphic = "  "

    def legalMove(self, pointB, grid):
        print("There is nothing to move!")
        return False

#Utilidades
def min(a,b):
    if a >= b:
        return a
    else:
        return b
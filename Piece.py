from VectorX import * 

class Piece:
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        self.player = player    #ownership
        self.index = index
        self.id = id
        self.whitePerspective = whitePerspectiveBool

    def move(self, pointB, grid):

        if (self.id[0] == "k"):
            ghost = Empty(pointB,"ghost", self.player, self.whitePerspective)
            if not ghost.amIUnderAttackedIn(grid):
                #Move
                grid[pointB.r][pointB.c].piece =  self
                grid[pointB.r][pointB.c].piece.die()
                #Update index
                tempIndex = Cell(self.index.r, self.index.c)
                self.index = Cell(pointB.r,pointB.c)
                grid[tempIndex.r][tempIndex.c].piece = Empty(Cell(tempIndex.r, tempIndex.c), "0", "none", self.whitePerspective)
                return True
            else:
                return False
        
        #Move
        grid[pointB.r][pointB.c].piece =  self
        grid[pointB.r][pointB.c].piece.die()
        #Update index
        tempIndex = Cell(self.index.r, self.index.c)
        self.index = Cell(pointB.r,pointB.c)
        grid[tempIndex.r][tempIndex.c].piece = Empty(Cell(tempIndex.r, tempIndex.c), "0", "none", self.whitePerspective)
        return True

    def amIUnderAttackedIn(self, grid):
        l = self.threatsRadar(grid)

        for i in range (len(l)):
            if (l[i].id)[0] == "0": #Empty PlaceHolder
                pass

            elif (l[i].id)[0] == "r":   #Rook
                if l[i].index.r == self.index.r or l[i].index.c == self.index.c:
                    return True

            elif (l[i].id)[0] == "b":   #Bishop
                deltaX = l[i].index.c - self.index.c
                deltaY = l[i].index.r - self.index.r
                if abs(deltaX) == abs(deltaY):
                    return True
            
            elif (l[i].id)[0] == "n":   #Knight
                deltaX = l[i].index.c - self.index.c
                deltaY = l[i].index.r - self.index.r
                if (abs(deltaY) == 2 and abs(deltaX) == 1) or (abs(deltaY) == 1 and abs(deltaX) == 2):
                    return True
    
            elif (l[i].id)[0] == "p":  #Pawn
                deltaX = l[i].index.c - self.index.c
                deltaY = l[i].index.r - self.index.r
                if (self.whitePerspective and self.player == "white") or (not self.whitePerspective and self.player == "black"):
                    if abs(deltaX) == 1 and deltaY == -1:
                        return True
                elif (self.whitePerspective and self.player == "black") or (not self.whitePerspective and self.player == "white"):
                    if abs(deltaX) == 1 and deltaY == 1:
                        return True

            elif (l[i].id)[0] == "q": #Queen
                deltaX = l[i].index.c - self.index.c
                deltaY = l[i].index.r - self.index.r
                if abs(deltaX) == abs(deltaY):  #Bishop
                    return True
                elif l[i].index.r == self.index.r or l[i].index.c == self.index.c:   #Rook
                    return True
    

    def threatsRadar(self, grid): #Returns a list of the first enemies encountered in the vulnerability line of a piece.
        l = []

        #Distances from the 4 edges of the board.
        squaresToTheBottom = 7 - self.index.r
        squaresToTheTop = 7 - squaresToTheBottom
        squaresToTheRight = 7 - self.index.c
        squaresToTheLeft =  7 - squaresToTheRight

        def linealChecks(rState, cState, distance):    #rBool -> + | cBool -> +
            trigger = True
            i = 1
            while (trigger and i <= distance):
                r = 0
                c = 0
                if rState == "+":
                    r = self.index.r + i
                elif rState == "-":
                    r = self.index.r - i
                elif rState == "0":
                    pass
                
                if cState == "+":
                    c = self.index.c + i
                elif cState == "-":
                    c = self.index.c - i
                elif cState == "0":
                    pass

                if (grid[r][c].piece.id != 0 and grid[r][c].piece.player != self.player):
                    return grid[r][c].piece
                elif (grid[r][c].piece.player == self.player):
                    trigger = False
            return Empty(Cell(-1,-1), "0", "none", True)  #PlaceHolder Piece
        def HorsePositonsCheck(topDiff,sideDiff):
            r = self.index.r + topDiff
            c = self.index.c + sideDiff
            if not (c > 7 or r >7) and grid[r][c].piece.id != 0:
                return grid[r][c].piece
            else:
                return Empty(Cell(-1,-1), "0", "none", True)  #PlaceHolder Piece

        #Lineal Checks: / / \ \   -> <- ^ v
        l.append(linealChecks("+","+",squaresToTheRight)) #+,+ #/
        l.append(linealChecks("-","-",squaresToTheLeft)) #-,- #/
        l.append(linealChecks("-","+",squaresToTheRight)) #-,+ #\
        l.append(linealChecks("+","-",squaresToTheLeft)) #+,- #\

        l.append(linealChecks("0","+",squaresToTheRight)) #0,+ #->
        l.append(linealChecks("0","-",squaresToTheLeft)) #0,- #<-
        l.append(linealChecks("-","0",squaresToTheTop)) #0,+ #^
        l.append(linealChecks("+","0",squaresToTheBottom)) #0,+ #v

        #Horse Positions Checks:
        #Top T
        l.append(HorsePositonsCheck(2,1))
        l.append(HorsePositonsCheck(2,-1))
        #Lower T
        l.append(HorsePositonsCheck(-2,1))
        l.append(HorsePositonsCheck(-2,-1))
        #Right T
        l.append(HorsePositonsCheck(-1,2))
        l.append(HorsePositonsCheck(1,2))
        #Left T
        l.append(HorsePositonsCheck(-1,-2))
        l.append(HorsePositonsCheck(1,-2))

        return l
        

    def die(self):
        pass

class Empty(Piece):
    graphic = "  "

    def moveable(self, pointB, grid):
        print("There is nothing to move!")
        return False

#Utilidades
def change(a,b):
    return b - a

def min(a,b):
    if a >= b:
        return a
    else:
        return b
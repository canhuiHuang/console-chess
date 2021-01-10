from VectorX import * 

class Piece:
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        self.player = player    #ownership
        self.index = index
        self.id = id
        self.whitePerspective = whitePerspectiveBool

    def move(self, pointB, board):
        #Move
        board.appendDeadPiece(board.grid[pointB.r][pointB.c].piece)
        board.grid[pointB.r][pointB.c].piece = self
        #Update index
        tempIndex = Cell(self.index.r, self.index.c)
        board.grid[self.index.r][self.index.c].piece.index = Cell(pointB.r,pointB.c)
        board.grid[tempIndex.r][tempIndex.c].piece = Empty(Cell(tempIndex.r, tempIndex.c), "0", "none", self.whitePerspective)
        return True
    
    def unmove(self, point, board):

        pass

    def isProtected(self, grid):
        rivalPlayer = "black"
        if self.player == "black":
            rivalPlayer = "white"
        ghostEvilSelf = Empty(Cell(self.index.r, self.index.c), "ghost", rivalPlayer, self.whitePerspective)
        if ghostEvilSelf.isUnderAttacked(grid):
            return True
        else:
            return False
    
    def isUnderAttacked(self, grid):
        l = self.radar("threats", grid)
        attackers = []

        for i in range (len(l)):
            if l[i].id[0] == "0": #Empty PlaceHolder
                pass

            elif l[i].id[0] == "r":   #Rook
                if l[i].index.r == self.index.r or l[i].index.c == self.index.c:
                    attackers.append(l[i])

            elif l[i].id[0] == "b":   #Bishop
                deltaX = l[i].index.c - self.index.c
                deltaY = l[i].index.r - self.index.r
                if abs(deltaX) == abs(deltaY):
                    attackers.append(l[i])
            
            elif l[i].id[0] == "n":   #Knight
                deltaX = l[i].index.c - self.index.c
                deltaY = l[i].index.r - self.index.r
                if (abs(deltaY) == 2 and abs(deltaX) == 1) or (abs(deltaY) == 1 and abs(deltaX) == 2):
                    attackers.append(l[i])
    
            elif l[i].id[0] == "p":  #Pawn
                deltaX = l[i].index.c - self.index.c
                deltaY = l[i].index.r - self.index.r
                if (self.whitePerspective and self.player == "white") or (not self.whitePerspective and self.player == "black"):
                    if abs(deltaX) == 1 and deltaY == -1:
                        attackers.append(l[i])
                elif (self.whitePerspective and self.player == "black") or (not self.whitePerspective and self.player == "white"):
                    if abs(deltaX) == 1 and deltaY == 1:
                        attackers.append(l[i])

            elif l[i].id[0] == "q": #Queen
                deltaX = l[i].index.c - self.index.c
                deltaY = l[i].index.r - self.index.r
                if abs(deltaX) == abs(deltaY):  #Bishop
                    attackers.append(l[i])
                elif l[i].index.r == self.index.r or l[i].index.c == self.index.c:   #Rook
                    attackers.append(l[i])

            elif l[i].id[0] == "k": #King
                deltaX = l[i].index.c - self.index.c
                deltaY = l[i].index.r - self.index.r
                if abs(deltaX) <= 1 and abs(deltaY) <= 1:
                    attackers.append(l[i])

        return attackers
    
    def radar(self, strType, grid): #Returns a list of the first enemies encountered in the vulnerability line of a piece.
        l = []

        #Distances from the 4 edges of the board.
        squaresToTheBottom = 7 - self.index.r
        squaresToTheTop = 7 - squaresToTheBottom
        squaresToTheRight = 7 - self.index.c
        squaresToTheLeft =  7 - squaresToTheRight

        def linealChecks(rState, cState, distance, strType):    #rBool -> + | cBool -> +
            trigger = True
            i = 1
            while (trigger and i <= distance):
                r = self.index.r
                c = self.index.c
                if rState == "+":
                    r += i
                elif rState == "-":
                    r -= i
                elif rState == "0":
                    pass
                
                if cState == "+":
                    c += i
                elif cState == "-":
                    c -= i
                elif cState == "0":
                    pass
                
                if strType == "threats":
                    if (grid[r][c].piece.id[0] != "0" and grid[r][c].piece.player != self.player):
                        return grid[r][c].piece
                    elif (grid[r][c].piece.player == self.player):
                        trigger = False
                elif strType == "allies" or strType == "allies+":
                    if (grid[r][c].piece.id[0] != "0" and grid[r][c].piece.player == self.player):
                        return grid[r][c].piece
                    elif (grid[r][c].piece.player != self.player):
                        trigger = False
                i += 1

            return Empty(Cell(-1,-1), "0", "none", True)  #PlaceHolder Piece

        def HorsePositonsCheck(topDiff,sideDiff, strType):
            r = self.index.r + topDiff
            c = self.index.c + sideDiff
            if not (c > 7 or r >7 or c < 0 or r < 0) and grid[r][c].piece.id[0] != 0:
                if strType == "allies+":
                    if grid[r][c].piece.player == self.player:
                        return grid[r][c].piece
                    elif grid[r][c].piece.player != self.player:
                        return Empty(Cell(-1,-1), "0", "none", True)
                elif strType == "threats":
                    if grid[r][c].piece.player != self.player:
                        return grid[r][c].piece
                    elif grid[r][c].piece.player == self.player:
                        return Empty(Cell(-1,-1), "0", "none", True)
            else:
                return Empty(Cell(-1,-1), "0", "none", True)  #PlaceHolder Piece

        #Lineal Checks: / / \ \   -> <- ^ v
        l.append(linealChecks("-","+",min(squaresToTheRight,squaresToTheTop),strType)) #-,+ #/
        l.append(linealChecks("+","-",min(squaresToTheLeft,squaresToTheBottom),strType)) #+,- #/
        l.append(linealChecks("+","+",min(squaresToTheRight,squaresToTheBottom),strType)) #-,+ #\
        l.append(linealChecks("-","-",min(squaresToTheLeft,squaresToTheTop),strType)) #+,- #\

        l.append(linealChecks("0","+",squaresToTheRight,strType)) #0,+ #->
        l.append(linealChecks("0","-",squaresToTheLeft,strType)) #0,- #<-
        l.append(linealChecks("-","0",squaresToTheTop,strType)) #0,+ #^
        l.append(linealChecks("+","0",squaresToTheBottom,strType)) #0,+ #v

        if (strType == "threats" or strType == "allies+"):
            #Horse Positions Checks:
            #Top T
            l.append(HorsePositonsCheck(2,1,strType))
            l.append(HorsePositonsCheck(2,-1,strType))
            #Lower T
            l.append(HorsePositonsCheck(-2,1,strType))
            l.append(HorsePositonsCheck(-2,-1,strType))
            #Right T
            l.append(HorsePositonsCheck(-1,2,strType))
            l.append(HorsePositonsCheck(1,2,strType))
            #Left T
            l.append(HorsePositonsCheck(-1,-2,strType))
            l.append(HorsePositonsCheck(1,-2,strType))

        return l
        
    def shootRayTo(self, pointB, grid): #Returns a list of pieces between self and pointB. Only works correctly on horizontaL, vertical, 45deg diagonals. SHOULD NOT BE USED ON HORSES AS POINTB!
        l = []
        deltaX = pointB.c - self.index.c
        deltaY = pointB.r - self.index.r
        direction = DirectionalVector(deltaY, deltaX)

        for i in range(1,max(abs(deltaX),abs(deltaY))):
            l.append(grid[self.index.r + (i * direction.r)][self.index.c + (i * direction.c)].piece)
        return l

    def shootRay(self, direction, grid):    #Shoot a ray in a direction and return an ordered list of pieces encountered
        l = []

        #calculate distance from piece to two edges:
        distanceC = 0
        distanceR = 0
        if direction.c > 0:
            distanceC = 7 - self.index.c
        elif direction.c < 0:
            distanceC = abs(0 - self.index.c)
        else:
            distanceC = 0
        
        if direction.r > 0:
            distanceR = 7 - self.index.r
        elif direction.r < 0:
            distanceR = abs(0 - self.index.r)
        else:
            distanceR = 0

        distance = max(distanceC, distanceR)
        for i in range (distance):
            l.append(grid[self.index.r + direction.r * (i + 1)][self.index.c + direction.c * (i + 1)].piece)

        return l

    def amIPinnedTo(self, pointB, board):    #Checks if a piece is pinned to move to pointB
        
        turn = 1
        if self.player == "black":
            turn = -1
        tempPointBPiece = board.grid[pointB.r][pointB.c].piece
        board.grid[pointB.r][pointB.c].piece = self
        board.grid[self.index.r][self.index.c].piece = Empty(Cell(self.index.r, self.index.c), "0", "none", self.whitePerspective)
        checkstate = board.checkStatus(turn)
        
        board.grid[pointB.r][pointB.c].piece = tempPointBPiece
        board.grid[self.index.r][self.index.c].piece = self
        if checkstate == 0:
            return False
        else:
            print("Pinned")
            return True

    def die(self,board):
        board.appendDeadPiece(self)
        self = Empty(Cell(self.index.r, self.index.c), "0", "none", self.whitePerspective)
class Empty(Piece):
    graphic = "  "
    value = 0

    def moveable(self, pointB, grid):
        print("There is nothing to move!")
        return False
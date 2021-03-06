from VectorX import * 

class Piece:
    def __init__(self, index, id, player):  #Cell, int, String, bool
        self.player = player    #ownership
        self.index = index
        self.id = id    #ID must be unique

    def __eq__(self, piece):
        return self.id == piece.id

    def __ne__(self, piece):
        return self.id != piece.id

    def moveable(self, pointB, board):
        pass

    def move(self, pointB, board):
        #Move
        board.grid[self.index.r][self.index.c] = Empty(Cell(self.index.r, self.index.c))
        board.grid[pointB.r][pointB.c].die(board)
        board.grid[pointB.r][pointB.c] = self
        #Update index
        self.index = Cell(pointB.r,pointB.c)

    def isProtected(self, board):
        rivalPlayer = "black"
        if self.player == "black":
            rivalPlayer = "white"
        ghostEvilSelf = Empty(Cell(self.index.r, self.index.c), "ghost", rivalPlayer)
        if ghostEvilSelf.isUnderAttacked(board):
            return True
        else:
            return False
    
    def isUnderAttacked(self, board):
        l = self.radar("threats", board.grid)
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
                if (board.whitePerspective and self.player == "white") or (not board.whitePerspective and self.player == "black"):
                    if abs(deltaX) == 1 and deltaY == -1:
                        attackers.append(l[i])
                elif (board.whitePerspective and self.player == "black") or (not board.whitePerspective and self.player == "white"):
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
                    if (grid[r][c].id[0] != "0" and grid[r][c].player != self.player):
                        return grid[r][c]
                    elif (grid[r][c].player == self.player):
                        trigger = False
                elif strType == "allies" or strType == "allies+":
                    if (grid[r][c].id[0] != "0" and grid[r][c].player == self.player):
                        return grid[r][c]
                    elif (grid[r][c].player != self.player):
                        trigger = False
                i += 1

            return Empty(Cell(-1,-1))  #PlaceHolder Piece

        def HorsePositonsCheck(topDiff,sideDiff, strType):
            r = self.index.r + topDiff
            c = self.index.c + sideDiff
            if not (c > 7 or r >7 or c < 0 or r < 0) and grid[r][c].id[0] != 0:
                if strType == "allies+" or strType == "horse":
                    if grid[r][c].player == self.player:
                        return grid[r][c]
                    if grid[r][c].player != self.player and strType == "horse":
                        return grid[r][c]
                    elif grid[r][c].player != self.player:
                        return Empty(Cell(-1,-1))
                elif strType == "threats" or strType == "horse":
                    if grid[r][c].player != self.player:
                        return grid[r][c]
                    elif grid[r][c].player == self.player:
                        return Empty(Cell(-1,-1))
            else:
                return Empty(Cell(-1,-1))  #PlaceHolder Piece

        #Lineal Checks: / / \ \   -> <- ^ v
        if (strType != "horse"):
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
        
    def shootRayTo(self, pointB, board): #Returns a list of pieces between self and pointB. Only works correctly on horizontaL, vertical, 45deg diagonals. SHOULD NOT BE USED ON HORSES AS POINTB!
        l = []
        deltaX = pointB.c - self.index.c
        deltaY = pointB.r - self.index.r
        direction = DirectionalVector(deltaY, deltaX)

        for i in range(1,max(abs(deltaX),abs(deltaY))):
            l.append(board.grid[self.index.r + (i * direction.r)][self.index.c + (i * direction.c)])
        return l

    def shootRay(self, direction, board):    #Shoot a ray in a direction and return an ordered list of pieces encountered
        l = []

        for i in range (1,8):
            r = self.index.r + direction.r * (i) 
            c = self.index.c + direction.c * (i)
            if r > 7 or r < 0 or c > 7 or c < 0:
                break
            l.append(board.grid[r][c])

        return l

    def amIPinnedTo(self, pointB, board):    #Checks if a piece is pinned to move to pointB
        
        turn = 1
        if self.player == "black":
            turn = -1
        tempPointBPiece = board.grid[pointB.r][pointB.c]
        board.grid[pointB.r][pointB.c] = self
        board.grid[self.index.r][self.index.c] = Empty(Cell(self.index.r, self.index.c))
        checkstate = board.checkStatus(turn)
        
        board.grid[pointB.r][pointB.c] = tempPointBPiece
        board.grid[self.index.r][self.index.c] = self
        if checkstate == 0:
            return False
        else:
            return True

    def die(self,board):
        if self.id[0] != "0":
            if self.player == "white":
                board.piecesWAlive.remove(self)
            elif self.player == "black":
                board.piecesBAlive.remove(self)
        board.grid[self.index.r][self.index.c] = Empty(Cell(self.index.r, self.index.c))
        board.appendDeadPiece(self)

    def legalSqrsCheck(self,direction,board):  #Check if a piece has legal moves on sqrs in a direction, but it stops when an obstacle is encountered.
        l = self.shootRay(direction,board)  #Direction can be either Cell or DirectionalVector.
        for piece in l:
            if piece.id[0] == "0":
                if self.moveable(piece.index,board):
                    return True
            elif piece.id[0] != "0" and piece.player != self.player:
                if self.moveable(piece.index,board):
                    return True
            elif piece.player == self.player:
                break
            else:
                print("WTH")
        return False

class Empty(Piece):
    def __init__(self, index, id = "0", player = "none"):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player)
        self.graphic = "  "
        self.value = 0

    def moveable(self, pointB, grid):
        print("There is nothing to move!")
        return False
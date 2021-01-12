from Piece import *

class King(Piece):
    def __init__(self, index, id, player):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player)
        self.graphic = "K" + player[0]
        self.value = 9999
        self.castleable = True

    def hasLegalMoves(self, board):
        unitVector = DirectionalVector(1,1)
        for i in range(9):
            sqr = self.index + unitVector
            if (sqr.r <= 7 and sqr.r >= 0) and (sqr.c <= 7 and sqr.c >= 0):
                if self.moveable(sqr,board):
                    return True
            unitVector.rotate()
        return False

    def moveable(self, pointB, board):
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        if (abs(deltaY) == 1 and abs(deltaY) == 1) or (abs(deltaY) == 1 and abs(deltaX) == 0) or (abs(deltaY) == 0 and abs(deltaX) == 1):
            if (board.grid[pointB.r][pointB.c].player == self.player):  #Moving to occupied square by allied piece
                return False
            elif board.grid[pointB.r][pointB.c].id[0] == "0":   #Moving to empty square
                ghost = Empty(pointB,"ghost", self.player)
                if ghost.isUnderAttacked(board):
                    return False
                else:
                    return True
            elif board.grid[pointB.r][pointB.c].player != self.player and board.grid[pointB.r][pointB.c].isProtected(board): #Trying to capture opponent's piece
                return False
            else:   
                return True
        elif (board.grid[pointB.r][pointB.c].id[0] == "r" and board.grid[pointB.r][pointB.c].player == self.player) and (self.castleable and board.grid[pointB.r][pointB.c].castleable) and deltaY == 0:    #Castling
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(0, deltaX)

            if self.isUnderAttacked(board):
                return False   
            for i in range(1,3):
                ghost = Empty(Cell(self.index.r, self.index.c + i * direction.c),"ghost", self.player)
                if board.grid[self.index.r][self.index.c + i * direction.c].id[0] != "0" or ghost.isUnderAttacked(board):
                    return False
            if board.grid[pointB.r][pointB.c].isUnderAttacked(board):
                return False

            return True
        else:
            return False

    def move(self, pointB, board):
        #Castle
        if (board.grid[pointB.r][pointB.c].id[0] == "r" and board.grid[pointB.r][pointB.c].player == self.player) and (self.castleable and board.grid[pointB.r][pointB.c].castleable):
            #Castling
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(0, deltaX)

            kingTempIndex = Cell(self.index.r, self.index.c)
            RookTempIndex = Cell(pointB.r, pointB.c)
            board.grid[self.index.r][self.index.c + direction.c] = board.grid[pointB.r][pointB.c]
            board.grid[self.index.r][self.index.c + direction.c].index = Cell(self.index.r, self.index.c + direction.c)
            board.grid[pointB.r][pointB.c + direction.c * -1] = self
            self.index = Cell(pointB.r,pointB.c + direction.c * -1)

            #Delete
            board.grid[kingTempIndex.r][kingTempIndex.c] = Empty(Cell(kingTempIndex.r, kingTempIndex.c))
            board.grid[RookTempIndex.r][RookTempIndex.c] = Empty(Cell(RookTempIndex.r, RookTempIndex.c))

            self.castleable = False

        else:
            #Move
            board.grid[self.index.r][self.index.c] = Empty(Cell(self.index.r, self.index.c))
            board.grid[pointB.r][pointB.c].die(board)
            board.grid[pointB.r][pointB.c] = self
            #Update index
            self.index = Cell(pointB.r,pointB.c)

            self.castleable = False

class Rook(Piece):
    def __init__(self, index, id, player):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player)
        self.graphic = "R" + player[0]
        self.value = 5
        self.castleable = True
    
    def hasLegalMoves(self, board):
        #Check on the 4 directions of Bishop
        direction = DirectionalVector(-1,0)
        for i in range(4):
            if self.legalSqrsCheck(direction, board):
                return True
            direction.rotate()
            direction.rotate()
        return False

    def moveable(self, pointB, board):
        if not self.amIPinnedTo(pointB, board):
            if (board.grid[pointB.r][pointB.c].player == self.player):
                return False    #Fuego Amigo xD 

            deltaY = pointB.r - self.index.r
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(deltaY,deltaX)

            if (deltaY == 0 and deltaX != 0) or (deltaY != 0 and deltaX == 0):  #There is only one 0 in {rb - ra, cb - ca}
                distance = abs(deltaY + deltaX)
                for i in range(1, distance + 1):
                    curPiece = board.grid[self.index.r + (i * direction.r)][self.index.c + (i * direction.c)]
                    if curPiece.id[0] != "0" and curPiece.index != pointB:
                        return False
            else:
                return False
            return True
        else:
            return False

    def move(self, pointB, board):
        #Move
        board.grid[self.index.r][self.index.c] = Empty(Cell(self.index.r, self.index.c))
        board.grid[pointB.r][pointB.c].die(board)
        board.grid[pointB.r][pointB.c] = self
        #Update index
        self.index = Cell(pointB.r,pointB.c)

        self.castleable = False

class Bishop(Piece):
    def __init__(self, index, id, player):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player)
        self.graphic = "B" + player[0]
        self.value = 3

    def hasLegalMoves(self, board):
        #Check on the 4 directions of Bishop
        direction = DirectionalVector(-1,1)
        for i in range(4):
            if self.legalSqrsCheck(direction, board):
                return True
            direction.rotate()
            direction.rotate()
        return False

    def moveable(self, pointB, board):
        if not self.amIPinnedTo(pointB, board):
            if (board.grid[pointB.r][pointB.c].player == self.player):
                return False    #Fuego Amigo xD 

            #Deltas from A to B:
            deltaY = pointB.r - self.index.r
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(deltaY, deltaX)

            if (abs(deltaX) != abs(deltaY)):   #Not valid diagonal? slope must be 1/2.
                return False

            for i in range(1, abs(deltaX) + 1):
                curPiece = board.grid[self.index.r + (i * direction.r)][self.index.c + (i * direction.c)]
                if curPiece.id[0] != "0" and curPiece.index != pointB:
                    return False
            return True
        else:
            return False

class Knight(Piece):
    def __init__(self, index, id, player):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player)
        self.graphic = "N" + player[0]
        self.value = 3

    def hasLegalMoves(self,board):
        PiecesOnHorseRadar = self.radar(board.grid,"horse")
        for piece in PiecesOnHorseRadar:
            if self.moveable(piece.index,board):
                return True
        return False

    def moveable(self, pointB, board):
        if not self.amIPinnedTo(pointB, board):
            deltaY = pointB.r - self.index.r
            deltaX = pointB.c - self.index.c

            if (board.grid[pointB.r][pointB.c].player == self.player):
                return False    #Fuego Amigo xD 

            if (abs(deltaY) == 2 and abs(deltaX) == 1) or (abs(deltaY == 1) and abs(deltaX == 2)):  #Only if move is an L mov
                if (board.grid[pointB.r][pointB.c].id == self.id):
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

class Pawn(Piece):
    def __init__(self, index, id, player):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player)
        self.graphic = "P" + player[0]
        self.value = 1
        self.doublePushAvailable = True
        self.enPassanteable = False
    
    def hasLegalMoves(self, board):
        sqrsIndexes = []
        if board.whitePerspective and self.player == "white":
            sqrsIndexes = [self.index + Cell(-1,0),self.index + Cell(-1,1),self.index + Cell(-1,-1)]
        elif board.whitePerspective and self.player == "black":
            sqrsIndexes = [self.index + Cell(1,0),self.index + Cell(1,1),self.index + Cell(1,-1)]
        elif not board.whitePerspective and self.player == "white":
            sqrsIndexes = [self.index + Cell(1,0),self.index + Cell(1,1),self.index + Cell(1,-1)]
        elif not board.whitePerspective and self.player == "black":
            sqrsIndexes = [self.index + Cell(-1,0),self.index + Cell(-1,1),self.index + Cell(-1,-1)]

        for sqr in sqrsIndexes:
            if sqr.r <= 7 and sqr.r >= 0 and sqr.c <= 7 and sqr.c >= 0:
                if self.moveable(sqr,board):
                    return True
        return False
    
    def move(self, pointB, board):
        def promote():
            cmd = (input("Promote to piece[Queen(Q), Knight(N),Bishop(B),Rook(R)]: ")).lower()
            while cmd not in ["q","n","b","r"]:
                cmd = (input("Please type Q, N, B or R: ")).lower()
            
            #Promote
            if cmd == "q":
                board.grid[self.index.r][self.index.c] = Queen(pointB,"q"+ self.id[1] + self.player[0],self.player)
            elif cmd == "n":
                board.grid[self.index.r][self.index.c] = Knight(pointB,"n"+ self.id[1] + self.player[0],self.player)
            elif cmd == "b":
                board.grid[self.index.r][self.index.c] = Bishop(pointB,"b"+ self.id[1] + self.player[0],self.player)
            elif cmd == "r":
                board.grid[self.index.r][self.index.c] = Rook(pointB,"r"+ self.id[1] + self.player[0],self.player)
            board.appendAlivePiece(self)
                
        #En passant Boolean
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c
        if abs(deltaY) == 2:
            self.enPassanteable = True
        else:
            self.enPassanteable = False

        if board.grid[self.index.r][self.index.c + deltaX].id[0] == "p" and board.grid[self.index.r][self.index.c + deltaX].player != self.player and board.grid[self.index.r][self.index.c + deltaX].enPassanteable: 
            board.grid[self.index.r][self.index.c + deltaX].die(board)

        #Move
        board.grid[self.index.r][self.index.c] = Empty(Cell(self.index.r, self.index.c))
        board.grid[pointB.r][pointB.c].die(board)
        board.grid[pointB.r][pointB.c] = self
        #Update index
        self.index = Cell(pointB.r,pointB.c)
        self.doublePushAvailable = False

        #Promotion?
        if board.whitePerspective and self.player == "white":
            if pointB.r == 0:
                promote()
        elif not board.whitePerspective and self.player == "black":
            if pointB.r == 0:
                promote()
        elif board.whitePerspective and self.player == "black":
            if pointB.r == 7:
                promote()
        elif not board.whitePerspective and self.player == "white":
            if pointB.r == 7:
                promote()

    def moveable(self, pointB, board):
        if not self.amIPinnedTo(pointB, board):
            if (board.grid[pointB.r][pointB.c].player == self.player):
                return False    #Fuego Amigo xD 

            #Determine directional slope from A to B:
            deltaY = pointB.r - self.index.r
            deltaX = pointB.c - self.index.c

            if abs(deltaY) > 2:
                return False

            if abs(deltaY) == 0:    #No vertical translation
                return False
            if abs(deltaX) > 1:    #deltaX can't be more than 1
                return False
            elif abs(deltaX) == 1 and abs(deltaY) == 1:      #If diagonal move
                if (board.grid[pointB.r][pointB.c].player != self.player and board.grid[pointB.r][pointB.c].id[0] != "0"):
                    return True
                elif (board.grid[self.index.r][self.index.c + deltaX].id[0] == "p" and board.grid[self.index.r][self.index.c + deltaX].player != self.player):    #If opponent's pawn is Enpassanteable.
                    if board.grid[self.index.r][self.index.c + deltaX].enPassanteable:
                        return True
                    else:
                        return False

                elif (board.grid[pointB.r][pointB.c].id == "0"):
                    return False
                else:
                    return False

            if (board.grid[pointB.r][pointB.c].id != "0"):    #Not 45 degree diagonal with obstruction on destiny 
                return False

            if (board.whitePerspective):     #Makes sure pawn can't move backward
                if (self.player == "white" and deltaY >= 0):
                    return False
                elif (self.player == "black" and deltaY <= 0):
                    return False
            else:
                if (self.player == "white" and deltaY <= 0):
                    return False
                elif (self.player == "black" and deltaY >= 0):
                    return False

            distance = abs(deltaY) 
            if (distance == 2 and abs(deltaX) == 0 and board.grid[pointB.r + deltaY][pointB.c].id[0] == "0" and board.grid[pointB.r + int(deltaY/abs(deltaY))][pointB.c].id[0] == "0"):  #If doublePush, and y+1 & y+2 are empty.
                if (not self.doublePushAvailable):
                    return False
                else:
                    self.doublePushAvailable = False
                    return True
            elif (distance == 1 and board.grid[pointB.r][pointB.c].id != "0"):    #If travel distance == 1 && with obstruction
                return False
            
            #Unless a case is missing, return True here should be fine
            return True
        else:
            return False

class Queen(Bishop, Rook):
    def __init__(self, index, id, player):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player)
        self.graphic = "Q" + player[0]
        self.value = 9

    def hasLegalMoves(self,board):
        if Bishop.hasLegalMoves(self,board):
            return True
        if Rook.hasLegalMoves(self,board):
            return True
        else:
            return False   

    def moveable(self, pointB, board):
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        if (abs(deltaY) == abs(deltaX)):
            return Bishop.moveable(self, pointB, board)
        elif (abs(deltaY) == 0 and abs(deltaX) != 0) or (abs(deltaY) != 0 and abs(deltaX) == 0):
            return Rook.moveable(self, pointB, board)





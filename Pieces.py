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
            if (board.grid[pointB.r][pointB.c].piece.player == self.player):  #Moving to occupied square by allied piece
                return False
            elif board.grid[pointB.r][pointB.c].piece.id[0] == "0":   #Moving to empty square
                ghost = Empty(pointB,"ghost", self.player)
                if ghost.isUnderAttacked(board):
                    return False
                else:
                    return True
            elif board.grid[pointB.r][pointB.c].piece.player != self.player and board.grid[pointB.r][pointB.c].piece.isProtected(board): #Trying to capture opponent's piece
                return False
            else:   
                return True
        elif (board.grid[pointB.r][pointB.c].piece.id[0] == "r" and board.grid[pointB.r][pointB.c].piece.player == self.player) and (self.castleable and board.grid[pointB.r][pointB.c].piece.castleable) and deltaY == 0:    #Castling
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(0, deltaX)

            if self.isUnderAttacked(board):
                return False   
            for i in range(1,3):
                ghost = Empty(Cell(self.index.r, self.index.c + i * direction.c),"ghost", self.player)
                if board.grid[self.index.r][self.index.c + i * direction.c].piece.id[0] != "0" or ghost.isUnderAttacked(board):
                    return False
            if board.grid[pointB.r][pointB.c].piece.isUnderAttacked(board):
                return False

            return True
        else:
            return False

    def move(self, pointB, board):
        #Castle
        if (board.grid[pointB.r][pointB.c].piece.id[0] == "r" and board.grid[pointB.r][pointB.c].piece.player == self.player) and (self.castleable and board.grid[pointB.r][pointB.c].piece.castleable):
            #Castling
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(0, deltaX)

            kingTempIndex = Cell(self.index.r, self.index.c)
            RookTempIndex = Cell(pointB.r, pointB.c)
            board.grid[self.index.r][self.index.c + direction.c].piece = board.grid[pointB.r][pointB.c].piece
            board.grid[self.index.r][self.index.c + direction.c].piece.index = Cell(self.index.r, self.index.c + direction.c)
            board.grid[pointB.r][pointB.c + direction.c * -1].piece = self
            self.index = Cell(pointB.r,pointB.c + direction.c * -1)

            #Delete
            board.grid[kingTempIndex.r][kingTempIndex.c].piece = Empty(Cell(kingTempIndex.r, kingTempIndex.c))
            board.grid[RookTempIndex.r][RookTempIndex.c].piece = Empty(Cell(RookTempIndex.r, RookTempIndex.c))

            self.castleable = False

        else:
            #Move
            board.grid[self.index.r][self.index.c].piece = Empty(Cell(self.index.r, self.index.c))
            board.grid[pointB.r][pointB.c].piece.die(board)
            board.grid[pointB.r][pointB.c].piece = self
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
            if (board.grid[pointB.r][pointB.c].piece.player == self.player):
                return False    #Fuego Amigo xD 

            deltaY = pointB.r - self.index.r
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(deltaY,deltaX)

            if (deltaY == 0 and deltaX != 0) or (deltaY != 0 and deltaX == 0):  #There is only one 0 in {rb - ra, cb - ca}
                distance = abs(deltaY + deltaX)
                for i in range(1, distance + 1):
                    curPiece = board.grid[self.index.r + (i * direction.r)][self.index.c + (i * direction.c)].piece
                    if curPiece.id[0] != "0" and curPiece.index != pointB:
                        return False
            else:
                return False
            return True
        else:
            return False

    def move(self, pointB, board):
        #Move
        board.grid[self.index.r][self.index.c].piece = Empty(Cell(self.index.r, self.index.c))
        board.grid[pointB.r][pointB.c].piece.die(board)
        board.grid[pointB.r][pointB.c].piece = self
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
            if (board.grid[pointB.r][pointB.c].piece.player == self.player):
                return False    #Fuego Amigo xD 

            #Deltas from A to B:
            deltaY = pointB.r - self.index.r
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(deltaY, deltaX)

            if (abs(deltaX) != abs(deltaY)):   #Not valid diagonal? slope must be 1/2.
                return False

            for i in range(1, abs(deltaX) + 1):
                curPiece = board.grid[self.index.r + (i * direction.r)][self.index.c + (i * direction.c)].piece
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

            if (board.grid[pointB.r][pointB.c].piece.player == self.player):
                return False    #Fuego Amigo xD 

            if (abs(deltaY) == 2 and abs(deltaX) == 1) or (abs(deltaY == 1) and abs(deltaX == 2)):  #Only if move is an L mov
                if (board.grid[pointB.r][pointB.c].piece.id == self.id):
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
        def promote(board):
            cmd = (input("Promote to piece[Queen(Q), Knight(N),Bishop(B),Rook(R)]: ")).lower()
            while cmd not in ["q","n","b","r"]:
                cmd = (input("Please type Q, N, B or R: ")).lower()
            
            #Mutate
            garbagePiece = self
            if cmd == "q":
                self = Queen(self.index,"q"+ self.id[1] + self.player[0],self.player)
            elif cmd == "n":
                self = Knight(self.index,"n"+ self.id[1] + self.player[0],self.player)
            elif cmd == "b":
                self = Bishop(self.index,"b"+ self.id[1] + self.player[0],self.player)
            elif cmd == "r":
                self = Rook(self.index,"r"+ self.id[1] + self.player[0],self.player)
            del garbagePiece
                
        #En passant Boolean
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c
        if abs(deltaY) == 2:
            self.enPassanteable = True
        else:
            self.enPassanteable = False

        if board.grid[self.index.r][self.index.c + deltaX].piece.id[0] == "p" and board.grid[self.index.r][self.index.c + deltaX].piece.player != self.player and board.grid[self.index.r][self.index.c + deltaX].piece.enPassanteable: 
            board.grid[self.index.r][self.index.c + deltaX].piece.die(board)

        #Move
        board.grid[self.index.r][self.index.c].piece = Empty(Cell(self.index.r, self.index.c))
        board.grid[pointB.r][pointB.c].piece.die(board)
        board.grid[pointB.r][pointB.c].piece = self
        #Update index
        self.index = Cell(pointB.r,pointB.c)
        self.doublePushAvailable = False

        #Promotion?
        if board.whitePerspective and self.player == "white":
            if pointB.index.r == 0:
                promote(board)
        elif not board.whitePerspective and self.player == "black":
            if pointB.index.r == 0:
                promote(board)
        elif board.whitePerspective and self.player == "black":
            if pointB.index.r == 7:
                promote(board)
        elif not board.whitePerspective and self.player == "white":
            if pointB.index.r == 7:
                promote(board)

    def moveable(self, pointB, board):
        if not self.amIPinnedTo(pointB, board):
            if (board.grid[pointB.r][pointB.c].piece.player == self.player):
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
                if (board.grid[pointB.r][pointB.c].piece.player != self.player and board.grid[pointB.r][pointB.c].piece.id[0] != "0"):
                    return True
                elif (board.grid[self.index.r][self.index.c + deltaX].piece.id[0] == "p" and board.grid[self.index.r][self.index.c + deltaX].piece.player != self.player):    #If opponent's pawn is Enpassanteable.
                    if board.grid[self.index.r][self.index.c + deltaX].piece.enPassanteable:
                        return True
                    else:
                        return False

                elif (board.grid[pointB.r][pointB.c].piece.id == "0"):
                    return False
                else:
                    return False

            if (board.grid[pointB.r][pointB.c].piece.id != "0"):    #Not 45 degree diagonal with obstruction on destiny 
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
            if (distance == 2 and abs(deltaX) == 0 and board.grid[pointB.r + deltaY][pointB.c].piece.id[0] == "0" and board.grid[pointB.r + int(deltaY/abs(deltaY))][pointB.c].piece.id[0] == "0"):  #If doublePush, and y+1 & y+2 are empty.
                if (not self.doublePushAvailable):
                    return False
                else:
                    self.doublePushAvailable = False
                    return True
            elif (distance == 1 and board.grid[pointB.r][pointB.c].piece.id != "0"):    #If travel distance == 1 && with obstruction
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





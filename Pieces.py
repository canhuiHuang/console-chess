from Piece import *

class King(Piece):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "K" + player[0]
        self.value = 9999
        self.castleable = True

    def moveable(self, pointB, board):
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        if (abs(deltaY) == 1 and abs(deltaY) == 1) or (abs(deltaY) == 1 and abs(deltaX) == 0) or (abs(deltaY) == 0 and abs(deltaX) == 1):
            if (board.grid[pointB.r][pointB.c].piece.player == self.player):  #Moving to occupied square by allied piece
                print("Obstructed.")
                return False
            elif board.grid[pointB.r][pointB.c].piece.id[0] == "0":   #Moving to empty square
                ghost = Empty(pointB,"ghost", self.player, self.whitePerspective)
                if ghost.isUnderAttacked(board.grid):
                    print("Can't move there.")
                    return False
                else:
                    return True
            elif board.grid[pointB.r][pointB.c].piece.player != self.player and board.grid[pointB.r][pointB.c].piece.isProtected(board.grid): #Trying to capture opponent's piece
                print("Piece is protected.")
                return False
            else:   
                return True
        elif (board.grid[pointB.r][pointB.c].piece.id[0] == "r" and board.grid[pointB.r][pointB.c].piece.player == self.player) and (self.castleable and board.grid[pointB.r][pointB.c].piece.castleable) and deltaY == 0:    #Castling
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(0, deltaX)

            if self.isUnderAttacked(board.grid):
                return False   
            for i in range(1,3):
                ghost = Empty(Cell(self.index.r, self.index.c + i * direction.c),"ghost", self.player, self.whitePerspective)
                if board.grid[self.index.r][self.index.c + i * direction.c].piece.id[0] != "0" or ghost.isUnderAttacked(board.grid):
                    print("Can't castle.")
                    return False
            if board.grid[pointB.r][pointB.c].piece.isUnderAttacked(board.grid):
                print("Can't castle.")
                return False

            return True
        else:
            print("Can't move there.")
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
            board.grid[kingTempIndex.r][kingTempIndex.c].piece = Empty(Cell(kingTempIndex.r, kingTempIndex.c), "0", "none", self.whitePerspective)
            board.grid[RookTempIndex.r][RookTempIndex.c].piece = Empty(Cell(RookTempIndex.r, RookTempIndex.c), "0", "none", self.whitePerspective)

            self.castleable = False

        else:
            #Move
            board.appendDeadPiece(board.grid[pointB.r][pointB.c].piece)
            board.grid[pointB.r][pointB.c].piece = self
            #Update index
            tempIndex = Cell(self.index.r, self.index.c)
            self.index = Cell(pointB.r,pointB.c)
            board.grid[tempIndex.r][tempIndex.c].piece = Empty(Cell(tempIndex.r, tempIndex.c), "0", "none", self.whitePerspective)

            self.castleable = False

class Rook(Piece):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "R" + player[0]
        self.value = 5
        self.castleable = True

    def moveable(self, pointB, board):
        if not self.amIPinnedTo(pointB, board):
            if (board.grid[pointB.r][pointB.c].piece.player == self.player):
                print("Can't do that.")
                return False    #Fuego Amigo xD 

            deltaY = pointB.r - self.index.r
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(deltaY,deltaX)

            if (deltaY == 0 and deltaX != 0) or (deltaY != 0 and deltaX == 0):  #There is only one 0 in {rb - ra, cb - ca}
                distance = abs(deltaY + deltaX)
                for i in range(1, distance + 1):
                    curPiece = board.grid[self.index.r + (i * direction.r)][self.index.c + (i * direction.c)].piece
                    if curPiece.id[0] != "0" and curPiece.index != pointB:
                        print("Obstructed.")
                        return False
            else:
                print("Can't move there.")
                return False
            return True
        else:
            return False

    def move(self, pointB, board):
        #Move
        board.appendDeadPiece(board.grid[pointB.r][pointB.c].piece)
        board.grid[pointB.r][pointB.c].piece =  self
        #Update index
        tempIndex = Cell(self.index.r, self.index.c)
        self.index = Cell(pointB.r,pointB.c)
        board.grid[tempIndex.r][tempIndex.c].piece = Empty(Cell(tempIndex.r, tempIndex.c), "0", "none", self.whitePerspective)

        self.castleable = False

class Bishop(Piece):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "B" + player[0]
        self.value = 3

    def moveable(self, pointB, board):
        if not self.amIPinnedTo(pointB, board):
            if (board.grid[pointB.r][pointB.c].piece.player == self.player):
                print("Can't do that.")
                return False    #Fuego Amigo xD 

            #Deltas from A to B:
            deltaY = pointB.r - self.index.r
            deltaX = pointB.c - self.index.c
            direction = DirectionalVector(deltaY, deltaX)

            if (abs(deltaX) != abs(deltaY)):   #Not valid diagonal? slope must be 1/2.
                print ("Can't move there.")
                return False

            for i in range(1, abs(deltaX) + 1):
                curPiece = board.grid[self.index.r + (i * direction.r)][self.index.c + (i * direction.c)].piece
                if curPiece.id[0] != "0" and curPiece.index != pointB:
                    print("Obstructed.")
                    return False
            return True
        else:
            return False

class Knight(Piece):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "N" + player[0]
        self.value = 3

    def moveable(self, pointB, board):
        if not self.amIPinnedTo(pointB, board):
            deltaY = pointB.r - self.index.r
            deltaX = pointB.c - self.index.c

            if (board.grid[pointB.r][pointB.c].piece.player == self.player):
                print("Can't do that.")
                return False    #Fuego Amigo xD 

            if (abs(deltaY) == 2 and abs(deltaX) == 1) or (abs(deltaY == 1) and abs(deltaX == 2)):  #Only if move is an L mov
                if (board.grid[pointB.r][pointB.c].piece.id == self.id):
                    print("Can't move there.")
                    return False
                else:
                    return True
            else:
                print("Can't move there.")
                return False
        else:
            return False

class Pawn(Piece):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "P" + player[0]
        self.value = 1
        self.doublePushAvailable = True
        self.enPassanteable = False

    def move(self, pointB, board):
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
        board.appendDeadPiece(board.grid[pointB.r][pointB.c].piece)
        board.grid[pointB.r][pointB.c].piece =  self
        #Update index
        tempIndex = Cell(self.index.r, self.index.c)
        self.index = Cell(pointB.r,pointB.c)
        board.grid[tempIndex.r][tempIndex.c].piece = Empty(Cell(tempIndex.r, tempIndex.c), "0", "none", self.whitePerspective)
        self.doublePushAvailable = False

    def moveable(self, pointB, board):
        if not self.amIPinnedTo(pointB, board):
            if (board.grid[pointB.r][pointB.c].piece.player == self.player):
                print("aca1")
                print(board.grid[pointB.r][pointB.c].piece.player)
                print(self.player)
                print("Can't do that.")
                return False    #Fuego Amigo xD 

            #Determine directional slope from A to B:
            deltaY = pointB.r - self.index.r
            deltaX = pointB.c - self.index.c

            if abs(deltaY) > 2:
                print("Can't move there.")
                return False

            if abs(deltaY) == 0:    #No vertical translation
                print("Can't move there.")
                return False
            if abs(deltaX) > 1:    #deltaX can't be more than 1
                print("Can't move there.")
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
                    print("Can't move there.")
                    return False
                else:
                    print("Can't move there.")
                    return False

            if (board.grid[pointB.r][pointB.c].piece.id != "0"):    #Not 45 degree diagonal with obstruction on destiny 
                print("Obstructed. Can't move there.")
                return False

            if (self.whitePerspective):     #Makes sure pawn can't move backward
                if (self.player == "white" and deltaY >= 0):
                    print("Can't move there.")
                    return False
                elif (self.player == "black" and deltaY <= 0):
                    print("Can't move there.")
                    return False
            else:
                if (self.player == "white" and deltaY <= 0):
                    print("Can't move there.")
                    return False
                elif (self.player == "black" and deltaY >= 0):
                    print("Can't move there.")
                    return False

            distance = abs(deltaY) 
            if (distance == 2 and abs(deltaX) == 0 and board.grid[pointB.r + deltaY][pointB.c].piece.id[0] == "0" and board.grid[pointB.r + int(deltaY/abs(deltaY))][pointB.c].piece.id[0] == "0"):  #If doublePush, and y+1 & y+2 are empty.
                if (not self.doublePushAvailable):
                    print("Can't do that.")
                    return False
                else:
                    self.doublePushAvailable = False
                    return True
            elif (distance == 1 and board.grid[pointB.r][pointB.c].piece.id != "0"):    #If travel distance == 1 && with obstruction
                print("Obstructed. Can't move there.")
                return False
            
            #Unless a case is missing, return True here should be fine
            return True
        else:
            print("pinned")
            return False

class Queen(Bishop, Rook):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "Q" + player[0]
        self.value = 9

    def moveable(self, pointB, board):
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        if (abs(deltaY) == abs(deltaX)):
            return Bishop.moveable(self, pointB, board)
        elif (abs(deltaY) == 0 and abs(deltaX) != 0) or (abs(deltaY) != 0 and abs(deltaX) == 0):
            return Rook.moveable(self, pointB, board)





from Piece import *

class King(Piece):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "K" + player[0]
        self.castleable = True

    def moveable(self, pointB, grid):
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        if (abs(deltaY) == 1 and abs(deltaY) == 1) or (abs(deltaY) == 1 and abs(deltaX) == 0) or (abs(deltaY) == 0 and abs(deltaX) == 1):
            if (grid[pointB.r][pointB.c].piece.id == self.id):
                print("Obstructed. ", end = '')
                return False
            elif grid[pointB.r][pointB.c].piece.id != self.id and grid[pointB.r][pointB.c].piece.isProtected(grid):
                print("Piece is protected. ", end = '')
                return False
            else:   
                return True
        elif (grid[pointB.r][pointB.c].piece.id[0] == "r" and grid[pointB.r][pointB.c].piece.player == self.player) and (self.castleable and grid[pointB.r][pointB.c].piece.castleable) and deltaY == 0:
            deltaX = pointB.c - self.index.c
            direction = directionalVector(0, deltaX)
            squaresBetweenKingNRook = self.shootRay(direction, grid)
            for i in range(len(squaresBetweenKingNRook)):
                if grid[self.index.r][self.index.c + i * direction.c].piece.id[0] not in ["0", "r", "k"] or grid[self.index.r][self.index.c + i * direction.c].piece.isUnderAttacked(grid):
                    print("Can't castle. ", end = '')
                    return False
            return True
        else:
            return False
            

    def move(self, pointB, grid):
        #Castle
        if (grid[pointB.r][pointB.c].piece.id[0] == "r" and grid[pointB.r][pointB.c].piece.player == self.player) and (self.castleable and grid[pointB.r][pointB.c].piece.castleable):
            #Castling
            deltaX = self.index.c - pointB.c
            direction = directionalVector(0, deltaX)

            grid[self.index.r][self.index.c + direction.c].piece = grid[pointB.r][pointB.c].piece
            grid[self.index.r][self.index.c + direction.c].piece.index = Cell(self.index.r, self.index.c + direction.c)
            grid[pointB.r][pointB.c + direction.c * -1].piece = self
            self.index = Cell(pointB.r,pointB.c + direction.c * -1)
            return True
        else:
            ghost = Empty(pointB,"ghost", self.player, self.whitePerspective)
            if not ghost.isUnderAttacked(grid):
                #Move
                grid[pointB.r][pointB.c].piece =  self
                grid[pointB.r][pointB.c].piece.die()
                #Update index
                tempIndex = Cell(self.index.r, self.index.c)
                self.index = Cell(pointB.r,pointB.c)
                grid[tempIndex.r][tempIndex.c].piece = Empty(Cell(tempIndex.r, tempIndex.c), "0", "none", self.whitePerspective)

                self.castleable = False
                return True
            else:
                return False

class Rook(Piece):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "R" + player[0]
        self.castleable = True

    def moveable(self, pointB, grid):
        if (grid[pointB.r][pointB.c].piece.player == self.player):
            return False    #Fuego Amigo xD 

        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        if (deltaY == 0 and deltaX != 0) or (deltaY != 0 and deltaX == 0):  #There is only one 0 in {rb - ra, cb - ca}
            distance = abs(deltaY + deltaX)

            if (deltaX > 0):
                for i in range(1, distance + 1):
                    if (grid[self.index.r][self.index.c + i].piece.id != "0" and grid[self.index.r][self.index.c + i].piece.player == self.player):   #if owned piece is in a way
                        return False
                    elif (grid[self.index.r][self.index.c + i].piece.id != "0" and grid[self.index.r][self.index.c + i].piece.player != self.player and i != distance): #If opponent piece on the way and is not pointB
                        return False
                    elif (grid[self.index.r][self.index.c + i].piece.id != "0" and grid[self.index.r][self.index.c + i].piece.player != self.player and i == distance):
                        return True
                    elif (grid[self.index.r][self.index.c + i].piece.id == "0" and i == distance):
                        return True

            
            if (deltaX < 0):
                for i in range(1, distance + 1):
                    if (grid[self.index.r][self.index.c - i].piece.id != "0" and grid[self.index.r][self.index.c - i].piece.player == self.player):   #if owned piece is in a way
                        return False
                    elif (grid[self.index.r][self.index.c - i].piece.id != "0" and grid[self.index.r][self.index.c - i].piece.player != self.player and i != distance): #If opponent piece on the way and is not pointB
                        return False
                    elif (grid[self.index.r][self.index.c - i].piece.id != "0" and grid[self.index.r][self.index.c - i].piece.player != self.player and i == distance):
                        return True
                    elif (grid[self.index.r][self.index.c - i].piece.id == "0" and i == distance):
                        return True


            if (deltaY > 0):
                for i in range(1, distance + 1):
                    if (grid[self.index.r + i][self.index.c].piece.id != "0" and grid[self.index.r + i][self.index.c].piece.player == self.player):   #if owned piece is in a way
                        return False
                    elif (grid[self.index.r + i][self.index.c].piece.id != "0" and grid[self.index.r + i][self.index.c].piece.player != self.player and i != distance): #If opponent piece on the way and is not pointB
                        return False
                    elif (grid[self.index.r + i][self.index.c].piece.id != "0" and grid[self.index.r + i][self.index.c].piece.player != self.player and i == distance):
                        return True
                    elif (grid[self.index.r + i][self.index.c].piece.id == "0" and i == distance):
                        return True

            if (deltaY < 0):
                for i in range(1, distance + 1):
                    if (grid[self.index.r - i][self.index.c].piece.id != "0" and grid[self.index.r - i][self.index.c].piece.player == self.player):   #if owned piece is in a way
                        return False
                    elif (grid[self.index.r - i][self.index.c].piece.id != "0" and grid[self.index.r - i][self.index.c].piece.player != self.player and i != distance): #If opponent piece on the way and is not pointB
                        return False
                    elif (grid[self.index.r - i][self.index.c].piece.id != "0" and grid[self.index.r - i][self.index.c].piece.player != self.player and i == distance):
                        return True
                    elif (grid[self.index.r - i][self.index.c].piece.id == "0" and i == distance):
                        return True

    def move(self, pointB, grid):
        #Move
        grid[pointB.r][pointB.c].piece =  self
        grid[pointB.r][pointB.c].piece.die()
        #Update index
        tempIndex = Cell(self.index.r, self.index.c)
        self.index = Cell(pointB.r,pointB.c)
        grid[tempIndex.r][tempIndex.c].piece = Empty(Cell(tempIndex.r, tempIndex.c), "0", "none", self.whitePerspective)

        self.castleable = False
        return True

class Bishop(Piece):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "B" + player[0]   

    def moveable(self, pointB, grid):
        if (grid[pointB.r][pointB.c].piece.player == self.player):
            return False    #Fuego Amigo xD 

        #Deltas from A to B:
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        if (abs(deltaX) != abs(deltaY)):   #Not valid diagonal? slope must be 1/2.
             print ("Can't move there. ", end = '')
             return False 

        nonHypotenuseDistance = abs(deltaX) #Catetos

        if (deltaY > 0 and deltaX > 0):     #\ down
            for i in range (1, nonHypotenuseDistance + 1):
                if (grid[self.index.r + i][self.index.c + i].piece.graphic != ' ' and grid[self.index.r + i][self.index.c + i].piece.id == grid[pointB.r][pointB.c].piece.id):
                    return True
                elif (grid[self.index.r + i][self.index.c + i].piece.graphic != ' '):
                    print ("Obstructed - Can't move there. ", end = '')
                    return False    #Obstructed.

        elif (deltaY < 0 and deltaX < 0):   #\ up
            for i in range (1, nonHypotenuseDistance + 1):
                if (grid[self.index.r - i][self.index.c - i].piece.graphic != ' ' and grid[self.index.r - i][self.index.c - i].piece.id == grid[pointB.r][pointB.c].piece.id):
                    return True
                elif (grid[self.index.r - i][self.index.c - i].piece.graphic != ' '):
                    print ("Obstructed - Can't move there. ", end = '')
                    return False    #Obstructed.
        
        elif (deltaY < 0 and deltaX > 0):   #/ up
            for i in range (1, nonHypotenuseDistance + 1):
                if (grid[self.index.r - i][self.index.c + i].piece.graphic != ' ' and grid[self.index.r - i][self.index.c + i].piece.id == grid[pointB.r][pointB.c].piece.id):
                    return True
                elif (grid[self.index.r - i][self.index.c + i].piece.graphic != ' '):
                    print ("Obstructed - Can't move there. ", end = '')
                    return False    #Obstructed.
        
        elif (deltaY > 0 and deltaX < 0):   #/ down
            for i in range (1, nonHypotenuseDistance + 1):
                if (grid[self.index.r + i][self.index.c - i].piece.graphic != ' ' and grid[self.index.r + i][self.index.c - i].piece.id == grid[pointB.r][pointB.c].piece.id):
                    return True
                elif (grid[self.index.r + i][self.index.c - i].piece.graphic != ' '):
                    print ("Obstructed - Can't move there. ", end = '')
                    return False    #Obstructed.

        return True

class Knight(Piece):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "N" + player[0]

    def moveable(self, pointB, grid):
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        if (abs(deltaY) == 2 and abs(deltaX) == 1) or (abs(deltaY == 1) and abs(deltaX == 2)):  #Only if move is an L mov
            if (grid[pointB.r][pointB.c].piece.id == self.id):
                print("Can't move there")
                return False
            else:
                return True
        else:
            return False

class Pawn(Piece):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "P" + player[0]

    doublePushAvailable = True
    enPassanteable = False

    prevActiveThreatSquares = []
    prevPassiveThreatSquares = []
    
    def move(self, pointB, grid):
        #En passant Boolean
        if (self.enPassanteable):
            self.enPassanteable = False

        #Move
        grid[pointB.r][pointB.c].piece =  self
        grid[pointB.r][pointB.c].piece.die()
        #Update index
        tempIndex = Cell(self.index.r, self.index.c)
        self.index = Cell(pointB.r,pointB.c)
        grid[tempIndex.r][tempIndex.c].piece = Empty(Cell(tempIndex.r, tempIndex.c), "0", "none", self.whitePerspective)
        return True

    def moveable(self, pointB, grid):
        if (grid[pointB.r][pointB.c].piece.player == self.player):
            return False    #Fuego Amigo xD 

        #Determine directional slope from A to B:
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        if abs(deltaY > 2):
            print("Can't move there. ", end = '')
            return False

        if abs(deltaY) == 0:    #No vertical translation
            print("Can't move there. ", end = '')
            return False
        if abs(deltaX) > 1:    #deltaX can't be more than 1
            print("Can't move there. ", end = '')
            return False
        elif abs(deltaX) == 1 and abs(deltaY) == 1:      #If diagonal move
            if (grid[self.index.r][self.index.c + deltaX].piece.enPassanteable and grid[self.index.r][self.index.c + deltaX].piece.player != self.player):    #If opponent's pawn is Enpassanteable.
                grid[self.index.r][self.index.c + deltaX].piece.player.die()    #Shouldn't kill a piece in this part of the code, but w.e lol
                return True

            if (grid[pointB.r][pointB.c].piece.id == "0"):
                print("Can't move there. ", end = '')
                return False
            elif (grid[pointB.r][pointB.c].piece.player != self.player):
                return True
            else:
                print("Can't move there. ", end = '')
                return False

        if (grid[pointB.r][pointB.c].piece.id != "0"):    #Not 45 degree diagonal with obstruction on destiny 
            print("Obstructed. Can't move there. ", end = '')
            return False

        if (self.whitePerspective):     #Makes sure pawn can't move backward
            if (self.player == "white" and deltaY >= 0):
                print("Can't move there. ", end = '')
                return False
            elif (self.player == "black" and deltaY <= 0):
                print("Can't move there. ", end = '')
                return False
        else:
            if (self.player == "white" and deltaY <= 0):
                print("Can't move there. ", end = '')
                return False
            elif (self.player == "black" and deltaY >= 0):
                print("Can't move there. ", end = '')
                return False

        distance = abs(deltaY)
        if (distance == 2 and abs(deltaX) == 0 and grid[pointB.r + deltaY][pointB.c].piece.id == "0"):  #If doublePush, and y+1 & y+2 are empty.
            if (not self.doublePushAvailable):
                print("Can't do that. ", end = '')
                return False
            else:
                self.doublePushAvailable = False
                self.enPassanteable = True
                return True
        elif (distance == 1 and grid[pointB.r][pointB.c].piece.id != "0"):    #If travel distance == 1 && with obstruction
            print("Obstructed. Can't move there.", end = '')
            return False
        
        #Unless a case is missing, return True here should be fine
        return True

class Queen(Bishop, Rook):
    def __init__(self, index, id, player, whitePerspectiveBool):  #Cell, int, String, bool
        Piece.__init__(self, index, id, player, whitePerspectiveBool)
        self.graphic = "Q" + player[0]

    def moveable(self, pointB, grid):
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        if (abs(deltaY) == abs(deltaX)):
            return Bishop.moveable(self, pointB, grid)
        elif (abs(deltaY) == 0 and abs(deltaX) != 0) or (abs(deltaY) != 0 and abs(deltaX) == 0):
            return Rook.moveable(self, pointB, grid)





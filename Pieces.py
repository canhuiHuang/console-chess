from Piece import *
from VectorX import * 
    
class Empty(Piece):
    graphic = ' '

class King(Piece):
    graphic = "K"

class Queen(Piece):
    graphic = "Q"

class Rook(Piece):
    graphic = "R"

class Bishop(Piece):
    graphic = "B"
    prevActiveThreatSquares = []
    prevPassiveThreatSquares = []

    def createMonoDirectionalThreatLine(self, y, x, guardEncountered, activethreatSquares, passivethreatSquares, grid, prevActiveThreatSquares, prevPassiveThreatSquares):
        if (grid[y][x].piece.graphic == ' ' and not guardEncountered):
            activethreatSquares[y][x] += 1
            prevActiveThreatSquares.append(Cell(y,x))
            return False
        elif (not guardEncountered):
            activethreatSquares[y][x] += 1
            prevActiveThreatSquares.append(Cell(y,x))
            return True
        elif (guardEncountered):
            passivethreatSquares[y][x] += 1
            prevPassiveThreatSquares.append(Cell(y,x))
            return guardEncountered

    def shootThreatLine(self, activethreatSquares, passivethreatSquares, grid, prevActiveThreatSquares, prevPassiveThreatSquares):   #Creates or Updates Threat Line
        #Example: pYpX is the distance from index to an end of the board with the Slope(positive Y,Positive X) . The slope on this one is: m = 1/2.
        pYpX = 8 - self.index.c
        nYpX = 8 - self.index.r
        nYnX = 8 - pYpX
        pYnX = 8 - nYpX

        #/
        guardEncountered = False
        for i in range(1, pYpX):
            y = self.index.r + i
            x = self.index.c + i
            guardEncountered = self.createMonoDirectionalThreatLine(y,x, guardEncountered, activethreatSquares, passivethreatSquares, grid, prevPassiveThreatSquares, prevPassiveThreatSquares)
        guardEncountered = False
        for i in range(1, nYnX):
            y = self.index.r - i
            x = self.index.c - i
            guardEncountered = self.createMonoDirectionalThreatLine(y,x, guardEncountered, activethreatSquares, passivethreatSquares, grid, prevPassiveThreatSquares, prevPassiveThreatSquares)

        #\
        guardEncountered = False
        for i in range(1, nYpX):
            y = self.index.r - i
            x = self.index.c + i
            guardEncountered = self.createMonoDirectionalThreatLine(y,x, guardEncountered, activethreatSquares, passivethreatSquares, grid, prevPassiveThreatSquares, prevPassiveThreatSquares)
        guardEncountered = False
        for i in range(1, pYnX):
            y = self.index.r + i
            x = self.index.c - i
            guardEncountered = self.createMonoDirectionalThreatLine(y,x, guardEncountered, activethreatSquares, passivethreatSquares, grid, prevPassiveThreatSquares, prevPassiveThreatSquares)
    
    def unthreat(self, activethreatSquares,passivethreatSquares, grid, prevActiveThreatSquares, prevPassiveThreatSquares):
        for i in range(len(prevActiveThreatSquares)):
            activethreatSquares[prevActiveThreatSquares[i].r][prevActiveThreatSquares[i].c] -= 1
        
        for i in range(len(prevPassiveThreatSquares)):
            passivethreatSquares[prevPassiveThreatSquares[i].r][prevPassiveThreatSquares[i].c] -= 1
                    
        prevActiveThreatSquares.clear()
        prevPassiveThreatSquares.clear()


    def legalMove(self, pointB, grid):
        if (grid[pointB.r][pointB.c].piece.player == self.player):
            return False    #Fuego Amigo xD 

        #Determine directional slope from A to B:
        deltaY = pointB.r - self.index.r
        deltaX = pointB.c - self.index.c

        distance = min(abs(deltaY), abs(deltaX))

        if (deltaY > 0 and deltaX > 0):
            for i in range (1, distance + 1):
                if (grid[self.index.r + i][self.index.c + i].piece.graphic != ' ' and grid[self.index.r + i][self.index.c + i].piece.id == grid[pointB.r][pointB.c].piece.id):
                    return True
                elif (grid[self.index.r + i][self.index.c + i].piece.graphic != ' '):
                    print ("Obstructed ", end = '')
                    return False    #Obstructed.

        elif (deltaY < 0 and deltaX < 0):
            for i in range (1, distance + 1):
                if (grid[self.index.r - i][self.index.c - i].piece.graphic != ' ' and grid[self.index.r - i][self.index.c - i].piece.id == grid[pointB.r][pointB.c].piece.id):
                    return True
                elif (grid[self.index.r - i][self.index.c - i].piece.graphic != ' '):
                    print ("Obstructed ", end = '')
                    return False    #Obstructed.
        
        elif (deltaY < 0 and deltaX > 0):
            for i in range (1, distance + 1):
                if (grid[self.index.r - i][self.index.c + i].piece.graphic != ' ' and grid[self.index.r - i][self.index.c + i].piece.id == grid[pointB.r][pointB.c].piece.id):
                    return True
                elif (grid[self.index.r - i][self.index.c + i].piece.graphic != ' '):
                    print ("Obstructed ", end = '')
                    return False    #Obstructed.
        
        elif (deltaY > 0 and deltaX < 0):
            for i in range (1, distance + 1):
                if (grid[self.index.r + i][self.index.c - i].piece.graphic != ' ' and grid[self.index.r + i][self.index.c - i].piece.id == grid[pointB.r][pointB.c].piece.id):
                    return True
                elif (grid[self.index.r + i][self.index.c - i].piece.graphic != ' '):
                    print ("Obstructed ", end = '')
                    return False    #Obstructed.

        


class Knight(Piece):
    graphic = "N"

class Pawn(Piece):
    graphic = "P"


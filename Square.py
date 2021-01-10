from VectorX import * 
from Pieces import *

class Square:
    threatened = "False"
    def __init__(self, index, piece, active):
        self.index = index
        self.piece = piece
        self.active = active

    #Setters:
    def setPiece(self, newPiece):
        self.piece = newPiece

class Board:
    def __init__(self, turn):

        self.whitePerspective = True
        self.yLabel = ['1','2','3','4','5','6','7','8']
        self.xLabel = ['a','b','c','d','e','f','g','h']

        if (turn == -1):        #Flip Labels if perspective player is black.
            tempY = [None]*8
            for i in range(len(self.yLabel)):
                tempY[i] = self.yLabel[7 - i]
            self.yLabel = tempY

            tempX = [None]*8
            for i in range(len(self.xLabel)):
                tempX[i] = self.xLabel[7 - i]
            self.xLabel = tempX
            self.whitePerspective = False

        self.whiteKing = Empty(Cell(-1,-1), "0", "none", self.whitePerspective)
        self.blackKing = Empty(Cell(-1,-1), "0", "none", self.whitePerspective)

        #Create Empty 8x8 Board
        self.grid = []
        for r in range(8):
            tempRow = []
            for c in range(8):
                tempRow.append(Square(Cell(self.yLabel[r], self.xLabel[c]),Empty(Cell(self.yLabel[r], self.xLabel[c]), "0", "none", self.whitePerspective), False))
            self.grid.append(tempRow)
        #Fill Board with pieces
        player = "black"
        if (turn == -1):
            player = "white"
        self.grid[0][0].piece = Rook(Cell(0,0), "r1" + player[0], player, self.whitePerspective)
        self.grid[0][1].piece = Knight(Cell(0,1), "n1" + player[0], player, self.whitePerspective)
        self.grid[0][2].piece = Bishop(Cell(0,2), "b1" + player[0], player, self.whitePerspective)
        if self.whitePerspective:
            self.grid[0][3].piece = Queen(Cell(0,3), "q" + player[0], player, self.whitePerspective)
            self.grid[0][4].piece = King(Cell(0,4), "k" + player[0], player, self.whitePerspective)
            self.blackKing = self.grid[0][4].piece
        else:
            self.grid[0][3].piece = King(Cell(0,3), "k" + player[0], player, self.whitePerspective)
            self.grid[0][4].piece = Queen(Cell(0,4), "q" + player[0], player, self.whitePerspective)
            self.whiteKing = self.grid[0][3].piece
        self.grid[0][5].piece = Bishop(Cell(0,5), "b2" + player[0], player, self.whitePerspective)
        self.grid[0][6].piece = Knight(Cell(0,6), "n2" + player[0], player, self.whitePerspective)
        self.grid[0][7].piece = Rook(Cell(0,7), "r2" + player[0], player, self.whitePerspective)
        for i in range(8):
            self.grid[1][i].piece = Pawn(Cell(1,i), "p" + str(i + 1) + player[0], player, self.whitePerspective)

        if (player == "black"):
            player = "white"
        else:
            player = "black"
        self.grid[7][0].piece = Rook(Cell(7,0), "r1" + player[0], player, self.whitePerspective)
        self.grid[7][1].piece = Knight(Cell(7,1), "n1" + player[0], player, self.whitePerspective)
        self.grid[7][2].piece = Bishop(Cell(7,2), "b1" + player[0], player, self.whitePerspective)
        if self.whitePerspective:
            self.grid[7][3].piece = Queen(Cell(7,3), "q" + player[0], player, self.whitePerspective)
            self.grid[7][4].piece = King(Cell(7,4), "k" + player[0], player, self.whitePerspective)
            self.whiteKing = self.grid[7][4].piece
        else:
            self.grid[7][3].piece = King(Cell(7,3), "k" + player[0], player, self.whitePerspective)
            self.grid[7][4].piece = Queen(Cell(7,4), "q" + player[0], player, self.whitePerspective)
            self.blackKing = self.grid[7][3].piece
        self.grid[7][5].piece = Bishop(Cell(7,5), "b2" + player[0], player, self.whitePerspective)
        self.grid[7][6].piece = Knight(Cell(7,6), "n2" + player[0], player, self.whitePerspective)
        self.grid[7][7].piece = Rook(Cell(7,7), "r2" + player[0], player, self.whitePerspective)
        for i in range(8):
            self.grid[6][i].piece = Pawn(Cell(6,i), "p" + str(i + 1) + player[0], player, self.whitePerspective)


        #White records
        self.pawnBCount = 0
        self.bishopBCount = 0
        self.knightBCount = 0
        self.rookBCount = 0
        self.queenBDead = False

        self.blackDeadsQueue = []
        self.whitePoints = 0
        
        #Black records
        self.pawnWCount = 0
        self.bishopWCount = 0
        self.knightWCount = 0
        self.rookWCount = 0
        self.queenWDead = False

        self.whiteDeadsQueue = []
        self.blackPoints = 0

    def appendDeadPiece(self,piece):
        if piece.player == "white":
            self.blackPoints += piece.value
            self.whiteDeadsQueue.append(piece)
            if piece.id[0] == "0":
                pass
            elif piece.id[0] == "p":
                self.pawnWCount += 1
            elif piece.id[0] == "b":
                self.bishopWCount += 1
            elif piece.id[0] == "n":
                self.knightWCount += 1
            elif piece.id[0] == "r":
                self.rookWCount += 1
            elif piece.id[0] == "q":
                self.queenWDead = True
        else:
            self.whitePoints += piece.value
            self.blackDeadsQueue.append(piece)
            if piece.id[0] == "0":
                pass
            elif piece.id[0] == "p":
                self.pawnBCount += 1
            elif piece.id[0] == "b":
                self.bishopBCount += 1
            elif piece.id[0] == "n":
                self.knightBCount += 1
            elif piece.id[0] == "r":
                self.rookBCount += 1
            elif piece.id[0] == "q":
                self.queenBDead = True

    def getCapturedPieces(self, playerStr):
        textStr =""
        emptySpace = ""
        if playerStr == "black":
            if self.pawnWCount < 3:
                if self.pawnWCount == 2:
                    textStr += "[p][p] "
                elif self.pawnWCount == 1:
                    textStr +="[p] "
                    emptySpace += "   "
                elif self.pawnWCount == 0:
                    emptySpace += "       "
            else:
                textStr += "[p]*" + str(self.pawnWCount)
                emptySpace += "  "
            
            if self.bishopWCount == 2:
                textStr +="[B][B] "
            elif self.bishopWCount == 1:
                textStr +="[B] "
                emptySpace += "   "
            else:
                emptySpace += "       "

            if self.knightWCount == 2:
                textStr +="[N][N] "
            elif self.knightWCount == 1:
                textStr +="[N] "
                emptySpace += "   "
            else:
                emptySpace += "       "

            if self.rookWCount == 2:
                textStr +="[R][R] "
            elif self.rookWCount == 1:
                textStr +="[R] "
                emptySpace += "   "
            else:
                emptySpace += "       "

            if self.queenWDead:
                textStr += "[Q]"
            else:
                emptySpace += "   "
        else:
            if self.pawnBCount < 3:
                if self.pawnBCount == 2:
                    textStr += "[p][p]"
                elif self.pawnBCount == 1:
                    textStr +="[p] "
                    emptySpace += "   "
                elif self.pawnWCount == 0:
                    emptySpace += "       "
            else:
                textStr += "[p]*" + str(self.pawnBCount)
                emptySpace += "  "
            
            if self.bishopBCount == 2:
                textStr +="[B][B] "
            elif self.bishopBCount == 1:
                textStr +="[B] "
                emptySpace += "   "
            else:
                emptySpace += "       "

            if self.knightBCount == 2:
                textStr +="[N][N] "
            elif self.knightBCount == 1:
                textStr +="[N] "
                emptySpace += "   "
            else:
                emptySpace += "       "

            if self.rookBCount == 2:
                textStr +="[R][R] "
            elif self.rookBCount == 1:
                textStr +="[R] "
                emptySpace += "   "
            else:
                emptySpace += "       "

            if self.queenBDead:
                textStr += "[Q]"
            else:
                emptySpace += "   "

        return textStr + emptySpace

    def checkStatus(self, turn):
        king = self.whiteKing
        if turn == -1:
            king = self.blackKing
        print ("wKing: ", self.whiteKing.index.r,self.whiteKing.index.c)
        print ("bKing: ", self.blackKing.index.r,self.blackKing.index.c)
        print ("this king: ", king.index.r, king.index.c)

        attackers = king.isUnderAttacked(self.grid)
        print(king.player)
        print("attackers: ", len(attackers))
        for var in attackers:
            print("attacker: ", var.id)

        if len(attackers) > 0:
            if len(attackers) == 1: #Single Attack
                
                print(1)
                attacker = attackers[0]
                #Can attacker be captured?
                defenders = attacker.isUnderAttacked(self.grid)
                print("defenders: ", len(defenders))
                for defender in defenders:
                    if defender.id[0] == "k":
                        if king.moveable(attacker.index, self):
                            print("king moveable")
                            return 1
                    elif not defender.amIPinnedTo(attacker.index, self):
                        print("a defender is not pinned")
                        return 1
                print(2)
                
                #The reason amIPinned can be used is because the defender is attacking the Attacker, which means that it is LEGAL to move there,
                #So, the only thing else that needs to be checked is to see whether the defender is pinned or not.

                #Can the attack be blocked?
                sqrsBetweenAttackerNKing = attacker.shootRayTo(king.index,self.grid)
                ghostSqrs = sqrsBetweenAttackerNKing
                for sqr in ghostSqrs:
                    sqr.player = attacker.player
                    possibleBlockers = sqr.isUnderAttacked(self.grid)
                    for blocker in possibleBlockers:
                        if not blocker.amIPinnedTo(sqr.index, self.grid):
                            return 1
                print(3)
                #Can King move?
                unitVector = DirectionalVector(1,1)
                for i in range(9):
                    sqr = king.index + unitVector
                    if (sqr.r <= 7 and sqr.r >= 0) and (sqr.c <= 7 and sqr.c >= 0):
                        print(sqr.r, sqr.c)
                        if king.moveable(sqr,self):
                            return 1
                    unitVector.rotate()
                print(4)
                
                return 2
            
            elif len(attackers) == 2: #Double Attack
                print(69)
                #Can King move?
                unitVector = DirectionalVector(1,1)
                for i in range(9):
                    sqr = king.index + unitVector
                    if king.moveable(sqr,self):
                        return 1
                return 2
        else:
            return 0





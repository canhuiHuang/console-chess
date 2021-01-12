from VectorX import * 
from Pieces import *

class Board:
    def __init__(self, turn):
        #Black killing records
        self.pawnBCount = 0
        self.bishopBCount = 0
        self.knightBCount = 0
        self.rookBCount = 0
        self.queenBCount = 0

        #Alive & Dead Pieces
        self.piecesBAlive = []  #Excludes King
        self.blackDeadsQueue = []
        
        #White killing records
        self.pawnWCount = 0
        self.bishopWCount = 0
        self.knightWCount = 0
        self.rookWCount = 0
        self.queenWCount = 0

        #Alive & Dead Pieces
        self.piecesWAlive = []  #Excludes King
        self.whiteDeadsQueue = []

        #Board Properties
        self.grid = []
        for r in range(8):
            tempRow = []
            for c in range(8):
                tempRow.append(Empty(Cell(r,c)))
            self.grid.append(tempRow)

        self.whitePerspective = True
        self.yLabel = ['1','2','3','4','5','6','7','8']
        self.xLabel = ['a','b','c','d','e','f','g','h']
        self.whiteKing = Empty(Cell(-1,-1))
        self.blackKing = Empty(Cell(-1,-1))

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

        #Fill Board with pieces
        player = "black"
        if (not self.whitePerspective):
            player = "white"
        self.grid[0][0] = Rook(Cell(0,0), "r1" + player[0], player)
        self.grid[0][1] = Knight(Cell(0,1), "n1" + player[0], player)
        self.grid[0][2] = Bishop(Cell(0,2), "b1" + player[0], player)
        if self.whitePerspective:
            self.grid[0][3] = Queen(Cell(0,3), "q" + player[0], player)
            self.grid[0][4] = King(Cell(0,4), "k" + player[0], player)
            self.blackKing = self.grid[0][4]
        else:
            self.grid[0][3] = King(Cell(0,3), "k" + player[0], player)
            self.grid[0][4] = Queen(Cell(0,4), "q" + player[0], player)
            self.whiteKing = self.grid[0][3]
        self.grid[0][5] = Bishop(Cell(0,5), "b2" + player[0], player)
        self.grid[0][6] = Knight(Cell(0,6), "n2" + player[0], player)
        self.grid[0][7] = Rook(Cell(0,7), "r2" + player[0], player)
        for i in range(8):
            self.grid[1][i] = Pawn(Cell(1,i), "p" + str(i + 1) + player[0], player)
        for r in range(2):
            for c in range(8):
                self.appendAlivePiece(self.grid[r][c])

        if (player == "black"):
            player = "white"
        else:
            player = "black"
        self.grid[7][0] = Rook(Cell(7,0), "r1" + player[0], player)
        self.grid[7][1] = Knight(Cell(7,1), "n1" + player[0], player)
        self.grid[7][2] = Bishop(Cell(7,2), "b1" + player[0], player)
        if self.whitePerspective:
            self.grid[7][3] = Queen(Cell(7,3), "q" + player[0], player)
            self.grid[7][4] = King(Cell(7,4), "k" + player[0], player)
            self.whiteKing = self.grid[7][4]
        else:
            self.grid[7][3] = King(Cell(7,3), "k" + player[0], player)
            self.grid[7][4] = Queen(Cell(7,4), "q" + player[0], player)
            self.blackKing = self.grid[7][3]
        self.grid[7][5] = Bishop(Cell(7,5), "b2" + player[0], player)
        self.grid[7][6] = Knight(Cell(7,6), "n2" + player[0], player)
        self.grid[7][7] = Rook(Cell(7,7), "r2" + player[0], player)
        for i in range(8):
            self.grid[6][i] = Pawn(Cell(6,i), "p" + str(i + 1) + player[0], player)
        for r in range(2):
            for c in range(8):
                self.appendAlivePiece(self.grid[7 - r][c])
        
        for r in range(2,6):
            for c in range(8):
                self.grid[r][c] = Empty(Cell(r,c))

    def showBoard(self,turn):
        print ("|‾‾‾‾‾‾‾||‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|")
        if self.whitePerspective and turn == -1:
            print("| black ||", self.getCapturedPieces("black"),"|")
        elif self.whitePerspective and turn == 1:
            print("|       ||", self.getCapturedPieces("black"),"|")
        elif (not self.whitePerspective and turn == 1):
            print("| white ||", self.getCapturedPieces("white"),"|")
        elif not self.whitePerspective and turn == -1:
            print("|       ||", self.getCapturedPieces("white"),"|")
        else:
            print("|                                             |")
        print ("|_______||____________________________________|")

        print ("  ", end = '')
        for i in range(8):
            print(" ", self.xLabel[i], " ", end = '')
        print()
        for r in range(8):
            print("  |‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|‾‾‾‾|")
            print(self.yLabel[7 - r], "| ", end = '')
            for c in range(8):
                print(self.grid[r][c].graphic,"| ", end = '')
            if r == 0:
                if self.whitePerspective:
                    print(self.getscoreDiff("black"))
                else:
                    print(self.getscoreDiff("white"))
            elif r == 7:
                if self.whitePerspective:
                    print(self.getscoreDiff("white"))
                else:
                    print(self.getscoreDiff("black"))
            else:
                print()
        print("   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ")
        print ("  ", end = '')
        for i in range(8):
            print(" ", self.xLabel[i], " ", end = '')
        print()

        print ("|‾‾‾‾‾‾‾||‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|")
        if self.whitePerspective and turn == 1:
            print("| white ||",self.getCapturedPieces("white"),"|")
        elif self.whitePerspective and turn == -1:
            print("|       ||",self.getCapturedPieces("white"),"|")
        elif not self.whitePerspective and turn == -1:
            print("| black ||",self.getCapturedPieces("black"),"|")
        elif not self.whitePerspective and turn == 1:
            print("|       ||",self.getCapturedPieces("black"),"|")
        else:
            print("|                                             |")
        print ("|_______||____________________________________|")

    def appendDeadPiece(self,piece):
        if piece.id[0] == "0":
            del piece
        elif piece.player == "white":
            self.whiteDeadsQueue.append(piece)
            if piece.id[0] == "p":
                self.pawnWCount += 1
            elif piece.id[0] == "b":
                self.bishopWCount += 1
            elif piece.id[0] == "n":
                self.knightWCount += 1
            elif piece.id[0] == "r":
                self.rookWCount += 1
            elif piece.id[0] == "q":
                self.queenWCount += 1
        else:
            self.blackDeadsQueue.append(piece)
            if piece.id[0] == "p":
                self.pawnBCount += 1
            elif piece.id[0] == "b":
                self.bishopBCount += 1
            elif piece.id[0] == "n":
                self.knightBCount += 1
            elif piece.id[0] == "r":
                self.rookBCount += 1
            elif piece.id[0] == "q":
                self.queenBCount += 1

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

            if self.queenWCount == 2:
                textStr += "[Q][Q]"
            elif self.queenWCount == 1:
                textStr +="[Q]"
                emptySpace += "  "
            else:
                emptySpace += "      "
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

            if self.queenBCount == 2:
                textStr += "[Q][Q]"
            elif self.queenBCount == 1:
                textStr +="[Q]"
                emptySpace += "  "
            else:
                emptySpace += "      "

        return textStr + emptySpace

    def checkStatus(self, turn):
        king = self.whiteKing
        if turn == -1:
            king = self.blackKing

        attackers = king.isUnderAttacked(self)
        if len(attackers) > 0:
            if len(attackers) == 1: #Single Attack
                
                attacker = attackers[0]
                #Can attacker be captured?
                defenders = attacker.isUnderAttacked(self)
                for defender in defenders:
                    if defender.id[0] == "k":
                        if king.moveable(attacker.index, self):
                            return 1
                    elif not defender.amIPinnedTo(attacker.index, self):
                        return 1
                
                #The reason amIPinned can be used is because the defender is attacking the Attacker, which means that it is LEGAL to move there,
                #So, the only thing else that needs to be checked is to see whether the defender is pinned or not.

                #Can the attack be blocked?
                sqrsBetweenAttackerNKing = attacker.shootRayTo(king.index,self)
                ghostSqrs = sqrsBetweenAttackerNKing
                for sqr in ghostSqrs:
                    sqr.player = attacker.player
                    possibleBlockers = sqr.isUnderAttacked(self)
                    for blocker in possibleBlockers:
                        if not blocker.amIPinnedTo(sqr.index, self):
                            return 1
                #Can King move?
                unitVector = DirectionalVector(1,1)
                for i in range(9):
                    sqr = king.index + unitVector
                    if (sqr.r <= 7 and sqr.r >= 0) and (sqr.c <= 7 and sqr.c >= 0):
                        if king.moveable(sqr,self):
                            return 1
                    unitVector.rotate()
                
                return 2
            
            elif len(attackers) == 2: #Double Attack
                #Can King move?
                unitVector = DirectionalVector(1,1)
                for i in range(9):
                    sqr = king.index + unitVector
                    if king.moveable(sqr,self):
                        return 1
                return 2
        else:
            return 0
    
    def appendAlivePiece(self, piece):
        if piece.player == "white":
            self.piecesWAlive.append(piece)
        elif piece.player == "black":
            self.piecesBAlive.append(piece)
    
    def removeAlivePiece(self, piece):
        if piece.player == "white":
            self.piecesWAlive.remove(piece)
            del piece
        elif piece.player == "black":
            self.piecesBAlive.remove(piece)
            del piece

    def getscoreDiff(self, playerStr):
        
        whiteScore = 0
        blackScore = 0
        scoreString = ""
        for piece in self.piecesWAlive:
            whiteScore += piece.value
        for piece in self.piecesBAlive:
            blackScore += piece.value

        if whiteScore - blackScore == 0:
            return scoreString

        if playerStr == "black":
            diff = blackScore - whiteScore
            if diff > 0:
                scoreString += "+"
            scoreString += str(diff)
        else:
            diff = whiteScore - blackScore
            if diff > 0:
                scoreString += "+"
            scoreString += str(diff)
        return scoreString



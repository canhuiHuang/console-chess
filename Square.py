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
    def __init__(self, grid, name, whiteKingIndex, blackKingIndex):
        self.grid = grid
        self.name = name

        #White records
        self.whiteKingIndex = whiteKingIndex
        self.pawnBCount = 0
        self.bishopBCount = 0
        self.knightBCount = 0
        self.rookBCount = 0
        self.queenBDead = False

        self.blackDeadsQueue = []
        self.whitePoints = 0
        
        #Black records
        self.blackKingIndex = blackKingIndex
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
                if self.bishopWCount == 2:
                    textStr += "[p][p]"
                elif self.pawnWCount == 1:
                    textStr +="[p] "
                    emptySpace += "   "
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
                if self.bishopBCount == 2:
                    textStr += "[p][p]"
                elif self.pawnBCount == 1:
                    textStr +="[p] "
                    emptySpace += "   "
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






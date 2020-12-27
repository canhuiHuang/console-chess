class Piece:
    def imprimirDelPiece(self):
        print ("Impreso desde Piece Base")

class PieceRey(Piece):
    def imprimirDelPiece(self):
        print ("Impreso desde pieceRey")

class Empty(Piece):
    graphic = " "
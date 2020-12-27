class Piece:
    def __init__(self, player):
        self.player = player    #ownership
    
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

class Knight(Piece):
    graphic = "N"

class Pawn(Piece):
    graphic = "P"


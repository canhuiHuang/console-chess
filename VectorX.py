class Cell:  #Vector2 in Row,Column format
    def __init__(self, r, c):
        self.r = r
        self.c = c

class threatenedPiece:      #Vector2 in Object,ID format
    def __init__(self, piece, order):
        self.piece = piece
        self.order = order
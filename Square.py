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
    def __init__(self, grid, name, piece):
        self.grid = grid
        self.name = name
        self.deadQueue = []
        self.deadQueue.append(piece)


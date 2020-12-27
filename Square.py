class Index:
    def __init__(self, r, c):
        self.row = r
        self.column = c


class Square:
    def __init__(self, index, piece, active):
        self.index = index
        self.piece = piece
        self.active = active
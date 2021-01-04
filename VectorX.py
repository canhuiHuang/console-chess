class Cell:  #Vector2 in Row,Column format
    def __init__(self, r, c):
        self.r = r
        self.c = c

class threatenedPiece:      #Vector2 in Object,ID format
    def __init__(self, piece, order):
        self.piece = piece
        self.order = order

class directionalVector:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.validLine = True

        if (abs(r) == abs(c)):
            self.r = r/abs(r)
            self.c = c/abs(c)
        elif r == 0 and c != 0:
            self.c = 1
        elif c == 0 and r != 0:
            self.r = 1
        else:
            self.validLine = False

    def reverse(self):
        return directionalVector(-1*self.r, -1*self.c)

#Utilidades
def change(a,b):
    return b - a

def min(a,b):
    if a <= b:
        return a
    else:
        return b

def max(a,b):
    if a >= b:
        return a
    else:
        return b
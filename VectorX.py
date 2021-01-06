class Cell:  #Vector2 in Row,Column format
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def __eq__(self,cell2):
        return self.r == cell2.r and self.c == cell2.c

    def __ne__(self, cell2):
        return self.r != cell2.r or self.c != cell2.c

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
            self.r = int(r/abs(r))
            self.c = int(c/abs(c))
        elif r == 0 and c != 0:
            self.c = int(c/abs(c))
        elif c == 0 and r != 0:
            self.r = int(r/abs(r))
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
class Cell:  #Vector2 in Row,Column format
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def set(self, r,c):
        self.r = r
        self.c = c

    def __eq__(self,cell2):
        return self.r == cell2.r and self.c == cell2.c

    def __ne__(self, cell2):
        return self.r != cell2.r or self.c != cell2.c

    def __add__(self,rcVector):
        return Cell(self.r + rcVector.r, self.c + rcVector.c)

class DirectionalVector:
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

    def rotate(self):   #clockwise
        i = 1
        if self.r == 0:
            i = self.c
        elif self.r == 1:
            i = -1

        if abs(self.c + i) == abs(i) or abs(self.c + i) == 0:
            self.c += i
        elif abs(self.r + i) == abs(i) or abs(self.r + i) == 0:
            self.r += i

    def reverse(self):
        return DirectionalVector(-1*self.r, -1*self.c)

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
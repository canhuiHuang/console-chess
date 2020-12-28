class Piece:
    def __init__(self, index, player):  #Vector2, String
        self.player = player    #ownership
        self.index = index

#Utilidades
def min(a,b):
    if a >= b:
        return a
    else:
        return b
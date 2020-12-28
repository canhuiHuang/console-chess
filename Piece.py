class Piece:
    def __init__(self, index, player = "none"):  #Vector2, String
        self.player = player    #ownership
        self.index = index

    def shootThreatLine(self):
        pass

    def unthreat(self):
        pass

    def legalMove(self):
        pass

    def die(self):
        pass

#Utilidades
def min(a,b):
    if a >= b:
        return a
    else:
        return b
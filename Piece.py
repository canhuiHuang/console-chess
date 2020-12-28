class Piece:
    def __init__(self, index, id, player, whitePerspectiveBool):  #Vector2, String
        self.player = player    #ownership
        self.index = index
        self.id = id
        self.whitePerspective = whitePerspectiveBool

    def die(self):
        pass

#Utilidades
def min(a,b):
    if a >= b:
        return a
    else:
        return b
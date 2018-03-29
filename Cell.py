
class Cell:

    def __init__(self, pos, order):
        self.order = order
        self.pos = pos
        self._holding = "empty"

    def set_holding(self, what):
        self._holding = what

    def get_holding(self):
        return self._holding

    def is_empty(self):
        if(self._holding == "empty"):
            return True
        else:
            return False

class Piece:

    def __init__(self, player, obj_type='regular'):
        self.owner = player
        self.type = obj_type

    def color(self):
        #print('color to owner ' + self.owner.color_to_rgb())
        return self.owner.color_to_rgb()
from fractions import Fraction
from functools import lru_cache

class Rule:

    def __init__(self, game, method):
        self.game = game
        self.method = method

    def curr_player(self, from_cell):
        curr_player = from_cell.get_holding().owner

    def do_rule(self, from_cell, to_cell):
        return self.method(from_cell, to_cell)
        #raise ValueError("Method not implemented in abstract class Rule") 


class NoInWay(Rule):

    def __init__(self, game):
        super().__init__(game, self.no_in_way)

    def no_in_way(self, from_cell, to_cell):
        #TODO needs work on one small case

        x_diff = to_cell.pos[0] - from_cell.pos[0]
        y_diff = to_cell.pos[1] - from_cell.pos[1]

        if(not to_cell.is_empty()):
            print("Cell not Empty")
            return False

        if(x_diff  == 0 and y_diff == 0):
            print("hmmm both x_diff and y_diff is 0")
            return True
        else:
            return self.line_move(from_cell, to_cell)

        print("Passed No piece in middle rule")
        return True

    def line_move(self, from_cell, to_cell):
        moved_cells = NoInWay.line(from_cell.pos[0], from_cell.pos[1], to_cell.pos[0], to_cell.pos[1])
        for y, x in moved_cells:
            print("X:%d, Y:%d and from[0]:%d and from[1]:%d" % (x,y, from_cell.pos[0], from_cell.pos[1]))
            if(x == from_cell.pos[0] and y == from_cell.pos[1]):
                continue
            if(not self.game._cells[x][y].is_empty()):
                print("Failed middle")
                return False
        return True


    @staticmethod
    @lru_cache(maxsize=256)
    def line(x0, y0, x1, y1):
        #Bresenham line algorithm from 
        #https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#Python
        points = []
        rev = reversed
        if abs(y1 - y0) <= abs(x1 - x0):
            x0, y0, x1, y1 = y0, x0, y1, x1
            rev = lambda x: x
        if x1 < x0:
            x0, y0, x1, y1 = x1, y1, x0, y0
        leny = abs(y1 - y0)
        for i in range(leny + 1):
            points.append([*rev((round(Fraction(i, leny) * (x1 - x0)) + x0, (1 if y1 > y0 else -1) * i + y0))])
        
        return points



class ChangePiece(Rule):

    def __init__(self, game):
        super().__init__(game, self.change_piece)

    def change_piece(self, from_cell, to_cell):
        curr_player = self.curr_player(from_cell)
        list_adject = self.get_adjencts(to_cell)
        
        for ad_cell in list_adject:
            if(ad_cell.get_holding().owner != curr_player):
                if(self.cell_attacked(ad_cell, curr_player)):
                    ad_cell.owner = curr_player

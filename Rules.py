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

        print("Xdiff: %d, Ydiff: %d" % (x_diff, y_diff))

        if(not to_cell.is_empty()):
            print("Cell not Empty")
            return False

        if(x_diff  == 0 and y_diff == 0):
            print("hmmm both x_diff and y_diff is 0")
            return True

        else:
            if(x_diff == 0):
                for i in range(from_cell.pos[1], to_cell.pos[1] + round(1*abs(y_diff)/y_diff)):
                    if(not self.game._cells[from_cell.pos[0]][i].is_empty()):
                        print("Tried to move piece on top of another")
                        return False
            elif(y_diff == 0):
                for i in range(from_cell.pos[0] + round(1*abs(x_diff)/x_diff), to_cell.pos[0]):
                    if(not self.game._cells[i][from_cell.pos[1]].is_empty()):
                        print("Tried to move piece on top of another")
                        return False
            else:
                return self.diagonal_move(from_cell, to_cell)

        print("Passed No piece in middle rule")
        return True

    def diagonal_move(self, from_cell, to_cell):
        moved_cells = NoInWay.line(from_cell.pos[0], from_cell.pos[1], to_cell.pos[0], to_cell.pos[1])
        for x, y in moved_cells:
            if(not self.game._cells[x][y].is_empty()):
                print("Failed diagonal move")
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

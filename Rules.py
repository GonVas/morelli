from fractions import Fraction
from functools import lru_cache

class Rule:

    def __init__(self, game, method):
        self.game = game
        self.method = method

    def curr_player(self, from_cell):
        return from_cell.get_holding().owner

    def do_rule(self, from_cell, to_cell):
        return self.method(from_cell, to_cell)
        #raise ValueError("Method not implemented in abstract class Rule") 


class NoInWay(Rule):

    def __init__(self, game):
        super().__init__(game, self.no_in_way)

    def no_in_way(self, from_cell, to_cell):

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

    def get_adjencts(self, cell):

        X = Y = self.game.dim

        neighbors = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if (-1 < x <= X and
                                   -1 < y <= Y and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 <= X) and
                                   (0 <= y2 <= Y))]

        adjencts = []
        for x, y in neighbors(cell.pos[0], cell.pos[1]):
            adjencts.append(self.game._cells[x][y])

        return adjencts

    def orth_check(self, adj_cell, curr_player):
        print(curr_player)
        curr_cell1 = self.game._cells[adj_cell.pos[0]+1][adj_cell.pos[1]]
        curr_cell2 = self.game._cells[adj_cell.pos[0]-1][adj_cell.pos[1]]
        if(not curr_cell1.is_empty() and not curr_cell2.is_empty()):
            if(curr_cell1.get_holding().owner == curr_cell2.get_holding().owner):
                return True

        curr_cell1 = self.game._cells[adj_cell.pos[0]][adj_cell.pos[1]+1]
        curr_cell2 = self.game._cells[adj_cell.pos[0]][adj_cell.pos[1]-1]
        if(not curr_cell1.is_empty() and not curr_cell2.is_empty()):
            if(curr_cell1.get_holding().owner == curr_cell2.get_holding().owner ):
                return True

        return False


    def cell_attacked(self, cell, curr_player):
        for adj_cell in self.get_adjencts(cell):
            if( self.orth_check(cell, curr_player)): #or self.diag_check(cell, curr_player) ):
                return True
        return False
            

    def change_piece(self, from_cell, to_cell):
        curr_player = self.curr_player(to_cell)
        list_adject = self.get_adjencts(to_cell)
        
        for ad_cell in list_adject:
            #print("ad_cell X,Y: (%d, %d)" % (ad_cell.pos[0], ad_cell.pos[1]))
            if(not ad_cell.is_empty() and ad_cell.get_holding().owner != curr_player):
                if(self.cell_attacked(ad_cell, curr_player)):
                    self.game.change_player(ad_cell)

class PutKing(Rule):

    def __init__(self, game):
        super().__init__(game, self.frames)

    def frames(self, from_cell, to_cell):
        curr_player = self.curr_player(to_cell)
        order = to_cell.order

        c1 = self.game._cells[order][order]
        c2 = self.game._cells[-order-1][-order-1]
        c3 = self.game._cells[+order][-order-1]
        c4 = self.game._cells[-order-1][+order]

        if(c1.is_empty() or c2.is_empty() or c3.is_empty() or c4.is_empty()):
            return

        print('Arent empty')

        if(c1.get_holding().owner == c2.get_holding().owner 
                and c2.get_holding().owner == c3.get_holding().owner
                and c3.get_holding().owner == c4.get_holding().owner):
            print("We have frame AND KING")
            self.game.put_king(curr_player)



class Winning(Rule):

    def __init__(self, game):
        super().__init__(game, self.avaliable_moves)

    def avaliable_moves(self):
        pass


"""
    def diag_check(cell, curr_player):
        return False
        if (self.game._cells[adj_cell.pos[0]][adj_cell.pos[1]+1].get_holding().owner ==
             self.game._cells[adj_cell.pos[0]][adj_cell.pos[1]-1].get_holding().owner and self.game._cells[adj_cell.pos[0]+1][adj_cell.pos[1]+1].get_holding().owner == curr_player):
                return True
            if (self.game._cells[adj_cell.pos[0]+1][adj_cell.pos[1]].get_holding().owner ==
             self.game._cells[adj_cell.pos[0]-1][adj_cell.pos[1]].get_holding().owner and self.game._cells[adj_cell.pos[0]+1][adj_cell.pos[1]+1].get_holding().owner == curr_player):
                return True
"""
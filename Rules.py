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

        if(x_diff  == 0 and y_diff == 0):
            print("hmmm both x_diff and y_diff is 0")
            return True

        if(x_diff == y_diff):
            print("RULE : Dont know how to do diagonal thing")
            return True
        else:
            if(y_diff > x_diff):
                for i in range(from_cell.pos[1], to_cell.pos[1] + round(1*abs(y_diff)/y_diff)):
                    if(not self.game._cells[from_cell.pos[0]][i].is_empty()):
                        print("Tried to move piece on top of another")
                        return False
            else:
                for i in range(from_cell.pos[0] + round(1*abs(x_diff)/x_diff), to_cell.pos[0]):
                    if(not self.game._cells[i][from_cell.pos[1]].is_empty()):
                        print("Tried to move piece on top of another")
                        return False

        print("Passed No piece in middle rule")
        return True

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

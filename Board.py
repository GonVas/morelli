import Rules
from Player import Player, AI
import math
import collections
import random
from functools import lru_cache
from Cell import Cell, Piece, King, PieceGhost
from copy import deepcopy, copy

class Board:

    def __init__(self, dim, option, turn_time):
        self.dim = dim
        self.turn_time = turn_time
        self.init_cells()
        self.init_players(option)
        self.init_place()
        self.add_rules()

    def init_cells(self):
        self._cells = []
        self.center = (self.dim//2, self.dim//2)
        for x in range(self.dim):
            cells = []
            for y in range(self.dim):
                order = int(Board.pnorm(
                    frozenset([abs(x-self.center[0]),abs(y-self.center[0])])))
                order = -order + self.center[0] 
                new_cell = Cell([x, y], order)
                cells.append(new_cell)
            self._cells.append(cells)

    def get_cells(self):
        return self._cells

    def get_player(self, numb):
        n = numb % 2
        return self._players[n]

    def init_place(self):
        pieces = [self.dim*2, self.dim*2]
        for i in range(self.dim):
            remove = round(random.uniform(0, 1))
            if(pieces[remove] == 0):
                remove = (remove + 1)%2

            pieces[remove] -= 1
            piece = Piece(self._players[remove])
            piece2 = Piece(self._players[(remove+1)%2])
            self._cells[i][0].set_holding(piece) 
            self._cells[i][self.dim-1].set_holding(piece2) 

        for i in range(1, self.dim):
            remove = round(random.uniform(0, 1))
            if(pieces[remove] == 0):
                remove = (remove + 1)%2

            pieces[remove] -= 1
            piece = Piece(self._players[remove])
            piece2 = Piece(self._players[(remove+1)%2])
            self._cells[0][i].set_holding(piece) 
            self._cells[self.dim-1][i].set_holding(piece2) 

        self._cells[0][0].set_holding(Piece(self._players[0]))
        self._cells[self.dim-1][self.dim-1].set_holding(Piece(self._players[1]))

        self._cells[0][self.dim-1].set_holding(Piece(self._players[1]))
        self._cells[self.dim-1][0].set_holding(Piece(self._players[0]))


    def get_center(self):
        return self._cells[self.center[0]][self.center[0]]

    def erase_ghosts(self):
        for cellx in self._cells:
            for cell in cellx:
                if(not cell.is_empty() and cell.get_holding().type == 'ghost'):
                    cell.set_empty()

    def get_order_cells(self, order, check_empty=False):
        res = []
        for cellx in self._cells:
            for cell in cellx:
                if(cell.order == order):
                    if(check_empty):
                        if(cell.is_empty()):
                            res.append(cell)
                    else:
                        res.append(cell)
        return res

    def select_cell(self, click_cell_x, click_cell_y, current_player):

        if(click_cell_x >= self.dim or click_cell_y >= self.dim):
            return

        is_buff_empty = not hasattr(self, 'sel_buf') or self.sel_buf == "empty"

        clicked_cell = self._cells[click_cell_x][click_cell_y]
        if(clicked_cell.is_empty() and is_buff_empty):
            return

        # forgive me, bad code ahead

        if is_buff_empty:
            #print('Sel buf: ' + str(clicked_cell.is_empty()))
            self.sel_buf = clicked_cell
            return
        else:
            if self.sel_buf.get_holding().owner == current_player and self.sel_buf.order < clicked_cell.order:
                #print('moving %s  to %s ' % (self.sel_buf, clicked_cell))
                self.move(self.sel_buf, clicked_cell)

        self.sel_buf = "empty"
        #print('Cliked cell %d,%d whose owner is: %s'% (click_cell_x, click_cell_y, owner) )

    def check_rules(self, from_cell, to_cell):
        for bool_rule in self.bool_rules:
            if(not bool_rule.do_rule(from_cell, to_cell)):
                #print("FAILED A RULE")
                return False
        #print("Passed all rules")
        return True

    def mod_rules(self, from_cell, to_cell):
        for mod_rule in self.modifying_rules:
            mod_rule.do_rule(from_cell, to_cell)
        #print("Done all mod rules")
        return True

    def move(self, from_cell, where_cell, destructive=True):
        if(from_cell.is_empty()):
            #print('Tried to move empty')
            return False

        #if(destructive):
            #print('WARNING destructive move')

        if(self.valid_move(from_cell,  where_cell)):
            if(destructive):
                where_cell.set_holding(from_cell.get_holding())
                from_cell.set_holding('empty')
                self.change_player()
                return self.mod_rules(from_cell, where_cell)
            else:
                new_cells = deepcopy(self)
                new_cells.move(new_cells._cells[where_cell.pos[0]][where_cell.pos[1]], new_cells._cells[from_cell.pos[0]][from_cell.pos[1]])
                return new_cells 

        return False


    def draw_ghosts(self, player, where):
        for cell in where:
            cell.set_holding(PieceGhost(player))

    def reset_test_env(self):

        for cellx in self._cells:
            for cellxy in cellx:
                cellxy.set_empty()

        self._cells[0][3].set_holding(Piece(self._players[0]))
        self._cells[1][3].set_holding(Piece(self._players[1]))
        self._cells[1][2].set_holding(Piece(self._players[0]))

    def reset_test_env2(self):

        for cellx in self._cells:
            for cellxy in cellx:
                cellxy.set_empty()

        self._cells[3][3].set_holding(Piece(self._players[0]))
        self._cells[-4][-4].set_holding(Piece(self._players[0]))
        self._cells[3][-4].set_holding(Piece(self._players[0]))

        self._cells[1][1].set_holding(Piece(self._players[0]))

    def reset_test_env3(self):

        self.reset_test_env()

    
        aval_moves = self.avaiable_moves(self._players[0])
        aval = aval_moves[self._cells[0][3]]
        
        #self.draw_ghosts(self._players[0], aval)
        
        for val in self.avaliable_moves_val(aval_moves):
            print("Val: %d", val)


    def change_player_holding(self, cell):
        if(cell.is_empty()):
            #print("Changed empty player")
            return False

        curr_owner = cell.get_holding().owner

        if(curr_owner == self._players[0]):
            cell.get_holding().owner = self._players[1]
        else:
            cell.get_holding().owner = self._players[0]

        return True

    def put_king(self, player):
        self._cells[self.center[0]][self.center[0]].set_holding(King(player))

    def check_winning(self):
        if(len(self.avaiable_moves(self._players[0])) == 0 or len(self.avaiable_moves(self._players[1])) == 0):
            if(self.get_center().is_empty()):
                return "tie"
            return self.get_center().get_holding().owner
        else:
            return None

    def add_rules(self):
        self.bool_rules = [Rules.NoInWay(self)]
        self.modifying_rules = [Rules.ChangePiece(self), Rules.PutKing(self)]
        self.winner_rules = [Rules.Winning(self)]

    def valid_move(self, from_cell, to_cell):
        if(to_cell.is_empty() and from_cell.pos != to_cell.pos):
            return self.check_rules(from_cell, to_cell)
        else:
            return False

    def avaliable_moves_val(self, aval_moves, player):
        vals = {}
        items = aval_moves

        if(isinstance(aval_moves, dict)):
           for from_cell, aval_move in aval_moves.items():
            for mov in aval_move:
                new_bd = self.move(from_cell, mov, destructive=False)
                vals[(from_cell, mov)] = Rules.board_value(new_bd)[player.color]
        else:
           for from_cell, to_cell in aval_moves:
                new_bd = self.move(from_cell, to_cell, destructive=False)
                val = Rules.board_value(new_bd)[player.color]
                #print('VALUE IS : %d ' % val)
                vals[(from_cell, to_cell)] = val
        return vals

    def init_players(self, option):
        p1 = Player('black')

        if option == 'AIvsAI':
            p1 = AI(self, 'black', turn_time=self.turn_time)

        p2 = AI(self, 'white', turn_time=self.turn_time)

        self.curr_player = 0
        self._players = [p1, p2]
        self.who_turn = 0

    def current_player(self):
        return self._players[self.curr_player]

    def other_player(self):
        return self._players[(self.curr_player + 1) % 2]

    def change_player(self):
        print('Changed player')
        self.curr_player = (self.curr_player + 1) % 2

    def get_state(self):
        state = ''
        for cell_line in self._cells:
            for cell in cell_line:
                holding = cell.get_holding()
                if(holding == 'empty'):
                    state += 'e'
                elif(holding.owner == self._players[0]):
                    if(holding.type == 'regular'):
                        state += 'w'
                    else:
                        state += 'k'
                elif(holding.owner == self._players[1]):
                    if(holding.type == 'regular'):
                        state += 'b'
                    else:
                        state += 'o'
        if(self.current_player() == self._players[0]):
            state += '0'
        else:
            state += '1'
        return state

    def set_state(self, state):
        for cell_line in range(len(self._cells)):
            for cell in range(len(self._cells)):
                hold = state[cell_line+(cell*len(self._cells))]
                if(hold == 'e'):
                    self._cells[cell][cell_line].set_empty()
                elif(hold == 'w'):
                    self._cells[cell][cell_line].set_holding(Piece(self._players[0]))
                elif(hold == 'b'):
                    self._cells[cell][cell_line].set_holding(Piece(self._players[1]))
                elif(hold == 'k'):
                    self._cells[cell][cell_line].set_holding(King(self._players[0]))
                elif(hold == 'o'):
                    self._cells[cell][cell_line].set_holding(King(self._players[1]))
        
        pl = state[-1]
        if(pl == '0'):
            self.curr_player = 0
        else:
            self.curr_player = 1


    def get_player_cells(self, player):
        res = []

        for cellx in self._cells:
            for cell in cellx:
                if(not cell.is_empty() and cell.get_holding().owner == player):
                    res.append(cell)

        return res

    def avaiable_moves(self, player, flat=False):
        can_move = self.get_player_cells(player)
        aval_moves = collections.defaultdict(list)
        for cell in can_move:
            if( cell.order < self.max_order()-1 ):
                for order_tolook in range(cell.order+1, self.max_order()):
                    empty_next_order = self.get_order_cells(order_tolook, check_empty=True)
                    for empty_cell in empty_next_order:
                        if(self.valid_move(cell, empty_cell)):
                            aval_moves[cell].append(empty_cell)
            else:
                can_move.remove(cell)
        
        if(flat == False):
            return aval_moves
        else:
            flat_list = []
            for from_cell, to_cells in aval_moves.items():
                for to_cell in to_cells:
                        flat_list.append([from_cell, to_cell])
            return flat_list

    def print(self):
        for cell_line in self._cells:
            for cell in cell_line:
                if(not cell.is_empty()):
                    print("On pos (%d,%d) have piece %s. \n" % (cell.pos[0], cell.pos[1], cell.get_holding().color_str()))


    def __eq__(self, other):
        for i in range(0, len(self._cells)):
            for j in range(0, len(self._cells[i])):
                if( self._cells[i][j].get_holding() != self._cells[i][j].get_holding() ):
                    return False

    @staticmethod
    @lru_cache(maxsize=256)
    def pnorm(vec, p=5):
        # en.wikipedia.org/wiki/Norm_(mathematics), pnorm
        # 1 - taxicab/manhattan distance
        # 2 - Euclidean distance
        # for morelli square, p must aproach infinity but carefull with OVF.
        vec_sum = 0
        for val in vec:
            vec_sum += val**p
        return (vec_sum**(1/p))

    def __hash__(self):
        return hash(repr(self))

    def max_order(self):
        return int(self.pnorm(self.center))

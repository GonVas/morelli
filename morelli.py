import pygame
import math
from time import sleep,time
from functools import lru_cache
import asyncio
import threading
import random

from Player import Player, AI
from Cell import Cell, Piece
import Rules

class Morelli:

    # defines colours
    white = (255, 255, 255)
    d_white = (250, 250, 250)
    black = (0, 0, 0)
    teal = (0, 128, 128)
    blue_black = (50, 50, 50)

    colors = [
        (255, 0, 0),
        (255, 165,0),
        (255, 255, 0),
        (128,128,0),
        (0, 255, 0),
        (0,100,0),
        (173,216,230),
        (0,0,255),
        (138,43,226),
        (75,0,130),
        (36,0,65)
    ]

    def __init__(self, dim=11, cell_size=50, bottom_bar=200, option='PvsAI', turn_time=15, testing=False):
        self.figure_dims(dim, cell_size, bottom_bar)

        self.testing = testing
        if(not testing):
            pygame.init()
            self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
            pygame.display.update()
            self.clock = pygame.time.Clock()
        
        self.init_cells()
        self.turn_time = turn_time
        self.init_players(option)
        self.init_place()
        self.add_rules()
        self.reset_test_env()

        if(testing):
            self.reset_test_env()

        self.main_loop()

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

        #print('Bag have %d whites and %d blacks'% (pieces[0], pieces[1]))

    def add_rules(self):
        self.bool_rules = [Rules.NoInWay(self)]
        self.modifying_rules = [Rules.ChangePiece(self)]

    def reset_test_env(self):

        for cellx in self._cells:
            for cellxy in cellx:
                cellxy.set_empty()

        self._cells[0][3].set_holding(Piece(self._players[0]))
        self._cells[1][3].set_holding(Piece(self._players[1]))
        self._cells[1][2].set_holding(Piece(self._players[0]))

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

    def init_players(self, option):
        p1 = Player('black', self, pygame)

        if option == 'AIvsAI':
            p1 = AI('black', self, pygame)

        p2 = AI('white', self, pygame)

        self._players = [p1, p2]
        self.who_turn = 0

    def init_cells(self):
        self._cells = []
        self.center = (self.dim//2, self.dim//2)
        for x in range(self.dim):
            cells = []
            for y in range(self.dim):
                order = int(Morelli.pnorm(
                    frozenset([abs(x-self.center[0]),abs(y-self.center[0])])))
                order = -order + self.center[0] 
                new_cell = Cell([x, y], order)
                cells.append(new_cell)
            self._cells.append(cells)

    def figure_dims(self, dim, cell_size, bottom_bar):
        if(dim < 7 or dim > 17):
            raise ValueError("Board is either too small or to big")

        if (dim%2 != 1): # Make sure dim is odd and below 11
            dim = dim + 1
        self.dim = min(dim, 11)

        self.cell_size = cell_size
        self.bottom_bar = bottom_bar

        self.display_width = dim*cell_size
        self.display_height = self.display_width + self.bottom_bar

        print("Game Board with dimension:%sx%s and size %sx%s" % (self.dim, self.dim, self.display_width, self.display_height))

    def board_draw(self):
        self.game_display.fill(Morelli.black)
        for i in range(self.dim):
            for j in range(self.dim):
                mod = self.dim//2
                cell = self._cells[i][j]
                final_pos = (cell.pos[0] * self.cell_size, cell.pos[1] * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.game_display, Morelli.colors[cell.order], final_pos)
                if(not cell.is_empty()):
                    holding_pos = (final_pos[0] + self.cell_size//4, final_pos[1] + self.cell_size//4, self.cell_size//2, self.cell_size//2)
                    pygame.draw.rect(self.game_display, cell.get_holding().color(), holding_pos)

    def sel_anim(self, click_cell_x, click_cell_y, time_dur = 5):
        beg_time = time()
        while (time() - beg_time < time_dur) :
            print('Going to draw selected')
            final_pos = (click_cell_x * self.cell_size, click_cell_y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.game_display, (0,250,0), final_pos)

    def select_cell(self, click_cell_x, click_cell_y):

        if(click_cell_x >= self.dim or click_cell_y >= self.dim):
            return

        is_buff_empty = not hasattr(self, 'sel_buf') or self.sel_buf == "empty"

        clicked_cell = self._cells[click_cell_x][click_cell_y]
        if(clicked_cell.is_empty() and is_buff_empty):
            return

        # forgive me, bad code ahead

        if is_buff_empty:
            print('Sel buf: ' + str(clicked_cell.is_empty()))
            self.sel_buf = clicked_cell
            return
        else:
            if self.sel_buf.get_holding().owner == self.current_player and self.sel_buf.order < clicked_cell.order:
                print('moving %s  to %s ' % (self.sel_buf, clicked_cell))
                self.move(self.sel_buf, clicked_cell)

        self.sel_buf = "empty"
        #print('Cliked cell %d,%d whose owner is: %s'% (click_cell_x, click_cell_y, owner) )

    def check_rules(self, from_cell, to_cell):
        for bool_rule in self.bool_rules:
            if(not bool_rule.do_rule(from_cell, to_cell)):
                print("FAILED A RULE")
                return False
        print("Passed all rules")
        return True

    def mod_rules(self, from_cell, to_cell):
        for mod_rule in self.modifying_rules:
            mod_rule.do_rule(from_cell, to_cell)
        print("Done all mod rules")
        return True

    def move(self, from_cell, where_cell):
        if(from_cell.is_empty()):
            print('Tried to move empty')
            return False
        if(self.check_rules(from_cell, where_cell)):
            where_cell.set_holding(from_cell.get_holding())
            from_cell.set_holding('empty')
            return self.mod_rules(from_cell, where_cell)

    def change_player(self, cell):
        if(cell.is_empty()):
            print("Changed empty player")
            return False

        curr_owner = cell.get_holding().owner

        if(curr_owner == self._players[0]):
            cell.get_holding().owner = self._players[1]
        else:
            cell.get_holding().owner = self._players[0]

        return True


    def main_loop(self):

         self.current_player = self._players[0]
         self.curr_turn_time = 0

         while True and not self.testing:

            frames_passed = self.clock.tick(16.6597)
            time_passed = 1/frames_passed
            self.curr_turn_time += time_passed

            self.turn = (self.curr_turn_time%(self.turn_time*2  )) // (self.turn_time//2)%2
            curr_player = self._players[round(self.turn)]

            self.board_draw()
            myfont = pygame.font.SysFont("comicsansms", 30)
            string = str(curr_player)
            label = myfont.render(string, 1, Morelli.white)

            self.game_display.blit(label, (20, 620))

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            curr_player.move(events)

            pygame.display.update()


if __name__ == "__main__":
    game = Morelli(turn_time=9)

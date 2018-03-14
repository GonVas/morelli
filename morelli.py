import pygame
import math
from time import sleep,time
from functools import lru_cache
import asyncio
import threading
import random

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

    class Player:

        player_color = {'black' : (10,10,10), 'white' : (240,240,240)}

        def __init__(self, color, game):
            self.game = game
            self.color = color
            self.ignore_mouse = False

        def color_to_rgb(self):
            #print('Owner color ' + Player.player_color[self.color])
            return Morelli.Player.player_color[self.color]

        def move(self, events):
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        click_cell_x = pos[0] // self.game.cell_size
                        click_cell_y = pos[1] // self.game.cell_size
                        self.game.select_cell(click_cell_x, click_cell_y)

        def __setitem__(self, key, item):
            if(key != 'color'):
                raise TypeError("Can only acess color")

            self.color = item

        def __getitem__(self, key):
            if(key != 'color'):
                raise TypeError("Can only acess color")

            return self.color

        def __str__(self):
            return self.color

    class AI(Player):

        def __init__(self, color, game, dificulty=0):
            super().__init__(color, game)
            self.dificulty = dificulty
            self.ignore_mouse = True

        def move(self, events):
            print('AI THINKING')


    class Piece:

        def __init__(self, player, obj_type='regular'):
            self.owner = player
            self.type = obj_type

        def color(self):
            #print('color to owner ' + self.owner.color_to_rgb())
            return self.owner.color_to_rgb()

    def __init__(self, dim=11, cell_size=50, bottom_bar=200, option='PvsAI', turn_time=5):
        self.figure_dims(dim, cell_size, bottom_bar)
        pygame.init()
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.update()
        self.clock = pygame.time.Clock()
        self.init_cells()
        self.turn_time = turn_time
        self.init_players(option)
        self.init_place()
        self.add_rules()
        self.main_loop()

    def init_place(self):
        pieces = [self.dim*2, self.dim*2]
        for i in range(self.dim):
            remove = round(random.uniform(0, 1))
            if(pieces[remove] == 0):
                remove = (remove + 1)%2

            pieces[remove] -= 1
            piece = Morelli.Piece(self._players[remove])
            piece2 = Morelli.Piece(self._players[(remove+1)%2])
            self._cells[i][0].set_holding(piece) 
            self._cells[i][self.dim-1].set_holding(piece2) 

        for i in range(1, self.dim):
            remove = round(random.uniform(0, 1))
            if(pieces[remove] == 0):
                remove = (remove + 1)%2

            pieces[remove] -= 1
            piece = Morelli.Piece(self._players[remove])
            piece2 = Morelli.Piece(self._players[(remove+1)%2])
            self._cells[0][i].set_holding(piece) 
            self._cells[self.dim-1][i].set_holding(piece2) 

        #print('Bag have %d whites and %d blacks'% (pieces[0], pieces[1]))

    def add_rules(self):
        self.bool_rules = []
        self.modifying_rules = []

        game = self

        def no_in_way(from_cell, to_cell):
            x_diff = to_cell.pos[0] - from_cell.pos[0]
            y_diff = to_cell.pos[1] - from_cell.pos[1]

            if(x_diff  == 0 and y_diff == 0):
                print("hmmm both x_diff and y_diff is 0")
                return True

            if(x_diff == y_diff):
                print("RULE : Dont know how to do diagonal thing")
                return True
            else:
                if(y_diff > x_diff):
                    for i in range(from_cell.pos[1], to_cell.pos[1] + round(1*abs(y_diff)/y_diff)):
                        if(not self._cells[from_cell.pos[0]][i].is_empty()):
                            print("Tried to move piece on top of another")
                            return False
                else:
                    for i in range(from_cell.pos[0] + round(1*abs(x_diff)/x_diff), to_cell.pos[0]):
                        if(not self._cells[i][from_cell.pos[1]].is_empty()):
                            print("Tried to move piece on top of another")
                            return False
            print("Passed No piece in middle rule")
            return True

        self.bool_rules.append(no_in_way)



    def testing(self):
        self._cells[2][3].set_holding(Morelli.Piece(self._players[0]))
        self._cells[3][3].set_holding(Morelli.Piece(self._players[1]))

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
        p1 = Morelli.Player('black', self)

        if option == 'AIvsAI':
            p1 = Morelli.AI('black', self)

        p2 = Morelli.AI('white', self)

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
                new_cell = Morelli.Cell([x, y], order)
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
        for bool_ruĺe in self.bool_rules:
            if(not bool_ruĺe(from_cell, to_cell)):
                print("FAILED A RULE")
                return False
        print("Passed all rules")
        return True

    def mod_rules(self, from_cell, to_cell):
        for mod_ruĺe in self.modifying_rules:
            mod_ruĺe(from_cell, to_cell)
        print("Done all mod rules")
        return True

    def move(self, from_cell, where_cell):
        if(from_cell.is_empty()):
            print('Tried to move empty')
            return
        if(self.check_rules(from_cell, where_cell)):
            where_cell.set_holding(from_cell.get_holding())
            from_cell.set_holding('empty')
            return self.mod_rules()



    def main_loop(self):
         #selec = False
         #global selected_family

         self.current_player = self._players[0]
         self.curr_turn_time = 0

         while True:

            frames_passed = self.clock.tick(16.6597)
            time_passed = 1/frames_passed
            self.curr_turn_time += time_passed

            self.turn = (self.curr_turn_time%(self.turn_time*2  )) // (self.turn_time//2)%2
            curr_player = self._players[round(self.turn)]

            #print('Passed : %fs' % time_passed)
            #print('Turn : ' + str(self.turn))

            self.board_draw()

            #initialize_piece()
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
    game = Morelli()


"""
        beg_time = time()
        while (time() - beg_time < time_dur) :
            print('Going to draw selected')
            final_pos = (click_cell_x * self.cell_size, click_cell_y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.game_display, (0,250,0), final_pos)
            await asyncio.sleep(1)

    async def select_cell(self, click_cell_x, click_cell_y, time_dur = 5):
        print('In async')
        end_time = loop.time() + time_dur
        while True:
            print('Going to draw selected')
            final_pos = (click_cell_x * self.cell_size, click_cell_y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.game_display, (0,250,0), final_pos)
            if (loop.time() + 1.0) >= end_time:
                break
            await asyncio.sleep(1)


                    #asyncio.run_coroutine_threadsafe(self.select_cell(click_cell_x, click_cell_y), loop)
                    #pygame.draw.rect(self.game_display, (20, 200, 10), (click_cell_x * self.cell_size, click_cell_y * self.cell_size, self.cell_size, self.cell_size))
                    #t1 = threading.Thread(target=self.select_cell(click_cell_x, click_cell_y))
                    #t1.start()


                    if not selec:
                        selected_piece = select_block(a, b)
                        selec = True
                        if selected_piece is not None:
                            print(selected_piece.x, " ", selected_piece.y)

                        else:
                            selec = False
                    else:
                        if selected_piece is not None:
                            move(selected_piece.x, selected_piece.y, a, b)
                        selec = False


"""


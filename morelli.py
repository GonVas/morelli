import pygame
import math
from time import sleep,time
from functools import lru_cache
import asyncio
import threading

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

        def __init__(self, color):
            self.color = color

        def color_to_rgb(self):
            #print('Owner color ' + Player.player_color[self.color])
            return Morelli.Player.player_color[self.color]

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


        def __init__(self, color, dificulty=0):
            super().__init__(color)
            self.dificulty = dificulty

    class Piece:

        def __init__(self, player, obj_type='regular'):
            self.owner = player
            self.type = obj_type

        def color(self):
            #print('color to owner ' + self.owner.color_to_rgb())
            return self.owner.color_to_rgb()

    def __init__(self, dim=11, cell_size=50, bottom_bar=200, option='PvsAI'):
        self.figure_dims(dim, cell_size, bottom_bar)
        pygame.init()
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.update()
        self.clock = pygame.time.Clock()
        self.init_cells()
        self.init_players(option)
        self.testing()
        self.main_loop()

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

        p1 = Morelli.Player('black')

        if option == 'AIvsAI':
            p1 = Morelli.AI('black')

        p2 = Morelli.AI('white')

        self._players = [p1, p2]

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
        clicked_cell = self._cells[click_cell_x][click_cell_y]
        if(clicked_cell.is_empty()):
            return
        owner = clicked_cell.get_holding().owner

        # forgive me bad code ahead

        if not hasattr(self, 'sel_buf'):
            print('Sel buf: ' + str(clicked_cell.is_empty()))
            self.sel_buf = clicked_cell
            return
        else:
            if self.sel_buf.get_holding().owner == self.current_player and self.sel_buf.order < clicked_cell.order:
                print('moving %s  to %s ' % (self.sel_buf, clicked_cell))
                self.move(self.sel_buf, clicked_cell)

        print('Cliked cell %d,%d whose owner is: %s'% (click_cell_x, click_cell_y, owner) )


    def move(self, from_cell, where_cell):
        if(from_cell.is_empty()):
            print('Tried to move empty')
            return
        where_cell.set_holding(from_cell.get_holding())
        from_cell.set_holding('empty')


    def main_loop(self):
         #selec = False
         #global selected_family

         self.current_player = self._players[0]

         while True:

            frames_passed = self.clock.tick(16.6597)
            time_passed = 1/frames_passed

            #print('Passed : %fs' % time_passed)

            self.board_draw()

            #initialize_piece()
            myfont = pygame.font.SysFont("comicsansms", 30)
            #string = selected_family +"'s turn"
            label = myfont.render("Teste", 1, Morelli.white)

            self.game_display.blit(label, (20, 620))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    click_cell_x = pos[0] // self.cell_size
                    click_cell_y = pos[1] // self.cell_size
                    print('In event mouse up')
                    self.select_cell(click_cell_x, click_cell_y)
                    #asyncio.run_coroutine_threadsafe(self.select_cell(click_cell_x, click_cell_y), loop)
                    #pygame.draw.rect(self.game_display, (20, 200, 10), (click_cell_x * self.cell_size, click_cell_y * self.cell_size, self.cell_size, self.cell_size))
                    #t1 = threading.Thread(target=self.select_cell(click_cell_x, click_cell_y))
                    #t1.start()

                    """
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
                        selec = False"""
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

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

"""


import pygame
import math
import time
from functools import lru_cache

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



    def __init__(self, dim=11, cell_size=50, bottom_bar=200):
        self.figure_dims(dim, cell_size, bottom_bar)
        pygame.init()
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.update()
        self.clock = pygame.time.Clock()
        self.init_cells()
        self.testing()
        self.main_loop()

    def testing(self):
        self._cells[2][3].set_holding({"color":(10,10,10)})
        self._cells[3][3].set_holding({"color":(240,240,240)})

    @staticmethod
    @lru_cache(maxsize=256)
    def pnorm(vec, p=5):
        # en.wikipedia.org/wiki/Norm_(mathematics), pnorm 
        # 1 - taxicab/manhattan distance
        # 2 - Euclidean distance
        # for morelli square p must aproach infinity but carefull with OVF. 
        vec_sum = 0
        for val in vec:
            vec_sum += val**p
        return (vec_sum**(1/p))


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
                    pygame.draw.rect(self.game_display, cell.get_holding()["color"], holding_pos)

    def select_cell(self, click_cell_x, click_cell_y, time = 3):
        pass

    def main_loop(self):
         #selec = False
         #global selected_family
         while True:
            self.board_draw()

            #initialize_piece()
            myfont = pygame.font.SysFont("comicsansms", 30)
            #string = selected_family +"'s turn"
            label = myfont.render("Teste", 1, Morelli.white)

            self.game_display.blit(label, (20, 620))
            pygame.display.update()

            time.sleep(0.03)

            self.clock.tick(20)

            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    click_cell_x = pos[0] // self.cell_size
                    click_cell_y = pos[1] // self.cell_size
                    self.select_cell(click_cell_x, click_cell_y)
                    #pygame.draw.rect(self.game_display, (20, 200, 10), (click_cell_x * self.cell_size, click_cell_y * self.cell_size, self.cell_size, self.cell_size))
                    #pygame.display.update()
                    #time.sleep(0.3)
                    

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
            

if __name__ == "__main__":
    game = Morelli()

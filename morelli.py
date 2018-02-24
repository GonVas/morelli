import pygame
import math
import time

class Morelli:

    # defines the width and height of the display
    #display_width = 600
    #display_height = 680

    # defines block width and height
    #block_height = 50 * 1.5
    #block_width = 50 * 1.5

    #factor = 25 * 1.5

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


    def __init__(self, dim=11, cell_size=50, bottom_bar=200):
        self.figure_dims(dim, cell_size, bottom_bar)
        pygame.init()
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.update()
        self.clock = pygame.time.Clock()
        self.main_loop()

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
                color = Morelli.colors[abs(min(i%mod,j%mod))]
                pygame.draw.rect(self.game_display, color, (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size))

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

            """
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    a = pos[0] // 75
                    b = pos[1] // 75
                    pygame.draw.rect(game_display, teal, (a * 50 * 1.5, b * 50 * 1.5, block_width, block_height))
                    pygame.display.update()
                    time.sleep(0.03)

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
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            """

if __name__ == "__main__":
    game = Morelli()

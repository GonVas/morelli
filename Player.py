import collections
from math import log, sqrt
from copy import deepcopy, copy
from MonteCarlo import MonteCarlo

class Player:

    player_color = {'black' : (10,10,10), 'white' : (240,240,240),
                    'very_grey' : (40,40,40), 'light_grey':(170, 170, 170),
                    'green' : (10, 220, 10), 'red' : (220, 10, 10)}

    def __init__(self, color, king_col='green', ghost_color='light_grey'):
        self.color = color
        self.ignore_mouse = False
        self.king_col = king_col
        self.ghost_color = ghost_color

    def color_to_rgb(self):
        return Player.player_color[self.color]

    def king_color_to_rgb(self):
        return Player.player_color[self.king_col]

    def ghost_color_to_rgb(self):
        return Player.player_color[self.ghost_color]

    def move(self, events, pygame, game):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    click_cell_x = pos[0] // game.cell_size
                    click_cell_y = pos[1] // game.cell_size
                    game.board.select_cell(click_cell_x, click_cell_y, self)


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

    def __init__(self, board, color, turn_time, dificulty=0):
        super().__init__(color)
        self.dificulty = dificulty
        self.ignore_mouse = True
        self.turn_time = turn_time
        self.monte = MonteCarlo(board, self , self.turn_time)

    def move(self, events, pygame, game):
        print('AI THINKING')
        #self.monte.get_play()


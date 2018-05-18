import pygame
import math
from time import sleep,time
from functools import lru_cache
import asyncio
import threading
import random
from Board import Board
from copy import deepcopy, copy

from Cell import Cell, Piece, King, PieceGhost

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

    def __init__(self, dim=11, cell_size=50, bottom_bar=200, option='PvsAI', turn_time=15, testing=False, gui=True):
        self.figure_dims(dim, cell_size, bottom_bar)

        self.testing = testing
        self.gui = gui

        if(self.gui):
            pygame.init()
            self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
            pygame.display.update()
            self.clock = pygame.time.Clock()
        
        self.board = Board(dim, option, turn_time)
        self.turn_time = turn_time
    
        #if(not testing):
            #self.board.reset_test_env3()

        self.main_loop()
        print("Game Ended")


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

        print("Game Board with dimension: %sx%s and size %sx%s" % (self.dim, self.dim, self.display_width, self.display_height))

    def board_draw(self):
        self.game_display.fill(Morelli.black)
        for i in range(self.dim):
            for j in range(self.dim):
                mod = self.dim//2
                cell = self.board.get_cells()[i][j]
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

    def game_draw(self):
        self.board_draw()
        myfont = pygame.font.SysFont("comicsansms", 30)
        string = str(self.board.current_player())
        label = myfont.render(string, 1, Morelli.white)

        self.game_display.blit(label, (20, 620))

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.board.current_player().move(events, pygame, self)

        pygame.display.update()

    def main_loop(self):

         #self.current_player = self.board._players[0]
         self.curr_turn_time = 0

         while True and not self.testing:

            frames_passed = self.clock.tick(16.6597)
            time_passed = 1/frames_passed
            self.curr_turn_time += time_passed

            self.turn = (self.curr_turn_time%(self.turn_time*2  )) // (self.turn_time//2)%2
            #curr_player = self.board.get_player(round(self.turn))

            winner = self.board.check_winning()
            if(winner != None):
                if(winner == "tie"):
                    print("It was a tie")
                    return True
                print("Congrats, player %s Won." % (str(winner)))
                return True

            if(self.gui):
                self.game_draw()



if __name__ == "__main__":
    game = Morelli(turn_time=9)

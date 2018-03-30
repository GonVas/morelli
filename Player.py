import collections

class Player:

    player_color = {'black' : (10,10,10), 'white' : (240,240,240),
                    'very_grey' : (40,40,40), 'light_grey':(170, 170, 170),
                    'green' : (10, 220, 10), 'red' : (220, 10, 10)}

    def __init__(self, color, game, pygame, king_col='green', ghost_color='light_grey'):
        self.game = game
        self.color = color
        self.ignore_mouse = False
        self.pygame = pygame
        self.king_col = king_col
        self.ghost_color = ghost_color

    def color_to_rgb(self):
        return Player.player_color[self.color]

    def king_color_to_rgb(self):
        return Player.player_color[self.king_col]

    def ghost_color_to_rgb(self):
        return Player.player_color[self.ghost_color]

    def move(self, events):
        for event in events:
            if event.type == self.pygame.MOUSEBUTTONUP:
                    pos = self.pygame.mouse.get_pos()
                    click_cell_x = pos[0] // self.game.cell_size
                    click_cell_y = pos[1] // self.game.cell_size
                    self.game.select_cell(click_cell_x, click_cell_y)


    def get_mycells(self):
        res = []

        for cellx in self.game._cells:
            for cell in cellx:
                if(not cell.is_empty() and cell.get_holding().owner == self):
                    res.append(cell)

        return res

    def avaiable_moves(self):
        can_move = self.get_mycells()
        aval_moves = collections.defaultdict(list)
        for cell in can_move:
            if( cell.order < self.game.max_order()-1 ):
                for order_tolook in range(cell.order+1, self.game.max_order()):
                    empty_next_order = self.game.get_order_cells(order_tolook, check_empty=True)
                    for empty_cell in empty_next_order:
                        if(self.game.valid_move(cell, empty_cell)):
                            aval_moves[cell].append(empty_cell)
            else:
                can_move.remove(cell)
        return aval_moves


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

    def __init__(self, color, game, pygame, dificulty=0):
        super().__init__(color, game, pygame)
        self.dificulty = dificulty
        self.ignore_mouse = True

    def move(self, events):
        print('AI THINKING')


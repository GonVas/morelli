class Player:

    player_color = {'black' : (10,10,10), 'white' : (240,240,240)}

    def __init__(self, color, game, pygame):
        self.game = game
        self.color = color
        self.ignore_mouse = False
        self.pygame = pygame

    def color_to_rgb(self):
        #print('Owner color ' + Player.player_color[self.color])
        return Player.player_color[self.color]

    def move(self, events):
        for event in events:
            if event.type == self.pygame.MOUSEBUTTONUP:
                    pos = self.pygame.mouse.get_pos()
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

    def __init__(self, color, game, pygame, dificulty=0):
        super().__init__(color, game, pygame)
        self.dificulty = dificulty
        self.ignore_mouse = True

    def move(self, events):
        print('AI THINKING')
import pygame

from fighters.metabee import Metabee
from fighters.sumilidon import Sumilidon
from room import Room

BACKGROUND_COLOR = pygame.Color("cyan")


class World:
    keys1 = {'right': pygame.K_RIGHT, 'left': pygame.K_LEFT, 'up': pygame.K_UP, 'down': pygame.K_DOWN,
             'space': pygame.K_SPACE, 'attack1': pygame.K_m, 'attack2': pygame.K_COMMA, 'attack3': pygame.K_PERIOD,
             'attack4': pygame.K_SLASH}
    keys2 = {'right': pygame.K_d, 'left': pygame.K_a, 'up': pygame.K_w, 'down': pygame.K_s,
             'space': pygame.K_f, 'attack1': pygame.K_e, 'attack2': pygame.K_r, 'attack3': pygame.K_y,
             'attack4': pygame.K_y}

    def __init__(self):
        # Players group used to draw multiple players
        self.player = Sumilidon(90, 200, 1256, keys=self.keys1)
        self.player2 = Metabee(290, 300, 1257, keys=self.keys2)
        self.players = {}
        self.add_player(self.player)
        self.add_player(self.player2)
        self.rooms = [Room("level1.txt"), Room("level2.txt")]
        self.current_room = 0
        # self.countdown = CountDown()
        # Main Game Loop variables
        self.done = False
        self.fps = 60.0
        self.clock = pygame.time.Clock()
        self.screen = None
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.game_font = pygame.font.SysFont('times', 20)

    def add_player(self, player):
        self.players[player.unique_id] = player

    def run(self, screen):
        self.screen = screen
        while not self.done:
            self.process_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)

    def process_events(self):
        keys = pygame.key.get_pressed()
        self.player.process_keys(keys)
        # Remove these line for networking
        self.player2.process_keys(keys)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def update(self):
        # Will only update count down timer until it's done
        # if not self.countdown.should_countdown():
        #    self.countdown.update()
        # else:
        # --- Game Logic ---
        self.player.set_room(self.rooms[self.current_room])
        self.player.update(self.players)
        # Remove these line for networking
        self.player2.set_room(self.rooms[self.current_room])
        self.player2.update(self.players)

    def draw_countdown(self):
        if not self.countdown.should_countdown():
            self.countdown.draw(self.screen)

    def draw_players(self):
        pos = 0
        for player in self.players:
            position = (pos, len(self.players))
            self.players[player].draw(self.screen, self.game_font, position)
            pos += 1

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.rooms[self.current_room].draw(self.screen)
        self.draw_players()
        # self.draw_countdown()

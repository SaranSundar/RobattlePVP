import pygame

from fighters.metabee import Metabee
from fighters.test_dummy import TestDummy
from room import Room

BACKGROUND_COLOR = pygame.Color("cyan")


class World:
    def __init__(self):
        # Players group used to draw multiple players
        self.player = Metabee(90, 300, 1256)
        self.player2 = TestDummy(290, 300, 1257)
        self.players = {}
        self.add_player(self.player)
        self.add_player(self.player2)
        self.rooms = [Room("level1.txt"), Room("level2.txt")]
        self.current_room = 0
        # Main Game Loop variables
        self.done = False
        self.fps = 60.0
        self.clock = pygame.time.Clock()
        self.screen = None

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
        # --- Game Logic ---
        self.player.set_room(self.rooms[self.current_room])
        self.player.update(self.players)
        # Remove these line for networking
        self.player2.set_room(self.rooms[self.current_room])
        self.player2.update(self.players)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.rooms[self.current_room].draw(self.screen)
        for player in self.players:
            self.players[player].draw(self.screen)

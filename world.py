import pygame

from player import Player
from room import Room

BACKGROUND_COLOR = pygame.Color("cyan")


class World:
    def __init__(self):
        # Players group used to draw multiple players
        self.players = pygame.sprite.Group()
        self.player = Player(90, 300)
        self.players.add(self.player)
        self.rooms = [Room("level1.txt"), Room("level2.txt")]
        self.current_room = 0
        # Main Game Loop variables
        self.done = False
        self.fps = 60.0
        self.clock = pygame.time.Clock()
        self.screen = None

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def update(self):
        # --- Game Logic ---
        self.player.set_room(self.rooms[self.current_room])
        self.player.update()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.rooms[self.current_room].draw(self.screen)
        self.players.draw(self.screen)

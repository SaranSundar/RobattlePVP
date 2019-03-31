import pygame

import constants
from player import Player
from room import Room


class World:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.player = Player(90, 300, 50, 50)
        self.sprites.add(self.player)

        self.rooms = [Room("level1.txt"), Room("level2.txt")]
        self.current_room = 1
        self.boundary_size = 200
        self.right_boundary = constants.SCREEN_WIDTH - self.boundary_size
        self.left_boundary = self.boundary_size

        self.player.set_room(self.rooms[self.current_room])

    def calculate_right_diff(self):
        return self.player.rect.right - self.right_boundary

    def calculate_left_diff(self):
        return self.left_boundary - self.player.rect.left

    def key_down(self, key):
        self.player.key_down(key)

    def key_up(self, key):
        self.player.key_up(key)

    def update(self):
        # --- Game Logic ---
        self.sprites.update()
        self.rooms[self.current_room].update()
        # Player status
        if self.player.rect.right >= constants.SCREEN_WIDTH:
            self.player.rect.right = constants.SCREEN_WIDTH
        elif self.player.rect.left <= 0:
            self.player.rect.left = 0

    def draw(self, screen):
        self.rooms[self.current_room].draw(screen)
        self.sprites.draw(screen)


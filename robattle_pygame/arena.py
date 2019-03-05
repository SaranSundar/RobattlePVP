import pygame

from robattle_pygame.block import Block

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)


def create_blocks(filename: str):
    width = 50
    height = 50
    background_blocks = pygame.sprite.Group()
    collision_blocks = pygame.sprite.Group()
    with open(filename, 'r') as f:
        lines = f.readlines()
        row = 0
        for line in lines:
            line = line.strip()
            col = 0
            for char in line:
                x = col * width
                y = row * height
                color = WHITE
                can_collide = True
                if char == ".":
                    color = BLACK
                    can_collide = False
                elif char == "r":
                    color = RED
                elif char == "g":
                    color = GREEN
                elif char == "b":
                    color = BLUE
                elif char == "p":
                    color = PURPLE
                block = Block(x, y, width, height, color, can_collide)
                if can_collide:
                    collision_blocks.add(block)
                else:
                    background_blocks.add(block)
    return background_blocks, collision_blocks


class Arena(object):
    # -- Methods
    def __init__(self):
        """ Constructor function """
        # Call the parent's constructor
        super().__init__()
        self.background_blocks, self.collision_blocks = create_blocks("Arena1.txt")

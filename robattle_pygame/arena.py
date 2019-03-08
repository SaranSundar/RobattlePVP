import pygame

from robattle_pygame.block import Block
from robattle_pygame.spritesheet_functions import SpriteSheet, get_path_name

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

# X, Y
GRASS_BLOCK = (9, 0)
PURPLE_BLOCK = (2, 0)
ALARM_BLOCK = (0, 2)
TORCH_BLOCK = (1, 2)


def create_blocks(filename: str):
    background_blocks = pygame.sprite.Group()
    collision_blocks = pygame.sprite.Group()
    spritesheet = SpriteSheet("tiles_spritesheet.png")
    scale_block_size = 55
    spritesheet_block_size = 72  # 72 x 72
    file_path = get_path_name("maps", filename)
    with open(file_path, 'r') as f:
        lines = f.readlines()
        row = 0
        for line in lines:
            line = line.strip()
            col = 0
            for char in line:
                x = col * scale_block_size
                y = row * scale_block_size
                color = WHITE
                can_collide = True
                image = None
                if char == ".":
                    color = BLACK
                    can_collide = False
                elif char == "r":
                    color = RED
                    image = get_block_sprite(GRASS_BLOCK, spritesheet_block_size, scale_block_size, spritesheet)
                elif char == "g":
                    color = GREEN
                    image = get_block_sprite(PURPLE_BLOCK, spritesheet_block_size, scale_block_size, spritesheet)
                elif char == "b":
                    color = BLUE
                    can_collide = False
                    image = get_block_sprite(TORCH_BLOCK, spritesheet_block_size, scale_block_size, spritesheet)
                elif char == "p":
                    color = PURPLE
                    image = get_block_sprite(ALARM_BLOCK, spritesheet_block_size, scale_block_size, spritesheet)
                block = Block(x, y, scale_block_size, scale_block_size, color, image, can_collide)
                if can_collide:
                    collision_blocks.add(block)
                else:
                    background_blocks.add(block)
                col += 1
            row += 1
    return background_blocks, collision_blocks


def get_block_sprite(block, block_size, scale_size, spritesheet):
    scale = 1
    if scale_size != block_size:
        scale = float(scale_size) / float(block_size)
    image = spritesheet.get_image(block[0], block[1], block_size, block_size, scale)
    return image


class Arena:
    # -- Methods
    def __init__(self, filename):
        """ Constructor function """
        self.background_blocks, self.collision_blocks = create_blocks(filename)
        self.background_color = WHITE

    def update(self):
        self.background_blocks.update()
        self.collision_blocks.update()

    def draw(self, screen):
        screen.fill(self.background_color)
        self.background_blocks.draw(screen)
        self.collision_blocks.draw(screen)

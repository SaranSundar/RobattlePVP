import pygame

import constants
from block import Block
from spritesheet_functions import SpriteSheet, get_path_name


def create_blocks(filename: str):
    background_blocks = pygame.sprite.Group()
    collision_blocks = pygame.sprite.Group()
    spritesheet = SpriteSheet("tiles_spritesheet.png")
    scale_block_size = 55
    spritesheet_block_size = 70  # 70 x 70
    file_path = get_path_name("maps", filename)
    block_mapping = create_block_mapping()
    with open(file_path, 'r') as f:
        lines = f.readlines()
        row = 0
        for line in lines:
            line = line.strip()
            col = 0
            for char in line:
                x = col * scale_block_size
                y = row * scale_block_size
                image = block_mapping[char][0]
                can_collide = block_mapping[char][1]
                image = get_block_sprite(image, spritesheet_block_size, scale_block_size,
                                         spritesheet)
                block = Block(x, y, scale_block_size, scale_block_size, image, can_collide)
                if char != ".":
                    bg_image = get_block_sprite(constants.BACKGROUND_BLOCK, spritesheet_block_size, scale_block_size,
                                                spritesheet)
                    bg = Block(x, y, scale_block_size, scale_block_size, bg_image, can_collide)
                    background_blocks.add(bg)
                if can_collide:
                    collision_blocks.add(block)
                else:
                    background_blocks.add(block)
                col += 1
            row += 1
    return background_blocks, collision_blocks


def create_block_mapping():
    file_path = get_path_name("maps", "block_mapping.txt")
    with open(file_path, 'r') as f:
        lines = f.readlines()
        block_mapping = {}
        for line in lines:
            line = line.strip()
            line = line.replace("\t", "")
            line = line.replace(" ", "")
            line = line.split("/")
            location = eval(line[1])
            letter = line[0].split("=")[1]
            if len(line) == 2:
                block = (location, True)
            else:
                block = (location, False)
            block_mapping[letter] = block
        return block_mapping


def get_block_sprite(block, block_size, scale_size, spritesheet):
    scale = 1
    if scale_size != block_size:
        scale = float(scale_size) / float(block_size)
    image = spritesheet.get_image(block[0], block[1], block_size, block_size, scale)
    return image


class Room:
    background_blocks = None
    collision_blocks = None

    def __init__(self, filename):
        """ Constructor, create our lists. """
        self.background_blocks, self.collision_blocks = create_blocks(filename)
        self.background_color = constants.TEAL

    def update(self):
        self.background_blocks.update()
        self.collision_blocks.update()

    def draw(self, screen):
        self.background_blocks.draw(screen)
        self.collision_blocks.draw(screen)

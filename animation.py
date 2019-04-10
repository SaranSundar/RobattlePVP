import collections

import pygame

from spritesheet_functions import get_path_name


def get_sprites_from_dict(spritesheet, sprite_dict, scale=1):
    spritesheet = get_path_name("images", spritesheet)
    spritesheet = pygame.image.load(spritesheet).convert_alpha()
    sprites = {}
    y = 0
    for key, value in sprite_dict.items():
        # print(key, value)
        sprites[key] = get_row_animations(spritesheet, y, value[0], value[1], value[2], scale)
        y += value[1]
    return sprites


def get_row_animations(spritesheet, y, width, height, length, scale):
    row = []
    for col in range(length):
        # Create a new blank image
        image = pygame.Surface([width, height], pygame.SRCALPHA)
        image.blit(spritesheet, (0, 0), (col * width, y, width, height))
        if scale != 1:
            image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        row.append(image)
    return row


def get_sprite_dict(filename):
    textfile_path = get_path_name("animations", filename)
    sprite_dict = collections.OrderedDict()
    with open(textfile_path) as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            name = lines[i].strip()
            dimensions = lines[i + 1].strip().split("x")
            dimensions = [int(x) for x in dimensions]
            # dashed_lines = lines[i + 2].strip()
            sprite_dict[name] = dimensions
            # print(name, dimensions, dashed_lines)
            i += 3
    return sprite_dict


def clock():
    current_time = pygame.time.get_ticks()
    return current_time


class Animation:
    def __init__(self, spritesheet, textfile, scale, animation_name):
        self.sprite_dict = get_sprite_dict(textfile)
        self.sprites = get_sprites_from_dict(spritesheet, self.sprite_dict, scale)
        self.current_frame = 0
        # Both will be set in calculate animation speed
        self.animation_speed = None
        self.timeOfNextFrame = None
        self.animation = animation_name
        self.calculate_animation_speed()

    def calculate_animation_speed(self):
        self.animation_speed = 640 / len(self.sprites[self.animation])
        self.current_frame = 0
        self.timeOfNextFrame = clock() + self.animation_speed

    def get_image(self):
        return self.sprites[self.animation][self.current_frame]

    def update_frame(self):
        if clock() > self.timeOfNextFrame:
            self.current_frame = (self.current_frame + 1) % len(self.sprites[self.animation])
            self.timeOfNextFrame += self.animation_speed

    def update_animation(self, animation_name):
        self.animation = animation_name
        self.calculate_animation_speed()

    def reset_clock(self):
        self.timeOfNextFrame = clock()
        self.current_frame = 0

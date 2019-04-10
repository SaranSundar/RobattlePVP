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
            width = int(width * scale)
            height = int(height * scale)
            image = pygame.transform.scale(image, (width, height))
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
    def __init__(self, spritesheet, textfile, scale):
        self.sprite_dict = get_sprite_dict(textfile)
        self.sprites = get_sprites_from_dict(spritesheet, self.sprite_dict, scale)
        self.current_frame = 0
        self.animation = "Walk"
        self.timeOfNextFrame = clock()
        self.animation_speed = 80  # ms

    def animate_sprite(self):
        if clock() > self.timeOfNextFrame:  # We only animate our character every 60ms.
            self.current_frame = (self.current_frame + 1) % len(
                self.sprites[self.animation])  # There are 6 frames of animation in each direction
            self.timeOfNextFrame += self.animation_speed  # so the modulus allows it to loop

    def reset_clock(self):
        self.timeOfNextFrame = clock()
        self.current_frame = 0

    def update_animation(self, animation_name):
        self.animation = animation_name

    def update_frame(self):
        self.current_frame += 1
        if self.current_frame >= len(self.sprites[self.animation]):
            self.current_frame = 0

    def get_image(self):
        return self.sprites[self.animation][self.current_frame]

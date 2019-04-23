import collections

import pygame

from spritesheet_functions import get_path_name


def get_sprites_from_dict(spritesheet, sprite_dict, scale=1):
    spritesheet = get_path_name("images", spritesheet)
    spritesheet = pygame.image.load(spritesheet).convert_alpha()
    sprites = {}
    animation_speeds = {}
    collision_masks = {}
    y = 0
    for key, value in sprite_dict.items():
        # print(key, value)
        sprites[key], collision_masks[key] = get_row_animations(spritesheet, y, value[0], value[1], value[2], scale)
        animation_speeds[key] = value[3]
        y += value[1]
    return sprites, collision_masks, animation_speeds


def get_row_animations(spritesheet, y, width, height, length, scale):
    row = []
    flip_row = []
    masks = []
    flip_masks = []
    for col in range(length):
        # Create a new blank image
        image = pygame.Surface([width, height], pygame.SRCALPHA)
        image.blit(spritesheet, (0, 0), (col * width, y, width, height))
        if scale != 1:
            image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        row.append(image)
        masks.append(pygame.mask.from_surface(image))
        flip_image = pygame.transform.flip(image, True, False)
        flip_row.append(flip_image)
        flip_masks.append(pygame.mask.from_surface(flip_image))
    return (row, flip_row), (masks, flip_masks)


def get_collision_image(image):
    orig_arr = pygame.PixelArray(image)
    pxarray = orig_arr.extract(0xFFFFFF)
    black = 4278190080
    cols = len(pxarray)  # 51
    rows = len(pxarray[0])  # 82
    max_black_count_width = 0
    max_black_count_height = 0
    count_y = False
    y_offset = 0
    total_x_offset = 0
    for row in pxarray:
        black_count_width = 0
        black_count_height = 0
        x_offset = 0
        count_x = False
        for col in row:
            if col == black:
                count_x = True
                count_y = True
                black_count_width += 1
                black_count_height = 1
            else:
                if not count_x:
                    x_offset += 1
        if count_x:
            total_x_offset = x_offset
        if not count_y:
            y_offset += 1
        max_black_count_height += black_count_height
        if black_count_width > max_black_count_width:
            max_black_count_width = black_count_width
    # somehow width and height are mixed for some unknown reason so flip them
    collision_image = pygame.Surface([max_black_count_height, max_black_count_width], pygame.SRCALPHA)
    collision_image.fill((0, 0, 0))
    # return collision_image, x_offset, y_offset
    return collision_image, total_x_offset, y_offset, pxarray.make_surface()


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
    def __init__(self, spritesheet, collision_spritesheet, textfile, scale, animation_name):
        self.sprite_dict = get_sprite_dict(textfile)
        self.sprites, unused_masks, unused_animation_speeds = get_sprites_from_dict(spritesheet, self.sprite_dict,
                                                                                    scale)
        self.collision_sprites, self.collision_masks, self.animation_speeds = get_sprites_from_dict(
            collision_spritesheet, self.sprite_dict,
            scale)
        self.current_frame = 0
        # Both will be set in calculate animation speed
        self.animation_speed = None
        self.timeOfNextFrame = None
        self.animation = animation_name
        self.is_left = 0
        self.calculate_animation_speed()
        # NEED TO CREATE LIST OF MASKS TO USE

    def calculate_animation_speed(self):
        self.animation_speed = self.animation_speeds[
            self.animation]  # 640 / len(self.sprites[self.animation][self.is_left])
        self.current_frame = 0
        self.timeOfNextFrame = clock() + self.animation_speed

    def get_image(self, last_press="r"):
        self.is_left = last_press is "l"
        return self.sprites[self.animation][self.is_left][self.current_frame], \
               self.collision_sprites[self.animation][self.is_left][self.current_frame], \
               self.collision_masks[self.animation][self.is_left][self.current_frame]

    def update_frame(self):
        if clock() > self.timeOfNextFrame:
            self.current_frame = (self.current_frame + 1) % len(self.sprites[self.animation][self.is_left])
            self.timeOfNextFrame += self.animation_speed

    def update_animation(self, animation_name):
        if self.animation != animation_name:
            if animation_name in self.sprites:
                self.animation = animation_name
                self.calculate_animation_speed()

    def reset_clock(self):
        self.timeOfNextFrame = clock()
        self.current_frame = 0

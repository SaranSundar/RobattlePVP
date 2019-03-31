"""
This module is used to pull individual sprites from sprite sheets.
"""
import os

import pygame


def get_path_name(folder, filename):
    # Load the sprite sheet.
    current_path = os.path.dirname(__file__)  # Where your .py file is located
    resource_path = os.path.join(current_path, 'resources')  # The resource folder path
    image_path = os.path.join(resource_path, folder)  # The image folder path
    final_path = os.path.join(image_path, filename)
    return final_path


class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, filename):
        """ Constructor. Pass in the file name of the sprite sheet. """

        file_path = get_path_name("images", filename)
        self.sprite_sheet = pygame.image.load(file_path).convert_alpha()
        #self.sprite_sheet.set_alpha(255)

    def get_image(self, col, row, width, height, scale=1, x=-1, y=-1, use_topleft=False):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert_alpha()

        # Copy the sprite from the large sheet onto the smaller image
        if x != -1 and y != -1:
            image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        else:
            image.blit(self.sprite_sheet, (0, 0), (col * width, row * height, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey((255, 255, 255))
        if use_topleft:
            # Use top left of image for transparent color
            transparent_color = image.get_at((0, 0))
            image.set_colorkey(transparent_color)

        if scale != 1:
            width = int(width * scale)
            height = int(height * scale)
            image = pygame.transform.scale(image, (width, height))

        # Return the image
        return image

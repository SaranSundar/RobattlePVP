"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame


class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, col, row, width, height, scale=1, x=-1, y=-1):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        if x != -1 and y != -1:
            image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        else:
            image.blit(self.sprite_sheet, (0, 0), (col * width, row * height, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey((255, 255, 255))

        if scale != 1:
            width = int(width * scale)
            height = int(height * scale)
            image = pygame.transform.scale(image, (width, height))

        # Return the image
        return image

    def get_images(self, x, y, width, height, scale, frames):
        images = []
        for i in range(frames):
            image = self.get_image(-1, -1, width, height, scale, x + (width * i), y)
            images.append(image)
        return images

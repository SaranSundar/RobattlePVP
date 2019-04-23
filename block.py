import pygame

from animation import get_collision_image


def mask_from_surface(surface, threshold=127):
    # return pygame.mask.from_surface(surface, threshold)

    mask = pygame.mask.Mask(surface.get_size())
    key = surface.get_colorkey()
    if key:
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                if surface.get_at((x + 0.1, y + 0.1)) != key:
                    mask.set_at((x, y), 1)
    else:
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                if surface.get_at((x, y))[3] > threshold:
                    mask.set_at((x, y), 1)
    return mask


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, can_collide):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.can_collide = can_collide
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collision_image = get_collision_image(image)[0]
        # self.rect = self.collision_image.get_rect()
        self.mask = pygame.mask.from_surface(self.collision_image)  # mask_from_surface(self.image,
        # threshold=constants.ALPHA_THRESHOLD)  # pygame.mask.from_surface(self.image)

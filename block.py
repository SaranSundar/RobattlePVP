import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, image, can_collide):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.can_collide = can_collide

        if image is not None:
            self.image = image
        else:
            self.image = pygame.Surface([width, height])
            self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

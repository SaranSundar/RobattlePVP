import pygame


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
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        self.rect = self.rect.clamp(surface.get_rect())
        surface.blit(self.image, self.rect)

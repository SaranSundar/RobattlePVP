import pygame

from animation import get_collision_image


class Projectile(pygame.sprite.Sprite):

    def __init__(self, image, x, y, velocity, dmg, direction, name):
        super().__init__()
        self.image = image
        self.collision_image = get_collision_image(image)[0]
        self.rect = self.collision_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_name = name
        self.velocity = -velocity if direction == "l" else velocity
        self.dmg = dmg
        self.collided = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.velocity

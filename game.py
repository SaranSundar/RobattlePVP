import sys

import pygame

import constants
from world import World

pygame.init()
screen = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])


def main():
    pygame.display.set_caption("Robattle Tournament")
    world = World()
    world.run(screen)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

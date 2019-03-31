import sys

import pygame

import constants
from world import World

pygame.init()
screen = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])


def main():
    pygame.display.set_caption("Walls and Rooms")
    world = World()
    clock = pygame.time.Clock()

    done = False
    while not done:
        # --- Event Processing ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                world.key_down(event.key)
            elif event.type == pygame.KEYUP:
                world.key_up(event.key)
        # --- Game Logic ---
        world.update()
        # --- Drawing ---
        world.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

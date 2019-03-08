# Screen dimensions
import queue
import sys

import pygame

from robattle_pygame.arena import Arena
from robattle_pygame.player import Player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def launch_game(server_queue=queue.Queue()):
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Robattle Tournament")
    arena = Arena("Arena1.txt")

    # Create the player
    player = Player()
    player.arena = arena

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    active_sprites = pygame.sprite.Group()
    active_sprites.add(player)

    server_message = {}

    # -------- Main Program Loop -----------
    while not done:
        new_message = player.get_json_values()
        if server_message != new_message:
            server_message = new_message
            server_queue.put(server_message)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                player.keydown(event.key)

            if event.type == pygame.KEYUP:
                player.keyup(event.key)

        active_sprites.update()
        arena.update()

        arena.draw(screen)
        active_sprites.draw(screen)

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    launch_game()

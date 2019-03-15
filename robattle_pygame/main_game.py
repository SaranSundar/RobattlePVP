# Screen dimensions
import queue
import sys
from threading import Thread

import pygame

from robattle_pygame.arena import Arena
from robattle_pygame.player import Player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

endgame = False

players = {}
arena = None


def get_other_players(player_queue):
    global players
    global arena
    while not endgame:
        player_data = player_queue.get()
        key = str(player_data['ip']) + str(player_data['port'])
        if key in players:
            player = players[key]
        else:
            player = Player(-1, -1)
        player.set_json_values(player_data)
        players[key] = player


def launch_game(server_queue=queue.Queue(), ip='127.0.0.1', port='8080', player_queue=queue.Queue()):
    global endgame
    global players
    global arena
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Robattle Tournament")
    arena = Arena("Arena1.txt")

    # Create the player
    player = Player(ip, port)
    player.arena = arena

    # Loop until the user clicks the close button.
    endgame = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    active_sprites = pygame.sprite.Group()
    active_sprites.add(player)

    server_message = {}

    Thread(target=get_other_players, args=(player_queue,)).start()

    # -------- Main Program Loop -----------
    while not endgame:
        new_message = player.get_json_values()
        if server_message != new_message:
            server_message = new_message
            server_queue.put(server_message)
        # if player_queue.get_nowait():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endgame = True

            if event.type == pygame.KEYDOWN:
                player.keydown(event.key)

            if event.type == pygame.KEYUP:
                player.keyup(event.key)

        active_sprites.empty()
        active_sprites.add(player)
        player.arena = arena
        for key, val in players.items():
            val.arena = arena
            active_sprites.add(val)

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

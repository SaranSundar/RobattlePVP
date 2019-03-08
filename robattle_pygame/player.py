import msgpack
import pygame

from robattle_pygame.spritesheet_functions import SpriteSheet

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)


def clock():
    current_time = pygame.time.get_ticks()
    return current_time


class Player(pygame.sprite.Sprite):
    # -- Methods
    def __init__(self, id):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        # IDLE GETTING READY TO FIGHT ANIMATION
        # width = 41
        # height = 55
        # offset_x = 7
        # offset_y = 10
        # self.frame_count = 6

        # WALK ANIMATION
        width = 35
        height = 53
        offset_x = 5
        offset_y = 80
        self.frame_count = 8

        # RUN ANIMATION
        # width = 46
        # height = 53
        # offset_x = 7
        # offset_y = 144
        # self.frame_count = 6

        spritesheet = SpriteSheet("metabee_spritesheet.png")
        scale = 1.75
        self.frame = 0
        self.animation_speed = self.frame_count * 10  # ms
        # Col and Row Dont Matter Here, X & Y Override It.
        self.images = spritesheet.get_images(offset_x, offset_y, width, height, scale, self.frame_count,
                                             use_topleft=True)

        # Start facing Right
        self.image = self.images[0][0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        self.rect.x = 200
        self.rect.y = 200

        # Set speed vector of player
        self.delta_x = 2
        self.delta_y = 2

        self.right = False
        self.left = False
        self.up = False
        self.down = False

        # Give reference to current arenas blocks
        self.arena = None
        self.timeOfNextFrame = clock()

        self.id = id

    def get_json_values(self):
        state = {
            'id': self.id,
            'frame_count': self.frame_count,
            'frame': self.frame,
            'animation_speed': self.animation_speed,
            'x': self.rect.x,
            'y': self.rect.y,
            'width': self.rect.width,
            'height': self.rect.height,
            'delta_x': self.delta_x,
            'delta_y': self.delta_y,
            'right': self.right,
            'left': self.left,
            'up': self.up,
            'down': self.down,
        }
        return msgpack.packb(state)

    def keydown(self, key):
        if key == pygame.K_LEFT:
            self.left = True
        if key == pygame.K_RIGHT:
            self.right = True
        if key == pygame.K_UP:
            self.up = True
        if key == pygame.K_DOWN:
            self.down = True

    def keyup(self, key):
        if key == pygame.K_LEFT:
            self.left = False
        if key == pygame.K_RIGHT:
            self.right = False
        if key == pygame.K_UP:
            self.up = False
        if key == pygame.K_DOWN:
            self.down = False

    def animate_sprite(self, direction):
        if clock() > self.timeOfNextFrame:  # We only animate our character every 60ms.
            self.frame = (self.frame + 1) % self.frame_count  # There are 6 frames of animation in each direction
            self.timeOfNextFrame += self.animation_speed  # so the modulus allows it to loop
            if direction == "r":
                self.image = self.images[self.frame][0]
            elif direction == "l":
                self.image = self.images[self.frame][1]

    def reset_clock(self):
        self.timeOfNextFrame = clock()
        self.frame = 0
        self.image = self.images[self.frame][0]

    def update(self):
        """ Move the player. """
        # Move left/right
        if self.right:
            self.rect.x += self.delta_x
            self.animate_sprite("r")
        elif self.left:
            self.rect.x -= self.delta_x
            self.animate_sprite("l")
        else:
            self.reset_clock()

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.arena.collision_blocks, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.right:
                self.rect.right = block.rect.left
            elif self.left:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
        """ Move the player. """
        if self.up:
            self.rect.y -= self.delta_y
        elif self.down:
            self.rect.y += self.delta_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.arena.collision_blocks, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.up:
                self.rect.top = block.rect.bottom
            elif self.down:
                self.rect.bottom = block.rect.top

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
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 41
        height = 55
        offset_x = 7
        offset_y = 10
        spritesheet = SpriteSheet("metabee_spritesheet.png")
        scale = 1.75
        self.frame_count = 6
        self.frame = 0
        # Col and Row Dont Matter Here, X & Y Override It.
        self.images = spritesheet.get_images(offset_x, offset_y, width, height, scale, self.frame_count)
        self.image = self.images[0]  # spritesheet.get_image(-1, -1, width, height, scale, offset_x, offset_y)

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        self.rect.x = 50
        self.rect.y = 50

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

    def animate_sprite(self):
        if clock() > self.timeOfNextFrame:  # We only animate our character every 60ms.
            self.frame = (self.frame + 1) % self.frame_count  # There are 6 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus allows it to loop
            self.image = self.images[self.frame]

    def reset_clock(self):
        self.timeOfNextFrame = clock()
        self.frame = 0
        self.image = self.images[self.frame]

    def update(self):
        """ Move the player. """
        # Move left/right
        if self.right:
            self.rect.x += self.delta_x
            self.animate_sprite()
        elif self.left:
            self.rect.x -= self.delta_x
            self.animate_sprite()
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

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)


class Player(pygame.sprite.Sprite):
    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.delta_x = 5
        self.delta_y = 5

        self.right = False
        self.left = False
        self.up = False
        self.down = False

        # Give reference to current arenas blocks
        self.arena = None

    def update(self):
        """ Move the player. """
        # Move left/right
        if self.right:
            self.rect.x += self.delta_x
        if self.left:
            self.rect.x -= self.delta_x
        if self.up:
            self.rect.y -= self.delta_y
        if self.down:
            self.rect.y += self.delta_y

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

        # Move up/down
        self.rect.y += self.delta_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.arena.collision_blocks, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.up:
                self.rect.bottom = block.rect.top
            elif self.down:
                self.rect.top = block.rect.bottom

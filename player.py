import math
import time

import pygame

import constants


class Player(pygame.sprite.Sprite):
    right = False
    left = False
    up = False
    down = False
    scale = 1.75

    def __init__(self, x, y, w, h):
        super().__init__()
        # self.image = pygame.image.load("metabee_spritesheet.png").convert()
        self.image = pygame.Surface([w, h])
        self.image.fill(constants.TEAL)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set speed vector of player
        self.delta_x = 5
        self.delta_y = 5
        self.room = None

        # Variables for knock back
        self.weight = 100  # kg
        self.damage_taken = 0.0
        self.gravity = .35
        self.time_override = int(round(time.time() * 1000))
        self.should_override = False
        self.x_velocity = 0
        self.y_velocity = 0

    def key_down(self, key):
        if key == pygame.K_LEFT:
            self.left = True
        elif key == pygame.K_RIGHT:
            self.right = True
        elif key == pygame.K_UP:
            self.up = True
            self.jump()
        elif key == pygame.K_DOWN:
            self.down = True
        elif key == pygame.K_SPACE:
            self.apply_damage()

    def key_up(self, key):
        if key == pygame.K_LEFT:
            self.left = False
        elif key == pygame.K_RIGHT:
            self.right = False
        elif key == pygame.K_UP:
            self.up = False
        elif key == pygame.K_DOWN:
            self.down = False

    def set_room(self, room):
        self.room = room

    def apply_damage(self, dmg=1, base_knock_back=5, angle=(7 * math.pi / 4)):
        angle = -angle
        # Knock-back calculations applied after applying the damage taken
        self.damage_taken += dmg

        # Calculate knock-back
        knock_back = base_knock_back + dmg

        # Calculate velocity and time (milliseconds)
        self.x_velocity = knock_back * math.cos(angle)
        self.y_velocity = knock_back * math.sin(angle)
        lockout_time = 500
        current_milli_sec = int(round(time.time() * 1000))
        self.time_override = current_milli_sec + lockout_time
        self.should_override = True

    # Use booleans for movement and update based on booleans in update method
    def update(self):
        if self.should_override:
            current_milli_sec = int(round(time.time() * 1000))
            if current_milli_sec >= self.time_override:
                self.should_override = False
        else:
            # Gravity
            self.calc_gravity()

        """ Move the player. """

        # Move left/right
        if self.should_override:
            self.rect.x += self.x_velocity
        else:
            if self.right:
                self.rect.x += self.delta_x
            elif self.left:
                self.rect.x -= self.delta_x

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.right:
                self.rect.right = block.rect.left
            elif self.left:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # # Move up/down
        if self.should_override:
            self.rect.y += self.y_velocity
        else:
            self.rect.y += self.delta_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.should_override:
                if self.y_velocity > 0:
                    self.rect.bottom = block.rect.top
                elif self.y_velocity < 0:
                    self.rect.top = block.rect.bottom
                # Stop our vertical movement
                self.y_velocity = 0

            else:
                if self.delta_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.delta_y < 0:
                    self.rect.top = block.rect.bottom
                # Stop our vertical movement
                self.delta_y = 0

    def calc_gravity(self):
        """ Calculate effect of gravity. """
        if self.delta_y == 0:
            self.delta_y = 1
        else:
            self.delta_y += self.gravity

        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.delta_y >= 0:
            self.delta_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.delta_y = -10

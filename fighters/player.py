import math
import pickle
import time

import pygame

import constants
from animation import Animation


class Player(pygame.sprite.Sprite):
    right = False
    left = False
    up = False
    down = False
    space = False
    attack1 = False
    attack2 = False
    attack3 = False
    attack4 = False
    on_ground = False
    last_press = "r"
    scale = 1.75

    def __init__(self, x, y, unique_id, spritesheet, hitbox, animations):
        super().__init__()
        self.unique_id = unique_id
        # Animation setup
        self.animation = Animation(spritesheet, hitbox, animations, scale=1.5, animation_name="Idle")
        self.animation.update_animation("Idle")
        self.image, collision_image, self.mask = self.animation.get_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set speed vector of player
        self.delta_x = 5
        self.delta_y = 0
        self.room = None

        # Variables for knock back
        self.weight = 100  # kg
        self.damage_taken = 0.0
        self.max_hp = 100
        self.gravity = 0.35
        self.time_override = int(round(time.time() * 1000))
        self.should_override = False
        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color("red"), (self.rect.x, self.rect.y - 12, self.rect.width, 10))
        health = int(
            max(min((self.max_hp - self.damage_taken) / float(self.max_hp) * self.rect.width, self.rect.width), 0))
        if health != 0:
            pygame.draw.rect(surface, pygame.Color("green"), (self.rect.x, self.rect.y - 12, health, 10))
        surface.blit(self.image, self.rect)

    def new_player(self, _dict):
        self.__dict__.update(_dict)

    def pickle_sprite(self):
        # Doesnt do deep copy which can cause some issues if you change copy variables
        copy = self.__dict__.copy()
        del copy["image"]
        del copy["mask"]
        del copy["room"]
        del copy["_Sprite__g"]
        p = Player(0, 0)
        p.new_player(copy)
        copy = pickle.dumps(copy)
        print(copy)

    def process_keys(self, keys):
        self.down = keys[pygame.K_DOWN]
        self.up = keys[pygame.K_UP]
        self.right = keys[pygame.K_RIGHT]
        self.left = keys[pygame.K_LEFT]
        self.space = keys[pygame.K_SPACE]
        self.attack1 = keys[pygame.K_q]
        self.attack2 = keys[pygame.K_w]
        self.attack3 = keys[pygame.K_e]
        self.attack4 = keys[pygame.K_r]
        if self.right:
            self.last_press = "r"
        elif self.left:
            self.last_press = "l"
        if self.up:
            self.jump()
        if self.space:
            # self.pickle_sprite()
            self.apply_damage()
        # print(self.up)

    def set_room(self, room):
        self.room = room

    def apply_damage(self, dmg=1, base_knock_back=5, angle=(math.pi / 4)):
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

    def choose_animation(self):
        # WRITE CODE TO DECIDE WHAT ANIMATION TO CHOOSE ALL IN THIS ONE METHOD THEN CALL IN UPDATE
        # Were on the ground
        # print(self.single_jump, self.right, self.left)
        # single jump is true or false, but left and right are 1 or 0
        if self.attack1:
            self.animation.update_animation("Attack-1")
        elif self.attack2:
            self.animation.update_animation("Attack-2")
        elif self.attack3:
            self.animation.update_animation("Attack-3")
        elif self.attack4:
            self.animation.update_animation("Attack-4")
        elif self.on_ground:
            if not self.right and not self.left:
                self.animation.update_animation("Idle")
            elif self.right or self.left:
                self.animation.update_animation("Walking")
        elif not self.on_ground:
            # Were jumping
            # print(self.delta_y)
            if self.delta_y < 0:
                self.animation.update_animation("Jumping")
            elif self.delta_y > 2:
                self.animation.update_animation("Falling")

    # Use booleans for movement and update based on booleans in update method
    def update(self, players):
        locked_image, collision_image, collision_mask = self.animation.get_image(self.last_press)
        self.image = collision_image
        self.mask = collision_mask
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
        block_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False,
                                                     pygame.sprite.collide_mask)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.right:
                # self.rect.x -= self.delta_x
                self.rect.right = block.rect.left
            elif self.left:
                # self.rect.x += self.delta_x
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # # Move up/down
        if self.should_override:
            self.rect.y += self.y_velocity
        else:
            self.rect.y += self.delta_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False,
                                                     pygame.sprite.collide_mask)

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
                    self.on_ground = True
                    self.rect.bottom = block.rect.top
                elif self.delta_y < 0:
                    self.on_ground = True
                    self.rect.bottom = block.rect.top
                # self.rect.top = block.rect.bottom
                # Stop our vertical movement
                self.delta_y = 0

        # Assume this is you attacking another player
        for key in players:
            if players[key] != self:
                player_hit = pygame.sprite.collide_rect(self, players[key])
                if player_hit:
                    players[key].apply_damage()

        # Player bounds
        if self.rect.right >= constants.SCREEN_WIDTH:
            self.rect.right = constants.SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

        self.image = collision_image
        self.choose_animation()
        self.animation.update_frame()

    def calc_gravity(self):
        """ Calculate effect of gravity. """
        if self.delta_y == 0:
            self.delta_y = 1
        else:
            self.delta_y += self.gravity

        # See if we are on the very bottom edge of the screen
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.delta_y >= 0:
            self.delta_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False,
                                                        pygame.sprite.collide_mask)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.left = False
            self.right = False
            self.on_ground = False
            self.delta_y = -11
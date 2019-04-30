import math
import pickle
import time

import pygame

import constants
from animation import Animation, get_collision_image, clock
from fighters.projectile import Projectile


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, unique_id, spritesheet, hitbox, animations, keys, scale=1.5, disable_second=False):
        super().__init__()
        self.set_init_variables()
        self.scale = scale
        self.unique_id = unique_id
        self.name = spritesheet.split("/")[0]
        # Animation setup
        self.animation = Animation(spritesheet, hitbox, animations, scale, animation_name="Idle")
        self.animation_name = "Idle"
        self.animation.update_animation(self.animation_name)
        self.image, collision_image, self.mask = self.animation.get_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.keys = keys

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
        self.disable_second = disable_second

        self.projectiles = []

        # Attack Settings
        self.attack_info = {}
        self.set_attack_info()

    def set_init_variables(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.space = False
        self.attack1 = False
        self.attack2 = False
        self.attack3 = False
        self.attack4 = False
        self.on_ground = False
        self.attack_interval = 1000
        self.attack_time = clock()
        self.last_press = "r"
        self.scale = 1.75

    # This method needs to be overridden in every fighters class
    def set_attack_info(self):
        pass
        # Angles should all be right facing and in radians, can be flipped when applying damage
        # self.create_attack("Attack-1", dmg=3, angle=math.pi / 8)
        # self.create_attack("Attack-2", dmg=3, angle=math.pi / 4)
        # self.create_attack("Attack-3")
        # self.create_attack("Attack-4")

    # Knock back time in ms
    def create_attack(self, attack_name, angle=0.0, dmg=1, bs_kbk=5, kbk_time=500):
        self.attack_info[attack_name] = {'angle': angle, 'dmg': dmg, 'bs_kbk': bs_kbk, 'kbk_time': kbk_time}

    def draw(self, surface, font, position=(1, 2)):  # Player order, Total players
        # DRAWS PLAYERS HEALTH BAR
        pygame.draw.rect(surface, pygame.Color("red"), (self.rect.x, self.rect.y - 12, self.rect.width, 10))
        health = int(
            max(min((self.max_hp - self.damage_taken) / float(self.max_hp) * self.rect.width, self.rect.width), 0))
        if health != 0:
            pygame.draw.rect(surface, pygame.Color("green"), (self.rect.x, self.rect.y - 12, health, 10))
        # DRAWS ICON AT BOTTOM FOR STATUS
        icon = self.animation.sprites["Icon"][0][0]
        icon = pygame.transform.scale(icon, (65, 65))
        padding = constants.SCREEN_WIDTH / 5
        box_x = (constants.SCREEN_WIDTH / position[1]) * position[0] + padding
        box_y = constants.SCREEN_HEIGHT - icon.get_height() - 25
        # DRAWS PLAYER
        surface.blit(icon, (box_x, box_y, icon.get_width(), icon.get_height()))
        surface.blit(self.image, self.rect)

        self.draw_projectiles(surface)
        # DRAWS NAME AND DAMAGE
        name_text = font.render(self.name, False, (0, 0, 0))
        surface.blit(name_text, (box_x, box_y + icon.get_height()))
        damage_text = font.render(str(self.damage_taken) + "%", False, (0, 0, 0))
        surface.blit(damage_text, (box_x + icon.get_width() + 10, box_y + icon.get_height() / 2))

    def draw_projectiles(self, surface):
        for projectile in self.projectiles:
            projectile.draw(surface)

    def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.update()
            if projectile.rect.x >= constants.SCREEN_WIDTH:
                self.projectiles.remove(projectile)
            elif projectile.rect.x + projectile.rect.width <= 0:
                self.projectiles.remove(projectile)
            elif projectile.collided:
                self.projectiles.remove(projectile)

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
        # Keys return 1 if true and 0 if false
        self.down = keys[self.keys['down']]
        self.up = keys[self.keys['up']]
        self.right = keys[self.keys['right']]
        self.left = keys[self.keys['left']]
        self.space = keys[self.keys['space']]
        self.attack1 = keys[self.keys['attack1']]
        self.attack2 = keys[self.keys['attack2']]
        self.attack3 = keys[self.keys['attack3']]
        self.attack4 = keys[self.keys['attack4']]

    def set_room(self, room):
        self.room = room

    def apply_damage(self, enemy_attack_info, angle):
        dmg = enemy_attack_info['dmg']
        bs_kbk = enemy_attack_info['bs_kbk']
        kbk_time = enemy_attack_info['kbk_time']
        angle = -angle
        # Knock-back calculations applied after applying the damage taken
        self.damage_taken += dmg

        # Calculate knock-back
        knock_back = bs_kbk

        # Calculate velocity and time (milliseconds)
        self.x_velocity = knock_back * math.cos(angle)
        self.y_velocity = knock_back * math.sin(angle)
        current_milli_sec = int(round(time.time() * 1000))
        self.time_override = current_milli_sec + kbk_time
        self.should_override = True

    def add_projectile(self, attack_name, attack_interval, animation_name):
        if clock() > self.attack_time:
            self.attack_interval = attack_interval
            self.attack_time = clock() + self.attack_interval
            self.projectiles.append(Projectile(self.animation.get_attack_image(attack_name, self.last_press),
                                               self.rect.x, self.rect.y + self.rect.height / 2, 7,
                                               self.last_press, animation_name))
            return True
        return False

    def choose_animation(self):
        animation_name = "Idle"
        if self.attack1:
            animation_name = "Attack-1"
            self.add_projectile("Projectile-1", 500, animation_name)
        elif self.attack2:
            animation_name = "Attack-2"
            self.add_projectile("Projectile-2", 200, animation_name)
        elif self.attack3 and not self.disable_second:
            animation_name = "Attack-3"
            self.add_projectile("Projectile-3", 350, animation_name)
        elif self.attack4 and not self.disable_second:
            animation_name = "Attack-4"
            self.add_projectile("Projectile-4", 1000, animation_name)
        elif self.on_ground:
            if not self.right and not self.left:
                animation_name = "Idle"
            elif self.right or self.left:
                animation_name = "Running"
        elif not self.on_ground:
            # Were jumping
            if self.delta_y < 0:
                animation_name = "Jumping"
            elif self.delta_y > 2:
                animation_name = "Falling"
        self.animation_name = animation_name
        self.animation.update_animation(self.animation_name)

    # Use booleans for movement and update based on booleans in update method
    def update(self, players):
        if self.right:
            self.last_press = "r"
        elif self.left:
            self.last_press = "l"
        locked_image, collision_image, collision_mask = self.animation.get_image(self.last_press)
        black_image, x_off, y_off, contrast_image = get_collision_image(collision_image)
        self.image = black_image
        curr_x = self.rect.x
        curr_y = self.rect.y
        curr_w = self.rect.width
        curr_h = self.rect.height
        # self.rect.x += curr_x + x_off
        # self.rect.y += y_off
        self.rect.width = black_image.get_width()
        self.rect.height = black_image.get_height()
        self.mask = collision_mask
        if self.up:
            self.jump()
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
        shift_lr = len(block_hit_list) > 0
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
        block_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False)
        shift_ud = len(block_hit_list) > 0
        # print("bot", self.rect.bottom)
        # print("delta", self.delta_y)

        for block in block_hit_list:
            # print("collision")
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
                    # print("top", block.rect.top)
                elif self.delta_y < 0:
                    self.on_ground = True
                    self.rect.bottom = block.rect.top
                # self.rect.top = block.rect.bottom
                # Stop our vertical movement
                self.delta_y = 0

        # Player bounds
        if self.rect.right >= constants.SCREEN_WIDTH:
            self.rect.right = constants.SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

        # Assume this is another player attacking you
        for key in players:
            enemy = players[key]  # type: Player
            if enemy.unique_id != self.unique_id:
                if "Attack" in enemy.animation_name:
                    if pygame.sprite.collide_rect(self, enemy):
                        enemy_attack_info = enemy.attack_info[enemy.animation_name]
                        angle = enemy_attack_info['angle']
                        if enemy.last_press is "l":
                            angle = math.pi - angle
                        self.apply_damage(enemy_attack_info, angle)
                for projectile in enemy.projectiles:
                    if pygame.sprite.collide_rect(self, projectile):
                        proj_info = enemy.attack_info[projectile.animation_name]
                        angle = proj_info['angle']
                        if projectile.velocity < 0:
                            angle = math.pi - angle
                        self.apply_damage(proj_info, angle)
                        projectile.collided = True

        # self.image = collision_image
        # self.rect.x = curr_x
        # self.rect.y = curr_y
        # if not shift_lr:
        #     self.rect.x -= x_off
        # if not shift_ud:
        #     self.rect.y -= y_off
        # if not shift_lr and not shift_ud:
        #     self.rect.x -= x_off
        #     self.rect.y -= y_off
        self.rect.width = curr_w
        self.rect.height = curr_h
        self.image = locked_image
        self.choose_animation()
        self.animation.update_frame()

        self.update_projectiles()

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
        platform_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.left = False
            self.right = False
            self.on_ground = False
            self.delta_y = -11

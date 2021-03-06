import pygame

import constants
from animation import Animation
from spritesheet_functions import get_path_name


class CountDown(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation = Animation("Timer_SpriteSheet.png", "Timer_SpriteSheet.png", "Timer.txt", 1, "Idle")
        self.image, collision_image, self.mask = self.animation.get_image()
        self.rect = self.image.get_rect()
        self.rect.x = constants.SCREEN_WIDTH / 2 - self.rect.width / 2.25
        self.rect.y = constants.SCREEN_HEIGHT / 2 - self.rect.height * 1.25
        self.animation_done = False
        self.prev_animation_frame = 0
        pygame.mixer.music.load(get_path_name("media", "announcer.mp3"))
        pygame.mixer.music.play(0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_game_over(self, surface, name):
        img = pygame.image.load(get_path_name("images", name))
        surface.blit(img, self.rect)

    def should_countdown(self, reset=False):
        if reset:
            self.animation.calculate_animation_speed()
            self.animation_done = False
        return self.animation_done

    def update(self):
        if self.animation.current_frame == 0:
            if self.prev_animation_frame != self.animation.current_frame:
                self.animation_done = True
                pygame.mixer.music.load(get_path_name("media", "background_music.mp3"))
                pygame.mixer.music.play(-1)
        locked_image, collision_image, collision_mask = self.animation.get_image()
        self.image = locked_image
        self.prev_animation_frame = self.animation.current_frame,
        self.animation.update_frame()

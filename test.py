import pygame as pg

from spritesheet_functions import get_path_name, SpriteSheet

TRANSPARENT = (0, 0, 0, 0)
BACKGROUND_COLOR = pg.Color("slategray")


class Player(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(Player, self).__init__(*groups)
        self.pos = pos
        spritesheet = SpriteSheet("tiles_spritesheet.png")
        file_path = get_path_name("images", "block.png")
        # self.image = pg.Surface((100, 100)).convert_alpha()
        self.image = spritesheet.get_image(2, 0, 70, 70, 1)  # pg.image.load(file_path).convert_alpha()
        # self.image.fill(TRANSPARENT)
        # pg.draw.polygon(self.image, (0, 255, 0), [(50, 0), (100, 50), (50, 100), (0, 50)])
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pg.mask.from_surface(self.image)

    def get_event(self, key):
        if key[pg.K_DOWN]:
            self.rect.y += 1
        if key[pg.K_UP]:
            self.rect.y -= 1
        if key[pg.K_LEFT]:
            self.rect.x -= 1
        if key[pg.K_RIGHT]:
            self.rect.x += 1

    def draw(self, surface):
        self.rect = self.rect.clamp(surface.get_rect())
        surface.blit(self.image, self.rect)


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(Enemy, self).__init__(*groups)
        self.pos = pos
        file_path = get_path_name("images", "block2.png")
        self.image = pg.image.load(file_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (100, 100))
        # self.image = pg.Surface((100, 100)).convert_alpha()
        # self.image.fill(TRANSPARENT)
        # pg.draw.circle(self.image, (0, 0, 255), (50, 50), 50)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pg.mask.from_surface(self.image)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((640, 480))
        self.player = Player((150, 150))
        self.enemies = pg.sprite.Group()
        Enemy((320, 240), self.enemies)
        self.done = False
        self.fps = 60.0
        self.clock = pg.time.Clock()

    def event_loop(self):
        key = pg.key.get_pressed()
        self.player.get_event(key)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def check_collide(self):
        if pg.sprite.spritecollide(self.player, self.enemies, False, pg.sprite.collide_mask):
            pg.display.set_caption('collide')
        else:
            pg.display.set_caption('do not collide')

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.player.draw(self.screen)
        self.enemies.draw(self.screen)

    def run(self):
        while not self.done:
            self.event_loop()
            self.draw()
            self.check_collide()
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    pg.init()
    game = Game()
    game.run()
    pg.quit()

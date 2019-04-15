from fighters.player import Player


class TestDummy(Player):
    def __init__(self, x, y, unique_id):
        super().__init__(x, y, unique_id, "Metabee/Metabee_SpriteSheet.png", "Metabee/Metabee_Hitbox.png",
                         "Metabee.txt")

    def process_keys(self, keys):
        # self.down = keys[pygame.K_DOWN]
        # self.up = keys[pygame.K_UP]
        # self.right = keys[pygame.K_RIGHT]
        # self.left = keys[pygame.K_LEFT]
        # self.space = keys[pygame.K_SPACE]
        # self.attack1 = keys[pygame.K_q]
        # self.attack2 = keys[pygame.K_w]
        # self.attack3 = keys[pygame.K_e]
        # self.attack4 = keys[pygame.K_r]
        self.attack1 = 1

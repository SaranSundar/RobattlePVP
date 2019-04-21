from fighters.player import Player


class Metabee(Player):
    def __init__(self, x, y, unique_id):
        super().__init__(x, y, unique_id, "Metabee/Metabee_SpriteSheet.png", "Metabee/Metabee_Hitbox_Red.png",
                         "Metabee.txt", scale=1.5)

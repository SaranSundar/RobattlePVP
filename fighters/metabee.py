from fighters.player import Player


class Metabee(Player):
    def __init__(self, x, y, unique_id, keys):
        super().__init__(x, y, unique_id, "Metabee/Metabee_SpriteSheet.png", "Metabee/Metabee_Hitbox.png",
                         "Metabee.txt", keys, scale=1.5, disable_second=True)

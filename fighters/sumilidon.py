from fighters.player import Player


class Sumilidon(Player):
    def __init__(self, x, y, unique_id):
        super().__init__(x, y, unique_id, "Sumilidon/Sumilidon_SpriteSheet.png", "Sumilidon/Sumilidon_Hitbox.png",
                         "Sumilidon.txt", scale=1.5)

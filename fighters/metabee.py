import math

from fighters.player import Player


class Metabee(Player):
    def __init__(self, x, y, unique_id, keys):
        super().__init__(x, y, unique_id, "Metabee/Metabee_SpriteSheet.png", "Metabee/Metabee_Hitbox.png",
                         "Metabee.txt", keys, scale=1.5, disable_second=True)

        # This method needs to be overridden in every fighters class

    def set_attack_info(self):
        # Angles should all be right facing and in radians, can be flipped when applying damage
        self.create_attack("Attack-1", kbk_time=500, dmg=12, angle=math.pi / 8)
        self.create_attack("Attack-2", kbk_time=200, dmg=9, angle=math.pi / 4)
        self.create_attack("Attack-3")
        self.create_attack("Attack-4")

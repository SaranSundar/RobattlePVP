from fighters.player import Player


class Metabee(Player):
    def __init__(self, x, y, unique_id):
        super().__init__(x, y, unique_id, "Metabee/Metabee_SpriteSheet.png", "Metabee/Metabee_Hitbox.png",
                         "Metabee.txt")

    def choose_animation(self):
        # WRITE CODE TO DECIDE WHAT ANIMATION TO CHOOSE ALL IN THIS ONE METHOD THEN CALL IN UPDATE
        # Were on the ground
        # print(self.single_jump, self.right, self.left)
        # single jump is true or false, but left and right are 1 or 0
        if self.attack1:
            self.animation.update_animation("Attack-1")
        elif self.attack2:
            self.animation.update_animation("Attack-2")
        # elif self.attack3:
        #     self.animation.update_animation("Attack-3")
        # elif self.attack4:
        #     self.animation.update_animation("Attack-4")
        elif self.on_ground:
            if not self.right and not self.left:
                self.animation.update_animation("Walking")
            elif self.right or self.left:
                self.animation.update_animation("Idle")
        elif not self.on_ground:
            # Were jumping
            # print(self.delta_y)
            if self.delta_y < 0:
                self.animation.update_animation("Jumping")
            elif self.delta_y > 2:
                self.animation.update_animation("Falling")

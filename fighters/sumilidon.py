from animation import clock
from fighters.player import Player
from fighters.projectile import Projectile


class Sumilidon(Player):
    def __init__(self, x, y, unique_id):
        super().__init__(x, y, unique_id, "Sumilidon/Sumilidon_SpriteSheet.png", "Sumilidon/Sumilidon_Hitbox.png",
                         "Sumilidon.txt", scale=1.5, disable_second=True)

    def add_projectile(self, attack_name, attack_interval):
        if clock() > self.attack_time:
            self.attack_interval = attack_interval
            self.attack_time = clock() + self.attack_interval
            if attack_name == "Projectile-1":
                self.projectiles.append(Projectile(self.animation.get_attack_image(attack_name, self.last_press),
                                                   self.rect.x, self.rect.y + self.rect.height / 2, 7, 1,
                                                   self.last_press))
            elif attack_name == "Projectile-2":
                self.projectiles.append(Projectile(self.animation.get_attack_image(attack_name, self.last_press),
                                                   self.rect.x, self.rect.y, 7, 1,
                                                   self.last_press))

    def choose_animation(self):
        animation_name = "Idle"
        if self.attack1:
            animation_name = "Attack-1"
            self.add_projectile("Projectile-1", 500)
        elif self.attack2:
            animation_name = "Attack-2"
            self.add_projectile("Projectile-2", 1000)
        elif self.attack3 and not self.disable_second:
            animation_name = "Attack-3"
            self.add_projectile("Projectile-3", 350)
        elif self.attack4 and not self.disable_second:
            animation_name = "Attack-4"
            self.add_projectile("Projectile-4", 1000)
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

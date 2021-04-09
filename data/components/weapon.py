class Weapon:
    def get_name(self):
        return self.name


class Uzi(Weapon):
    damage = 20
    delay = 150
    initial_ammo = 150
    max_ammo = 150
    name = "Uzi"
    bullet_image_index = 32
    image_index = 6


class AK47(Weapon):
    damage = 30
    delay = 300
    initial_ammo = 30
    max_ammo = 40
    name = "AK47"
    bullet_image_index = 39
    image_index = 7


class Shotgun(Weapon):
    damage = 40
    delay = 550
    initial_ammo = 10
    max_ammo = 20
    name = "Shotgun"
    bullet_image_index = 48
    image_index = 8
"""
Module that contains weapons' characteristics
"""

class Weapon:
    """
    The base class for a weapon
    """
    def __init__(self):
        self.damage = None
        self.delay = None
        self.initial_ammo = None
        self.max_ammo = None
        self.name = None
        self.bullet_image_index = None
        self.image_index = None

    def get_damage(self):
        """
        Returns weapon's damage
        """
        return self.damage

    def get_delay(self):
        """
        Returns the delay in milliseconds between two consecutives shots
        """
        return self.delay

    def get_initial_ammo(self):
        """
        Returns weapon's initial ammo
        """
        return self.initial_ammo

    def get_max_ammo(self):
        """
        Returns weapon's max ammo
        """
        return self.max_ammo

    def get_name(self):
        """
        Returns weapon's name
        """
        return self.name

    def get_bullet_image_index(self):
        """
        Returns the index of the weapon's bullet at the bullets' spritesheet
        """
        return self.bullet_image_index

    def get_image_index(self):
        """
        Returns the index of the weapon's sprite at the itens' spritesheet
        """
        return self.image_index


class Uzi(Weapon):
    """
    The submachine used by main character.
    """
    def __init__(self):
        self.damage = 25
        self.delay = 120
        self.initial_ammo = 150
        self.max_ammo = 200
        self.name = "Uzi"
        self.bullet_image_index = 32
        self.image_index = 7


class AK47(Weapon):
    """
    The rifle used by the main character.
    """
    def __init__(self):
        self.damage = 40
        self.delay = 200
        self.initial_ammo = 50
        self.max_ammo = 100
        self.name = "AK47"
        self.bullet_image_index = 39
        self.image_index = 6


class Shotgun(Weapon):
    """
    The shotgun used by the main character.
    """
    def __init__(self):
        self.damage = 70
        self.delay = 1000
        self.initial_ammo = 10
        self.max_ammo = 40
        self.name = "Shotgun"
        self.bullet_image_index = 48
        self.image_index = 8
import pygame

from ..setup import sound_dict

DEFAULT_ITEM_DURATION = 1000 * 10
class Bag:
    def __init__(self, items_graphics, bag_graphic):
        self.item = None
        self.expiration_time = 40000
        self.sprites = {
            "ITEM_SKULL": items_graphics.get_image(3, (50, 50)).convert_alpha(),
            "ITEM_HEALTH": items_graphics.get_image(2, (50, 50)).convert_alpha(),
            "ITEM_BLUEPOTION": items_graphics.get_image(0, (50, 50)).convert_alpha(),
            "ITEM_GREENPOTION": items_graphics.get_image(1, (50, 50)).convert_alpha(),
            "ITEM_AMMO": items_graphics.get_image(10, (50, 50)).convert_alpha()
        }
        self.bag_sprite = bag_graphic.get_image(0, (102, 84))

    def set_item(self, item, start_time, duration=DEFAULT_ITEM_DURATION):
        self.expiration_time = start_time + duration
        self.item = item
        sound_dict['item_sound'].play()

    def update(self, time):
        if time > self.expiration_time:
            self.item = None

    def use(self, player, time):
        if self.item is not None:
            self.item.apply_effect(player, time)
            self.item = None

    def draw(self, screen):
        screen.blit_rel(self.bag_sprite, (0, 0))

        if self.item is not None:
            sprite = self.sprites[self.item.get_sprite()]
            sprite = pygame.transform.scale(sprite, (33, 36))
            screen.blit_rel(sprite, (33, 40))

from data.components import player_state
from data.utils import RandomEventGenerator


class ItemGenerator:
    def __init__(self):
        item_probs = {
            Skull: 0.1,
            Health: 0.1,
            BluePotion: 0.30,
            GreenPotion: 0.30,
            Ammo: 0.2
        }
        self.debuf_generator = RandomEventGenerator(item_probs, null_event=None)

    def generate_item(self):
        item_type = self.debuf_generator.generate()
        item = item_type()
        return item


class Item:
    def __init__(self):
        pass

    def get_sprite(self):
        pass

    def apply_effect(self, player, time):
        pass


class Skull(Item):
    def __init__(self):
        super().__init__()
        print("Gerado skull")

    def get_sprite(self):
        pass

    def apply_effect(self, player, time):
        player.state.send_event(player_state.STRONGER_EVENT, time)


class Health(Item):
    def __init__(self):
        super().__init__()
        print("Gerado health")

    def get_sprite(self):
        pass

    def apply_effect(self, player, time):
        player.health += 1


class BluePotion(Item):
    def __init__(self):
        super().__init__()
        print("Gerado bp")

    def get_sprite(self):
        pass

    def apply_effect(self, player, time):
        player.state.send_event(player_state.STOP_BLEEDING_EVENT, time)


class GreenPotion(Item):
    def __init__(self):
        super().__init__()
        print("Gerado gp")

    def get_sprite(self):
        pass

    def apply_effect(self, player, time):
        player.state.send_event(player_state.STOP_SLOW_EVENT, time)


class Ammo(Item):
    def __init__(self):
        super().__init__()
        print("Gerado ammo")

    def get_sprite(self):
        pass

    def apply_effect(self, player, time):
        pass

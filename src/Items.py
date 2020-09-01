"""
Items for RPG

"""
from Fortuna import dice


class Item:

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Weapon(Item):

    def damage(self):
        return dice(1, 6)

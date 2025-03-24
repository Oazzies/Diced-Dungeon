import random

from enum import Enum

class Action(Enum):
    LIGHT_ATTACK = 0
    HEAVY_ATTACK = 1
    SPECIAL_ATTACK = 2

class Enemy():
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

    def action(self):
        action_choice = random.randint(0, 2)

        match action_choice:
            case 0:
                return Action.LIGHT_ATTACK
            case 1:
                return Action.HEAVY_ATTACK
            case 2:
                return Action.SPECIAL_ATTACK
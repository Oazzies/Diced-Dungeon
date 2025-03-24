import random

class Pack():
    def __init__(self, name):
        self.name = name

    def open(self):

        match self.name:
            case "Common":
                gold_cost = 20
                

                return gold_cost
            case "Uncommon":
                gold_cost = 40
                print("You found an uncommon pack")

                return gold_cost
            case "Rare":
                gold_cost = 60
                print("You found a rare pack")

                return gold_cost
            case "Epic":
                gold_cost = 80
                print("You found an epic pack")

                return gold_cost
            case "Legendary":
                gold_cost = 100
                print("You found a legendary pack")

                return gold_cost
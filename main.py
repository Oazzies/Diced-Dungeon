import random
import time

from player import Player
from enemy import Enemy, Action

def dice(sides):
    return random.randint(1, int(sides))

def roll():
    global sides
    dice_choice = input("[What dice will you use? (" + ", ".join(map(lambda x: f"{x[1]}d{x[0]}", player.dices.items())) + ")] \n")

    sides = int(dice_choice[1:])
    
    if sides in player.dices:
        player.dices[sides] -= 1
        
        if player.dices[sides] == 0:
            del player.dices[sides]
    
        roll = dice(sides)

        print("[You rolled a: " + str(roll) + "]\n")

        return roll
    else:
        print("[You don't have that dice]\n")
        exit()
        

def player_stats():
    print("[Player Stats]")
    time.sleep(0.3)
    print("Health: " + str(player.health))
    time.sleep(0.3)
    print("Attack: " + str(player.attack))
    time.sleep(0.3)
    print("Defense: " + str(player.defense))
    time.sleep(0.3)
    print("Dices: " + ", ".join(map(lambda x: f"{x[1]}d{x[0]}", player.dices.items())) + "\n")

def enemy_stats():
    enemy_name = enemy.name
    if enemy_name[-1].lower() in ["s", "x", "z", "ch", "sh"]:
        enemy_name += "es"
    elif enemy_name[-1].lower() == "y":
        enemy_name += "ies"
    else:
        enemy_name += "s"
    print(f"[{enemy_name} Stats]")
    time.sleep(0.3)
    print("Health: " + str(enemy.health))
    time.sleep(0.3)
    print("Attack: " + str(enemy.attack))
    time.sleep(0.3)
    print("Defense: " + str(enemy.defense) + "\n")

def increase_turn():
    global turn
    turn = turn + 1
    time.sleep(3)

print("---------- Welcome to Diced Dungeon ----------\n")

player = Player(100, 40, 10, 10, {10: 6, 30: 3, 50: 1}, 300)
enemy = Enemy("Goblin Lord", 300, 15, 5)

turn = 1

while True:
    print("\n---------- Turn " + str(turn) + " ----------\n")
    time.sleep(1)
    player_stats()
    time.sleep(1)
    enemy_stats()
    time.sleep(1)

    enemy_action = enemy.action()

    time.sleep(0.7)

    match enemy_action:
        case Action.LIGHT_ATTACK:
            print("[" + enemy.name + " will do a light attack]")
            time.sleep(0.2)
            print("- A light attack will do the enemy attack stats amount of damage (" + str(enemy.attack) + ")")
            time.sleep(0.1)
            print("- To dodge, roll lower then your dice choice divided by 2")
            time.sleep(0.1)
            print("- To parry, roll higher than the enemy attack stats (" + str(enemy.attack) + ")\n")
        case Action.HEAVY_ATTACK:
            print("[" + enemy.name + " will do a heavy attack]")
            time.sleep(0.2)
            print("- A heavy attack will do 50% more damage then a light attack (" + str(enemy.attack + (enemy.attack / 2)) + ")")
            time.sleep(0.1)
            print("- To dodge, roll lower then your dice choice divided by 4")
            time.sleep(0.1)
            print("- To parry, roll higher than the enemy attack stats (" + str(enemy.attack + (enemy.attack / 2)) + ")\n")
        case Action.SPECIAL_ATTACK:
            print("[" + enemy.name + " will do a special attack]")
            time.sleep(0.2)
            print("- A special attack will do half of the enemy attack stats amount of damage (" + str(enemy.attack / 2) + ")")
            time.sleep(0.1)
            print("- Since a special attack is AOE its impossible to dodge")
            time.sleep(0.1)
            print("- To parry, roll higher than the special attack damage (" + str(enemy.attack / 2) + ")")
            print("- A successfull parry gives the player a free attack\n")
    time.sleep(0.5)
    command = input("[What will you do? (attack, parry, dodge)] \n")

    match command.lower().strip():
        case "attack":
            damage = roll()
            enemy.health -= (player.attack + damage) - enemy.defense
            print(f"[You dealt: ({player.attack} + {damage}) - {enemy.defense} = {(player.attack + damage) - enemy.defense} damage] \n")
        case "parry":
            if Action.LIGHT_ATTACK:
                [f"[You wil need to roll higher than {enemy.attack} to parry]"]
                chance = roll() + player.speed
                if chance >= enemy.attack:
                    print("[You parried the attack] \n")
                    damaged = False

                    damage = roll()
                    enemy.health -= (player.attack + damage) - enemy.defense
                    print(f"[You dealt: ({player.attack} + {damage}) - {enemy.defense} = {(player.attack + damage) - enemy.defense} damage] \n")
                    increase_turn()
                    continue
            elif Action.HEAVY_ATTACK:
                [f"[You wil need to roll higher than {enemy.attack + (enemy.attack / 2)} to parry]"]
                chance = roll()
                if chance >= enemy.attack + (enemy.attack / 2):
                    print("[You parried the attack] \n")
                    damaged = False

                    damage = roll()
                    enemy.health -= (player.attack + damage) - enemy.defense
                    print(f"[You dealt: ({player.attack} + {damage}) - {enemy.defense} = {(player.attack + damage) - enemy.defense} damage] \n")
                    increase_turn()
                    continue
            elif Action.SPECIAL_ATTACK:            
                [f"[You wil need to roll higher than {enemy.attack / 2} to parry]"]
                chance = roll()
                if chance >= enemy.attack / 2:
                    print("[You parried the attack] \n")
                    damaged = False

                    damage = roll()
                    enemy.health -= (player.attack + damage) - enemy.defense
                    print(f"[You dealt: ({player.attack} + {damage}) - {enemy.defense} = {(player.attack + damage) - enemy.defense} damage] \n")
                    increase_turn()
                    continue
        case "dodge":
            if enemy_action != Action.SPECIAL_ATTACK:
                if enemy_action == Action.LIGHT_ATTACK:
                    chance = roll()
                    if chance <= sides // 4:
                        print("[You dodged the attack] \n")
                        increase_turn()
                        continue
                    print("[Dodge failed]")
                elif enemy_action == Action.HEAVY_ATTACK:
                    chance = roll()
                    if chance <= sides // 2:
                        print("[You dodged the attack] \n")
                        increase_turn()
                        continue 
                    print("[Dodge failed]")
            else:
                print("[The area damage still got to you!]")
        case _:
            print("[Invalid command] \n")
            break

    if enemy_action == Action.LIGHT_ATTACK:
        damage = enemy.attack - player.defense
        player.health -= damage
        print(f"[Enemy dealt {enemy.attack} - {player.defense} = {damage} damage] \n")
    elif enemy_action == Action.HEAVY_ATTACK:
        damage = (enemy.attack) * 2 - player.defense
        player.health -= damage
        print(f"[Enemy dealt ({enemy.attack} * 2) - {player.defense} = {damage} damage] \n")
    elif enemy_action == Action.SPECIAL_ATTACK:
        damage = (enemy.attack) / 2 - player.defense
        player.health -= damage / 2
        print(f"[Enemy dealt ({enemy.attack} / 2) - {player.defense} = {damage} damage] \n")

    if player.health <= 0:
        print("[You lose!]")
        break

    if enemy.health <= 0:
        print("[You win!]")
        break

    increase_turn()
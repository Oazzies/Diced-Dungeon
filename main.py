import random
import time

from player import Player
from enemy import Enemy, Action

def dice(sides):
    return random.randint(1, int(sides))

def roll():
    global dice_choice
    dice_choice = input("[What dice will you use? (" + ", ".join(player.dices) + ")] \n")

    print("You chose: " + dice_choice)

    if dice_choice not in player.dices:
        print("[Invalid dice]")
        return "break"
    
    roll = dice(dice_choice.split("d")[1])
    
    player.dices.remove(dice_choice)

    print("[You rolled a: " + str(roll) + "]\n")

    return roll

def player_stats():
    print("[Player Stats]")
    time.sleep(0.3)
    print("Health: " + str(player.health))
    time.sleep(0.3)
    print("Attack: " + str(player.attack))
    time.sleep(0.3)
    print("Defense:" + str(player.defense))
    time.sleep(0.3)
    print("Dices: " + ", ".join(player.dices) + "\n")

def enemy_stats():
    print("[Enemy Stats]")
    time.sleep(0.3)
    print("Health: " + str(enemy.health))
    time.sleep(0.3)
    print("Attack: " + str(enemy.attack))
    time.sleep(0.3)
    print("Defense:" + str(enemy.defense) + "\n")

def increase_turn():
    global turn
    turn = turn + 1
    time.sleep(3)

print("---------- Welcome to Diced Dungeon ----------\n")

player = Player(100, 20, 10, ["d2", "d6", "d10", "d16", "d20", "d32", "d54"], 300)
enemy = Enemy(500, 30, 5)

turn = 1

while True:
    print("---------- Turn " + str(turn) + " ----------\n")
    time.sleep(1)
    player_stats()
    time.sleep(1)
    enemy_stats()
    time.sleep(1)

    enemy_action = enemy.action()
    time.sleep(1)

    match enemy_action:
        case Action.LIGHT_ATTACK:
            print("[Enemy will do a light attack]")
            print("- To dodge, roll lower then your dice choice divided by 2")
            print("- To parry, roll higher than the enemy attack stats (" + str(enemy.attack) + ")\n")
        case Action.HEAVY_ATTACK:
            print("[Enemy will do a heavy attack]")
            print("- To dodge, roll lower then your dice choice divided by 4")
            print("- To parry, roll higher than the enemy attack stats (" + str(enemy.attack) + ")\n")
        case Action.SPECIAL_ATTACK:
            print("[Enemy will do a special attack]")
            print("- Since a special attack is AOE its impossible to dodge")
            print("- To parry, roll higher than the enemy attack stats (" + str(enemy.attack) + ")\n")
    
    command = input("[What will you do? (attack, parry, dodge)] \n")

    match command.lower().strip():
        case "attack":
            damage = roll()
            enemy.health -= player.attack + damage
            print("[You dealt " + str(player.attack + damage) + " damage]")
        case "parry":
            chance = roll()
            if chance >= enemy.attack:
                print("[You parried the attack] \n")
                damaged = False

                damage = roll()
                enemy.health -= player.attack + damage
                print("[You dealt " + str(player.attack + damage) + " damage] \n")
                increase_turn()
                continue
        case "dodge":
            if enemy_action != "special attack":
                if enemy_action == "light attack":
                    chance = roll()
                    if chance <= int(dice_choice.split("d")[1]) / 4:
                        print("[You dodged the attack] \n")
                        increase_turn()
                        continue
                elif enemy_action == "heavy attack":
                        chance = roll()
                        if chance <= int(dice_choice.split("d")[1]) / 2:
                            print("[You dodged the attack] \n")
                            increase_turn()
                            continue 
            else:
                print("[The area damage still got to you] \n")
        case _:
            print("[Invalid command] \n")
            break

    if enemy_action == "light attack":
        damage = enemy.attack - player.defense
        player.health -= damage
        print("[Enemy dealt " + str(damage) + " damage] \n")
    elif enemy_action == "heavy attack":
        damage = round(enemy.attack + (enemy.attack / 2)) - player.defense
        player.health -= damage
        print("[Enemy dealt " + str(damage) + " damage] \n")
    elif enemy_action == "special attack":
        damage = enemy.attack - player.defense
        player.health -= damage
        print("[Enemy dealt " + str(damage) + " damage] \n")

    if player.health <= 0:
        print("[You lose!]")
        break

    if enemy.health <= 0:
        print("[You win!]")
        break

    increase_turn()
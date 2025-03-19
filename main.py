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
        return 0
        

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

player = Player(100, 20, 10, {30: 6, 2: 30, 3: 40}, 300)
enemy = Enemy("Tim", 500, 30, 5)

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
            print("[Enemy will do a light attack]")
            time.sleep(0.1)
            print("- To dodge, roll lower then your dice choice divided by 2")
            time.sleep(0.1)
            print("- To parry, roll higher than the enemy attack stats (" + str(enemy.attack) + ")\n")
        case Action.HEAVY_ATTACK:
            print("[Enemy will do a heavy attack]")
            time.sleep(0.1)
            print("- To dodge, roll lower then your dice choice divided by 4")
            time.sleep(0.1)
            print("- To parry, roll higher than the enemy attack stats (" + str(enemy.attack) + ")\n")
        case Action.SPECIAL_ATTACK:
            print("[Enemy will do a special attack]")
            time.sleep(0.1)
            print("- Since a special attack is AOE its impossible to dodge")
            time.sleep(0.1)
            print("- To parry, roll higher than the enemy attack stats (" + str(enemy.attack) + ")\n")
    time.sleep(0.5)
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
            if enemy_action != Action.SPECIAL_ATTACK:
                if enemy_action == Action.LIGHT_ATTACK:
                    chance = roll()
                    if chance <= sides / 4:
                        print("[You dodged the attack] \n")
                        increase_turn()
                        continue
                elif enemy_action == Action.HEAVY_ATTACK:
                        chance = roll()
                        if chance <= sides / 2:
                            print("[You dodged the attack] \n")
                            increase_turn()
                            continue 
            else:
                print("[The area damage still got to you] \n")
        case _:
            print("[Invalid command] \n")
            break

    if enemy_action == Action.LIGHT_ATTACK:
        damage = enemy.attack - player.defense
        player.health -= damage
        print("[Enemy dealt " + str(damage) + " damage] \n")
    elif enemy_action == Action.HEAVY_ATTACK:
        damage = round(enemy.attack + (enemy.attack / 2)) - player.defense
        player.health -= damage
        print("[Enemy dealt " + str(damage) + " damage] \n")
    elif enemy_action == Action.SPECIAL_ATTACK:
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
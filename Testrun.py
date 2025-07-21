import pygame
from Player_Class import Player
from Enemy_Class import Enemy
from Battlemode import Battle
print("Loading player") # debug
# Player = Player(100,20,1.5,1,0,3,2,25,10) # dont know what values mean
Player = Player(HP=200, SP=20, ATK=1.5, DEF=1, GOLD=0, cooldown=3, SKILLCOST=25, Special_dmg=25, Basic_dmg=10) # shows what the values mean
print("Loading enemy")
Enemy = Enemy(HP=100,SP=0,ATK=1.5,DEF=10,GOLD=0,x=0,y=0,cooldown=3,SKILLCOST=25, Special_Damage=15, Basic_Dmg= 10)
print("Inputting battle values")
battle = Battle(Player, Enemy,0) #turn counter = 0
print("Starting battle")
counter = 1
while battle.is_battle_over() == False:
    print("battle started")
    try:
        print("-------------------------------------------turn",counter, "-----------------------------------------------------")
        battle.Turn_player("Basic")
        battle.Turn_enemy()
        Player.HP = battle.player.HP # sets the player values here with the player values in battlemode
        Player.SP = battle.player.SP
        Enemy.HP =  battle.enemy.HP
        Enemy.SP = battle.enemy.SP
        # print(f"{Player.HP}") # f string, adding strings and variables together
        # print(f"{Enemy.HP}")
        print(f"{battle.player.HP}") # f string, adding strings and variables together, checking battle player hp
        print(f"{battle.enemy.HP}")
        print("------------------------------------------------------------------------------------------------")
        counter += 1


    except Exception as e:
        print(f"An error occurred: {e}")
        break

# print("------------------------------------------------------------------------------------------------")
# print("Player is attacking")
# battle.Turn_player("Basic")
# print("Enemy is attacking")
# battle.Turn_enemy()
# print("------------------------------------------------------------------------------------------------")


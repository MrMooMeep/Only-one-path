import pygame
import random
from Player_Class import Player
from Enemy_Class import Enemy

class Battle:
    def __init__(self,Player,Enemy,Turn):
        self.player = Player
        self.enemy = Enemy
        self.win = False #if player wins the encounter
        self.turn = Turn #0,1, Player is 0, enemy is 1
        self.battle_over = False #if player loses the game
    
    def Turn_player(self,attack_type): #attack_type is a string
        if self.turn == 0: # == compares, = converts value to the once current
            print("Player's Turn.")
            if attack_type == "Basic":
                dmg = self.player.use_basic()
                print("Player uses their basic and dealt", dmg ,"damage")
            elif attack_type == "Special" and self.player.can_use_special() == True:
                dmg = self.player.use_special()
                print("Player uses their Special and dealt", dmg ,"damage")
            elif attack_type == "Guard":
                dmg = 0
                self.player.use_guard()
                print("Player guards")

            else:
                print("Player tries to use special but can't")
                return # breaks out of turn player skips line 24-25, allows them to pick another option
            self.enemy.damage_intake(dmg)   #call Enemy_class on what dmg is taken, reduce the enemy's HP
            self.turn += 1 # adds 1 to turn counter
    
    def Turn_enemy(self):
        if self.turn == 1:
            print("Enemy's Turn")
            if self.enemy.HP < int(self.enemy.MAX_HP*.99): # random generates a random number from 0 to 1, MAX HP conditional
                dmg = 0
                self.enemy.use_guard() #may infinitely guard when below 50% hp, 
                print("Enemy guards")
            elif self.enemy.can_use_special() == True:
                dmg = self.enemy.use_special()
                print("Enemy uses their special and dealt", dmg ,"damage")
            else:
                dmg = self.enemy.use_basic_atk()
                print("Enemy uses their basic and dealt", dmg ,"damage")
            self.player.damage_intake(dmg) # dmg is input into the parenthesis so the player gets this value and takes dmg accordingly 
            self.turn -=1 # minus 1 from turn counter
    
    def Victory(self):
        if self.enemy.HP <= 0:
            self.win = True
            print("You won the battle")
            return True # expect output, true or false, true win, output false (not done yet)
        else:
            return False
   
    def is_battle_over(self):
        if self.player.HP <= 0:
            self.battle_over = True
            print("You succumb to the enemy and fall")
            return True # checks if the player's dead, returns true if so
        else:
            return self.Victory() #checks if the enemy's dead, returns true if so

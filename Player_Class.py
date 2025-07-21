import pygame
import sys

class Player:
    def __init__(self,HP,SP,ATK,DEF,GOLD,cooldown=3, SKILLCOST=25, Special_dmg=25, Basic_dmg=10): # self.GOLD is player's gold here, the other self.gold is the enemy's gold
        self.HP = HP
        self.MAX_HP = HP # gets this info once and stays constant unless changed
        self.SP = SP
        self.ATK = ATK
        self.DEF = DEF
        self.GOLD = GOLD
        self.cooldown = cooldown -1 #fixes the offset because if didnt it would be off 1 number
        self.cooldown_counter = 0
        self.SKILLCOST = SKILLCOST
        self.Special_dmg = Special_dmg
        self.Basic_dmg = Basic_dmg
        self.is_guarding = False
    
    def can_use_special(self):
        if self.SP >= self.SKILLCOST and self.cooldown_counter <= 0:
            self.use_special
            return True
    
    def use_special(self):
        self.cooldown_counter = self.cooldown
        self.SP -= self.SKILLCOST
        return int(self.Special_dmg* self.ATK)
    
    def use_basic(self):
        self.cooldown_counter -= 1
        return int(self.Basic_dmg* self.ATK)

    def damage_intake(self, incoming_damage):
        if incoming_damage == 0:
            return #break out of the function since no dmg has been intaked


        elif self.is_guarding == True:
            print("the damage initially was", int(incoming_damage))
            print("but since Player was guarding they only took", int(incoming_damage - (self.DEF*2)))
            self.HP -= abs(int(incoming_damage - (self.DEF*2)))
            self.is_guarding = False
        else:
            self.HP -= abs(int(incoming_damage - self.DEF))

    def use_guard(self): #mutliplies DEF by 2 to reduce incoming dmg
        self.is_guarding = True
    


    def is_dead(self):
        if self.HP <= 0:
            return True
        else:
            return False

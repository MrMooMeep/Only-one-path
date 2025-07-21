import pygame
import sys
import math

RED = (255,0,0)
# Enemy_Img= pygame.image.load("Enemy.png") # temp disabled for testing

class Enemy:
    def __init__(self,HP,SP,ATK,DEF,GOLD,x,y,cooldown=3,SKILLCOST=25, Special_Damage=15, Basic_Dmg= 10): #GOLD is like how much the enemy would drop when defeated
        self.HP = HP
        self.MAX_HP = HP
        self.SP = SP
        self.ATK = ATK
        self.DEF = DEF
        self.GOLD = GOLD
        self.x = x
        self.y = y
        self.cooldown = cooldown -1
        self.counter_cooldown = 0
        self.SKILLCOST = SKILLCOST
        self.Special_Damage = Special_Damage
        self.Basic_Dmg = Basic_Dmg
        self.is_guarding = False
    
    # def draw(self,win):
    #     win.blit(Enemy_Img,(self.x,self.y),) #image,position,size?
    
    def can_use_special(self):
        if self.SP >= self.SKILLCOST and self.counter_cooldown <= 0:
            self.use_special # run line 26-29 whne conditions are viable
            return True
        
    
    def use_special(self):
        self.counter_cooldown = self.cooldown
        self.SP -= self.SKILLCOST
        return int(self.Special_Damage * self.ATK)  # damage dealt, int converts into integer and cuts off the decimals
    
    def use_basic_atk(self):
        self.counter_cooldown -= 1
        return int(self.Basic_Dmg * self.ATK)
    
    def damage_intake(self,incoming_dmg):
        if incoming_dmg == 0:
            return #break out of the function since no dmg has been intaked
        
        elif self.is_guarding == True:
            print("the damage initially was", int(incoming_dmg))
            print("but since Enemy was guarding they only took", int(incoming_dmg - (self.DEF*2)))
            self.HP -= abs(int(incoming_dmg - (self.DEF*2)))
            self.is_guarding = False
        else:
            self.HP -= abs(int(incoming_dmg - (self.DEF)))
    
    def use_guard(self):
            self.is_guarding = True #need to find a way to set it false again
            

    def is_dead(self):
        if self.HP <= 0:
            return True
        else:
            return False


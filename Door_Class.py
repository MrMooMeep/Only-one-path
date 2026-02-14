import random
from Enemy_Class import Enemy
from shared import swidth,sheight


class Door:
    def __init__(self, encounter, playerhp):
        self.encounter = encounter
        self.playerhp = playerhp
    
    def generate_outcome(self):
        door_type = random.randint(1,3) # random number generation between 1-3, temporary value
        # 1 = encounter, 2 = GOLD , 3 = heal

        if door_type == 1: 
            Enemy_HP = int(100*(1 + 1*((self.encounter)/5)))
            Enemy_SP = 45
            Enemy_ATK = int(1*(1 + 1*((self.encounter)/10)))
            Enemy_DEF = int(1 + ((Enemy_HP)*((self.encounter)/20)))
            Enemy_GOLD = int(10*((self.encounter)/2))
            Enemy_Special_Damage = 60
            Basic_Dmg = 10   
            enemy = Enemy(HP=Enemy_HP,SP=Enemy_SP,ATK=Enemy_ATK,DEF=Enemy_DEF,GOLD=Enemy_GOLD,x=(swidth//2),y=(sheight//2-(50)),cooldown=3,SKILLCOST=25, Special_Damage=Enemy_Special_Damage, Basic_Dmg= Basic_Dmg)
            return door_type,enemy # returns the enemy stats and door_type (number)
        
        elif door_type == 2:
            GOLD = 10*(self.encounter/5) #gives gold according to the (amount of doors passed/5)*10
            return door_type, GOLD 

        elif door_type == 3: 
            heal = int(self.playerhp*(.25)) #heals by 25% of players MAX HP
            return door_type, heal
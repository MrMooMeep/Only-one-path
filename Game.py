import pygame
import sys
from ui import TextBox, Text, Button, ImageButton
from Title_and_other_UI import Title_UI, Shop_UI, Door_UI
from shared import sheight, swidth, fantasy_fonts
from state_manager import State_manager
from state import State
from Player_Class import Player
from Enemy_Class import Enemy
from Door_Class import Door


class game:
    def __init__(self,player,enemy):      
# Initialize Pygame
        pygame.init()
        self.state_manager = State_manager()
        self.encounter_counter = 0

        self.screen = pygame.display.set_mode((swidth,sheight)) # Width & height is a tuple (ordered couple of stuff)
        self.running = True
        self.player = player
        self.enemy = enemy

    def render_ui(self):
        self.state_manager.state[self.state_manager.current_state].render(self.screen) #if render diffrent screens, calls render method to use state manager to render the other screen ui's
    # go to staet manager and access state variables within( a map), pick corrent ui to render (has a variable taht tracks the state), uses it to track the correct screen
        if self.state_manager.check_state('battle'): #checks if the current state is in battle
            self.HP_SP_UI('player') # if is in battle, HP, SP of both entities will be displayed
            self.HP_SP_UI('enemy')
             
        elif self.state_manager.check_state('door'): #checks if the current state is in battle
            # print('checking door...')
            for ui in Door_UI.values(): # for loop going through your map[], slight flaw: what if ui component has something not a button, text ex. image
                ui.draw(self.screen) #draws the image onto the screen from door_UI


    def HP_SP_UI(self,unit):

        if unit == 'player':
            bar_width = 450
            bar_height = 30

            HP_bar_position = (0,((sheight//2)+170))
            pygame.draw.rect(self.screen, (100,100,100),(HP_bar_position[0],HP_bar_position[1],bar_width,bar_height),2)

            hp_ratio =  self.player.HP/self.player.MAX_HP
            hp_color = (0,255,0) if hp_ratio > .5 else (255,0,0)

            pygame.draw.rect(self.screen, hp_color,(HP_bar_position[0],HP_bar_position[1],bar_width*hp_ratio,bar_height))
            

            SP_bar_position = (swidth-bar_width,((sheight//2)+170))
            pygame.draw.rect(self.screen, (100,100,100),(SP_bar_position[0],SP_bar_position[1],bar_width,bar_height),2)

            sp_ratio =  self.player.SP/self.player.MAX_SP
            sp_color = (0,50,255) if sp_ratio > .5 else (255,127,80)

            pygame.draw.rect(self.screen, sp_color,(SP_bar_position[0],SP_bar_position[1],bar_width*sp_ratio,bar_height))
        elif unit == 'enemy':
            unit_bar_width = 100
            unit_bar_height = 10

            unit_HP_position = ((self.enemy.x-(50)),(self.enemy.y-(150)))
            pygame.draw.rect(self.screen,(100,100,100),(unit_HP_position[0],unit_HP_position[1],unit_bar_width,unit_bar_height))
            # where its going, what the background color, where its gonna go ([x],[y] is 0, 1 bc it starts at 0 first), (width,height)
            unit_hp_ratio = self.enemy.HP/self.enemy.MAX_HP
            unit_hp_color = (0,255,0) if unit_hp_ratio > .5 else (255,0,0)
            pygame.draw.rect(self.screen, unit_hp_color, (unit_HP_position[0],unit_HP_position[1],unit_bar_width*unit_hp_ratio,unit_bar_height))


    def input_handler(self):
        for event in pygame.event.get(): # get() <--- prob a function when has this
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: #tells code if clicking down on mouse, do this cmd, left click = mb 1, right click =3, scroll = 2
                if event.button == 1: 
                    mouse_position = pygame.mouse.get_pos() # pygame figuring out where the mouse is located on window, local variable (lives only here)

            # Access the current UI components from the current state
            current_ui = self.state_manager.state[self.state_manager.current_state].ui

            # Loop through all UI components in the current state's UI map
            for component_name, component in current_ui.items():  # Get both key and value
                # Check if the component has an 'handle_event' or 'update' method (like buttons)
                
                mouse_position = pygame.mouse.get_pos()

                if hasattr(component, 'handle_event'):
                    component.handle_event(event)
                elif hasattr(component, 'update'):  # If you're using update instead
                    component.update(pygame.time.get_ticks())  # or pass `event` if required , if on top of box do this cmd right now, needs click requirment
                    #print(f"Clicked on component: {component_name}")
                
                if hasattr(component, 'rect') and component.rect.collidepoint(mouse_position):
                    if event.type == pygame.MOUSEBUTTONDOWN: #tells code if clicking down on mouse, do this cmd, left click = mb 1, right click =
                        if event.button == 1: #The click cmd, click requirement 
                            #print(f"Clicked on component: {component_name}")
                    
                            # Handle specific button clicks based on component name
                            if component_name == 'shop':  # This matches your Title_UI['shop'] key
                                print("Shop button clicked!")
                                self.state_manager.switch_state("shop")
                            
                            elif component_name == 'start':  # This matches your Title_UI['start'] key
                                print("Start button clicked!")
                                self.state_manager.switch_state("door")
                            
                            elif component_name == 'exit':  # This matches your Title_UI['exit'] key
                                print("Exit button clicked!")
                                self.running = False
                            
                            elif component_name == 'Door_1' or component_name == 'Door_2' or component_name == 'Door_3':  # This matches your TDoor_UI['Door_1'] key
                                print("Door button clicked!")
                                door_rand = Door(encounter=self.encounter_counter,playerhp=self.player.MAX_HP)# the 'holder' of the door class, takes in the encounter count and the player's MAX HP
                                
                                door_type,outcome = door_rand.generate_outcome() # python can return 2 or more values, but others can only return 1, sets the outcome values for the 2 values
                                if door_type == 3: # door_type is a number 1= enemy battle, 2= gold, 3= heal
                                    self.player.HP = min(self.player.MAX_HP,self.player.HP+outcome) # takes the smallest value to convert to player hp to prevent overheal, if max = 100 and hp = 250, takes max hp for hp
                                    print('A spot to rest')

                                elif door_type == 2: # door_type is a number 1= enemy battle, 2= gold, 3= heal
                                    self.player.GOLD += outcome
                                    print('gained GOLD')

                                if door_type == 1: # door_type is a number 1= enemy battle, 2= gold, 3= heal
                                    self.enemy = outcome #stores the enemy's new stats affected by encounter count
                                    self.state_manager.switch_state("battle")
                                    print('You find a enemy')

                                self.encounter_counter += 1
                                print(f'encounter counter is now at: {self.encounter_counter}')



                                

                            if component_name == 'back':  # This matches your Title_UI['shop'] key
                                print("Back button clicked!")
                                self.state_manager.switch_state("title")

# we gonna add atk, def, etc buttons here later
    def run(self):
#Starting Game, Front screen
        while self.running == True:
            self.input_handler()

            # screen.blit(TextBox,(600,250)) #displays screen or text in parenthesis, where it displays it
            self.screen.fill((244,244,244)) #tuple,filling background with colors first before anything
            self.render_ui()

        # End of Front page

            pygame.display.flip() #Updates the screen, basically the fps

player = Player(HP=200, SP=20, ATK=1.5, DEF=1, GOLD=0, cooldown=3, SKILLCOST=25, Special_dmg=25, Basic_dmg=10)
enemy = Enemy(HP=100,SP=0,ATK=1.5,DEF=10,GOLD=0,x=(swidth//2),y=(sheight//2-(50)),cooldown=3,SKILLCOST=25, Special_Damage=15, Basic_Dmg= 10)
game = game(player,enemy) # the blueprint manifested via variable (thats the instance of the class)
game.run() #runs the class method (run) executes the blueprint


    

    


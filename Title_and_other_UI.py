from ui import Text, Button, TextBox
import pygame
from shared import sheight, swidth, fantasy_fonts
from Upgrade_glow import UpgradeIndicator



#Using Maps to make it easier to collect lines of codes for specific events easily, much faster than an array, basically uses a (ctrl=F) cmd and finds the code immediatly

Title_UI = {
    'title' :  Text(x=(swidth//2)-(280//2), y=(sheight//2)-(150), width=280, height=50, text='One way out', font=fantasy_fonts), #doing - numbers to bring the height up bc (0,0) in top left
    'start' :  Button(x=((swidth//2)-(190/2)), y=(sheight//2), width=190,height=50, text='Start'),
    'shop'  :  Button(x=((swidth//2)-(190/2)), y=(sheight//2)+(60), width=190,height=50, text='Shop'), # y is adding because 0,0 starts at the top left
    'exit'  :  Button(x=((swidth//2)-(190/2)), y=(sheight//2)+(120), width=190,height=50, text='Exit')
}

# indicator = UpgradeIndicator(x=100, y=80, box_width=60, box_height=20, gap=10, count=5) # reference on how to make an upgrade_indicator button
# Create a button using your Button class
def upgrade_action(upgrade_indicator): #function that lights up the next box

    upgrade_indicator.activate_next()




# upgrade_button = Button(250, 150, 150, 60, "Upgrade", action=upgrade_action) # upgrade_action passing a function that activates box lights, an example


Shop_UI = {
    'atk_indicator' :UpgradeIndicator(x=((swidth//2))-(500), y=60, box_width=300, box_height=100, gap=30, count=5),
    'dialogue_text': TextBox(x=(swidth//2)-(155), y=(sheight/2)-(20), width=700, height=250, borderColor=(43, 44, 58, 160)),
    'def_indicator' : UpgradeIndicator(x=((swidth//2))-(500), y=60, box_width=300, box_height=100, gap=30, count=5),
    # 'atk' : Button(x=((swidth//2)-(190/2)), y=(sheight//2)+(60), width=190,height=50, text='Atk', action=upgrade_action(Shop_UI["atk_indicator"])),
    # 'def' : Button(x=((swidth//2)-(260/2)), y=(sheight//2)+(60), width=190,height=50, text='Def',action=upgrade_action()) #needs to know what Upgrade_action is (make sure the code is above the cmd so it could be used)
    # 'potion' : # later
    'back' : Button(x=((swidth//2)+(750/2)), y=(sheight//2)+(290), width=190,height=100, text='back', )

    
}

atk_button = Button(x=((swidth//2)-(190/2)), y=(sheight//2)+(290), width=190,height=100, text='Atk', action=upgrade_action(Shop_UI['atk_indicator'])) #requires to reference Shop_UI, but if in Sho_Ui while being made, cannot implemnt when not complete
def_button = Button(x=((swidth//2)+(300/2)), y=(sheight//2)+(290), width=190,height=100, text='Def',action=upgrade_action(Shop_UI['def_indicator']))
Shop_UI["atk"] = atk_button #reimplement atk
Shop_UI["def"] = def_button

button_x = (swidth//2)-(850/2)

Battle_UI = {
    'background_fill' : TextBox(x=0, y=(sheight)-(250), width=swidth, height=250, borderColor=(43, 44, 58, 160)),
    'dialogue_text' : TextBox(x=(swidth//2)-(10), y=(sheight)-(235), width=600, height=220, borderColor=(43, 44, 58, 160)),
    'atk_button' : Button(x=(button_x), y=(sheight//2)+(225), width=250,height=50, text='Attack', action=""),
    'special_button' : Button(x=(button_x), y=(sheight//2)+(295), width=250,height=50, text='Special', action=""),
    'def_button' : Button(x=(button_x), y=(sheight//2)+(365), width=250,height=50, text='Defend', action="")
    
    
    # 'item_button' :

}

Door_UI = {
    'Door_1' :
    'Door_2' :
    'Door_3' :







}


# front_text = Text(x=(swidth//2)-(280//2), y=(sheight//2)-(150), width=280, height=50, text='One way out', font=fantasy_fonts) #doing - numbers to bring the height up bc (0,0) in top left

# start_button =  Button(x=((swidth//2)-(190/2)), y=(sheight//2), width=190,height=50, text='Start')
#                        # // cuts off decimal points and never rounds
# settings_button = Button(x=((swidth//2)-(190/2)), y=(sheight//2)+(60), width=190,height=50, text='Settings') # y is adding because 0,0 starts at the top left
# exit_button = Button(x=((swidth//2)-(190/2)), y=(sheight//2)+(120), width=190,height=50, text='Exit')



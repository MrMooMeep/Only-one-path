import pygame
import sys
from ui import TextBox, Text, Button
from Title_and_other_UI import Title_UI, Shop_UI
from shared import sheight, swidth, fantasy_fonts

# Initialize Pygame
pygame.init()



screen = pygame.display.set_mode((swidth,sheight)) # Width & height is a tuple (ordered couple of stuff)

running = True



#Starting Game, Front screen
while running == True:
    for event in pygame.event.get(): # get() <--- prob a function when has this
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN: #tells code if clicking down on mouse, do this cmd, left click = mb 1, right click =
            if event.button == 1:
                mouse_position = pygame.mouse.get_pos() # pygame figuring out where the mouse is located on window
                if Title_UI['exit'].rect.collidepoint(mouse_position): # if mouse position with 'click' interacts with this "rectangle button" named exit_button, do this cmd
                    running = False


    # screen.blit(TextBox,(600,250)) #displays screen or text in parenthesis, where it displays it
    screen.fill((244,244,244)) #tuple,filling background with colors first before anything
    # Textbox.draw(screen) #draws textbox onto display or surface
    # Title_UI['start'].draw(screen) #inserts the button into screen aka the game window
    # Title_UI['shop'].draw(screen)
    # Title_UI['exit'].draw(screen)
    # Title_UI['title'].draw(screen)

    Shop_UI['dialogue_text'].draw(screen)
    Shop_UI['atk_indicator'].draw(screen)
    Shop_UI['def_indicator'].draw(screen)
    Shop_UI['atk'].draw(screen)
    Shop_UI['def'].draw(screen)



# End of Front page

    pygame.display.flip()




    

    


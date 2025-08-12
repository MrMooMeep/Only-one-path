from Title_and_other_UI import Title_UI, Shop_UI





class State:
    def __init__(self,ui):
        self.is_state_active = False #screen should be displayed or not, cannot have multiple screens active at once, 
        self.ui = ui # a map
    def render(self,screen):
        for ui in self.ui.values(): # for loop going through your map[], slight flaw: what if ui component has something not a button, text ex. image
            ui.draw(screen)
    def check_active(self):
        # if self.is_state_active == True: # checks if is_state_active hold value true or false and returns the values it has (true/False)
        #     return True
        # elif self.is_state_active == False:
        #     return False
        return self.is_state_active # returns the values you want to check, if its either true or false for running certain ui displays, most optimized way
    def change_screen_value(self,input):
        # if input == True:
        #     self.is_state_active = True
        # elif input == False:
        #     self.is_state_active = False
        self.is_state_active = input # same thing, since they try to show the same value, turns on/off state values
    
        
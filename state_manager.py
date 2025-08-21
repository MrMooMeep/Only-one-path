from state import State
from Title_and_other_UI import Title_UI, Shop_UI, Battle_UI

class State_manager:
    def __init__(self):
        self.state = {
            'title' : State(Title_UI), # Title State
            'shop' : State(Shop_UI), # Shop State
            'battle' : State(Battle_UI), # Battle State 
            # 'path' : State(Path_UI) #Path State, shows where you wanna go next




         } # creating map
        self.current_state = 'battle' # what current screen to display, since theres a bunch rn, which it should turn on when game is booted, stores a key to render(keyholder), will change states
    def check_state(self,state): # check state for if certain states ex.(battle) have same value, return true/false
        if self.current_state == state: #if aligned with the same title, return True
            return True
        else: # everything else isnt aligned
            return False
    def switch_state(self,input):
        self.current_state = input # cetain flaws, may skips many states if not careful

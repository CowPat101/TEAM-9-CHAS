#Python program to make a pygame settings page - Morgan Stanley hackathon - Jack Cavar

#import the necessary modules
import pygame
import pygame_menu as pm

#Initialize pygame, screen and colours

pygame.init() 
  
# Screen 
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
  
# Standard RGB colors 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
CYAN = (0, 100, 100) 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 

#Main function of the program

def main(): 
    # List that is displayed while selecting the graphics level 
    graphics = [("Low", "low"), 
                ("Medium", "medium"), 
                ("High", "high"), 
                ("Ultra High", "ultra high")] 
  
    # List that is displayed while selecting the window resolution level 
    resolution = [("1920x1080", "1920x1080"), 
                  ("1920x1200", "1920x1200"), 
                  ("1280x720", "1280x720"), 
                  ("2560x1440", "2560x1440"), 
                  ("3840x2160", "3840x2160")] 
  
    # List that is displayed while selecting the difficulty 
    difficulty = [("Easy", "Easy"), 
                  ("Medium", "Medium"), 
                  ("Expert", "Expert")] 
  
    # List that is displayed while selecting the player's perspective 
    perspectives = [("FPP", "fpp"), 
                    ("TPP", "tpp")] 
  
    # This function displays the currently selected options 
  
    def printSettings(): 
        print("\n\n") 
        # getting the data using "get_input_data" method of the Menu class 
        settingsData = settings.get_input_data() 
  
        for key in settingsData.keys(): 
            print(f"{key}\t:\t{settingsData[key]}") 
  
    # Creating the settings menu 
    settings = pm.Menu(title="Settings", 
                       width=WIDTH, 
                       height=HEIGHT, 
                       theme=pm.themes.THEME_GREEN) 
  
    # Adjusting the default values 
    settings._theme.widget_font_size = 25
    settings._theme.widget_font_color = BLACK 
    settings._theme.widget_alignment = pm.locals.ALIGN_LEFT 

    def button_1_func():
        print("Button 1 clicked!")

    def button_2_func():
        print("Button 2 clicked!")

    settings.add.button(title="test", font_color=WHITE, background_color=GREEN, action=button_1_func)

    settings.add.button(title="test2", font_color=WHITE, background_color=RED, action=button_2_func) 
  
    
    # 2 different Drop-downs to select the graphics level and the resolution level 
    settings.add.dropselect(title="Graphics Level", items=graphics, 
                            dropselect_id="graphics level", default=0) 
    settings.add.dropselect_multiple(title="Window Resolution", items=resolution, 
                                     dropselect_multiple_id="Resolution", 
                                     open_middle=True, max_selected=1, 
                                     selection_box_height=6) 
  
    # Toggle switches to turn on/off the music and sound 
    settings.add.toggle_switch( 
        title="Music", default=True, toggleswitch_id="music") 
    settings.add.toggle_switch( 
        title="Sounds", default=False, toggleswitch_id="sound") 
  
    # Selector to choose between the types of difficulties available 
    settings.add.selector(title="Difficulty\t", items=difficulty, 
                          selector_id="difficulty", default=0) 
  
    # Range slider that lets to choose a value using a slider 
    settings.add.range_slider(title="FOV", default=60, range_values=( 
        50, 100), increment=1, value_format=lambda x: str(int(x)), rangeslider_id="fov") 
  
    # Fancy selector (style added to the default selector) to choose between  
    #first person and third person perspectives 
    settings.add.selector(title="Perspective", items=perspectives, 
                          default=0, style="fancy", selector_id="perspective") 
  
    # clock that displays the current date and time 
    settings.add.clock(clock_format="%d-%m-%y %H:%M:%S", 
                       title_format="Local Time : {0}") 
  
    # 3 different buttons each with a different style and purpose 
    settings.add.button(title="Print Settings", action=printSettings, 
                        font_color=WHITE, background_color=GREEN) 
    settings.add.button(title="Restore Defaults", action=settings.reset_value, 
                        font_color=WHITE, background_color=RED) 
    settings.add.button(title="Return To Main Menu", 
                        action=pm.events.BACK, align=pm.locals.ALIGN_CENTER) 
  
    # Creating the main menu 
    mainMenu = pm.Menu(title="Main Menu", 
                       width=WIDTH, 
                       height=HEIGHT, 
                       theme=pm.themes.THEME_GREEN) 
  
    # Adjusting the default values 
    mainMenu._theme.widget_alignment = pm.locals.ALIGN_CENTER 
  
    # Button that takes to the settings menu when clicked 
    mainMenu.add.button(title="Settings", action=settings, 
                        font_color=WHITE, background_color=GREEN) 
  
    # An empty label that is used to add a seperation between the two buttons 
    mainMenu.add.label(title="") 
  
    # Exit button that is used to terminate the program 
    mainMenu.add.button(title="Exit", action=pm.events.EXIT, 
                        font_color=WHITE, background_color=RED) 
  
    # Lets us loop the main menu on the screen 
    mainMenu.mainloop(screen) 

  
if __name__ == "__main__": 
    main() 
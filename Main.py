import pygame
import sys
import pygame_menu as pm
import campaign
import freestyle
import configparser

pygame.mixer.pre_init()
pygame.init()
window_width = 800  # Set your window dimensions
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("My Game")
 

#Reset the config file to default settings for new user
def reset_config_file_new_user():
    config_object = configparser.ConfigParser()

    config_object['Subtitles'] = {
        'subtitles_on': False
    }
    config_object['Font'] = {
        'font_id': "arial"
    }
    config_object['Font Size'] = {
        'sub_font_size': "medium"
    }
    config_object['Font Colour'] = {
        'sub_colour': "black"
    }
    config_object['Audio'] = {
        'mute': False
    }
    config_object['Levels'] = {
        'level': 1
    }

    #save the config file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)

#Display Main menu
def display_main_menu():
    # Create a Pygame Menu instance
    main_menu = pm.Menu("Main Menu", window_width, window_height, theme=pm.themes.THEME_DEFAULT)

    # Add buttons to the menu
    main_menu.add.button(title="Play", 
                        action=display_game_menu, align=pm.locals.ALIGN_CENTER)
    main_menu.add.button(title="Settings", 
                        action=display_settings_menu, align=pm.locals.ALIGN_CENTER)
    main_menu.add.button(title="Quit", 
                        action=pm.events.EXIT, align=pm.locals.ALIGN_CENTER)
    
    print("Printing config file contents:")
    #get the data from the config file
    config_object = configparser.ConfigParser()
    config_object.read("config.ini")
    for section in config_object.sections():
        print(f"[{section}]")
        for key in config_object[section]:
            print(f"{key} : {config_object[section][key]}")
    
    reset_config_file_new_user()
    
    main_menu.mainloop(screen)

# display game menu
def display_game_menu():
    # Create a Pygame Menu instance
    game_menu = pm.Menu("Settings", window_width, window_height, theme=pm.themes.THEME_DEFAULT)

    # Add buttons to the menu
    game_menu.add.button(title="Campaign mode", 
                        action=campaign_mode, align=pm.locals.ALIGN_CENTER)
    game_menu.add.button(title="Freestyle mode", 
                        action=freestyle_mode, align=pm.locals.ALIGN_CENTER)
    # Create a back button to return to the main menu
    game_menu.add.button(title="Return To Main Menu", 
                        action=display_main_menu, align=pm.locals.ALIGN_CENTER) 
    # Start the menu
    game_menu.mainloop(screen)

def display_game_screen(gamemode):
    # load background image to the screen
    background = pygame.image.load("placeholder_sprites\IMG_5565.jpeg")
    screen.blit(background, (0, 0))
    pygame.display.flip()  # update the screen
    # load an image to the screen to the bottom left corner
    image = pygame.image.load("placeholder_sprites\Hands.png")
    screen.blit(image, (0, 500))
    # game loop to keep the window open
    while True:
        for event in pygame.event.get():
            if gamemode == 0:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    clap()
                # when the user clicks the left mouse button play the sound
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clap()
            if gamemode == 1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        play_sound(1)
                    if event.key == pygame.K_s:
                        play_sound(2)
                    if event.key ==  pygame.K_d:
                        play_sound(3)
                    if event.key == pygame.K_f:
                        play_sound(4)
                    if event.key == pygame.K_g:
                        play_sound(5)
                    if event.key == pygame.K_h:
                        clap()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
                
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        

def play_sound(sound):
    pygame.mixer.music.load(f"placeholder_sounds/beep{sound}.ogg")
    pygame.mixer.music.play()

def clap():
    pygame.mixer.music.load("placeholder_sounds\clap.wav")
    pygame.mixer.music.play()


def campaign_mode():
    campaign.main()
    display_game_screen(0)
    
    
    pass
def freestyle_mode():
    display_game_screen(1)
    freestyle.main()
    pass

#Settings menu logic
def display_settings_menu():

    #Make the settings in config be reset to default
    def reset_config_file():
        config_object['Subtitles'] = {
            'subtitles_on': False
        }
        config_object['Font'] = {
            'font_id': "arial"
        }
        config_object['Font Size'] = {
            'sub_font_size': "medium"
        }
        config_object['Font Colour'] = {
            'sub_colour': "black"
        }
        config_object['Audio'] = {
            'mute': False
        }

        #save the config file
        with open('config.ini', 'w') as conf:
            config_object.write(conf)
        
        display_main_menu()



    #Function to process the data from the settings menu and update settings menu
    def processSettingData():
        #print the data settings to the console
        print("\n\n")
        settingsData = settings_menu.get_input_data() 

        #write the data to the config file
        for key in settingsData.keys():
            print(f"{key}\t:\t{settingsData[key]}")

            if key == "subtitles":
                config_object['Subtitles'] = {
                    'subtitles_on': settingsData[key]
                }
            
            elif key == "font id":
                config_object['Font'] = {
                    'font_id': settingsData[key]
                }
            
            elif key == "sub font size":
                config_object['Font Size'] = {
                    'sub_font_size': settingsData[key]
                }
            
            elif key == "sub colour":
                config_object['Font Colour'] = {
                    'sub_colour': settingsData[key]
                }
            elif key == "mute":
                config_object['Audio'] = {
                    'mute': settingsData[key]
                }
            elif key == "setting reset":
                reset_config_file()
            

        #save the config file
        with open('config.ini', 'w') as conf:
            config_object.write(conf)
        
        display_main_menu()

    # Create a Pygame Menu instance
    settings_menu = pm.Menu("Settings", window_width, window_height, theme=pm.themes.THEME_DEFAULT)

    #Subtitle activation

    settings_menu.add.toggle_switch(title="Subtitles", default=False, toggleswitch_id="subtitles")     

    #create the congifparser object for subtitles
    config_object = configparser.ConfigParser()

    config_object.add_section('Subtitles')
    
    #Font changes

    fonts = [("Arial", "arial"), ("Helvetica Neue", "helvetica"), ("Verdana", "verdana")] 

    settings_menu.add.dropselect(title="Select Subtitle Font", items=fonts, dropselect_id="font id", default=0) 
    
    config_object.add_section('Font')

    #Font size changes

    font_sizes = [("Small", "small"), ("Medium", "medium"), ("Large", "large")]

    settings_menu.add.selector(title="Subtitle Font size", items=font_sizes, selector_id="sub font size", default=0) 

    config_object.add_section('Font Size')

    #Subtitle colour changes

    subtitle_colours = [("Black", "black"), ("White", "white"), ("Red", "red"), ("Green", "green"), ("Blue", "blue"), ("Cyan", "cyan")]

    settings_menu.add.dropselect(title="Select Subtitle Font", items=subtitle_colours, dropselect_id="sub colour", default=0) 

    config_object.add_section('Font Colour')

    #Audio mute toggle

    settings_menu.add.toggle_switch(title="Mute audio", default=False, toggleswitch_id="mute")  

    config_object.add_section('Audio')

    #Reset to default settings

    settings_menu.add.toggle_switch(title="Reset Settings?", default=False, toggleswitch_id="setting reset")

    config_object.add_section('Reset')

    #Reset levels

    settings_menu.add.toggle_switch(title="Reset levels?", default=False, toggleswitch_id="level reset")

    config_object.add_section('Level Reset')
    
    # Sound Levels
    settings_menu.add.range_slider("Music", 50, [0, 100], 1)
    settings_menu.add.range_slider("SFX Volume", 50, [0, 100], 1)

    # Create a back button to return to the main menu
    settings_menu.add.button(title="Return To Main Menu", 
                        action=processSettingData, align=pm.locals.ALIGN_CENTER) 

    # Start the settings menu
    settings_menu.mainloop(screen)

#Back button to go to the main menu
def draw_back_button():
    # Create a new surface for the button
    button = pygame.Surface((100, 50))
    button.fill((255, 0, 0))  # Fill with red color

    # Get the rectangle of the button surface and set its top left position to (0, 0)
    button_rect = button.get_rect(topleft=(0, 0))

    # Blit the button surface onto the main screen surface
    screen.blit(button, button_rect)

    # Check if the button has been clicked
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            go_back = True
            return go_back   


display_main_menu()


import pygame
import sys
import pygame_menu as pm
import Campaign
import configparser
import os.path
import Settings

pygame.mixer.pre_init()
pygame.init()
window_width = 800  # Set your window dimensions
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("My Game")

IMAGE = pygame.image.load("placeholder_sprites\Clapping.png").convert_alpha()
class Player(pygame.sprite.Sprite):

    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

#Reset the config file to default settings for new user
def reset_config_file_new_user(settings):
    config_object = configparser.ConfigParser()

    config_object['Subtitles'] = {
        'subtitles_on': settings.getSubtitles()
    }
    config_object['Font'] = {
        'font_id': settings.getFont()
    }
    config_object['Font Size'] = {
        'sub_font_size': settings.getFontSize()
    }
    config_object['Font Colour'] = {
        'sub_colour': settings.getFontColour()
    }
    config_object['Audio'] = {
        'audio_level': settings.getAudio()
    }
    config_object['SFX'] = {
        'sfx_level': settings.getSFX()
    }
    config_object['Levels'] = {
        'level': settings.getLevel()
    }
    print(config_object)
    #save the config file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)

#Display Main menu
def display_main_menu():
    settings = Settings.Settings(False, 0, 1, 0, 0.5, 1.0, 1)


    # Create a Pygame Menu instance
    main_menu = pm.Menu("Main Menu", window_width, window_height, theme=pm.themes.THEME_DEFAULT)
    if os.path.isfile("config.ini") == False:
        reset_config_file_new_user(settings)
    #loads the info from the config file
    config_object = configparser.ConfigParser()
    config_object.read("config.ini")
    #if config function exist then update the global variables
    for section in config_object.sections():
        if section == "Subtitles":
            for key in config_object[section]:
                if key == "subtitles_on":
                    settings.setSubtitles(config_object[section][key] == "True")
        elif section == "Font":
            for key in config_object[section]:
                if key == "font_id":
                    settings.setFont(int(config_object[section][key]))
        elif section == "Font Size":
            for key in config_object[section]:
                if key == "sub_font_size":
                    settings.setFontSize(int(config_object[section][key]))
        elif section == "Font Colour":
            for key in config_object[section]:
                if key == "sub_colour":
                    settings.setFontColour(int(config_object[section][key]))
        elif section == "Audio":
            for key in config_object[section]:
                if key == "audio_level":
                    settings.setAudio(float(config_object[section][key]))
        elif section == "SFX":
            for key in config_object[section]:
                if key == "sfx_level":
                    settings.setSFX(float(config_object[section][key]))
        elif section == "Levels":
            for key in config_object[section]:
                if key == "level":
                    settings.setLevel(int(config_object[section][key]))


    # Add buttons to the menu
    main_menu.add.button(title="Play", 
                        action=lambda: display_game_menu(settings), align=pm.locals.ALIGN_CENTER)
    main_menu.add.button(title="Settings", 
                        action=lambda: display_settings_menu(settings), align=pm.locals.ALIGN_CENTER)
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
    
    main_menu.mainloop(screen)

# display game menu
def display_game_menu(settings):
    # Create a Pygame Menu instance
    game_menu = pm.Menu("Game menu", window_width, window_height, theme=pm.themes.THEME_DEFAULT)

    print("at the game menu")

    # Add buttons to the menu
    game_menu.add.button(title="Campaign mode", 
                        action=lambda: display_game_screen(0, settings), align=pm.locals.ALIGN_CENTER)
    game_menu.add.button(title="Freestyle mode", 
                        action=lambda: display_game_screen(1, settings), align=pm.locals.ALIGN_CENTER)
    # Create a back button to return to the main menu
    game_menu.add.button(title="Return To Main Menu", 
                        action=display_main_menu, align=pm.locals.ALIGN_CENTER) 
    # Start the menu
    game_menu.mainloop(screen)

def next_game(settings):
    # Create a Pygame Menu instance
    next_menu = pm.Menu("Congrats", window_width, window_height, theme=pm.themes.THEME_DEFAULT)

    # Add buttons to the menu
    next_menu.add.label(title="You have completed the level!", align=pm.locals.ALIGN_CENTER)
    next_menu.add.label(title="Well done!", align=pm.locals.ALIGN_CENTER)
    next_menu.add.label(title="You have unlocked the next level!", align=pm.locals.ALIGN_CENTER)
    #increment the global variable level by one
    newSetting = Settings.Settings(settings.getSubtitles(), settings.getFont(), settings.getFontSize(), settings.getFontColour(),settings.getAudio(), settings.getSFX(), settings.getLevel()+1)
    reset_config_file_new_user(newSetting)
    next_menu.add.button(title="Next Level", 
                        action=lambda: display_game_screen(0,settings), align=pm.locals.ALIGN_CENTER)
    next_menu.add.button(title="Return To Main Menu", 
                        action=display_main_menu, align=pm.locals.ALIGN_CENTER) 
    print("next level")
    # Start the menu
    next_menu.mainloop(screen)

def finished_campaign(settings):
    # Create a Pygame Menu instance
    next_menu = pm.Menu("Congrats", window_width, window_height, theme=pm.themes.THEME_DEFAULT)

    # Add buttons to the menu
    next_menu.add.label(title="You have completed the campaign!", align=pm.locals.ALIGN_CENTER)
    next_menu.add.label(title="Well done!", align=pm.locals.ALIGN_CENTER)
    newSetting = Settings.Settings(settings.getSubtitles(), settings.getFont(), settings.getFontSize(), settings.getFontColour(),settings.getAudio(), settings.getSFX(),1)
    reset_config_file_new_user(newSetting)
    next_menu.add.button(title="Return To Main Menu", 
                        action=display_main_menu, align=pm.locals.ALIGN_CENTER) 
    # Start the menu
    next_menu.mainloop(screen)


def display_game_screen(gamemode, settings):
    if gamemode == 0:
        try:
            game = Campaign.Campaign(settings.getLevel())
        except:
            finished_campaign(settings)
            return
    total_rounds = game.get_rounds()
    current_round = 0
    played = 0
    computer_played = False
    # load background image to the screen
    background = pygame.image.load("placeholder_sprites\IMG_5565.jpeg")
    # game loop to keep the window open
    while True:
        #clear the screen

        screen.blit(background, (0, 0))
        pygame.display.flip()  # update the screen
        if gamemode == 0:
            if current_round == total_rounds:
                next_game(settings)
                return
            if computer_played == False:
                pygame.time.delay(250)
                claps = int(game.get_round(current_round))
                for i in range(claps):

                    clap()
                    # make the sprite with image 1
                    player = Player((window_width / 2, window_height / 2), IMAGE)
                    # add the sprite to the group
                    player_group = pygame.sprite.Group(player)
                    # draw the sprite
                    player_group.draw(screen)
                    pygame.display.flip()  # update the screen
                    pygame.time.delay(500)
                    player_group.empty()
                    player_group.draw(screen)
                    pygame.display.flip()  # update the screen
                    print(f"clap {i} of {claps}" )
                computer_played = True

            if played > claps:
                played = 0
                current_round = 0
                computer_played = False
            if played == claps:
                current_round += 1
                played = 0
                computer_played = False
        for event in pygame.event.get():
            if gamemode == 0:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # make the sprite with image 1
                    player = Player((window_width / 2, window_height / 2), IMAGE)
                    # add the sprite to the group
                    player_group = pygame.sprite.Group(player)
                    # draw the sprite
                    player_group.draw(screen)
                    pygame.display.flip()  # update the screen
                    played += 1
                    clap()
                    pygame.time.delay(250)  
                    print(f"played {played} of {claps}")                  
                # when the user clicks the left mouse button play the sound
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print("mouse clicked")
                    # make the sprite with image 1
                    player = Player((window_width / 2, window_height / 2), IMAGE)
                    # add the sprite to the group
                    player_group = pygame.sprite.Group(player)
                    # draw the sprite
                    player_group.draw(screen)
                    pygame.display.flip()  # update the screen
                    played += 1
                    clap()
                    pygame.time.delay(250)      
                    print(f"played {played} of {claps}")
                    
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

#Settings menu logic
def display_settings_menu(settings):

    #Make the settings in config be reset to default
    def reset_settings():
        resetSettings = Settings.Settings(False, 0, 1, 0, 0.5, 1.0, 1)
        reset_config_file_new_user(resetSettings)   
        display_main_menu()


    def reset_level():
        resetSetting = Settings.Settings(settings.getSubtitles(), settings.getFont(), settings.getFontSize(), settings.getFontColour(),settings.getAudio(), settings.getSFX(), 1)
        reset_config_file_new_user(resetSetting)   
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
                    'font_id': settingsData[key][1]
                }
            elif key == "sub font size":
                config_object['Font Size'] = {
                    'sub_font_size': settingsData[key][1]
                }
            elif key == "sub colour":
                config_object['Font Colour'] = {
                    'sub_colour': settingsData[key][1]
                }
        config_object['Audio'] = {
            'audio_level': settings.getAudio()
        }
        config_object['SFX'] = {
            'sfx_level': settings.getSFX()
        }
        config_object['Levels'] = {
            'level': settings.getLevel()
        }

        #save the config file
        with open('config.ini', 'w') as conf:
            config_object.write(conf)
        
        display_main_menu()

    # Create a Pygame Menu instance
    settings_menu = pm.Menu("Settings", window_width, window_height, theme=pm.themes.THEME_DEFAULT)

    #Subtitle activation

    settings_menu.add.toggle_switch(title="Subtitles", default=settings.getSubtitles(), toggleswitch_id="subtitles")     

    #create the congifparser object for subtitles
    config_object = configparser.ConfigParser()

    config_object.add_section('Subtitles')
    
    #Font changes

    fonts = [("Arial", "arial"), ("Helvetica Neue", "helvetica"), ("Verdana", "verdana")] 

    settings_menu.add.dropselect(title="Select Subtitle Font", items=fonts, dropselect_id="font id", default=settings.getFont()) 
    
    config_object.add_section('Font')

    #Font size changes
    font_sizes = [("Small", "small"), ("Medium", "medium"), ("Large", "large")]

    settings_menu.add.selector(title="Subtitle Font size", items=font_sizes, selector_id="sub font size", default=settings.getFontSize()) 

    config_object.add_section('Font Size')

    subtitle_colours = [("Black", "black"), ("White", "white"), ("Red", "red"), ("Green", "green"), ("Blue", "blue"), ("Cyan", "cyan")]

    settings_menu.add.dropselect(title="Select Subtitle Font", items=subtitle_colours, dropselect_id="sub colour", default=settings.getFontColour()) 

    config_object.add_section('Font Colour')

    #Reset to default settings

    settings_menu.add.button(title="Reset settings", action=reset_settings, align=pm.locals.ALIGN_CENTER) 

    #Reset levels

    settings_menu.add.button(title="Reset level", action=reset_level, align=pm.locals.ALIGN_CENTER)


    def update_audio_level(value):
        settings.setAudio(value/100)

    # Sound Levels
    config_object.add_section('Audio')
    settings_menu.add.range_slider("Music", settings.getAudio()*100, [0, 100], 1,onchange=update_audio_level)

    def update_sfx_level(value):
        SFX_global = value/100

    config_object.add_section('SFX')
    settings_menu.add.range_slider("SFX Volume", settings.getSFX()*100, [0, 100], 1,onchange=update_sfx_level)

    # Create a back button to return to the main menu
    settings_menu.add.button(title="Return To Main Menu", action=processSettingData, align=pm.locals.ALIGN_CENTER) 

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


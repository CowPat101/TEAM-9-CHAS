import pygame
import sys
import pygame_menu as pm
import Campaign
import configparser
import os.path
import Settings
import time
import colours

pygame.mixer.pre_init()
pygame.init()
window_width = 800  # Set your window dimensions
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("My Game")
clap_x = pygame.mixer.Sound("placeholder_sounds\clap.ogg")

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
    pygame.mixer.music.stop()
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
    settings.setLevel(settings.getLevel()+1)
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


    #Function to display a subtitle to the screen while allowing complete interaction with the game
    def display(user, message):
        if settings.getSubtitles() == True:
            if time.time() - text_start_time < 3:  # Display text for 3 seconds

                
                #Choose a font and size
                if settings.getFont() == 0:
                    font = "Arial"
                elif settings.getFont() == 1:
                    font = "Helvetica Neue"
                elif settings.getFont() == 2:
                    font = "Verdana"  

                if settings.getFontSize() == 0:
                    font_size = 30 
                elif settings.getFontSize() == 1:
                    font_size = 40
                elif settings.getFontSize() == 2:
                    font_size = 50

                my_font = pygame.font.SysFont(font, font_size)

                if settings.getFontColour() == 0:
                    font_colour = colours.BLACK
                elif settings.getFontColour() == 1:
                    font_colour = colours.WHITE
                elif settings.getFontColour() == 2:
                    font_colour = colours.RED
                elif settings.getFontColour() == 3:
                    font_colour = colours.GREEN
                elif settings.getFontColour() == 4: 
                    font_colour = colours.BLUE
                elif settings.getFontColour() == 5:
                    font_colour = colours.CYAN 

                # Make the text and text box surfaces
                text_surface = my_font.render(f"{user} {message}", False, font_colour)  #Change font colour at the end
                text_rect = text_surface.get_rect() 

                # Create a new surface for the text box (Background colour)
                text_box = pygame.Surface((text_rect.width, text_rect.height))
                text_box.set_alpha(128)  # Set the alpha value of the color to make it transparent
                text_box.fill((200, 200, 200))  # Fill with light gray color

                #Modify the screen alignment of the text box

                # Get the rectangle of the text surface and center it in the text box surface
                text_rect.center = text_box.get_rect().center

                # Blit the text surface onto the text box surface
                text_box.blit(text_surface, text_rect)

                # Get the new rectangle of the text surface and center it in the screen surface
                text_rect = text_box.get_rect()
                text_rect.midbottom = screen.get_rect().midbottom

                # Blit the text box surface onto the main screen surface
                screen.blit(text_box, text_rect)
                
    pygame.mixer.music.load("placeholder_sounds/simple-loop.ogg") #sets music
    pygame.mixer.music.play(-1) #"-1" plays music indefinitely
    pygame.mixer.music.set_volume(0.5)  # Adjust the volume level (0.0 - 1.0)

    if gamemode == 0:
        try:
            game = Campaign.Campaign(settings.getLevel())
            print(f"level: {settings.getLevel()}")
            total_rounds = game.get_rounds()
            current_round = 0
            played = 0
            computer_played = False
        except:
            pygame.mixer.music.stop()
            finished_campaign(settings)
            display_main_menu()
    
    s1 = pygame.mixer.Sound("placeholder_sounds/beep1.ogg")
    s2 = pygame.mixer.Sound("placeholder_sounds/beep2.ogg")
    s3 = pygame.mixer.Sound("placeholder_sounds/beep3.ogg")
    s4 = pygame.mixer.Sound("placeholder_sounds/beep4.ogg")
    s5 = pygame.mixer.Sound("placeholder_sounds/beep5.ogg")

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
                    text_start_time = time.time()
                    display("Ringleader", "claps")
                    clap()
                    # make the sprite with image 1
                    comp = Player((window_width / 2, window_height / 2), IMAGE)
                    # add the sprite to the group
                    comp_group = pygame.sprite.Group(comp)
                    # draw the sprite
                    comp_group.draw(screen)
                    pygame.display.flip()  # update the screen
                    pygame.time.delay(500)
                    # the sprite with image deletes itself
                    screen.blit(background, (0, 0))
                    pygame.display.flip()  
                    pygame.time.delay(500)
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
            text_start_time = time.time()  
            if gamemode == 0:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    display("Player", "claps")
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
                    display("Player", "claps")
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
                        display("Player", "plays sound 1")
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s1)
                        pygame.time.delay(250)
                    if event.key == pygame.K_s:
                        display("Player", "plays sound 2")
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s2)
                        pygame.time.delay(250)
                    if event.key ==  pygame.K_d:
                        display("Player", "plays sound 3")
                        pygame.mixer.Sound.play(s3)
                        pygame.display.flip()
                        pygame.time.delay(250)
                    if event.key == pygame.K_f:
                        display("Player", "plays sound 4")
                        pygame.mixer.Sound.play(s4)
                        pygame.display.flip()
                        pygame.time.delay(250)
                    if event.key == pygame.K_g:
                        display("Player", "plays sound 5")
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s5)
                        pygame.time.delay(250)
                    if event.key == pygame.K_h:
                        display("Player", "claps")
                        print("mouse clicked")
                        # make the sprite with image 1
                        player = Player((window_width / 2, window_height / 2), IMAGE)
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()  # update the screen
                        clap()
                        pygame.time.delay(250)      
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                display_main_menu()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        

def play_sound(sound):
    """"""
    pass

def clap():
    pygame.mixer.Sound.play(clap_x)

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


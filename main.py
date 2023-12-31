import pygame
import sys
import pygame_menu as pm
import configparser
import os.path
import time

# Constants for fonts
FONT_OPTIONS = [
    ("Arial", "arial"),
    ("Helvetica Neue", "helvetica"),
    ("Verdana", "verdana"),
]
FONT_SIZE_OPTIONS = [
    ("Small", "small", 30),
    ("Medium", "medium", 40),
    ("Large", "large", 50),
]
FONT_COLOR_OPTIONS = [
    ("Black", "black"),
    ("White", "white"),
    ("Red", "red"),
    ("Green", "green"),
    ("Blue", "blue"),
    ("Cyan", "cyan"),
]


# fixes all files acessed for pyinstaller
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#Define colours global
RED = (255, 0, 0)
CYAN = (0, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)

#Update background theme
BACKGROUND_IMAGE = resource_path("resources/placeholder_sprites/background.png")
MYTHEME_GLOBAL = pm.themes.THEME_ORANGE.copy()
MYTHEME_GLOBAL.widget_font_color = BLACK
MYTHEME_GLOBAL.widget_font_color_focused = BLACK
MYTHEME_GLOBAL.widget_font_color_selected = BLACK
MYTHEME_GLOBAL.title_background_color = BLACK
MYTHEME_GLOBAL.selection_color = BLACK

myimage = pm.baseimage.BaseImage(
    image_path=BACKGROUND_IMAGE, drawing_mode=pm.baseimage.IMAGE_MODE_SIMPLE
)

MYTHEME_GLOBAL.background_color = myimage

#Define the class for the campaign
class Campaign:
    level_info = []
    rounds = -1
    current_round = 0

    def __init__(self, level):
        try:
            # Use resource_path to get the absolute path of the level file
            level_file = resource_path(f"resources/levels/level{level}.txt")
            open_level = open(level_file, "r")
            self.level_info = open_level.readlines()
            self.rounds = len(self.level_info)
        except:
            print("Error: Level not found")
            exit()

    def get_round(self, round_num):
        return self.level_info[round_num]

    def get_rounds(self):
        return self.rounds

#Define the class for the settings
class Settings:
    Subtitles = False
    Font = "arial"
    Font_size = "medium"
    Font_colour = "black"
    Audio = 0.5
    SFX = 1.0
    Level = 1

    # declare all the variables that will be used in the settings menu
    def __init__(
        self, gSubtitles, gFont, gFont_size, gFont_colour, gAudio, gSFX, gLevel
    ):
        # assign the variables to the values passed in the constructor
        self.Subtitles = gSubtitles
        self.Font = gFont
        self.Font_size = gFont_size
        self.Font_colour = gFont_colour
        self.Audio = gAudio
        self.SFX = gSFX
        self.Level = gLevel

    # getters for all the variables
    getSubtitles = lambda self: self.Subtitles
    getFont = lambda self: self.Font
    getFontSize = lambda self: self.Font_size
    getFontColour = lambda self: self.Font_colour
    getAudio = lambda self: self.Audio
    getSFX = lambda self: self.SFX
    getLevel = lambda self: self.Level
    # setters for all the variables
    setSubtitles = lambda self, gSubtitles: setattr(self, "Subtitles", gSubtitles)
    setFont = lambda self, gFont: setattr(self, "Font", gFont)
    setFontSize = lambda self, gFont_size: setattr(self, "Font_size", gFont_size)
    setFontColour = lambda self, gFont_colour: setattr(
        self, "Font_colour", gFont_colour
    )
    setAudio = lambda self, gAudio: setattr(self, "Audio", gAudio)
    setSFX = lambda self, gSFX: setattr(self, "SFX", gSFX)
    setLevel = lambda self, gLevel: setattr(self, "Level", gLevel)

#Initialise pygame
def initialize_pygame():
    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.init()
    window_width = 800
    window_height = 600
    screen = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption("My Game")
    return screen, window_width, window_height

#Load sound
def load_sound(filename, volume):
    sound = pygame.mixer.Sound(filename)
    sound.set_volume(volume)
    return sound

#Define the class for the images
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)


# Reset the config file to default settings for new user
def reset_config_file_new_user(settings):
    config_object = configparser.ConfigParser()

    config_object["Subtitles"] = {"subtitles_on": settings.getSubtitles()}
    config_object["Font"] = {"font_id": settings.getFont()}
    config_object["Font Size"] = {"sub_font_size": settings.getFontSize()}
    config_object["Font Colour"] = {"sub_colour": settings.getFontColour()}
    config_object["Audio"] = {"audio_level": settings.getAudio()}
    config_object["SFX"] = {"sfx_level": settings.getSFX()}
    config_object["Levels"] = {"level": settings.getLevel()}
    print(config_object)
    # save the config file
    with open("config.ini", "w") as conf:
        config_object.write(conf)


# Display Main menu
def display_main_menu(screen, window_width, window_height):
    settings = Settings(False, 0, 1, 0, 0.5, 1.0, 1)

    # Create a Pygame Menu instance
    main_menu = pm.Menu("Main Menu", window_width, window_height, theme=MYTHEME_GLOBAL)

    main_menu._touchscreen = True
    if os.path.isfile("config.ini") == False:
        reset_config_file_new_user(settings)
    # loads the info from the config file
    config_object = configparser.ConfigParser()
    config_object.read("config.ini")
    # if config function exist then update the global variables
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
    main_menu.add.button(
        title="Play",
        action=lambda: display_game_menu(settings, screen, window_width, window_height),
        align=pm.locals.ALIGN_CENTER,
    )
    main_menu.add.button(
        title="Settings",
        action=lambda: display_settings_menu(
            settings, screen, window_width, window_height
        ),
        align=pm.locals.ALIGN_CENTER,
    )
    main_menu.add.button(
        title="Quit", action=pm.events.EXIT, align=pm.locals.ALIGN_CENTER
    )

    print("Printing config file contents:")

    # get the data from the config file
    config_object = configparser.ConfigParser()
    config_object.read("config.ini")
    for section in config_object.sections():
        print(f"[{section}]")
        for key in config_object[section]:
            print(f"{key} : {config_object[section][key]}")

    main_menu.mainloop(screen)


# display game menu
def display_game_menu(settings, screen, window_width, window_height):
    pygame.mixer.music.stop()
    # Create a Pygame Menu instance
    game_menu = pm.Menu("Game menu", window_width, window_height, theme=MYTHEME_GLOBAL)
    game_menu._touchscreen = True

    print("at the game menu")

    # Add buttons to the menu
    game_menu.add.button(
        title="Campaign mode",
        action=lambda: display_game_screen(
            0, settings, screen, window_width, window_height
        ),
        align=pm.locals.ALIGN_CENTER,
    )
    game_menu.add.button(
        title="Freestyle mode",
        action=lambda: display_game_screen(
            1, settings, screen, window_width, window_height
        ),
        align=pm.locals.ALIGN_CENTER,
    )
    # Create a back button to return to the main menu
    game_menu.add.button(
        title="Return To Main Menu",
        action=lambda: display_main_menu(screen, window_width, window_height),
        align=pm.locals.ALIGN_CENTER,
    )
    # Start the menu
    game_menu.mainloop(screen)

#Display if level complete
def next_game(settings, screen, window_width, window_height):
    # Create a Pygame Menu instance
    next_menu = pm.Menu("Congrats", window_width, window_height, theme=MYTHEME_GLOBAL)
    next_menu._touchscreen = True

    # Add buttons to the menu
    next_menu.add.label(
        title="You have completed the level!", align=pm.locals.ALIGN_CENTER
    )
    next_menu.add.label(title="Well done!", align=pm.locals.ALIGN_CENTER)
    next_menu.add.label(
        title="You have unlocked the next level!", align=pm.locals.ALIGN_CENTER
    )
    # increment the global variable level by one
    newSetting = Settings(
        settings.getSubtitles(),
        settings.getFont(),
        settings.getFontSize(),
        settings.getFontColour(),
        settings.getAudio(),
        settings.getSFX(),
        settings.getLevel() + 1,
    )
    settings.setLevel(settings.getLevel() + 1)
    reset_config_file_new_user(newSetting)
    next_menu.add.button(
        title="Next Level",
        action=lambda: display_game_screen(
            0, settings, screen, window_width, window_height
        ),
        align=pm.locals.ALIGN_CENTER,
    )
    next_menu.add.button(
        title="Return To Main Menu",
        action=lambda: display_main_menu(screen, window_width, window_height),
        align=pm.locals.ALIGN_CENTER,
    )
    print("next level")
    # Start the menu
    next_menu.mainloop(screen)

#Display after all levels complete
def finished_campaign(settings, screen, window_width, window_height):
    # Create a Pygame Menu instance
    next_menu = pm.Menu("Congrats", window_width, window_height, theme=MYTHEME_GLOBAL)
    next_menu._touchscreen = True

    # Add buttons to the menu
    next_menu.add.label(
        title="You have completed the campaign!", align=pm.locals.ALIGN_CENTER
    )
    next_menu.add.label(title="Well done!", align=pm.locals.ALIGN_CENTER)
    newSetting = Settings(
        settings.getSubtitles(),
        settings.getFont(),
        settings.getFontSize(),
        settings.getFontColour(),
        settings.getAudio(),
        settings.getSFX(),
        1,
    )
    reset_config_file_new_user(newSetting)
    next_menu.add.button(
        title="Return To Main Menu",
        action=lambda: display_main_menu(screen, window_width, window_height),
        align=pm.locals.ALIGN_CENTER,
    )
    # Start the menu
    next_menu.mainloop(screen)

#Display the game being played
def display_game_screen(gamemode, settings, screen, window_width, window_height):
    # Function to display a subtitle to the screen while allowing complete interaction with the game
    def display(user, message):
        if settings.getSubtitles() == True:
            if time.time() - text_start_time < 3:  # Display text for 3 seconds
                my_font = pygame.font.SysFont(
                    FONT_OPTIONS[settings.getFont()][1],
                    FONT_SIZE_OPTIONS[settings.getFontSize()][2],
                )

                if settings.getFontColour() == 0:
                    font_colour = BLACK
                elif settings.getFontColour() == 1:
                    font_colour = WHITE
                elif settings.getFontColour() == 2:
                    font_colour = RED
                elif settings.getFontColour() == 3:
                    font_colour = GREEN
                elif settings.getFontColour() == 4:
                    font_colour = BLUE
                elif settings.getFontColour() == 5:
                    font_colour = CYAN

                # Make the text and text box surfaces
                text_surface = my_font.render(
                    f"{user} {message}", False, font_colour
                )  # Change font colour at the end
                text_rect = text_surface.get_rect()

                # Create a new surface for the text box (Background colour)
                text_box = pygame.Surface((text_rect.width, text_rect.height))
                text_box.set_alpha(
                    128
                )  # Set the alpha value of the color to make it transparent
                text_box.fill((200, 200, 200))  # Fill with light gray color

                # Modify the screen alignment of the text box

                # Get the rectangle of the text surface and center it in the text box surface
                text_rect.center = text_box.get_rect().center

                # Blit the text surface onto the text box surface
                text_box.blit(text_surface, text_rect)

                # Get the new rectangle of the text surface and center it in the screen surface
                text_rect = text_box.get_rect()
                text_rect.midbottom = screen.get_rect().midbottom

                # Blit the text box surface onto the main screen surface
                screen.blit(text_box, text_rect)

    pygame.mixer.music.load(
        resource_path("resources/placeholder_sounds/simple-loop.ogg")
    )  # sets music
    pygame.mixer.music.play(-1)  # "-1" plays music indefinitely
    pygame.mixer.music.set_volume(
        1 * settings.getAudio()
    )  # Adjust the volume level (0.0 - 1.0)
    # Adjust the volume level (0.0 - 1.0)

    if gamemode == 0:
        try:
            game = Campaign(settings.getLevel())
            print(f"level: {settings.getLevel()}")
            total_rounds = game.get_rounds()
            current_round = 0
            played = 0
            computer_played = False
        except:
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(0)
            finished_campaign(settings, screen, window_width, window_height)
            display_main_menu(screen, window_width, window_height)

    clap_x = pygame.mixer.Sound(resource_path("resources/placeholder_sounds/clap.ogg"))
    clap_y = pygame.mixer.Sound(resource_path("resources/placeholder_sounds/con_clap.ogg"))
    s1 = pygame.mixer.Sound(resource_path("resources/placeholder_sounds/piano-a.ogg"))
    s2 = pygame.mixer.Sound(resource_path("resources/placeholder_sounds/piano-b.ogg"))
    s3 = pygame.mixer.Sound(resource_path("resources/placeholder_sounds/piano-c.ogg"))
    s4 = pygame.mixer.Sound(resource_path("resources/placeholder_sounds/piano-d.ogg"))
    s5 = pygame.mixer.Sound(resource_path("resources/placeholder_sounds/piano-e.ogg"))
    s6 = pygame.mixer.Sound(resource_path("resources/placeholder_sounds/piano-f.ogg"))
    s7 = pygame.mixer.Sound(resource_path("resources/placeholder_sounds/piano-g.ogg"))

    # set volume of sounds
    s1.set_volume(1 * settings.getSFX())
    s2.set_volume(1 * settings.getSFX())
    s3.set_volume(1 * settings.getSFX())
    s4.set_volume(1 * settings.getSFX())
    s5.set_volume(1 * settings.getSFX())
    s6.set_volume(1 * settings.getSFX())
    s7.set_volume(1 * settings.getSFX())
    clap_x.set_volume(1 * settings.getSFX())
    clap_y.set_volume(1 * settings.getSFX())

    # load background image to the screen
    background = pygame.image.load(BACKGROUND_IMAGE)
    clap_image = pygame.image.load(
        resource_path("resources/placeholder_sprites/Clapping.png")
    ).convert_alpha()
    piano_image_blank = pygame.image.load(
        resource_path("resources/placeholder_sprites/keyboards/Keyboard-blank.png")
    ).convert_alpha()
    piano_image_blank = pygame.transform.scale(
        piano_image_blank,
        (
            int(piano_image_blank.get_width() * 0.75),
            int(piano_image_blank.get_height() * 0.75),
        ),
    )
    piano_imageA = pygame.image.load(
        resource_path("resources/placeholder_sprites/keyboards/Keyboard-A.png")
    ).convert_alpha()
    piano_imageA = pygame.transform.scale(
        piano_imageA,
        (int(piano_imageA.get_width() * 0.75), int(piano_imageA.get_height() * 0.75)),
    )
    piano_imageB = pygame.image.load(
        resource_path("resources/placeholder_sprites/keyboards/Keyboard-B.png")
    ).convert_alpha()
    piano_imageB = pygame.transform.scale(
        piano_imageB,
        (int(piano_imageB.get_width() * 0.75), int(piano_imageB.get_height() * 0.75)),
    )
    piano_imageC = pygame.image.load(
        resource_path("resources/placeholder_sprites/keyboards/Keyboard-C.png")
    ).convert_alpha()
    piano_imageC = pygame.transform.scale(
        piano_imageC,
        (int(piano_imageC.get_width() * 0.75), int(piano_imageC.get_height() * 0.75)),
    )
    piano_imageD = pygame.image.load(
        resource_path("resources/placeholder_sprites/keyboards/Keyboard-D.png")
    ).convert_alpha()
    piano_imageD = pygame.transform.scale(
        piano_imageD,
        (int(piano_imageD.get_width() * 0.75), int(piano_imageD.get_height() * 0.75)),
    )
    piano_imageE = pygame.image.load(
        resource_path("resources/placeholder_sprites/keyboards/Keyboard-E.png")
    ).convert_alpha()
    piano_imageE = pygame.transform.scale(
        piano_imageE,
        (int(piano_imageE.get_width() * 0.75), int(piano_imageE.get_height() * 0.75)),
    )
    piano_imageF = pygame.image.load(
        resource_path("resources/placeholder_sprites/keyboards/Keyboard-F.png")
    ).convert_alpha()
    piano_imageF = pygame.transform.scale(
        piano_imageF,
        (int(piano_imageF.get_width() * 0.75), int(piano_imageF.get_height() * 0.75)),
    )
    piano_imageG = pygame.image.load(
        resource_path("resources/placeholder_sprites/keyboards/Keyboard-G.png")
    ).convert_alpha()
    piano_imageG = pygame.transform.scale(
        piano_imageG,
        (int(piano_imageG.get_width() * 0.75), int(piano_imageG.get_height() * 0.75)),
    )

    # Define the button rectangle
    button_rect = pygame.Rect(10, 10, 100, 50)

    key_rectA = pygame.Rect(96, 92, 82, 347)
    key_rectB = pygame.Rect(184, 92, 82, 347)
    key_rectC = pygame.Rect(272, 92, 82, 347)
    key_rectD = pygame.Rect(360, 92, 82, 347)
    key_rectE = pygame.Rect(448, 92, 82, 347)
    key_rectF = pygame.Rect(536, 92, 82, 347)
    key_rectG = pygame.Rect(624, 92, 82, 347)


    # Define the button text
    button_font = pygame.font.SysFont("Helvetica Neue", 40)
    if settings.getFontColour() == 0:
        font_default_colour = BLACK
    elif settings.getFontColour() == 1:
        font_default_colour = WHITE
    elif settings.getFontColour() == 2:
        font_default_colour = RED
    elif settings.getFontColour() == 3:
        font_default_colour = GREEN
    elif settings.getFontColour() == 4:
        font_default_colour = BLUE
    elif settings.getFontColour() == 5:
        font_default_colour = CYAN
    button_text = button_font.render("Return", True, font_default_colour)

    # game loop to keep the window open
    while True:
        # clear the screen
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, GREY, button_rect)
        screen.blit(button_text, button_rect.move(5, 5))
        if gamemode == 1:
            blank = Player((window_width / 2, window_height / 2), piano_image_blank)
            # add the sprite to the group
            blank_group = pygame.sprite.Group(blank)
            # draw the sprite
            blank_group.draw(screen)
        pygame.display.flip()  # update the screen
        if gamemode == 0:
            if current_round == total_rounds:
                pygame.mixer.music.set_volume(0)
                next_game(settings, screen, window_width, window_height)
                return
            if computer_played == False:
                pygame.time.delay(250)
                claps = int(game.get_round(current_round))
                for i in range(claps):
                    text_start_time = time.time()
                    display("Ringleader", "claps")
                    pygame.mixer.Sound.play(clap_y)
                    # make the sprite with image 1clapclap_image
                    comp = Player((window_width / 2, window_height / 2), clap_image)
                    # add the sprite to the group
                    comp_group = pygame.sprite.Group(comp)
                    # draw the sprite
                    comp_group.draw(screen)
                    pygame.display.flip()  # update the screen
                    pygame.time.delay(500)
                    # the sprite with image deletes itself
                    screen.blit(background, (0, 0))
                    pygame.draw.rect(screen, GREY, button_rect)
                    screen.blit(button_text, button_rect.move(5, 5))
                    pygame.display.flip()
                    pygame.time.delay(500)
                    print(f"clap {i} of {claps}")
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
                    # make the sprite with image clap_image
                    player = Player((window_width / 2, window_height / 2), clap_image)
                    # add the sprite to the group
                    player_group = pygame.sprite.Group(player)
                    # draw the sprite
                    player_group.draw(screen)
                    pygame.display.flip()  # update the screen
                    played += 1
                    pygame.mixer.Sound.play(clap_x)
                    pygame.time.delay(250)
                    print(f"played {played} of {claps}")
                # when the user clicks the left mouse button play the sound
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    display("Player", "claps")
                    print("mouse clicked")
                    # make the sprite with image clap_image
                    player = Player((window_width / 2, window_height / 2), clap_image)
                    # add the sprite to the group
                    player_group = pygame.sprite.Group(player)
                    # draw the sprite
                    player_group.draw(screen)
                    pygame.display.flip()  # update the screen
                    played += 1
                    pygame.mixer.Sound.play(clap_x)
                    pygame.time.delay(250)
                    print(f"played {played} of {claps}")

            if gamemode == 1:
                # draw the button for the keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key A")
                        # load the image and scale it to 75% of its original size
                        # add an image of piano key A in the bottom center by padd it so its 30 pixels above it
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageA
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s1)
                        pygame.time.delay(250)
                    if event.key == pygame.K_s:
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key B")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageB
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s2)
                        pygame.time.delay(250)
                    if event.key == pygame.K_d:
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key C")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageC
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s3)
                        pygame.time.delay(250)
                    if event.key == pygame.K_f:
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key D")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageD
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s4)
                        pygame.time.delay(250)
                    if event.key == pygame.K_g:
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key E")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageE
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s5)
                        pygame.time.delay(250)
                    if event.key == pygame.K_h:
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key F")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageF
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s6)
                        pygame.time.delay(250)
                    if event.key == pygame.K_j:
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key G")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageG
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s7)
                        pygame.time.delay(250)
                    if event.key == pygame.K_k:
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "claps")
                        print("mouse clicked")
                        # make the sprite with image 1clapclap_image
                        player = Player(
                            (window_width / 2, window_height / 2), clap_image
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()  # update the screen
                        pygame.mixer.Sound.play(clap_x)
                        pygame.time.delay(250)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if key_rectA.collidepoint(pygame.mouse.get_pos()):
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key A")
                        # load the image and scale it to 75% of its original size
                        # add an image of piano key A in the bottom center by padd it so its 30 pixels above it
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageA
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s1)
                        pygame.time.delay(250)
                    if key_rectB.collidepoint(pygame.mouse.get_pos()):
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key B")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageB
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s2)
                        pygame.time.delay(250)
                    if key_rectC.collidepoint(pygame.mouse.get_pos()):
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key C")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageC
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s3)
                        pygame.time.delay(250)
                    if key_rectD.collidepoint(pygame.mouse.get_pos()):
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key D")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageD
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s4)
                        pygame.time.delay(250)
                    if key_rectE.collidepoint(pygame.mouse.get_pos()):
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key E")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageE
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s5)
                        pygame.time.delay(250)
                    if key_rectF.collidepoint(pygame.mouse.get_pos()):
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key F")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageF
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s6)
                        pygame.time.delay(250)
                    if key_rectG.collidepoint(pygame.mouse.get_pos()):
                        screen.blit(background, (0, 0))
                        pygame.draw.rect(screen, GREY, button_rect)
                        screen.blit(button_text, button_rect.move(5, 5))
                        display("Player", "plays piano key G")
                        player = Player(
                            (window_width / 2, window_height / 2), piano_imageG
                        )
                        # add the sprite to the group
                        player_group = pygame.sprite.Group(player)
                        # draw the sprite
                        player_group.draw(screen)
                        pygame.display.flip()
                        pygame.mixer.Sound.play(s7)
                        pygame.time.delay(250)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                display_main_menu(screen, window_width, window_height)
            elif (
                button_rect.collidepoint(pygame.mouse.get_pos())
                and event.type == pygame.MOUSEBUTTONDOWN
            ):
                pygame.mixer.music.stop()
                display_main_menu(screen, window_width, window_height)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Settings menu logic
def display_settings_menu(settings, screen, window_width, window_height):
    # Make the settings in config be reset to default
    def reset_settings():
        resetSettings = Settings(False, 0, 1, 0, 0.5, 1.0, settings.getLevel())
        reset_config_file_new_user(resetSettings)
        display_main_menu(screen, window_width, window_height)

    def reset_level():
        resetSetting = Settings(
            settings.getSubtitles(),
            settings.getFont(),
            settings.getFontSize(),
            settings.getFontColour(),
            settings.getAudio(),
            settings.getSFX(),
            1,
        )
        reset_config_file_new_user(resetSetting)
        display_main_menu(screen, window_width, window_height)

    # Function to process the data from the settings menu and update settings menu
    def processSettingData():
        # print the data settings to the console
        print("\n\n")
        settingsData = settings_menu.get_input_data()

        # write the data to the config file
        for key in settingsData.keys():
            print(f"{key}\t:\t{settingsData[key]}")

            if key == "subtitles":
                config_object["Subtitles"] = {"subtitles_on": settingsData[key]}
            elif key == "font id":
                config_object["Font"] = {"font_id": settingsData[key][1]}
            elif key == "sub font size":
                config_object["Font Size"] = {"sub_font_size": settingsData[key][1]}
            elif key == "sub colour":
                config_object["Font Colour"] = {"sub_colour": settingsData[key][1]}
        config_object["Audio"] = {"audio_level": settings.getAudio()}
        config_object["SFX"] = {"sfx_level": settings.getSFX()}
        config_object["Levels"] = {"level": settings.getLevel()}

        # save the config file
        with open("config.ini", "w") as conf:
            config_object.write(conf)

        display_main_menu(screen, window_width, window_height)

    # Create a Pygame Menu instance
    settings_menu = pm.Menu(
        "Settings", window_width, window_height, theme=MYTHEME_GLOBAL
    )
    settings_menu._touchscreen = True

    config_object = configparser.ConfigParser()
    # Subtitle activation

    settings_menu.add.toggle_switch(
        title="Subtitles", default=settings.getSubtitles(), toggleswitch_id="subtitles"
    )

    # create the congifparser object for subtitles

    config_object.add_section("Subtitles")

    settings_menu.add.dropselect(
        title="Select Subtitle Font",
        items=FONT_OPTIONS,
        dropselect_id="font id",
        default=settings.getFont(),
    )

    config_object.add_section("Font")

    settings_menu.add.selector(
        title="Subtitle Font size",
        items=FONT_SIZE_OPTIONS,
        selector_id="sub font size",
        default=settings.getFontSize(),
    )

    config_object.add_section("Font Size")

    subtitle_colours = [
        ("Black", "black"),
        ("White", "white"),
        ("Red", "red"),
        ("Green", "green"),
        ("Blue", "blue"),
        ("Cyan", "cyan"),
    ]

    settings_menu.add.dropselect(
        title="Select Subtitle Font",
        items=FONT_COLOR_OPTIONS,
        dropselect_id="sub colour",
        default=settings.getFontColour(),
    )

    config_object.add_section("Font Colour")

    # Reset to default settings

    settings_menu.add.button(
        title="Reset settings", action=reset_settings, align=pm.locals.ALIGN_CENTER
    )

    # Reset levels

    settings_menu.add.button(
        title="Reset level", action=reset_level, align=pm.locals.ALIGN_CENTER
    )

    def update_audio_level(value):
        settings.setAudio(value / 100)

    # Sound Levels
    config_object.add_section("Audio")
    settings_menu.add.range_slider(
        "Music", settings.getAudio() * 100, [0, 100], 1, onchange=update_audio_level
    )

    def update_sfx_level(value):
        settings.setSFX(value / 100)

    config_object.add_section("SFX")
    settings_menu.add.range_slider(
        "SFX Volume", settings.getSFX() * 100, [0, 100], 1, onchange=update_sfx_level
    )

    # Create a back button to return to the main menu
    settings_menu.add.button(
        title="Return To Main Menu",
        action=processSettingData,
        align=pm.locals.ALIGN_CENTER,
    )

    # Start the settings menu
    settings_menu.mainloop(screen)


if __name__ == "__main__":
    screen, window_width, window_height = initialize_pygame()
    display_main_menu(screen, window_width, window_height)

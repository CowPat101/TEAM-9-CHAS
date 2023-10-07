import pygame
import sys
import pygame_menu as pm
import campaign
import freestyle

pygame.mixer.pre_init()
pygame.init()
window_width = 800  # Set your window dimensions
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("My Game")
 
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

    # Start the menu
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
    image = pygame.image.load("placeholder_sprites\NotClapping.png")
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
    # Create a Pygame Menu instance
    settings_menu = pm.Menu("Settings", window_width, window_height, theme=pm.themes.THEME_DEFAULT)

    # Add settings items here (e.g., sliders, checkboxes)

    # Create a back button to return to the main menu
    settings_menu.add.button(title="Return To Main Menu", 
                        action=display_main_menu, align=pm.locals.ALIGN_CENTER) 

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


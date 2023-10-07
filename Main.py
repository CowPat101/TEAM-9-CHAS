import pygame
import sys
import time
import pygame_menu as pm
import colours as cs


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

def display_game_screen():
    # load background image to the screen
    background = pygame.image.load("placeholder_sprites\IMG_5565.jpeg")
    screen.blit(background, (0, 0))
    pygame.display.flip()  # update the screen

    # game loop to keep the window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def campaign_mode():
    display_game_screen()
    pass
def freestyle_mode():
    display_game_screen()
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


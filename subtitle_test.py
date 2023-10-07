import pygame
import sys
import time
import pygame_menu as pm

pygame.init()
window_width = 800  # Set your window dimensions
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("My Game")
 
# Standard RGB colors 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
CYAN = (0, 100, 100) 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 

import pygame
import sys
import time
import pygame_menu as pm

pygame.init()
window_width = 800  # Set your window dimensions
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("My Game")
 
# Standard RGB colors 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
CYAN = (0, 100, 100) 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 

#Settings menu logic
def display_settings_menu():
    # Create a Pygame Menu instance
    settings_menu = pm.Menu("Settings", window_width, window_height, theme=pm.themes.THEME_DEFAULT)

    # Add settings items here (e.g., sliders, checkboxes)

    # Create a back button to return to the main menu
    settings_menu.add.button(title="Return To Main Menu", 
                        action=game_loop, align=pm.locals.ALIGN_CENTER) 

    # Start the settings menu
    settings_menu.mainloop(screen)

#Test button to ensure interaction can be completed while subtitles are displayed
def draw_button():
    # Create a new surface for the button
    button = pygame.Surface((100, 50))
    button.fill((255, 0, 0))  # Fill with red color

    # Get the rectangle of the button surface and center it in the screen surface
    button_rect = button.get_rect()
    button_rect.center = screen.get_rect().center

    # Blit the button surface onto the main screen surface
    screen.blit(button, button_rect)

    # Check if the button has been clicked
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            print("test")

def game_loop():

    text_to_display = ""
    display_text = False
    text_start_time = 0

    #Function to display a subtitle to the screen while allowing complete interaction with the game
    def display():
        if time.time() - text_start_time < 3:  # Display text for 3 seconds
            #Choose a font and size
            my_font = pygame.font.SysFont('Comic Sans MS', 30) 

            # Make the text and text box surfaces
            text_surface = my_font.render('Some Text', False, (255, 255, 255))  #Change font colour at the end
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
        else:
            display_text = False   

    #Main game loop for interaction with the game - be it display subtitles, access a menu, hit a beat etc.   
    running = True
    test = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    display_text = True
                    text_start_time = time.time()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    running = False
                    test = True
                    
        if test == False:

            screen.fill((0, 0, 0))  

            draw_button()

            if display_text:
                display()
                print("testing")

            pygame.display.flip()


    #Break out of the loop once button is clicked - Allows menu changes
    if test == True:
        #open settings menu
        display_settings_menu()
        game_loop()
    else:
        pygame.quit()
        sys.exit()


game_loop()



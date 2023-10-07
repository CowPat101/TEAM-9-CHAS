import pygame
import sys
import time
import pygame_menu as pm
import colours as cs

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
                        action=game_loop, align=pm.locals.ALIGN_CENTER)
    main_menu.add.button(title="Settings", 
                        action=display_settings_menu, align=pm.locals.ALIGN_CENTER)
    main_menu.add.button(title="Quit", 
                        action=pm.events.EXIT, align=pm.locals.ALIGN_CENTER)

    # Start the menu
    main_menu.mainloop(screen)


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

#Back button to go to the main menu
def draw_back_button():
    # Create a new surface for the button
    button = pygame.Surface((100, 50))
    button.fill(cs.RED)  # Fill with red color

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

#Main Logic function of the program
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
            text_box.fill(cs.GREY)  # Fill with light gray color

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
     
    #Set up identifiers for the loop for exiting the main page
    running = True
    go_back = False
    exit_loop = False
    go_settings = False
    go_main = False

    while running:
        #These for loops look for keyboard inputs for their functions to run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    display_text = True
                    text_start_time = time.time()
            elif event.type == pygame.MOUSEBUTTONDOWN: # Go to settings from mouseclick on game screen
                if event.button == 3:
                    running = False
                    exit_loop = True
                    go_settings = True

        #This loop runs the main game screen - WRITE YOUR GAME CODE IN THIS IF STATEMENT - FOR THE GAME SCREEN            
        if exit_loop == False:

            screen.fill(cs.WHITE)  

            #Get the action from the back button on the game screen
            go_back = draw_back_button()

            #Update the loop exit identifiers
            if go_back == True:
                running = False
                exit_loop = True
                go_main = True

            if display_text:
                display()
                print("testing")

            pygame.display.flip()
        

    #Break out of the loop to different menus
    if exit_loop == True:
        if go_settings == True:
            display_settings_menu()
        elif go_main == True:
            display_main_menu()
    else:
        pygame.quit()
        sys.exit()


display_main_menu()



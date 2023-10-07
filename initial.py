#import necessary modules
import pygame
import time

def quitgame():
    pygame.quit()
    quit()

#gets sounds from source files and loads them into mixer so they can be recalled
def load_sounds(source_list):
    sounds = []
    
    for s in source_list:
        sounds.append(pygame.mixer.Sound(s))
    
    return sounds

#contains code that only needs to be executed when running this .py file as standalone program
def main():
    pygame.mixer.pre_init() #dark magic to ward away input lag, must be cast before pygame.init()
    pygame.init()
    
    #display settings
    display_width = 800
    display_height = 600
    pygame.display.set_mode((display_width,display_height))	

#main game function
def game():
    
    clock = pygame.time.Clock() #will be used eventually to set framerate
    
    paused = False
    
    #actually linking sounds from source files (ideally this would be done through some sort of settings file)
    sound_sources = ["placeholder_sounds/beep1.ogg",
                     "placeholder_sounds/beep2.ogg",
                     "placeholder_sounds/beep3.ogg",
                     "placeholder_sounds/beep4.ogg",
                     "placeholder_sounds/beep5.ogg"]
    sound = load_sounds(sound_sources)
    
    pygame.mixer.music.load("placeholder_sounds/simple-loop.ogg") #sets music
    pygame.mixer.music.play(-1) #"-1" plays music indefinitely
    
    #sets keybindings (again, ideally settings file)
    keybinds = {"s0": pygame.K_a,
                "s1": pygame.K_s,
                "s2": pygame.K_d,
                "s3": pygame.K_f,
                "s4": pygame.K_g,
                "pause": pygame.K_p,
                }
    
    #main game loop
    while not paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            
            #handles button presses
            if event.type == pygame.KEYDOWN:
                if event.key == keybinds["s0"]:
                    pygame.mixer.Sound.play(sound[0])
                if event.key == keybinds["s1"]:
                    pygame.mixer.Sound.play(sound[1])
                if event.key == keybinds["s2"]:
                    pygame.mixer.Sound.play(sound[2])
                if event.key == keybinds["s3"]:
                    pygame.mixer.Sound.play(sound[3])
                if event.key == keybinds["s4"]:
                    pygame.mixer.Sound.play(sound[4])
                if event.key == keybinds["pause"]:
                    if paused:
                        pygame.mixer.music.unpause()
                    if not paused:
                        pygame.mixer.music.pause()
        
        pygame.display.update()
        clock.tick(240) #sets framerate

if __name__=="__main__":
    main()
    game()
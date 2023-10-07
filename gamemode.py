import time

class Game:
    def __init__(self):
        self.set_sounds
        
    def set_sounds(self, sound_assets):
        self.sounds = {}
        for sound_name in sound_assets:
            self.sounds[sound_name] = pygame.mixer.Sound(sound_assets[sound_name]["source"])
            self.sounds[sound_name].set_volume(sound_assets[sound_name]["volume"])

    def set_keybinds(self, keybinds):
        self.keybinds = keybinds

class Clapper(Game):
    def __init__(self):
        Game.__init__(self)

        #load clap sound
        self.set_sounds({"sound_1": {"source":"placeholder_sounds/Kim_clap-1.ogg", "volume": 0.1,}})

        #load keybindings
        keybinds = {"clap": pygame.K_SPACE,}
        self.set_keybinds(keybinds)

        self.t0= time.time_ns()

        self.clap_buffer = []

        self.clapout = False
        
        self.music("placeholder_sounds/simple-loop.ogg")

        self.note_timings = [self.beat_to_seconds(1), 
                             self.beat_to_seconds(2),
                             self.beat_to_seconds(3),
                             self.beat_to_seconds(4),
                             self.beat_to_seconds(5)]

        print(self.note_timings)

        self.a = True

        self.next_note()

        self.response = True



    def beat_to_seconds(self, value):
        return int(value*60*10**9/self.tempo)

    def eventhandler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.keybinds["clap"]:
                pygame.mixer.Sound.play(self.sounds["sound_1"])
                self.clap_buffer.append(time.time_ns() - self.t0)
    
    def call_clap(self):
        pygame.mixer.Sound.play(self.sounds["sound_1"])
        print("c")
    
    def next_note(self):
        try:
            self.next_note_time = self.note_timings.pop(0)
            self.clapout = False
        except:
            pass

    
    def music(self, file_src):
        pygame.mixer.music.load(file_src) #sets music
        pygame.mixer.music.play(-1) #"-1" plays music indefinitely
        pygame.mixer.music.set_volume(0.1)  # Adjust the volume level (0.0 - 1.0)

        self.tempo = 80 #bpm
        
    def game_logic(self):
        
        #play claps
        if time.time_ns() - self.t0 > self.next_note_time and self.clapout == False:
            self.call_clap()
            self.clapout = True
            self.next_note()
        
        if time.time_ns() - self.t0 > 5*10**9 and self.a == True:
            print(self.clap_buffer)
            self.a = False


def main():

    pygame.mixer.pre_init() #dark magic to ward away input lag, must be cast before pygame.init()
    pygame.init()
    
    #display settings
    display_width = 800
    display_height = 600
    pygame.display.set_mode((display_width,display_height))
    
    """
    sounds = {"sound_1": {"source":"placeholder_sounds/beep1.ogg", "volume": 1,},
              "sound_2": {"source":"placeholder_sounds/beep2.ogg", "volume": 1,},
              "sound_3": {"source":"placeholder_sounds/beep3.ogg", "volume": 1,},
              "sound_4": {"source":"placeholder_sounds/beep4.ogg", "volume": 1,},  
              "sound_5": {"source":"placeholder_sounds/beep5.ogg", "volume": 1,}}

    keybinds = {"s0": pygame.K_a,
                "s1": pygame.K_s,
                "s2": pygame.K_d,
                "s3": pygame.K_f,
                "s4": pygame.K_g,
                "pause": pygame.K_p,
                }
    

    class Piano(Game):
        def __init__(self):
            Game.__init__(self)
        
        def eventhandler(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == self.keybinds["s0"]:
                    pygame.mixer.Sound.play(self.sounds["sound_1"])
                if event.key == self.keybinds["s1"]:
                    pygame.mixer.Sound.play(self.sounds["sound_2"])
                if event.key == self.keybinds["s2"]:
                    pygame.mixer.Sound.play(self.sounds["sound_3"])
                if event.key == self.keybinds["s3"]:
                    pygame.mixer.Sound.play(self.sounds["sound_4"])
                if event.key == self.keybinds["s4"]:
                    pygame.mixer.Sound.play(self.sounds["sound_5"])
                    """
            
    current_game = Clapper()
    
    """    pygame.mixer.music.load("placeholder_sounds/simple-loop.ogg") #sets music
    pygame.mixer.music.play(-1) #"-1" plays music indefinitely
    pygame.mixer.music.set_volume(0.1)  # Adjust the volume level (0.0 - 1.0)
    """
    
    while True:
        for event in pygame.event.get():
            current_game.eventhandler(event)
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current_game.game_logic()

        #pygame.display.update()



if __name__ == "__main__":
    import pygame
    main()
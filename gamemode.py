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

        self.t0= time.time_ns() # sets initial time
        self.clap_buffer = [] #ideally 

        self.clapout = False #makes it clap once
        
        self.music("placeholder_sounds/simple-loop.ogg") #links music file

        #list of notes that need playing, ideally this is done through a level file of some sort or something
        self.note_timings = [self.beat_to_seconds(1), 
                             self.beat_to_seconds(2),
                             self.beat_to_seconds(3),
                             self.beat_to_seconds(4),
                             self.beat_to_seconds(5)]

        print(self.note_timings)

        self.next_note()

        self.response = True

    #converts beat timings to seconds
    def beat_to_seconds(self, value):
        return int(value*60*10**9/self.tempo)

    #checks events, just keypress for now
    def eventhandler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.keybinds["clap"]:
                pygame.mixer.Sound.play(self.sounds["sound_1"])
                self.clap_buffer.append(time.time_ns() - self.t0)
    
    #code to run when clap occurs
    def call_clap(self):
        pygame.mixer.Sound.play(self.sounds["sound_1"])
    
    #sets next note timing
    def next_note(self):
        try:
            self.next_note_time = self.note_timings.pop(0)
            self.clapout = False
        except:
            pass

    #sets music and tempo
    def music(self, file_src):
        pygame.mixer.music.load(file_src) #sets music
        pygame.mixer.music.play(-1) #"-1" plays music indefinitely
        pygame.mixer.music.set_volume(0.1)  # Adjust the volume level (0.0 - 1.0)

        self.tempo = 80 #bpm
        
    def game_logic(self):
        
        #checks if there's a note queued up and plays it
        if time.time_ns() - self.t0 > self.next_note_time and self.clapout == False: 
            self.call_clap()
            self.clapout = True
            self.next_note()


def main():

    pygame.mixer.pre_init() #dark magic to ward away input lag, must be cast before pygame.init()
    pygame.init()
    
    #display settings
    display_width = 800
    display_height = 600
    pygame.display.set_mode((display_width,display_height))
            
    current_game = Clapper()

    #game loop
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
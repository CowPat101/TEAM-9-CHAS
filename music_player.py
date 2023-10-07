import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sound_sources = [
            "placeholder_sounds/beep1.ogg",
            "placeholder_sounds/beep2.ogg",
            "placeholder_sounds/beep3.ogg",
            "placeholder_sounds/beep4.ogg",
            "placeholder_sounds/beep5.ogg"
        ]
        self.sounds = self.load_sounds(self.sound_sources)
        self.music_volume = 0.1

        # Initialize Pygame mixer and load music
        pygame.mixer.music.load("placeholder_sounds/simple-loop.ogg")
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def load_sounds(self, source_list, volume=1.0):
        sounds = []
        for s in source_list:
            sound = pygame.mixer.Sound(s)
            sound.set_volume(volume)
            sounds.append(sound)
        return sounds

    def play_action(self, index):
        if 0 <= index < len(self.sounds):
            pygame.mixer.Sound.play(self.sounds[index])

if __name__ == "__main__":
    pygame.init()
    sound_manager = SoundManager()

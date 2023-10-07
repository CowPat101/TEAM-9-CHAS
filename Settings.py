class Settings():
    Subtitles = False
    Font = "arial"
    Font_size = "medium"
    Font_colour = "black"
    Audio = 0.5
    SFX = 1.0
    Level = 1
    #declare all the variables that will be used in the settings menu
    def __init__(self, gSubtitles, gFont, gFont_size, gFont_colour, gAudio, gSFX, gLevel):
        #assign the variables to the values passed in the constructor
        self.Subtitles = gSubtitles
        self.Font = gFont
        self.Font_size = gFont_size
        self.Font_colour = gFont_colour
        self.Audio = gAudio
        self.SFX = gSFX
        self.Level = gLevel
    #getters for all the variables
    getSubtitles = lambda self: self.Subtitles
    getFont = lambda self: self.Font
    getFontSize = lambda self: self.Font_size
    getFontColour = lambda self: self.Font_colour
    getAudio = lambda self: self.Audio
    getSFX = lambda self: self.SFX
    getLevel = lambda self: self.Level
    #setters for all the variables
    setSubtitles = lambda self, gSubtitles: setattr(self, "Subtitles", gSubtitles)
    setFont = lambda self, gFont: setattr(self, "Font", gFont)
    setFontSize = lambda self, gFont_size: setattr(self, "Font_size", gFont_size)
    setFontColour = lambda self, gFont_colour: setattr(self, "Font_colour", gFont_colour)
    setAudio = lambda self, gAudio: setattr(self, "Audio", gAudio)
    setSFX = lambda self, gSFX: setattr(self, "SFX", gSFX)
    setLevel = lambda self, gLevel: setattr(self, "Level", gLevel)

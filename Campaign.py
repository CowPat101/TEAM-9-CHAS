class Campaign:
    level_info = []
    rounds = -1
    current_round = 0
    def __init__(self, level):
        try:
            open_level = open(f"levels/level{level}.txt", "r")
            self.level_info = open_level.readlines()
            self.rounds = len(self.level_info)
        except:
            print("Error: Level not found")
            exit()
    
    def get_round(self, round_num):
        return self.level_info[round_num]
    def get_rounds(self):
        return self.rounds


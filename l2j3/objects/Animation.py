class Animation:
    
    # 60 ticks = 1 seconde
    def __init__(self, duration = 60):
        self.currentTick = 0
        self.animation = None
        self.duration = duration

    def Increment(self):
        if self.currentTick < self.duration:
            self.currentTick += 1
            self.animation()
            return True
        else:
            return False
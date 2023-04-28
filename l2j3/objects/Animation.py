class Animation:
    currentTick = 0

    # 60 ticks = 1 seconde
    def __init__(self, action, duration = 60):
        self.animation = action
        self.duration = duration

    def Increment(self):
        if self.currentTick < self.duration:
            self.currentTick += 1
            self.animation()
            return True
        else:
            return False
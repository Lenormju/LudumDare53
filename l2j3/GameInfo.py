from dataclasses import dataclass


@dataclass
class _GameInfo:
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
    CURRENT_TICK_NUMBER = 0
    TARGET_FPS = 60


GAME_INFO = _GameInfo()

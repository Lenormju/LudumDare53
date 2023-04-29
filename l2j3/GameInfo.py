from dataclasses import dataclass
from enum import Enum


class GameScreen(Enum):
    TITLE = "title"
    GAME_GOOD = "good"


@dataclass
class _GameInfo:
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
    CURRENT_TICK_NUMBER = 0
    TARGET_FPS = 60
    CURRENT_GAME_SCREEN = GameScreen.TITLE
    NEXT_GAME_SCREEN = GameScreen.TITLE


GAME_INFO = _GameInfo()

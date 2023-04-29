from dataclasses import dataclass
from enum import Enum


class GameScreen(Enum):
    TITLE = "title"
    GAME_GOOD = "good"
    GAME_GOOD_ENDING_GOOD = "good / good ending"
    QUIT = "quit"


@dataclass
class _GameInfo:
    SCREEN_WIDTH, SCREEN_HEIGHT = 580, 600
    CURRENT_TICK_NUMBER = 0
    TARGET_FPS = 60
    SCORE = 0
    CURRENT_GAME_SCREEN = GameScreen.TITLE
    NEXT_GAME_SCREEN = GameScreen.TITLE


GAME_INFO = _GameInfo()

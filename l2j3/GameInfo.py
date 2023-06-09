from dataclasses import dataclass
from enum import Enum


class GameScreen(Enum):
    TITLE = "title"
    GOOD_LEVEL_ONE = "good 1"
    GOOD_LEVEL_ONE_INTERLUDE = "good 1 inter"
    GOOD_LEVEL_TWO = "good 2"
    GOOD_LEVEL_TWO_INTERLUDE = "good 2 inter"
    GOOD_LEVEL_THREE = "good 3"
    GOOD_ENDING = "good ending"
    BAD_INTRO = "bad intro"
    BAD_LEVEL_ONE = "bad 1"
    BAD_LEVEL_ONE_INTERLUDE = "bad 1 inter"
    BAD_LEVEL_TWO = "bad 2"
    BAD_LEVEL_TWO_INTERLUDE = "bad 2 inter"
    BAD_LEVEL_THREE = "bad 3"
    BAD_ENDING = "bad ending"
    NEUTRAL_ENDING = "neutral ending"
    QUIT = "quit"


@dataclass
class _GameInfo:
    SCREEN_WIDTH, SCREEN_HEIGHT = 580, 600
    CURRENT_TICK_NUMBER = 0
    TARGET_FPS = 60
    SCORE = 0
    CUMULATIF_SCORE = 0
    CURRENT_GAME_SCREEN = GameScreen.TITLE
    NEXT_GAME_SCREEN = GameScreen.TITLE


GAME_INFO = _GameInfo()

import enum

class Direction(enum.Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

import random
random.choice([Direction.LEFT, Direction.RIGHT])
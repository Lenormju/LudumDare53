from dataclasses import dataclass

@dataclass
class MouseButtons:
    left_is_pressed: bool
    middle_is_pressed: bool
    right_is_pressed: bool

MY_MOUSE_BUTTON_LEFT = 1
MY_MOUSE_BUTTON_RIGHT = 3

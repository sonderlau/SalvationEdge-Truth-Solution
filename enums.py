from enum import Enum


class SHAPES(Enum):
    SQUARE = 1
    CIRCLE = 2
    TRIANGLE = 3


class LOCATION(Enum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class INTERACTION_TYPE(Enum):
    REGISTER = 1
    EXCHANGE = 2

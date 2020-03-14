from enum import Enum


class PlayerConfiguration:
    def __init__(self):
        pass


class GameConfiguration:
    def __init__(self):
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FIELD_SIZE = 10
        while self.SCREEN_WIDTH % self.FIELD_SIZE != 0 or self.SCREEN_HEIGHT % self.FIELD_SIZE:
            self.FIELD_SIZE += 1  # just to make sure that the surface is dividable by the field
        self.PADDING = 1
        self.SNAKE_SIZE = self.FIELD_SIZE - 2 * self.PADDING
        self.APPLE_SIZE = self.SNAKE_SIZE
        self.NUM_APPLES = 3
        self.FPS = 60
        self.DELAY_FACTOR = 2  # < basically the speed


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class PyGameEnv:
    def __init__(self):
        self.surface = None
        self.clock = None


player_config = PlayerConfiguration()
GAME_CFG = GameConfiguration()
GAME_ENV = PyGameEnv()

from enum import Enum

import pygame


class PlayerControls:
    def __init__(self):
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN

    def set_left(self, key):
        self.left = key

    def set_right(self, key):
        self.right = key

    def set_up(self, key):
        self.up = key

    def set_down(self, key):
        self.down = key


class PlayerConfiguration:
    def __init__(self):
        self.NUM_PLAYERS = 1
        self.CONTROLS = [PlayerControls()]
        self.SNAKE_START_LEN = 5


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
        self.main_menu = None


PLAYER_CFG = PlayerConfiguration()
GAME_CFG = GameConfiguration()
GAME_ENV = PyGameEnv()

import pygame

from collision import collides
from config import Direction
from config import GAME_CFG
from config import GAME_ENV


class Snake:
    class Segment:
        def __init__(self, x, y, color="white"):
            """
            :param x: x-coord of the upper left corner of the surface's segment
            :param y: y-coord of the upper left corner of the surface's segment
            """
            self.x = x
            self.y = y
            self.color = color

        def draw(self):
            pygame.draw.rect(GAME_ENV.surface, pygame.color.Color(self.color),
                             (self.x + GAME_CFG.PADDING,
                              self.y + GAME_CFG.PADDING,
                              GAME_CFG.SNAKE_SIZE, GAME_CFG.SNAKE_SIZE), 0)
            pass

    def __init__(self, x, y):
        """
        :param x: x-coord of the upper left corner of the surface's segment
        :param y: y-coord of the upper left corner of the surface's segment
        """
        self.direction = Direction.UP
        self.stack = []
        self.stack.append(self.Segment(x, y, "yellow"))  # add head

    def update(self):
        """
        Updates the position of all snake parts \ref{stack}
        """
        for seg_idx in reversed(range(1, len(self.stack))):
            self.stack[seg_idx].x = self.stack[seg_idx - 1].x
            self.stack[seg_idx].y = self.stack[seg_idx - 1].y
        if self.direction == Direction.UP:
            self.stack[0].y -= GAME_CFG.FIELD_SIZE
        elif self.direction == Direction.DOWN:
            self.stack[0].y += GAME_CFG.FIELD_SIZE
        elif self.direction == Direction.LEFT:
            self.stack[0].x -= GAME_CFG.FIELD_SIZE
        elif self.direction == Direction.RIGHT:
            self.stack[0].x += GAME_CFG.FIELD_SIZE
        self.__check_surface_border()

    def __check_surface_border(self):
        if self.stack[0].x >= GAME_CFG.SCREEN_WIDTH:
            self.stack[0].x = 0
        elif self.stack[0].x < 0:
            self.stack[0].x = GAME_CFG.SCREEN_WIDTH - GAME_CFG.FIELD_SIZE
        if self.stack[0].y >= GAME_CFG.SCREEN_HEIGHT:
            self.stack[0].y = 0
        elif self.stack[0].y < 0:
            self.stack[0].y = GAME_CFG.SCREEN_HEIGHT - GAME_CFG.FIELD_SIZE

    def get_head(self):
        return self.stack[0]

    def grow(self):
        last_element_idx = len(self.stack) - 1
        x_pos = self.stack[last_element_idx].x
        y_pos = self.stack[last_element_idx].y
        if self.direction == Direction.UP:
            y_pos += GAME_CFG.FIELD_SIZE
        elif self.direction == Direction.DOWN:
            y_pos -= GAME_CFG.FIELD_SIZE
        elif self.direction == Direction.LEFT:
            x_pos += GAME_CFG.FIELD_SIZE
        elif self.direction == Direction.RIGHT:
            x_pos -= GAME_CFG.FIELD_SIZE

        new_element = self.Segment(x_pos, y_pos)
        self.stack.append(new_element)

    def set_direction(self, direction):
        if (self.direction == Direction.UP and direction == Direction.DOWN) \
                or (self.direction == Direction.DOWN and direction == Direction.UP) \
                or (self.direction == Direction.LEFT and direction == Direction.RIGHT) \
                or (self.direction == Direction.RIGHT and direction == Direction.LEFT):
            return
        self.direction = direction

    def collides_with_body(self):
        for seg_idx in range(1, len(self.stack)):
            if collides(self.stack[0], self.stack[seg_idx]):
                return True
        return False

    def collides(self, obj):
        #  just to not place an apple under a snake's body
        for seg in self.stack:
            if collides(seg, obj):
                return True
        return False

    def draw(self):
        for part in self.stack:
            part.draw()

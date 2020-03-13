# coding=utf-8
import random
from enum import Enum

import pygame
import sys

random.seed()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FIELD_SIZE = 10
while SCREEN_WIDTH % FIELD_SIZE != 0 or SCREEN_HEIGHT % FIELD_SIZE:
    FIELD_SIZE += 1  # just to make sure that the surface is dividable by the field
PADDING = 1
SNAKE_SIZE = FIELD_SIZE - 2 * PADDING
APPLE_SIZE = SNAKE_SIZE
NUM_APPLES = 3
FPS = 60

DELAY_FACTOR = 2  # < basically the speed
PLAYERS = 1
CONTROLS = None

surface = None
clock = None


def collides(left_obj, right_obj):
    if left_obj.x < right_obj.x + FIELD_SIZE and left_obj.x + FIELD_SIZE > right_obj.x \
            and left_obj.y < right_obj.y + FIELD_SIZE and left_obj.y + FIELD_SIZE > right_obj.y:
        return True
    return False


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


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


class Apple:
    def __init__(self, x, y):
        """
        :param x: x-coord of the upper left corner of the surface's rect
        :param y: y-coord of the upper left corner of the surface's rect
        """
        self.x = x
        self.y = y
        self.color = pygame.color.Color("red")

    def draw(self):
        global surface
        pygame.draw.rect(surface, self.color, (self.x + PADDING, self.y + PADDING, APPLE_SIZE, APPLE_SIZE), 0)

    @staticmethod
    def get_new():
        new_x = random.randint(0, SCREEN_WIDTH)
        new_y = random.randint(0, SCREEN_HEIGHT)
        return Apple(int(new_x / FIELD_SIZE) * FIELD_SIZE,
                     int(new_y / FIELD_SIZE) * FIELD_SIZE)


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
            global surface
            pygame.draw.rect(surface, pygame.color.Color(self.color),
                             (self.x + PADDING, self.y + PADDING, SNAKE_SIZE, SNAKE_SIZE), 0)
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
            self.stack[0].y -= FIELD_SIZE
        elif self.direction == Direction.DOWN:
            self.stack[0].y += FIELD_SIZE
        elif self.direction == Direction.LEFT:
            self.stack[0].x -= FIELD_SIZE
        elif self.direction == Direction.RIGHT:
            self.stack[0].x += FIELD_SIZE
        self.__check_surface_border()

    def __check_surface_border(self):
        if self.stack[0].x >= SCREEN_WIDTH:
            self.stack[0].x = 0
        elif self.stack[0].x < 0:
            self.stack[0].x = SCREEN_WIDTH - FIELD_SIZE
        if self.stack[0].y >= SCREEN_HEIGHT:
            self.stack[0].y = 0
        elif self.stack[0].y < 0:
            self.stack[0].y = SCREEN_HEIGHT - FIELD_SIZE

    def get_head(self):
        return self.stack[0]

    def grow(self):
        last_element_idx = len(self.stack) - 1
        x_pos = self.stack[last_element_idx].x
        y_pos = self.stack[last_element_idx].y
        if self.direction == Direction.UP:
            y_pos += FIELD_SIZE
        elif self.direction == Direction.DOWN:
            y_pos -= FIELD_SIZE
        elif self.direction == Direction.LEFT:
            x_pos += FIELD_SIZE
        elif self.direction == Direction.RIGHT:
            x_pos -= FIELD_SIZE

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
        for seg in self.stack:
            if collides(seg, obj):
                return True
        return False

    def draw(self):
        for part in self.stack:
            part.draw()


class Game:
    def __init__(self, menu=None):
        self.start_time = pygame.time.get_ticks()
        self.score_font = pygame.font.Font(None, 38)
        self.score_numb_font = pygame.font.Font(None, 28)
        self.game_over_font = pygame.font.Font(None, 46)
        self.play_again_font = self.score_numb_font
        self.score_msg = self.score_font.render("Score:", 1, pygame.Color("green"))
        self.score_msg_size = self.score_font.size("Score")
        self.background_color = pygame.Color(74, 74, 74)
        self.speed_counter = 0
        self.main_menu = menu
        self.__init_game_params()

    def __init_game_params(self):
        self.score = 0
        self.apples = []
        self.snake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        for snake_starting_segments in range(5):
            self.snake.grow()
        while len(self.apples) < NUM_APPLES:
            self.__insert_new_apple()
        self.is_game_over = False

    def __insert_new_apple(self):
        new_apple = Apple.get_new()
        for a in self.apples:
            if collides(a, new_apple):
                return False
        if not self.snake.collides(new_apple):
            self.apples.append(new_apple)
            return True
        return False

    def __draw_score(self, score):
        global surface
        score_numb = self.score_numb_font.render(str(score), 1, pygame.Color("red"))
        surface.blit(self.score_msg, (SCREEN_WIDTH - self.score_msg_size[0] - 60, 10))
        surface.blit(score_numb, (SCREEN_WIDTH - 45, 14))

    def __draw_time(self, game_time):
        global surface
        game_time_str = self.score_font.render("Time:", 1, pygame.Color("green"))
        game_time_numb = self.score_numb_font.render(str(game_time / 1000), 1, pygame.Color("red"))
        surface.blit(game_time_str, (30, 10))
        surface.blit(game_time_numb, (105, 14))

    def __process_event_loop(self):
        result = True
        events = pygame.event.get()
        new_direction = self.snake.direction
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    new_direction = Direction.UP
                elif e.key == pygame.K_DOWN:
                    new_direction = Direction.DOWN
                elif e.key == pygame.K_LEFT:
                    new_direction = Direction.LEFT
                elif e.key == pygame.K_RIGHT:
                    new_direction = Direction.RIGHT
                elif e.key == pygame.K_y and self.is_game_over:
                    self.is_game_over = False
                    result = True
                elif e.key == pygame.K_n and self.is_game_over:
                    self.is_game_over = False
                    result = False
                elif e.key == pygame.K_ESCAPE and self.main_menu and self.main_menu.is_disabled():
                    self.main_menu.enable()
            if e.type == pygame.QUIT:
                sys.exit()
        self.snake.set_direction(new_direction)
        if self.main_menu:
            self.main_menu.mainloop(events)
        return result

    def __draw_game(self):
        global surface
        surface.fill(self.background_color)
        for a in self.apples:
            a.draw()
        self.snake.draw()
        self.__draw_score(self.score)
        self.__draw_time(pygame.time.get_ticks() - self.start_time)
        pygame.display.flip()
        pygame.display.update()

    def __update_objects(self):
        if self.snake.collides_with_body():
            self.is_game_over = True
            return
        for apple in self.apples:
            if collides(apple, self.snake.get_head()):
                self.snake.grow()
                self.score += 5
                self.apples.remove(apple)
                break
        self.snake.update()
        if len(self.apples) < NUM_APPLES:
            while not self.__insert_new_apple():
                pass

    def __new_game_requested(self):
        global surface
        global clock
        txt_game_over = "Game Over"
        rendered_game_over = self.game_over_font.render(txt_game_over, 1, pygame.Color("white"))
        game_over_size = self.game_over_font.size(txt_game_over)
        surface.blit(rendered_game_over,
                     (SCREEN_WIDTH / 2 - game_over_size[0] / 2,
                      SCREEN_HEIGHT / 2 - game_over_size[1]))
        txt_play_again = "Play again? (y/n)"
        message_play_again = self.play_again_font.render(txt_play_again, 1, pygame.Color("green"))
        play_again_size = self.play_again_font.size(txt_play_again)
        surface.blit(message_play_again,
                     (SCREEN_WIDTH / 2 - play_again_size[0] / 2,
                      SCREEN_HEIGHT / 2))
        pygame.display.flip()
        pygame.display.update()
        while self.is_game_over:
            clock.tick(FPS)
            if not self.__process_event_loop():
                return False
        self.__init_game_params()
        return True

    def game_loop(self):
        global clock
        self.speed_counter = 0
        while True:
            clock.tick(FPS)
            self.speed_counter = self.speed_counter + 1
            self.__process_event_loop()
            if self.speed_counter >= DELAY_FACTOR:
                self.speed_counter = 0
                self.__update_objects()
            if self.is_game_over:
                if self.__new_game_requested():
                    continue
                break
            self.__draw_game()


def init(c, s):
    global clock
    global surface
    surface = s
    clock = c


def set_params(speed, players, controls):
    global DELAY_FACTOR
    global PLAYERS
    global CONTROLS
    assert 0 < speed < 10
    assert 0 < players < 5
    DELAY_FACTOR = 10 - speed
    PLAYERS = players
    CONTROLS = controls


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Snake v1.0")
    pygame.font.init()

    CONTROLS = [PlayerControls()]

    init(pygame.time.Clock(),
         pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE))

    game_engine = Game()
    game_engine.game_loop()  # doesn't return until game is over or close is requested

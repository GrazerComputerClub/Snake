# coding=utf-8
import random

import pygame
import sys

from collision import collides
from config import Direction
from config import GAME_CFG
from config import GAME_ENV
from snake import Snake

random.seed()

PLAYERS = 1
CONTROLS = None


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
        pygame.draw.rect(GAME_ENV.surface, self.color, (self.x + GAME_CFG.PADDING,
                                                        self.y + GAME_CFG.PADDING,
                                                        GAME_CFG.APPLE_SIZE, GAME_CFG.APPLE_SIZE), 0)

    @staticmethod
    def get_new():
        new_x = random.randint(0, GAME_CFG.SCREEN_WIDTH)
        new_y = random.randint(0, GAME_CFG.SCREEN_HEIGHT)
        return Apple(int(new_x / GAME_CFG.FIELD_SIZE) * GAME_CFG.FIELD_SIZE,
                     int(new_y / GAME_CFG.FIELD_SIZE) * GAME_CFG.FIELD_SIZE)


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
        self.snake = Snake(GAME_CFG.SCREEN_WIDTH / 2, GAME_CFG.SCREEN_HEIGHT / 2)
        for snake_starting_segments in range(5):
            self.snake.grow()
        while len(self.apples) < GAME_CFG.NUM_APPLES:
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
        score_numb = self.score_numb_font.render(str(score), 1, pygame.Color("red"))
        GAME_ENV.surface.blit(self.score_msg, (GAME_CFG.SCREEN_WIDTH - self.score_msg_size[0] - 60, 10))
        GAME_ENV.surface.blit(score_numb, (GAME_CFG.SCREEN_WIDTH - 45, 14))

    def __draw_time(self, game_time):
        game_time_str = self.score_font.render("Time:", 1, pygame.Color("green"))
        game_time_numb = self.score_numb_font.render(str(game_time / 1000), 1, pygame.Color("red"))
        GAME_ENV.surface.blit(game_time_str, (30, 10))
        GAME_ENV.surface.blit(game_time_numb, (105, 14))

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
        GAME_ENV.surface.fill(self.background_color)
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
        if len(self.apples) < GAME_CFG.NUM_APPLES:
            while not self.__insert_new_apple():
                pass

    def __new_game_requested(self):
        txt_game_over = "Game Over"
        rendered_game_over = self.game_over_font.render(txt_game_over, 1, pygame.Color("white"))
        game_over_size = self.game_over_font.size(txt_game_over)
        GAME_ENV.surface.blit(rendered_game_over,
                              (GAME_CFG.SCREEN_WIDTH / 2 - game_over_size[0] / 2,
                               GAME_CFG.SCREEN_HEIGHT / 2 - game_over_size[1]))
        txt_play_again = "Play again? (y/n)"
        message_play_again = self.play_again_font.render(txt_play_again, 1, pygame.Color("green"))
        play_again_size = self.play_again_font.size(txt_play_again)
        GAME_ENV.surface.blit(message_play_again,
                              (GAME_CFG.SCREEN_WIDTH / 2 - play_again_size[0] / 2,
                               GAME_CFG.SCREEN_HEIGHT / 2))
        pygame.display.flip()
        pygame.display.update()
        while self.is_game_over:
            GAME_ENV.clock.tick(GAME_CFG.FPS)
            if not self.__process_event_loop():
                return False
        self.__init_game_params()
        return True

    def game_loop(self):
        self.speed_counter = 0
        while True:
            GAME_ENV.clock.tick(GAME_CFG.FPS)
            self.speed_counter = self.speed_counter + 1
            self.__process_event_loop()
            if self.speed_counter >= GAME_CFG.DELAY_FACTOR:
                self.speed_counter = 0
                self.__update_objects()
            if self.is_game_over:
                if self.__new_game_requested():
                    continue
                break
            self.__draw_game()


def set_params(speed, players, controls):
    assert 0 < speed < 10
    assert 0 < players < 5
    GAME_CFG.DELAY_FACTOR = 10 - speed
    GAME_CFG.PLAYERS = players
    GAME_CFG.CONTROLS = controls


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Snake v1.0")
    pygame.font.init()

    CONTROLS = [PlayerControls()]

    GAME_ENV.clock = pygame.time.Clock()
    GAME_ENV.surface = pygame.display.set_mode((GAME_CFG.SCREEN_WIDTH, GAME_CFG.SCREEN_HEIGHT), pygame.HWSURFACE)

    game_engine = Game()
    game_engine.game_loop()  # doesn't return until game is over or close is requested

# coding=utf-8
import random

import pygame
import sys

from collision import collides
from config import Direction
from config import GAME_CFG
from config import GAME_ENV
from config import PLAYER_CFG
from snake import Snake

random.seed()


def get_random_coord(max_coord):
    return int(random.randint(0, max_coord) / GAME_CFG.FIELD_SIZE) * GAME_CFG.FIELD_SIZE


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
        return Apple(get_random_coord(GAME_CFG.SCREEN_WIDTH), get_random_coord(GAME_CFG.SCREEN_HEIGHT))


class Game:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        self.score_font = pygame.font.Font(None, 38)
        self.score_numb_font = pygame.font.Font(None, 28)
        self.game_over_font = pygame.font.Font(None, 46)
        self.play_again_font = self.score_numb_font
        self.score_msg = self.score_font.render("Score:", 1, pygame.Color("green"))
        self.score_msg_size = self.score_font.size("Score")
        self.background_color = pygame.Color(74, 74, 74)
        self.speed_counter = 0
        self.__init_game_params()

    def __init_game_params(self):
        self.score = 0
        self.apples = []
        self.snakes = []
        self.__create_snakes()
        while len(self.apples) < GAME_CFG.NUM_APPLES:
            self.__insert_new_apple()
        self.is_game_over = False

    def __create_snakes(self):
        snake_rect = []
        snake_radius = PLAYER_CFG.SNAKE_START_LEN * GAME_CFG.FIELD_SIZE
        for s in range(0, PLAYER_CFG.NUM_PLAYERS):
            tries_before_reduce_distance = 10
            while True:
                tries_before_reduce_distance = tries_before_reduce_distance - 1
                if tries_before_reduce_distance == 0:
                    tries_before_reduce_distance = 10
                    snake_radius = snake_radius - GAME_CFG.FIELD_SIZE
                    if snake_radius <= 0:
                        snake_radius = 1  # minimum distance to avoid that snake's head will be placed on the same field
                snake_head_pos = (get_random_coord(GAME_CFG.SCREEN_WIDTH), get_random_coord(GAME_CFG.SCREEN_HEIGHT))
                snake_start_area = pygame.Rect(snake_head_pos[0] - snake_radius,
                                               snake_head_pos[1] - snake_radius,
                                               snake_head_pos[0] + snake_radius,
                                               snake_head_pos[1] + snake_radius)
                snake_collides = False
                for placed_snake_pos in snake_rect:
                    if snake_start_area.colliderect(placed_snake_pos):
                        snake_collides = True
                        break
                if not snake_collides:
                    snake_rect.append(snake_start_area)
                    self.snakes.append(Snake(snake_head_pos[0], snake_head_pos[1], PLAYER_CFG.SNAKE_START_LEN))
                    break

    def __insert_new_apple(self):
        new_apple = Apple.get_new()
        for a in self.apples:
            if collides(a, new_apple):
                return False
        no_snake_field = True
        for snake in self.snakes:
            if snake.collides(new_apple):
                no_snake_field = False
                break
        if no_snake_field:
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
        new_directions = []
        for s in self.snakes:
            new_directions.append(s.direction)
        for e in events:
            if e.type == pygame.KEYDOWN:
                for player_idx in range(PLAYER_CFG.NUM_PLAYERS):
                    if e.key == PLAYER_CFG.CONTROLS[player_idx].up:
                        new_directions[player_idx] = Direction.UP
                    elif e.key == PLAYER_CFG.CONTROLS[player_idx].down:
                        new_directions[player_idx] = Direction.DOWN
                    elif e.key == PLAYER_CFG.CONTROLS[player_idx].left:
                        new_directions[player_idx] = Direction.LEFT
                    elif e.key == PLAYER_CFG.CONTROLS[player_idx].right:
                        new_directions[player_idx] = Direction.RIGHT
                if e.key == pygame.K_y and self.is_game_over:
                    self.is_game_over = False
                    result = True
                elif e.key == pygame.K_n and self.is_game_over:
                    self.is_game_over = False
                    result = False
                elif e.key == pygame.K_ESCAPE and GAME_ENV.main_menu and GAME_ENV.main_menu.is_disabled():
                    GAME_ENV.main_menu.enable()
            if e.type == pygame.QUIT:
                sys.exit()
        for player_idx in range(PLAYER_CFG.NUM_PLAYERS):
            self.snakes[player_idx].set_direction(new_directions[player_idx])
        if GAME_ENV.main_menu:
            GAME_ENV.main_menu.mainloop(events)
        return result

    def __draw_game(self):
        GAME_ENV.surface.fill(self.background_color)
        for a in self.apples:
            a.draw()
        for s in self.snakes:
            s.draw()
        self.__draw_score(self.score)
        self.__draw_time(pygame.time.get_ticks() - self.start_time)
        pygame.display.flip()
        pygame.display.update()

    def __update_objects(self):
        dead_snakes = 0
        for s in self.snakes:
            s.update_alive()
            if not s.is_alive():
                dead_snakes = dead_snakes + 1
        if dead_snakes == PLAYER_CFG.NUM_PLAYERS:
            self.is_game_over = True
            return
        for apple in self.apples:
            for s in self.snakes:
                if collides(apple, s.get_head()):
                    s.grow()
                    self.score += 5
                    self.apples.remove(apple)
                    break
        for s in self.snakes:
            if s.is_alive():
                s.update()
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


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Snake v1.0")
    pygame.font.init()

    GAME_ENV.clock = pygame.time.Clock()
    GAME_ENV.surface = pygame.display.set_mode((GAME_CFG.SCREEN_WIDTH, GAME_CFG.SCREEN_HEIGHT), pygame.HWSURFACE)

    game_engine = Game()
    game_engine.game_loop()  # doesn't return until game is over or close is requested

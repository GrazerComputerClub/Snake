# coding=utf-8
import os

import pygame
import pygameMenu

import engine

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['GC2\'s Snake',
         'Author: @woergi',
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: office@gc2.at']
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BACKGROUND = (74, 74, 74)
FPS = 60.0
MENU_BACKGROUND_COLOR = (37, 133, 47)
WINDOW_SIZE = (1024, 768)
PLAYERS = 1
SPEED = 6

clock = None
main_menu = None
surface = None


def player_changed(value, num_players):
    global PLAYERS
    PLAYERS = num_players


def speed_changed(value, s):
    global SPEED
    SPEED = s


def play_function():
    """
    Main game function.
    :return: None
    """
    global main_menu
    global clock
    global PLAYERS
    global SPEED
    print('Game starts for {0} players'.format(PLAYERS))
    # Reset main menu and disable
    # You also can set another menu, like a 'pause menu', or just use the same
    # main_menu as the menu that will check all your input.
    main_menu.disable()
    main_menu.reset(1)
    engine.set_params(speed=SPEED, players=PLAYERS)
    game_engine = engine.Game(menu=main_menu)
    game_engine.game_loop()  # doesn't return until game is over or close is requested
    main_menu.enable()


def main_background():
    """
    Function used by menus, draw on background while menu is active.
    :return: None
    """
    global surface
    surface.fill(COLOR_BACKGROUND)


def create_menu(menu_title):
    return pygameMenu.TextMenu(surface,
                               bgfun=main_background,
                               color_selected=COLOR_WHITE,
                               font=pygameMenu.font.FONT_BEBAS,
                               font_color=COLOR_BLACK,
                               font_size_title=30,
                               font_title=pygameMenu.font.FONT_8BIT,
                               menu_color=MENU_BACKGROUND_COLOR,
                               menu_color_title=COLOR_WHITE,
                               menu_height=int(WINDOW_SIZE[1] * 0.6),
                               menu_width=int(WINDOW_SIZE[0] * 0.6),
                               onclose=pygameMenu.events.DISABLE_CLOSE,
                               option_shadow=False,
                               text_color=COLOR_BLACK,
                               text_fontsize=20,
                               title=menu_title,
                               window_height=WINDOW_SIZE[1],
                               window_width=WINDOW_SIZE[0]
                               )


def main():
    global clock
    global main_menu
    global surface

    pygame.init()
    pygame.display.set_caption("GC2 Snake v1.0")
    pygame.font.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    surface = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    setting_menu = create_menu('Settings')
    setting_menu.add_selector('Players: ',
                              [('1', 1),
                               ('2', 2),
                               ('3', 3),
                               ('4', 4)
                               ],
                              selector_id='players',
                              default=0,
                              onchange=player_changed)
    setting_menu.add_selector('Speed: ',
                              [('1', 1),
                               ('2', 2),
                               ('3', 3),
                               ('4', 4),
                               ('5', 5),
                               ('6', 6),
                               ('7', 7),
                               ('8', 8),
                               ('9', 9)
                               ],
                              selector_id='speed',
                              default=5,
                              onchange=speed_changed)
    setting_menu.add_option('Return to main', pygameMenu.events.BACK)
    about_menu = create_menu('About')
    for m in ABOUT:
        about_menu.add_line(m)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_option('Return to main', pygameMenu.events.BACK)

    main_menu = create_menu('Main')
    main_menu.add_option('Start', play_function)
    main_menu.add_option('Settings', setting_menu)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    main_menu.set_fps(FPS)
    engine.init(clock, surface)

    while True:
        clock.tick(FPS)
        main_background()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        main_menu.mainloop(events)
        pygame.display.flip()


if __name__ == '__main__':
    main()

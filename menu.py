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
MENU_FONT = pygameMenu.font.FONT_BEBAS

WINDOW_SIZE = (1024, 768)
PLAYERS = 1
SPEED = 6

MAX_PLAYERS = 4

clock = None
main_menu = None
surface = None

player_controls = []
for i in range(0, MAX_PLAYERS):
    player_controls.append(engine.PlayerControls())
input_ctrl_sel_player = [player_controls[0]]


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
    engine.set_params(speed=SPEED, players=PLAYERS, controls=player_controls)
    game_engine = engine.Game(menu=main_menu)
    game_engine.game_loop()  # doesn't return until game is over or close is requested
    main_menu.enable()


def key_input(msg, on_key_pressed, *args, **kwargs):
    """
    Draws an overlay, so that a input key can be retrieved
    :return: None
    """
    global surface
    global main_menu
    while True:
        clock.tick(FPS)
        main_background()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                on_key_pressed(event.key, args, kwargs)
                return
        # main_menu.mainloop(None, disable_loop=True)  # disable events in menu
        main_menu._actual.draw()  # has to be used because mainloop flips internally
        rect_size = (256, 48)
        frame_size = 6
        # inner frame
        pygame.draw.rect(surface, MENU_BACKGROUND_COLOR,
                         (WINDOW_SIZE[0] / 2 - rect_size[0] / 2,
                          WINDOW_SIZE[1] / 2 - rect_size[1] / 2,
                          rect_size[0], rect_size[1]), 0)
        # outer frame
        pygame.draw.rect(surface, COLOR_BACKGROUND,
                         (WINDOW_SIZE[0] / 2 - rect_size[0] / 2,
                          WINDOW_SIZE[1] / 2 - rect_size[1] / 2,
                          rect_size[0], rect_size[1]), frame_size)
        # msg
        font = pygame.font.Font(MENU_FONT, 30)
        rendered_msg = font.render(msg, 1, COLOR_BLACK)
        rendered_msg_size = font.size(msg)
        surface.blit(rendered_msg,
                     (WINDOW_SIZE[0] / 2 - rendered_msg_size[0] / 2,
                      WINDOW_SIZE[1] / 2 - rendered_msg_size[1] / 2))

        pygame.display.flip()


def store_key(key, *args, **kwargs):
    # args[0][0][0] ... 1st and 2nd to access proper element, 3rd because it has to be a ref (which is a list here)
    getattr(args[0][0][0], args[0][1])(key)


def ctrl_player_changed(value, sel_player):
    input_ctrl_sel_player[0] = player_controls[sel_player]


def main_background():
    """
    Function used by menus, draw on background while menu is active.
    :return: None
    """
    global surface
    surface.fill(COLOR_BACKGROUND)


def create_menu(menu_title, font_size=30):
    return pygameMenu.TextMenu(surface,
                               bgfun=main_background,
                               color_selected=COLOR_WHITE,
                               font=MENU_FONT,
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
                               font_size=font_size,
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
    player_select = []
    for p in range(1, MAX_PLAYERS + 1):
        player_select.append((str(p), p))
    setting_menu.add_selector('Players: ', player_select,
                              selector_id='players',
                              default=0,
                              onchange=player_changed)
    speed_select = []
    for p in range(1, 10):
        speed_select.append((str(p), p))
    setting_menu.add_selector('Speed: ', speed_select,
                              selector_id='speed',
                              default=5,
                              onchange=speed_changed)

    ctrl_menu = create_menu('Controls')
    ctrl_menu.add_selector('Select player: ', player_select,
                           selector_id='players',
                           default=0,
                           onchange=ctrl_player_changed)
    ctrl_menu.add_option("Left", key_input, 'Press a key...', store_key, input_ctrl_sel_player, 'set_left')
    ctrl_menu.add_option("Right", key_input, 'Press a key...', store_key, input_ctrl_sel_player, 'set_right')
    ctrl_menu.add_option("Up", key_input, 'Press a key...', store_key, input_ctrl_sel_player, 'set_up')
    ctrl_menu.add_option("Down", key_input, 'Press a key...', store_key, input_ctrl_sel_player, 'set_down')
    ctrl_menu.add_option('Back', pygameMenu.events.BACK)
    setting_menu.add_option('Controls', ctrl_menu)

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
        main_menu.mainloop(events, disable_loop=True)
        pygame.display.flip()


if __name__ == '__main__':
    main()

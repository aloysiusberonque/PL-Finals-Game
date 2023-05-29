import sys

import simplified_pygame

SCREEN = simplified_pygame.PyGameWindow(
    w=640,
    h=480,
    caption='Love Love Love Love Love',
    use_icon=True,
    bg_color=(0, 0, 0),
    default_font='cambria')


import sprite_loader
from maze import Maze, Maze2p
from settings import SETTINGS


def apply_settings():
    SCREEN.set_window_resolution(SETTINGS['resolution'])
    simplified_pygame.mixer.volume = SETTINGS['volume']

apply_settings()


class AppControlls(simplified_pygame.EventReaderAsClass):
    def on_key_f1():
        SCREEN.set_window_resolution(1)
        SETTINGS['resolution'] = 1
    def on_key_f2():
        SCREEN.set_window_resolution(2)
        SETTINGS['resolution'] = 2
    def on_key_f3():
        SCREEN.set_window_resolution('fullscreen')
        SETTINGS['resolution'] = 'fullscreen'
    def on_key_f12():
        import importlib
        importlib.reload(sprite_loader)
    def on_key_escape():
        global GAME_STATE
        if GAME_STATE == 'game' or GAME_STATE == 'settings':
            GAME_STATE = 'menu'
        elif GAME_STATE == 'menu':
            SCREEN.exit()

    def on_key_enter():
        game.new_game()


class MenuControlls(simplified_pygame.EventReader):
    def __init__(self, x, buttons):
        self.x = x
        self.buttons = buttons
        self._old_mouse_pos = None

    def draw(self, W):
        selection_col = (255, 140, 80, 150)
        with W.part(self.x, 0, 170, 480, bg_col=(0, 0, 0, 200)) as layer:
            for x, y, action, text, t in self.buttons:
                if t == 'button':
                    if action == self._mouse_pos:
                        layer.rect((x, y, 150, 40), col=selection_col)
                    layer.write(x+75, y+10, text, pos='.', size=15, col=(255, 255, 255))
                elif t == 'text':
                    layer.write(x, y, text, pos='>', size=15, col=(255, 255, 255))
                elif t == 'small text':
                    layer.write(x, y, text, pos='>', size=12, col=(200, 200, 200))
                elif t == 'switch':
                    if action == self._mouse_pos:
                        layer.rect((x, y, 40, 80), col=selection_col)
                    if SETTINGS[action] == 1:
                        layer.sprite(x+5, y+5, action)
                        layer.sprite(x+5, y+35, 'off')
                    elif SETTINGS[action] == 2:
                        layer.sprite(x+5, y+35, action)
                        layer.sprite(x+5, y+5, 'off')
                elif t == 'on/off':
                    if action == self._mouse_pos:
                        layer.rect((x, y+30, 40, 40), col=selection_col)
                    layer.write(x+20, y+10, text, pos='.', size=12, col=(255, 255, 255))
                    if SETTINGS[action] == True:
                        layer.sprite(x+5, y+35, 'on')
                    else:
                        layer.sprite(x+5, y+35, 'off')
                elif t == 'setter':
                    if action == self._mouse_pos:
                        layer.rect((x, y+30, 40, 40), col=selection_col)
                    layer.write(x+20, y+10, text, pos='.', size=12, col=(255, 255, 255))
                    if SETTINGS[action[0]] == action[1]:
                        layer.sprite(x+5, y+35, 'on')
                    else:
                        layer.sprite(x+5, y+35, 'off')
        # titres
        #for i in range(7, 20):
            #W.write(400, i*30-200, str(i)+'  +- = ABCD abscf 1llllL', pos='>', size=i, col=(255, 255, 255))

    def mouse_map(self, x, y):
        for x0, y0, action, text, t in self.buttons:
            if action is None:
                continue
            if t == 'button':
                w, h = 150, 40
            elif t == 'switch':
                w, h = 40, 80
            elif t == 'on/off' or t == 'setter':
                w, h = 40, 60
            else:
                continue
            if x0 < x-self.x < x0+w and y0 < y <= y0+h:
                button = action
                if action != self._mouse_pos:
                    simplified_pygame.play_sound('mouse_over_sound', volume=0.3)
                return action

    def on_mouse_click(self, button):
        global game
        global GAME_STATE
        if button == '1p':
            GAME_STATE = 'game'
            game = Maze(15, 11)
        elif button == '2p':
            GAME_STATE = 'game'
            game = Maze2p(15, 11)
        elif button == 'exit':
            SCREEN.exit()
        elif button == 'settings':
            GAME_STATE = {'settings': 'menu', 'menu': 'settings'}[GAME_STATE]
        elif isinstance(button, tuple):
            SETTINGS[button[0]] = button[1]
        elif button in ('arrows', 'wasd', 'controller'):
            SETTINGS[button] = 3 - SETTINGS[button]
            if SETTINGS['arrows'] == SETTINGS['wasd'] == SETTINGS['controller']:
                SETTINGS['arrows'] = SETTINGS['wasd'] = SETTINGS['controller'] = 3 - SETTINGS[button]
                SETTINGS[button] = 3 - SETTINGS[button]
        apply_settings()
        simplified_pygame.play_sound('mouse_select_sound', volume=0.5)


credits = """\
game by
    Mikhail Shubin

music by
    Jani Anttila


version 1.0
"""


menu1 = MenuControlls(
    x=0, buttons=[
        (10, 30, '1p', 'One  player', 'button'),
        (10, 90, '2p', 'Two  players', 'button'),
        (10, 150, 'settings', 'Settings', 'button'),
        (10, 250, None, credits, 'small text'),
        (10, 420, 'exit', 'Exit', 'button')
    ])


menu2 = MenuControlls(
    x=470, buttons=[
        (10, 30,  None, 'screen resolution:','text'),
        (10, 60, ('resolution', 1), 'x1', 'setter'),
        (60, 60, ('resolution', 2), 'x2', 'setter'),
        (110, 60, ('resolution', 'fullscreen'), 'fullscreen', 'setter'),
        (10, 170, None, 'controlls:', 'text'),
        (10, 210, None, 'L', 'text'),
        (10, 240, None, 'R', 'text'),
        (35, 200, 'controller', None, 'switch'),
        (75, 200, 'wasd', None, 'switch'),
        (115, 200, 'arrows', None, 'switch'),
        (10, 320,  None, 'music:','text'),
        (10, 350, ('volume', 0), 'off', 'setter'),
        (60, 350, ('volume', 1/2), '1/2', 'setter'),
        (110, 350, ('volume', 1), '1', 'setter'),
    ])



GAME_STATE = "menu"

for events, time_passed, pressed_keys in SCREEN.main_loop(framerate=600):
    AppControlls.read_events(events, time_passed, pressed_keys)
    if GAME_STATE == 'game':
        simplified_pygame.play_music('opus6b', volume=1)
        game.read_events(events, time_passed, pressed_keys)
        game.draw(SCREEN.with_offset(15, 10))
    elif GAME_STATE == 'settings':
        simplified_pygame.play_music('opus6b', volume=0.2)
        SCREEN.sprite(0, 0, 'into')
        menu1.read_events(events, time_passed, pressed_keys)
        menu2.read_events(events, time_passed, pressed_keys)
        menu1.draw(SCREEN)
        menu2.draw(SCREEN)
    else:
        simplified_pygame.play_music('opus6b', volume=0.2)
        SCREEN.sprite(0, 0, 'into')
        menu1.read_events(events, time_passed, pressed_keys)
        menu1.draw(SCREEN)

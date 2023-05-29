import random

import simplified_pygame
from sprite_loader import random_character
from settings import SETTINGS
import threading

class Character(simplified_pygame.EventReader):
    def __init__(self, x, y, maze, controlls=0):
        self.x = x
        self.y = y
        self.maze = maze
        self.pos = 'v'
        self.dx = 0
        self.dy = 0
        self.step = 1
        self.sprs = random_character()

        if controlls == 0:
            # single-player game
            self.key_map = simplified_pygame.DPAD_AS_ARROWS | simplified_pygame.WASD_AS_ARROWS
        elif controlls == 1:
            if SETTINGS['controller'] == 1:
                self.key_map |= simplified_pygame.DPAD_AS_ARROWS
            if SETTINGS['wasd'] == 1:
                self.key_map |= simplified_pygame.WASD_AS_ARROWS
            if SETTINGS['arrows'] == 2:
                self.key_map |= simplified_pygame.DISABLE_ARROWS
        elif controlls == 2:
            if SETTINGS['controller'] == 2:
                self.key_map |= simplified_pygame.DPAD_AS_ARROWS
            if SETTINGS['wasd'] == 2:
                self.key_map |= simplified_pygame.WASD_AS_ARROWS
            if SETTINGS['arrows'] == 1:
                self.key_map |= simplified_pygame.DISABLE_ARROWS


    def set_pos(self, pos):
        self.step = 3-self.step
        self.pos = pos + str(self.step)
        self.delayed_setattr_seq('pos', [(f'{pos}{self.step}', 0),
                                         (f'{pos}{self.step}b', 400),
                                         (f'{pos}{self.step}a', 500),
                                         (pos, 600)])

    def on_key_right(self):
        if not self.maze.right(self.y, self.x):
            self.x += 1
            self.set_pos('>')
            self.delayed_setattr_seq('dx', [(-16, 0), (-8, 100), (-4, 200), (-2, 300), (0, 400)])
            self.delayed_setattr('dy', 0, 0)
            self.maze.victory_screen.draw_line(self.x, self.y, -1, 0)
            self.maze.check_status()

    def on_key_left(self):
        if not self.maze.left(self.y, self.x):
            self.x -= 1
            self.set_pos('<')
            self.delayed_setattr_seq('dx', [(16, 0), (8, 100), (4, 200), (2, 300), (0, 400)])
            self.delayed_setattr('dy', 0, 0)
            self.maze.victory_screen.draw_line(self.x, self.y, 1, 0)
            self.maze.check_status()

    def on_key_down(self):
        if not self.maze.bottom(self.y, self.x):
            self.y += 1
            self.set_pos('v')
            self.dy = -16
            self.delayed_setattr_seq('dy', [(-16, 0), (-8, 100), (-4, 200), (-2, 300), (0, 400)])
            self.delayed_setattr('dx', 0, 0)
            self.maze.victory_screen.draw_line(self.x, self.y, 0, -1)
            self.maze.check_status()

    def on_key_up(self):
        if not self.maze.top(self.y, self.x):
            self.y -= 1
            self.set_pos('^')
            self.dy = 16
            self.delayed_setattr_seq('dy', [(16, 0), (8, 100), (4, 200), (2, 300), (0, 400)])
            self.delayed_setattr('dx', 0, 0)
            self.maze.victory_screen.draw_line(self.x, self.y, 0, 1)
            self.maze.check_status()

    def draw(self, C):
        C.sprite(10 + self.x*40 + self.dx, 10+self.y*40  + self.dy, self.sprs[self.pos])


class VicroryScreen(simplified_pygame.EventReader):
    def __init__(self):
        self.bg = simplified_pygame.Canvas(640, 480)

    def draw(self, C):
        C.sprite(0, 0, self.bg)
        C.write(320, 0, 'Press [Enter] to restart', pos='.', border=True, size=15)

    def draw_line(self, x, y, dx, dy):
        self.bg.line((x*40+23, y*40+30, dx*40, dy*40), col=(200, 0, 0), width=5)


class Heart():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.t = 0

    def draw(self, C):
        spr = 2 if self.t < 100 else 3 if self.t < 200 else 4 if self.t < 300 else 1
        C.sprite(self.x*40+10, self.y*40+15, 'heart'+str(spr))

    def update(self, dt, character):
        dist = abs(self.x - character.x) + abs(self.y - character.y)
        if dist < 5:
            dt *= 2
        self.t = (self.t + dt) % (400 + dist*100)

class Maze():
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self._top = [[j==0 for i in range(w)] for j in range(h)]
        self._left = [[i==0 for i in range(w)] for j in range(h)]
        self.light_now = [[1 for i in range(w)] for j in range(h)]
        self.light_should = [[0 for i in range(w)] for j in range(h)]
        self.sprites = [['fv^<>' for i in range(w)] for j in range(h)]
        self.sprites_w = [['' for i in range(w)] for j in range(h)]

        self.new_game()

    def new_game(self):
        self.ch1 = Character(0, 0, maze = self)
        self.heart = Heart(self.w-1, self.h-1)
        self.victory_screen = VicroryScreen()
        self.plan()
        self.light_now = [[0 for i in range(self.w)] for j in range(self.h)]
        self.state = 'GAME'
        self.check_status()
        
        
    def plan(self):
        self._top = [[True for i in range(self.w)] for j in range(self.h)]
        self._left = [[True for i in range(self.w)] for j in range(self.h)]

        # create sections
        sections = []
        for i in range(self.h):
            for j in range(self.w):
                walls = set()
                if self.have(i-1, j): walls.add((i, j, '^'))
                if self.have(i+1, j): walls.add((i+1, j, '^'))
                if self.have(i, j-1): walls.add((i, j, '<'))
                if self.have(i, j+1): walls.add((i, j+1, '<'))
                sections.append(walls)

        # merge sections
        while len(sections) > 1:
            outer_walls = random.choice(sections)
            wall = random.choice(list(outer_walls))

            # destroy wall
            i, j, lr = wall
            if lr == '<': self._left[i][j] = False
            elif lr == '^': self._top[i][j] = False

            # merge sections
            two_merging = [sec for sec in sections if wall in sec]
            other  = [sec for sec in sections if wall not in sec]

            sections = other + [(two_merging[0] ^ two_merging[1]) - (two_merging[0] & two_merging[1])]

        # choose sprites
        for i in range(self.h):
            for j in range(self.w):
                spr = ''
                if not self.bottom(i, j): spr += 'v'
                if not self.top(i, j): spr += '^'
                if not self.left(i, j): spr += '<'
                if not self.right(i, j): spr += '>'
                self.sprites[i][j] = 'f' + random.choice('012') + spr
                self.sprites_w[i][j] = 'w' + spr.replace('v', '') + random.choice('012')

    def top(self, i, j):    return self._top[i][j]
    def left(self, i, j):   return self._left[i][j]
    def right(self, i, j):  return self._left[i][j+1] if j < self.w-1 else True
    def bottom(self, i, j): return self._top[i+1][j] if i < self.h-1 else True

    def have(self, i, j): return (0 <= i < self.h) and (0 <= j < self.w)

    def reset_light(self):
        self.light_should = [[0 for i in range(self.w)] for j in range(self.h)]

    def cast_light(self, character):
        x, y = character.y, character.x

        def light_right(i, j, power, can_turn):
            if not self.right(i, j) and power > 0:
                j += 1
                self.light_should[i][j] = max(self.light_should[i][j], power)
                light_right(i, j, power - 0.2, can_turn)
                if can_turn:
                    light_up(i, j, (power - 0.4), False)
                    light_down(i, j, (power - 0.4), False)

        def light_left(i, j, power, can_turn):
            if not self.left(i, j) and power > 0:
                j -= 1
                self.light_should[i][j] = max(self.light_should[i][j], power)
                light_left(i, j, power - 0.2, can_turn)
                if can_turn:
                    light_up(i, j, (power - 0.4), False)
                    light_down(i, j, (power - 0.4), False)

        def light_up(i, j, power, can_turn):
            if not self.top(i, j) and power > 0:
                i -= 1
                self.light_should[i][j] = max(self.light_should[i][j], power)
                light_up(i, j, power - 0.2, can_turn)
                if can_turn:
                    light_right(i, j, (power - 0.4), False)
                    light_left(i, j, (power - 0.4), False)

        def light_down(i, j, power, can_turn):
            if not self.bottom(i, j) and power > 0:
                i += 1
                self.light_should[i][j] = max(self.light_should[i][j], power)
                light_down(i, j, power - 0.2, can_turn)
                if can_turn:
                    light_right(i, j, (power - 0.4), False)
                    light_left(i, j, (power - 0.4), False)

        self.light_should[x][y] = 1
        light_right(x, y, 0.8, True)
        light_left(x, y, 0.8, True)
        light_up(x, y, 0.8, True)
        light_down(x, y, 0.8, True)

    def check_status(self):
        self.reset_light()
        self.cast_light(self.ch1)
        if self.ch1.x == self.w-1 and self.ch1.y == self.h-1:
            self.state = 'WIN'
            simplified_pygame.play_sound('victory_sound')

    def draw_walls(self, C):
        for i in range(self.h):
            for j in range(self.w):
                l = self.light_now[i][j]
                if l <= 0:
                    continue
                spr = simplified_pygame.SPRITES[self.sprites[i][j]]
                spr.set_alpha(l*255)
                C.sprite(j*40+5, i*40, spr)
                if i==0 or self.light_should[i-1][j] < self.light_should[i][j]:
                    C.sprite(j*40+5, i*40-10, simplified_pygame.SPRITES['m'+self.sprites_w[i][j][:-1]])
                    spr = simplified_pygame.SPRITES[self.sprites_w[i][j]]
                    spr.set_alpha(l*255)
                    C.sprite(j*40+5, i*40-10, spr)

    def draw(self, C):
        self.draw_walls(C)
        self.ch1.draw(C)
        self.heart.draw(C)
        if self.state == 'WIN':
            self.victory_screen.draw(C)

    def read_events(self, events, time_passed, pressed_keys):
        if self.state == 'GAME':
            self.ch1.read_events(events, time_passed, pressed_keys)
            self.heart.update(time_passed, self.ch1)
            self.raise_light_level(time_passed)

    def raise_light_level(self, dt):
        for i in range(self.h):
            for j in range(self.w):
                if self.light_now[i][j] >= self.light_should[i][j]:
                    self.light_now[i][j] = self.light_should[i][j]
                else:
                    self.light_now[i][j] = min(self.light_should[i][j], self.light_now[i][j] + 0.0003*dt*self.light_should[i][j])


class Maze2p(Maze):
    def new_game(self):
        self.ch1 = Character(0, 0, maze=self, controlls=2)
        self.ch2 = Character(self.w-1, self.h-1, maze=self, controlls=1)
        self.victory_screen = VicroryScreen()
        self.plan()
        self.light_now = [[0 for i in range(self.w)] for j in range(self.h)]
        self.state = 'GAME'
        self.check_status()

    def draw(self, C):
        self.draw_walls(C)
        self.ch1.draw(C)
        self.ch2.draw(C)
        if self.state == 'WIN':
            self.victory_screen.draw(C)

    def check_status(self):
        self.reset_light()
        self.cast_light(self.ch1)
        self.cast_light(self.ch2)
        if self.ch1.x == self.ch2.x and self.ch1.y == self.ch2.y:
            self.state = 'WIN'

    def read_events(self, events, time_passed, pressed_keys):
        if self.state == 'GAME':
            self.ch1.read_events(events, time_passed, pressed_keys)
            self.ch2.read_events(events, time_passed, pressed_keys)
            self.raise_light_level(time_passed)

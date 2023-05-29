"""
PYGAME SIMPLIFIER
(c) Mikhail Shubin
2pi360@gmail.com


Introduction
============

Using `pygame` can be cumbersome sometimes.  `pygame_simplifier` module simplifies the use of `pygame` by providing shortcuts for the most used function and turning game coding into `Event-driven programming`.  This simplification is not comprehensive - I developed it for my own games first -- But it is designed to be easily modified and adopted.

Simplest possible code:

    import simplified_pygame

    WINDOW = simplified_pygame.PyGameWindow(640, 480)

    for events, time_passed, key_pressed in WINDOW.main_loop(framerate=60):
         pass

This code creates a windows, which can be closed.

Simple code with interactivity would look like this:


    import simplified_pygame

    WINDOW = simplified_pygame.PyGameWindow(640, 480)

    class Box(simplified_pygame.EventReader):

        def __init__(self):
            self.x = 0
            self.y = 0

        def on_key_right(self):
            self.x+=1
        def on_key_left(self):
            self.x-=1
        def on_key_up(self):
            self.y-=1
        def on_key_down(self):
            self.y+=1

    box = Box()

    for events, time_passed, key_pressed in WINDOW.main_loop(framerate=60):
         box.read_events(events, time_passed, key_pressed)
         WINDOW.rect((self.x*10+100, self.y*10+100, 10, 10), col=(255, 0, 0))

This would start window with small rectangle, reacting on arrow keys

System function can be implemented like this:

    import simplified_pygame

    WINDOW = simplified_pygame.PyGameWindow(640, 480)

    class AppControlls(simplified_pygame.EventReaderAsClass):

        def on_key_f1():
            WINDOW.set_screen_resolution(1)
        def on_key_f2():
            WINDOW.set_screen_resolution(2)
        def on_key_f3():
            WINDOW.set_screen_resolution('fullscreen')
        def on_key_escape():
            WINDOW.exit()

    for events, time_passed, key_pressed in WINDOW.main_loop(framerate=60):
         AppControlls.read_events(events, time_passed, key_pressed)

This would create a window which closes on pressing `escape` and changes a resolution on pressing `f1`, `f2` and `f3`.



Installation
============

Copy this file `pygame_simplifier.py` into your local folder.



Initialising pygame and the Main Loop
=====================================

To run a game, create a single instance of `simplified_pygame.PyGameWindow`.

    simplified_pygame.PyGameWindow(self, w, h, *, caption='my game', use_icon=False, on_exit=exit_pygame, bg_color=(0, 0, 0), default_font=None, resizable=False)

arguments: `w` and `h`: width and height of the window; `caption`: caption of the window; `use_icon`: whatever to load `icon.ico` from the assets local folder; `on_exit`: function to run when exit button on the window is pressed; `bg_color`: background color; `default_font`: default font to be used; `resizable`: whatever window can be resized.

to run the main loop, call

    for events, time_passed, key_pressed in WINDOW.main_loop(framerate):

here `framerate` is the desired number of loops per second. `main_loop` returns:

`events`: list of user input happened during the last loop. Events dont use `pygame` codes, but simple strings.

`time_passed`: integer, number of milliseconds passed since last loop.

`key_pressed`: set of keys (represented by strings), pressed at the end of the last loop.



Event-driven programming
========================

To used the benefits of event-driven programming paradigm, (1) inhering your custom class from `simplified_pygame.EventReader` (2) create an instance of this class and (3) call `read_events(events, time_passed, key_pressed)` on this instance from the main loop. Object's methods with the certain specific names would be called in response to user actions.


Keyboard and controller keys
----------------------------

### `.on_key_<key-name>(self)`
would be called every time the corresponding key is pressed.


### `.on_hold_<key-name>(self, total_duration, time_passed)`
would be called every loop when the corresponding key is hold down. This event handler receive two positional integer arguments: first is the total number of milliseconds when the key was pressed, second is duration of the last loop. The first argument can also be accessed from instance's `self._hold_duration[key]`. Here is a list of implemented keys:

* arrow keys:  `left`, `right`, `up`, `down`;
* keyboard letters numbers:  `a`, `b` ... `z`;
* numbers:  `0`, `1` ... `9`;
* f-keys:  `f1`, `f2` ... `f12`;
* `+` and `-`: `plus`, `minus`;
* other keys: `enter`, `escape`, `space`, `shift`, `ctrl`, `alt`;
* controller keys: `joy_A`, `joy_B`, `joy_X`, `joy_Y`, `joy_LB`, `joy_RB`, `joy_back`, `joy_start`;
* controller's dpad: `dpad_left`, `dpad_right`, `dpad_up`, `dpad_down`.

I only implement the support of a single controller, as I have a single controller.

Keys can be remaped by modifying `.key_map` dictionary. For example, with `.key_map == {'w': 'up'}` pressing both `w` and `up` will trigger `.on_key_up()` event handler, and holding
both `w` and `up` will trigger `.on_hold_up()` (once per loop, even if both keys are pressed). If you would like to disable a button, assign it to None, eg
when `.key_map == {'w': 'up', 'up': None}` only pressing `w` would trigger `.on_key_up()`.


### `.on_any_key(self, key)`

would be called every time the any key is pressed. Note that if handler for this particular key is also implemented, it would also be called after `on_any_key`.


Mouse
-----

### `.on_mouse_move(self, pos)`
### `.on_mouse_click(self, pos)`
### ` on_mouse_midclick(self, pos)`
### `.on_mouse_rightclick(self, pos)`
### `.on_mouse_wheel_up(self, pos)`
### `.on_mouse_wheel_down(self, pos)`
would be called every time the corresponding events happens. Methods are give a single positional argument: `pos`, which is a tuple `(x, y)` of the mouse coordinates. Coordinates are given relative to the in-game resolution, so one should not care about the screen resolution. If `.mouse_map` is defined, `pos` is replaced by `.mouse_map(x, y)`.

Mouse keys can also be remaped or disabled by modifying `.key_map` dictionary, eg with `.key_map == {'mouse_rightclick': 'mouse_click'}`. Remapping between keyboard and mouse
keys is possible, but remember that mouse event handles are given one positional argument while keyboard events are not.

### `.mouse_map(self, x, y)`
when this method is defined, the positional argument given to all mouse-related handlers is changed to `.mouse_map(x, y)` instead of `(x, y)`. If `mouse_map` returns None, handles except `.on_mouse_move` are not called at all.

This could be useful when, for example, implementing buttons:

    def mouse_map(self, x, y):
        if 100 < x 200 and 100 < y < 200: return 'button1'
        if 100 < x 200 and 300 < y < 400: return 'button2'
        return None

    def on_mouse_click(self, button):
        # here button would be either 'button1' or 'button2',
        # otherwise method is not called at all
        # ...

    def on_mouse_move(self, button):
       # here button would be 'button1', 'button2' or None
       # ...

Implementing `.mouse_map`, would also initialize a `._mouse_pos` attribute which would keep the latest mapped position of the mouse.


Timer
-----

### `.update(self, time_passed)`
If implemented, this method would be triggered every loop. Receive one positional integer argument: number of milliseconds passed since last loop.


### `.on_repeat_every_<milliseconds>(self)`
would be called every `<milliseconds>`, here `<milliseconds>` should be integer, for example method can be called `.on_repeat_every_1000(self)` to be called every second. This handler is called only once per loop, even if a multiple of `<milliseconds>` passed. As any class cannot have multiple methods with the same name, class cant have multiple metronomes with the same frequency. The number of milliseconds left for each of the metronomes can be accessed from `self._metronome_left[milliseconds]`


### `.start_timer(timer_name, duration, reset=True)`
Calling this would trigger `.on_timer_<timer_name>(self)` in `duration` milliseconds. If `.on_timer_<timer_name>(self)` is not declared,
exception would be raised. Example:

    def on_timer_explosion(self):
        # ...

    def put_explisve(self, x):
        # make an explosion in 10 seconds
        self.start_timer(explosion, 1000*10)

If `reset` is `True` (default), all previous triggers for this timer will be cancelled.

### `.delayed_setattr(attr, value, duration, reset=True)`
Calling this would trigger `setattr(self, attr, value)` in `duration` milliseconds. If `attr` is not declared,
exception would be raised. The purpose of this methods is to serve as an simpler alternative to start_timer. Example:

    def take_damage(self, x):
        if self.vulnerability:
            self.hp -= x
            # become invulnerable for 1 second
            self.vulnerability = False
            self.delayed_setattr('vulnerability', True, 1000)


This would be identical to

    def on_timer_vulnerability(self):
        self.vulnerability = True

    def take_damage(self, x):
        if self.vulnerability:
            self.hp -= x
            # become invulnerable for 1 second
            self.vulnerability = False
            self.start_timer('vulnerability', 1000)

If `reset` is `True` (default), all previous triggers for this attribute will be cancelled.

### `.delayed_setattr_seq(attr, pairs)`
Simplifies calling `.delayed_setattr` for one attributs. `pairs` should contain pairs of values and delays. Usefull for animation sequences.

    def start_animation(self):
        self.delayed_setattr_seq('frame', [(0, 0), (1, 100), (2, 200), (3, 300), (4, 400)])

    # this would be identical to

    def start_animation(self):
        self.delayed_setattr('frame', 0, 0)  # it there is any animation running, it will be cancelled
        self.delayed_setattr('frame', 1, 100, reset=False)
        self.delayed_setattr('frame', 2, 200, reset=False)
        self.delayed_setattr('frame', 3, 300, reset=False)
        self.delayed_setattr('frame', 4, 400, reset=False)



System Events
-------------

### `.on_window_resize(self, w, h)`
If implemented, this method would be called every time application window is resized. This can happen only if `PyGameWindow` is initialised with `resizable=True`. This methods receives two positional arguments: new width and height of the window.

### Implementing exit trigger
Custom function which is triggered on closing the application window can be implemented, but in a different way. Write the function, as pass in as an argument when creating `PyGameWindow`. Exit function is triggered before any other events.


Order of execution
------------------

Event handlers are executed in the following order:

1. pressed keys
2. held keys
3. update
4. metronomes
5. timers
6. delayed_setattr

Order of execution between objects is controlled by used calling `read_events()`

Redefining `read_events`
--------------------------

`read_events(events, time_passed, key_pressed)` can be redefined, for example, to call `read_events` of children objects. Call `.__read_events__(events, time_passed, status)` to access the underlying implementation. For example:

    class Character():
       # ...
       def read_events(self, events, time_passed, key_pressed):
           self.right_hand.read_events(events, time_passed, key_pressed)
           self.left_hand.read_events(events, time_passed, key_pressed)
           if not self.sleep:
               self.__read_events__(events, time_passed, key_pressed)


EventReaderAsClass
------------------

Instead of inheriting event handler class from `simplified_pygame.EventReader`, one can inherit from  `simplified_pygame.EventReaderAsClass`. In this case, no instance is needed, as handler would be called for the class methods instead object methods. This approach seems like a hack for me, I dont know if I should recommencement using it. But it seems nice for event handles which dont have any inner state.



Graphics
========

`simplified_pygame.Canvas`
----------------------------

This class implements several shortcuts for `pygame` graphics. Note that `simplified_pygame.PyGameWindow` is an instance of `simplified_pygame.Canvas`.

### `Canvas.fill(col)`
Fill the whole canvas with a given color.

### `Canvas.rect((x0, y0, width, height), col)`
### `Canvas.box((x0, y0, width, height), col)`
Draw a filled (`rect`) or not filled (`box`) rectangle of a given color.

### `Canvas.write(x, y, s, font=None, size=20, col=(100, 100, 100), pos='>', border=False, bold=False, italic=False)`
Write text `s` onto canvas. Text alignment is defined with the `pos` argument, and can be `'.'`, `'<'` or `'>'`.
Uses `Canvas.default_font`, unless other font is provided. Font with the given name is loaded from the `assets` sub directory. Text can contain multiple lines.

### `Canvas.sprite(self, x, y, sprite, scale=1)`
Paste a sprite onto canvas. `sprite` can be `pygame.Surface`, `simplified_pygame.Canvas` or sprite name.
Sprite name is searched in the `simplified_pygame.SPRITES` dictionary. If it is not found there, it is loaded from the `assets` sub directory.
### `Canvas.stack(self, sprite, x=0, y=0)`
Paste a sprite onto the copy of the canvas, and return the copy.

### `Canvas.copy(self)`
### `Canvas.crop(self, x, y, w, h)`
### `Canvas.rotate(self, angle)`
### `Canvas.flip(self, vertical_flip, horizontal_flip)`
Returns the canvas with the cropped, rotated or flipped surface.

### `Canvas.add_outline(self, col=(0, 0, 0))`
Adds a pixel-wide outline around the sprite

### `Canvas.replace_colors(self, mapping)`
Replaces the colors in the sprire according to the mapping

### `Canvas.with_offset(dx, dy)`
Return `simplified_pygame.Canvas` object referring to the same canvas, but every drawing method which would be called on it would be offset by (dx, dy) pixels.

### `Canvas.part(x, y, w, h, bg_col=(0, 0, 0, 0))`
### `Canvas.layer(bg_col=(0, 0, 0, 0))`
Separates a part of the surface. Can be used within a context manager:

    with Canvas.part(...) as subcanvas:
         # draw on subcanvas
    # when exiting from the context, subcanvas will be pasted back on the Canvas

This is useful when working with transparent colors. `part` returns a part of the surface, specified by coordinates; `layer` takes the whole surface.

### `simplified_pygame.Canvas.load(filename, corner_alpha=False)`
Constructor, loading the `.png` file with the given name. If `corner_alpha` is True, all pixels with the same color as top left corner would be treated as transparent.


`simplified_pygame.PyGameWindow`
----------------------------------
In additional to canvas properties, this class have the following methods


### `PyGameWindow.set_game_resolution(w, h)`
Set the resolution of the game, if it should be changed. Mouse events and drawing happens in relation to game resolution.

### `PyGameWindow.set_window_resolution(new_res)`
Set the resolution of the game window, as displayed. `new_res` can be a pair of `(width, height)`, a single number setting the scale between the  game resolution and window resolution, or `'fullscreen'`.


Sound
=====

### `simplified_pygame.play_sound(name, volume=1, repeat=0)`
Play a sound from a given file in the assets folder.

### `simplified_pygame.play_music(name, volume=1, channel=0)`
Start playing a music from a given file in the assets folder. Music plays on repeat.
There could be only one music file per channel. Calling the fuction again with the same argumets does nothing.
Calling the fuction again with the same file and channel but another volume will change we colume, but will not reset the music.
Calling the fuction again with the same channel but another file will stop the current file and start another one.

This function is designed to be called in the main loop, like this:

    for events, time_passed, key_pressed in WINDOW.main_loop(framerate=60):
        ...
        # this would be called 60 times per second, but the music will behave as expected
        if GAME_STATE == 'menu':
            simplified_pygame.play_music('menu_music')
        elif GAME_STATE == 'game':
            simplified_pygame.play_music('game_music')
        elif GAME_STATE == 'combat':
            simplified_pygame.play_music('combat_music')
        ....


### `simplified_pygame.stop_music(channel=0)`
Stop the music on a given channel:

### `simplified_pygame.mixer.volume`
This property can be used to controll master volume. Default is 0.5

Data Files
==========

Use `simplified_pygame.DataFile(filename, *args, **kwargs)` as dictionary which would be saved to the local file every time it is modified. `*args` and `**kwargs` define the values
of the dictionary for the first time the application is execute. Subsequently, values would be loaded from a file.

"""

import os
import sys
import json

import pygame
import pygame.locals as pygame_locals


__version__ = '1.4'


## ---------------------------------------------------------------------------
## Initialization functions
## ---------------------------------------------------------------------------


SPRITES = {}
SOUNDS = {}
FONTS = {}

def assets_path(filename, folder='assets'):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, folder, filename)


def _get_sprite(sprite_name):
    if sprite_name not in SPRITES:
        SPRITES[sprite_name] = Canvas.load(assets_path(sprite_name.removesuffix('.png')+'.png'))
    return SPRITES[sprite_name]


def _get_sound(sound_name):
    if sound_name not in SOUNDS:
        path = assets_path(sound_name)
        if os.path.exists(path.removesuffix('.wav')+'.wav'):
            SOUNDS[sound_name] = pygame.mixer.Sound(path.removesuffix('.wav')+'.wav')
        elif os.path.exists(path.removesuffix('.ogg')+'.ogg'):
            SOUNDS[sound_name] = pygame.mixer.Sound(path.removesuffix('.ogg')+'.ogg')
        elif os.path.exists(path.removesuffix('.mp3')+'.mp3'):
            SOUNDS[sound_name] = pygame.mixer.Sound(path.removesuffix('.mp3')+'.mp3')
        else:
            raise Exception('sound or music file not found: f{path.removesuffix(".wav")+".wav"} or f{path.removesuffix(".mp3")+".mp3"}')
    return SOUNDS[sound_name]


def _get_font(font_name, size, bold=False, italic=False):
    name_tuple = (font_name, size, bold, italic)
    if name_tuple in FONTS:
        pass
    else:
        font_path = None if font_name is None else assets_path(font_name.removesuffix('.ttf')+'.ttf')
        FONTS[name_tuple] = pygame.font.Font(font_path, size)
    return FONTS[name_tuple]


def init_pygame(caption, use_icon):
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'
    info = pygame.display.Info()

    pygame.display.set_caption(caption)
    if use_icon:
        icon = pygame.image.load(assets_path('icon.ico'))
        pygame.display.set_icon(icon)

    return info


def exit_pygame():
    pygame.quit()
    sys.exit()


## ---------------------------------------------------------------------------
## Canvas
## ---------------------------------------------------------------------------
## Canvas object contains pygame.Surface, simplifying access to some basic drawing


class Canvas():
    def __init__(self, w, h, dx=0, dy=0, default_font=None):
        self.surface = pygame.Surface((w, h))
        self.surface.set_colorkey((0, 0, 0, 0), pygame.RLEACCEL)
        self.x0 = dx
        self.y0 = dy
        self.default_font = default_font

    @classmethod
    def from_pygame_surface(cls, surface):
        new = Canvas.__new__(Canvas)
        new.surface = surface
        new.x0 = new.y0 = 0
        new.default_font = None
        return new

    @classmethod
    def load(cls, filename, corner_alpha=False):
        new = Canvas.from_pygame_surface(pygame.image.load(filename))
        if corner_alpha:
            new.surface = new.surface.convert_alpha()
            new.surface.set_colorkey(new.surface.get_at((0, 0)), pygame.RLEACCEL)
        return new

    def with_offset(self, dx, dy):
        new = Canvas.__new__(Canvas)
        new.surface = self.surface
        new.x0 = self.x0 + dx
        new.y0 = self.y0 + dy
        new.default_font = self.default_font
        return new

    def part(self, x, y, w, h, bg_col=(0, 0, 0, 0)):
        return _CanvasContext(x, y, w, h, bg_col, parent=self)
    def layer(self, bg_col=(0, 0, 0, 0)):
        return _CanvasContext(0, 0, self.w, self.h, bg_col, parent=self)

    def _writeln(self, x, y, s, font_object, col=(100, 100, 100), border=False):
        if border:
            txt = font_object.render(s, True, (0, 0, 0))
            self.blit(txt, x-1, y)
            self.blit(txt, x,   y-1)
            self.blit(txt, x+1, y)
            self.blit(txt, x,   y+1)
        txt = font_object.render(s, True, col)
        self.blit(txt, x, y)

    def write(self, x, y, s, font=None, size=20, col=(100, 100, 100), pos='>', border=False, bold=False, italic=False):
        if font is None:
            font = self.default_font
        font_object = _get_font(font, int(size), bold=bold, italic=italic)
        for line in s.split('\n'):
            w = font_object.size(line)[0]
            x1 = x - {'>': 0, '.': w//2, '<': w}[pos]
            self._writeln(x1, y, line, font_object=font_object, col=col, border=border)
            y += font_object.size(line)[1]

    ## reimplement some pygame drawing routines
    ## ----------------------------------------

    def rect(self, coords, col):
        x, y, w, h = coords
        if w < 0: x += w; w *= -1
        if h < 0: y += h; h *= -1
        if col is None:
            return
        pygame.draw.rect(self.surface, [int(c) for c in col], (x+self.x0, y+self.y0, w, h))

    def box(self, coords, col):
        x, y, w, h = coords
        if w < 0: x += w; w *= -1
        if h < 0: y += h; h *= -1
        if col is None:
            return
        pygame.draw.lines(self.surface, [int(c) for c in col], True, [(x+self.x0, y+self.y0), (x+self.x0+w, y+self.y0), (x+self.x0+w, y+self.y0+h), (x+self.x0, y+self.y0+h)])

    def line(self, coords, col, width):
        x, y, w, h = coords
        if col is None:
            return
        pygame.draw.line(self.surface, [int(c) for c in col], start_pos=(x+self.x0, y+self.y0), end_pos=(w+x+self.x0, h+y+self.y0), width=width)

    def fill(self, col):
        self.surface.fill(col)

    def sprite(self, x, y, sprite, scale=1):
        if isinstance(sprite, pygame.Surface):
            pass
        elif isinstance(sprite, Canvas):
            sprite = sprite.surface
        else:
            sprite = _get_sprite(sprite)
            if isinstance(sprite, Canvas):
                sprite = sprite.surface
        if scale != 1:
            final_size = int(sprite.get_size()[0]*scale), int(sprite.get_size()[1]*scale)
            sprite = pygame.transform.scale(sprite, final_size).convert_alpha()
        self.blit(sprite, x, y)
    def blit(self, surface, x, y):
        self.surface.blit(surface, (self.x0 + x, self.y0 + y))
    def stack(self, sprite, x=0, y=0):
        new = self.copy()
        new.blit(sprite.surface, x, y)
        return new

    def crop(self, x, y, w, h):
        return Canvas.from_pygame_surface(self.surface.subsurface((x+self.x0, y+self.y0, w, h)).copy())
    def rotate(self, angle):
        return Canvas.from_pygame_surface(pygame.transform.rotate(self.surface, angle).copy())
    def flip(self, vertical_flip, horizontal_flip):
        return Canvas.from_pygame_surface(pygame.transform.flip(self.surface, vertical_flip, horizontal_flip).copy())
    def copy(self):
        return Canvas.from_pygame_surface(self.surface.copy())
    def set_alpha(self, *args):
        self.surface.set_alpha(*args)
        return self

    def add_outline(self, col=(0, 0, 0)):
        img = self.surface.copy()
        key = img.get_colorkey() if img.get_colorkey() else (157, 112, 170, 0)
        substance = set()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                c = img.get_at((x, y))
                if c != key and c[:3] != col:
                    substance.add((x, y))
        neighbours = set()
        for x, y in substance:
            for dx, dy in (-1, 0), (1, 0), (0, 1), (0, -1):
                neighbours.add((x+dx, y+dy))
        neighbours -= substance
        for x, y in neighbours:
            img.set_at((x, y), col)
        return Canvas.from_pygame_surface(img)

    def replace_colors(self, mapping):
        img = self.surface.copy()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                c = self.surface.get_at((x, y))
                if c[:3] in mapping:
                    img.set_at((x, y), mapping[c[:3]])
        return Canvas.from_pygame_surface(img)

    @property
    def w(self): return self.surface.get_size()[0]
    @property
    def h(self): return self.surface.get_size()[1]

    def __repr__(self):
        return f'sprite {self.w}x{self.h}'


class _CanvasContext(Canvas):
    def __init__(self, x, y, w, h, bg_col, parent):
        self.surface = pygame.Surface((w, h), pygame_locals.SRCALPHA)
        self.surface.set_colorkey((0, 0, 0, 0), pygame.RLEACCEL)
        self.x0 = parent.x0
        self.y0 = parent.y0
        self.default_font = parent.default_font
        self._offset = (x, y)
        self._parent = parent
        self.fill(bg_col)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._parent.surface.blit(self.surface, self._offset)


## ---------------------------------------------------------------------------
## Sounds
## ---------------------------------------------------------------------------


class _Mixer():
    def __init__(self):
        self._on = True
        self.volume = 0.5
        self.music_channels = {}

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, val):
        self._on = val
        if val:
            pygame.mixer.unpause()
        else:
            pygame.mixer.pause()

    def play_sound(self, name, volume=1, repeat=0):
        if self.on:
            sound = _get_sound(name)
            sound.play(repeat)
            sound.set_volume(volume*self.volume)

    def play_music(self, name, volume=1, channel=1):
        if self.on:
            if channel in self.music_channels:
                if name == self.music_channels[channel][0]:
                    # music already playing
                    music = self.music_channels[channel][1]
                    music.set_volume(volume*self.volume)
                    return
                else:
                    # channel exists, but other music is playing
                    music = self.music_channels[channel][1]
                    music.stop()
            # load music
            music = _get_sound(name)
            self.music_channels[channel] = name, music
            music.play(-1)
            music.set_volume(volume*self.volume)

    def stop_music(self, name, channel=None):
        self.music_slots[name, channel].stop()



mixer = _Mixer()

play_sound = mixer.play_sound
play_music = mixer.play_music
stop_music = mixer.stop_music


## ---------------------------------------------------------------------------
## Main Window
## ---------------------------------------------------------------------------


MAIN_WINDOW = None


class PyGameWindow(Canvas):
    def __init__(self, w, h, *, caption='my game', use_icon=False, on_exit=exit_pygame, bg_color=(0, 0, 0), default_font=None, resizable=False):
        global MAIN_WINDOW
        if MAIN_WINDOW is None:
            MAIN_WINDOW = self
        else:
            raise Exception('Window already created')

        # init python
        info = init_pygame(caption, use_icon)
        self._fullscreen_res = (info.current_w, info.current_h)

        # init the window
        self.fullscreen = False
        self._pygame_flags = pygame.RESIZABLE if resizable else 0
        self.current_res = 1
        self.set_game_resolution(w, h)
        self.x0 = 0
        self.y0 = 0
        self.default_font = default_font

        self.exit = on_exit
        self.bg_color = bg_color

    def update_screen(self):
        if self.scale == 1:
            scaled = self.surface
        else:
            scaled = pygame.transform.scale(self.surface, (self.screen_w, self.screen_h))
        self.screen0.blit(scaled, (self.screen_x0, self.screen_y0))
        pygame.display.flip()
        self.surface.fill(self.bg_color)

    def set_game_resolution(self, w, h):
        self.surface = pygame.Surface((w, h))
        self.set_window_resolution(self.current_res)

    def set_window_resolution(self, new_res):
        self.current_res = new_res
        # unpack parameters
        if isinstance(new_res, (int, float)):
            fullscreen = False
            self.scale = scale = new_res
            w, h = self.w * scale, self.h * scale
            self.screen_x0 = self.screen_y0 = 0
            self.screen_w = self.display_w = w
            self.screen_h = self.display_h = h
        else:
            if new_res == 'fullscreen':
                fullscreen = True
                w, h = self._fullscreen_res
            elif isinstance(new_res, (list, tuple)):
                fullscreen = False
                w, h = new_res
            else:
                raise KeyError('Wrong resolution given: ', str(new_res))

            # compute screen's scale compared to game screen
            self.scale = scale = min(w/self.w, h/self.h)
            self.screen_w = int(self.w * scale)
            self.screen_h = int(self.h * scale)
            self.screen_x0 = (w - self.screen_w) // 2
            self.screen_y0 = (h - self.screen_h) // 2
            self.display_w = w
            self.display_h = h

        if self.fullscreen and not fullscreen:
            pygame.display.toggle_fullscreen()
            self.screen0 = pygame.display.set_mode((w, h), flags=self._pygame_flags)
        elif not self.fullscreen and fullscreen:
            self.screen0 = pygame.display.set_mode((w, h), flags=self._pygame_flags)
            pygame.display.toggle_fullscreen()
        elif not self.fullscreen and not fullscreen:
            self.screen0 = pygame.display.set_mode((w, h), flags=self._pygame_flags)

        self.fullscreen = fullscreen

    def main_loop(self, framerate):
        Clock = pygame.time.Clock()

        pressed_keys = set()
        dpad_position = (0, 0)
        joystick_position = [0, 0, 0, 0]

        pygame.joystick.init()
        _joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        while True:
            time_passed = Clock.tick(framerate)  # framerate
            pygame_events = pygame.event.get()
            events = []

            # Translate the list of pygame events into human-readable form
            for event in pygame_events:
                try:
                    # system events
                    if event.type == pygame_locals.QUIT:
                        self.exit()
                    elif event.type == pygame_locals.VIDEORESIZE:
                        events.append(('window_resize', 'sys', event.w, event.h))
                    elif event.type in (pygame_locals.JOYDEVICEADDED, pygame_locals.JOYDEVICEREMOVED):
                        # reinit Joistics
                        _joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

                    # keyboard
                    elif event.type == pygame_locals.KEYDOWN:
                        key = _KEY_MAPPING[event.key]
                        pressed_keys.add(key)
                        events.append((key, 'key'))
                    elif event.type == pygame_locals.KEYUP:
                        key = _KEY_MAPPING[event.key]
                        pressed_keys.discard(key)

                    # joystick
                    elif event.type == pygame_locals.JOYBUTTONDOWN:
                        key = _JOYSTICK_MAPPING[event.button]
                        pressed_keys.add(key)
                        events.append((key, 'key'))
                    elif event.type == pygame_locals.JOYBUTTONUP:
                        key = _JOYSTICK_MAPPING[event.button]
                        pressed_keys.discard(key)
                    elif event.type == pygame_locals.JOYHATMOTION:
                        dpad_position = event.value
                        if dpad_position[0] == +1: events.append(('dpad_right', 'key'))
                        if dpad_position[0] == -1: events.append(('dpad_left', 'key'))
                        if dpad_position[1] == +1: events.append(('dpad_up', 'key'))
                        if dpad_position[1] == -1: events.append(('dpad_down', 'key' ))
                    #elif event.type == pygame_locals.JOYAXISMOTION:
                    #    joystick_position[event.axis] = event.value
                    # not implemented =(

                    # mouse
                    elif event.type in (pygame_locals.MOUSEBUTTONDOWN, pygame_locals.MOUSEMOTION):
                        pos_x = (event.pos[0] - self.screen_x0) / self.scale
                        pos_y = (event.pos[1] - self.screen_y0) / self.scale
                        if event.type == pygame_locals.MOUSEBUTTONDOWN and event.button in _MOUSE_MAPPING:
                            key = _MOUSE_MAPPING[event.button]
                            events.append((key, 'mouse', (pos_x, pos_y)))
                        elif event.type == pygame_locals.MOUSEMOTION:
                            events.append(('mouse_move', 'mouse', (pos_x, pos_y)))
                except KeyError:
                    # currently, not all pygame event keys are presented here
                    pass

            # check dpad position
            pressed_keys -= {'dpad_right', 'dpad_left', 'dpad_up', 'dpad_down'}
            if dpad_position[0] == +1: pressed_keys.add('dpad_right')
            if dpad_position[0] == -1: pressed_keys.add('dpad_left')
            if dpad_position[1] == +1: pressed_keys.add('dpad_up')
            if dpad_position[1] == -1: pressed_keys.add('dpad_down')

            yield events, time_passed, pressed_keys

            # update window
            self.update_screen()


## ---------------------------------------------------------------------------
## EVENT READER
## ---------------------------------------------------------------------------

_KEY_MAPPING = {
    pygame_locals.K_RETURN: 'enter',
    pygame_locals.K_EQUALS: 'plus',
    **{getattr(pygame_locals, 'K_'+k.upper()): k for k in 'escape space   plus minus   left right up down'.split()},
    **{getattr(pygame_locals, 'K_L'+k.upper()): k for k in 'shift ctrl alt'.split()},
    **{getattr(pygame_locals, 'K_R'+k.upper()): k for k in 'shift ctrl alt'.split()},
    **{getattr(pygame_locals, f'K_{k}'): str(k) for k in range(0, 10)},
    **{getattr(pygame_locals, f'K_F{k}'): 'f'+str(k) for k in range(1, 13)},
    **{ord(k): k for k in 'abcdefghijklmnopqrstuvwxyz'}
    }


_JOYSTICK_MAPPING = {
    0: 'joy_A',
    1: 'joy_B',
    2: 'joy_X',
    3: 'joy_Y',
    4: 'joy_LB',
    5: 'joy_RB',
    6: 'joy_back',
    7: 'joy_start',
    }

_MOUSE_MAPPING = {
    1: 'mouse_click',
    2: 'mouse_midclick',
    3: 'mouse_rightclick',
    4: 'mouse_wheel_up',
    5: 'mouse_wheel_down',
    }

_ALL_KEYS = list(_KEY_MAPPING.values()) + list(_JOYSTICK_MAPPING.values())


DPAD_AS_ARROWS = {
    (-1,  0): 'left',
    ( 1,  0): 'right',
    ( 0,  1): 'up',
    ( 0, -1): 'down',
    }

WASD_AS_ARROWS = {'a': 'left', 'd': 'right', 'w': 'up', 's': 'down'}
DPAD_AS_ARROWS = {'dpad_left': 'left', 'dpad_right': 'right', 'dpad_up': 'up', 'dpad_down': 'down'}
DISABLE_ARROWS = {'left': None, 'right': None, 'up': None, 'down': None}


class EventReader():
    def __init__(self):
        self.__init_event_reader__()

    def __init_subclass__(cls):
        # if class have its own init, decorate it to call _init_event_reader() beforehand
        if hasattr(cls, '__init__'):
            class_init = cls.__init__

            def make_decorated_init():
                def decorated_init(self, *args, **kwargs):
                    self.__init_event_reader__()
                    class_init(self, *args, **kwargs)
                return decorated_init

            cls.__init__ = make_decorated_init()

    def __init_event_reader__(self):
        """
        Add handles and additional function to the object
        """
        #################
        ## init timers ##
        #################
        # update
        self._update = hasattr(self, 'update')

        # timers
        self._timers = []

        # delayed setattr
        self._delayed_setattr = []

        # metronomes
        self._metronomes = {}
        self._metronome_left = {}

        # look for methods with particular names
        for method_name in dir(self):
            if method_name.startswith('on_repeat_every_'):
                duration = int(method_name[16:])
                self._metronome_left[duration] = 0
                self._metronomes[duration] = getattr(self, method_name)

        #################################
        ## init imput devices handlers ##
        #################################
        self.key_map = {}
        self._handles = {}
        self._category_handles = set()

        # system events
        if hasattr(self, 'on_window_resize'):
            self._handles['window_resize'] = self.on_window_resize

        # keyboard and joistick
        for key in _ALL_KEYS:
            if hasattr(self, 'on_key_'+key):
                self._handles[key] = getattr(self, 'on_key_'+key)

        if hasattr(self, 'on_any_key'):
            self._category_handles.add('key')

        # mouse
        def make_rejector_of_None(handle):
            def rejector_of_None(z):
                if z is not None:
                    handle(z)
            return rejector_of_None

        for key in _MOUSE_MAPPING.values():
            if hasattr(self, 'on_'+key):
                self._handles[key] = make_rejector_of_None(getattr(self, 'on_'+key))

        if hasattr(self, 'on_mouse_move'):
            self._handles['mouse_move'] = self.on_mouse_move

        if hasattr(self, 'mouse_map'):
            self._category_handles.add('mouse')
            self._mouse_pos = None

        ####################
        ## init hold keys ##
        ####################
        self._hold_handles = {}
        self._hold_duration = {}
        for key in _ALL_KEYS:
            if hasattr(self, 'on_hold_'+key):
                self._hold_handles[key] = getattr(self, 'on_hold_'+key)
                self._hold_duration[key] = 0

    def __read_events__(self, events, time_passed, key_pressed):
        # map keys
        if self.key_map:
            events = [(self.key_map.get(key, key), *args) for (key, *args) in events]
            key_pressed = {self.key_map.get(key, key) for key in key_pressed}

        # process all event
        for (key, category, *args) in events:
            # some handles apply for the whole categories of events
            if category in self._category_handles:
                if category == 'key':
                    self.on_any_key(key)
                elif category == 'mouse':
                    self._mouse_pos = pos = self.mouse_map(*args[0])
                    args = [pos]
            # some only apply to specific events
            if key in self._handles:
                self._handles[key](*args)

        # hold keys
        for key, func in self._hold_handles.items():
            if key in key_pressed:
                self._hold_duration[key] += time_passed
                func(self._hold_duration[key], time_passed)
            else:
                self._hold_duration[key] = 0

        # update
        if self._update:
            self.update(time_passed)

        # metronomes
        for duration, func in self._metronomes.items():
            self._metronome_left[duration] += time_passed
            if self._metronome_left[duration] > duration:
                self._metronome_left[duration] -= duration
                func()

        # timers
        self._timers = [[timer, delay-time_passed] for timer, delay in self._timers]
        while self._timers and self._timers[0][-1] <= 0:
            (timer, delay), *self._timers = self._timers
            getattr(self, 'on_timer_'+timer)()

        # delayed setattr
        self._delayed_setattr = [[attr, value, delay-time_passed] for attr, value, delay in self._delayed_setattr]
        while self._delayed_setattr and self._delayed_setattr[0][-1] <= 0:
            (attr, value, delay), *self._delayed_setattr = self._delayed_setattr
            setattr(self, attr, value)

    def read_events(self, events, time_passed, key_pressed):
        self.__read_events__(events, time_passed, key_pressed)

    def start_timer(self, timer, delay, reset=True):
        if not hasattr(self, 'on_timer_'+timer):
            raise KeyError(f'timer on_timer_{timer} is not declared')
        if reset:
            self._timers = [[key, delay] for key, delay in self._timers if key != timer]
        self._timers.append([timer, delay])
        # sort by delay only
        self._timers = list(sorted(self._timers, key=lambda x: x[-1]))

    def delayed_setattr(self, attr, value, delay, reset=True):
        if not hasattr(self, attr):
            raise AttributeError(f'no attribute {attr}')
        if reset:
            self._delayed_setattr = [[key, value, delay] for key, value, delay in self._delayed_setattr if key != attr]
        self._delayed_setattr.append([attr, value, delay])
        # sort by delay only
        self._delayed_setattr = list(sorted(self._delayed_setattr, key=lambda x: x[-1]))

    def delayed_setattr_seq(self, attr, pairs):
        if not hasattr(self, attr):
            raise AttributeError(f'no attribute {attr}')
        self._delayed_setattr = [[key, value, delay] for key, value, delay in self._delayed_setattr if key != attr]
        self._delayed_setattr += [[attr, v, d] for v, d in pairs]
        # sort by delay only
        self._delayed_setattr = list(sorted(self._delayed_setattr, key=lambda x: x[-1]))


class EventReaderAsClass():
    def __init_subclass__(cls):
        EventReader.__init_event_reader__(cls)

    @classmethod
    def read_events(cls, events, time_passed, key_pressed):
        EventReader.__read_events__(cls, events, time_passed, key_pressed)

    @classmethod
    def start_timer(cls, timer, delay):
        EventReader.start_timer(cls, timer, delay)

    @classmethod
    def delayed_setattr(cls, attr, value, delay):
        EventReader.delayed_setattr(cls, attr, value, delay)


## ---------------------------------------------------------------------------
## DATA FILE
## ---------------------------------------------------------------------------

from collections import UserDict


class DataFile(UserDict):
    def __init__(self, filename, *args, **kwargs):
        self.data = dict(*args, **kwargs)
        path = assets_path(filename, folder='datafiles')
        self._path = path
        try:
            with open(path) as f:
                self.data.update(json.load(f))
        except:
            # what if datafiles folder does not exist?
            folder = assets_path('', folder='datafiles')
            if not os.path.exists(folder):
                os.mkdir(folder)

    def save(self):
        with open(self._path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()

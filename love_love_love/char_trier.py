import sys

import simplified_pygame

SCREEN = simplified_pygame.PyGameWindow(
    w=500,
    h=500,
    caption='Love Love Love Love Love',
    use_icon=True,
    bg_color=(60, 60, 60),
    default_font='cambria')
SCREEN.set_window_resolution(2)


body_n = 0
head_n = 0
head_col = 0
body_col = 0


def recolor_map(mapspr):
    j = 1
    maps = []
    while mapspr.surface.get_at((j, 0))[:3] != (157, 112, 170):
        maps.append({})
        i = 0
        while (new_col := mapspr.surface.get_at((j, i))[:3]) != (157, 112, 170):
            cur_col = mapspr.surface.get_at((0, i))[:3]
            maps[-1][cur_col] = new_col
            i += 1
        j += 1
    return maps


HEADS = []
BODYS = []


sprites = simplified_pygame.Canvas.load(simplified_pygame.assets_path('heads.png'), corner_alpha=True)
k = 0
while sprites.surface.get_at((5, 5 + k*31))[:3] != (0, 0, 0):
    temp = []
    head = {}
    for i, U in enumerate('v va vb ^ ^a ^b > >a >b >c _'.split()):
        X, Y = 5 + i*31, 5 + k*31
        head[U] = sprites.crop(X, Y, 30, 30)
    temp.append(head)
    mappings = recolor_map(head['_'])
    for m in mappings:
        temp.append({k: v.replace_colors(m) for k, v in head.items()})
    HEADS.append(temp)
    k += 1


sprites = simplified_pygame.Canvas.load(simplified_pygame.assets_path('body.png'), corner_alpha=True)
k = 0
while sprites.surface.get_at((5, 5 + k*31))[:3] != (0, 0, 0):
    temp = []
    bodys = {}
    for i, U in enumerate('v v1a v1b v1 ^ ^1a ^1b ^1 > >1a >1b >1 >2a >2b >2 _'.split()):
        X, Y = 5 + i*31, 5 + k*31
        bodys[U] = sprites.crop(X, Y, 30, 30)
    temp.append(bodys)
    mappings = recolor_map(bodys['_'])
    for m in mappings:
        temp.append({k: v.replace_colors(m) for k, v in bodys.items()})    BODYS.append(temp)
    k += 1


CHAR = {}
CHAR_1 = {}
CHAR_2 = {}
CHAR_3 = {}
CHAR_4 = {}
CHAR_5 = {}
CHAR_6 = {}
CHAR_7 = {}
CHAR_8 = {}


def get_sprites(head_n, head_col, body_n, body_col):
    head_col = head_col % len(HEADS[head_n])
    body_col = body_col % len(BODYS[body_n])
    head = HEADS[head_n][head_col]
    body = BODYS[body_n][body_col]
    sprs = {}

    sprs['v'] = head['v'].stack(body['v']).add_outline()
    sprs['v1a'] = head['va'].stack(body['v1a']).add_outline()
    sprs['v1b'] = head['vb'].stack(body['v1b']).add_outline()
    sprs['v1'] = head['vb'].stack(body['v1']).add_outline()

    sprs['^'] = body['^'].stack(head['^']).add_outline()
    sprs['^1a'] = body['^1a'].stack(head['^a']).add_outline()
    sprs['^1b'] = body['^1b'].stack(head['^b']).add_outline()
    sprs['^1'] = body['^1'].stack(head['^b']).add_outline()

    sprs['>'] = head['>'].stack(body['>']).add_outline()
    sprs['>1a'] = head['>a'].stack(body['>1a']).add_outline()
    sprs['>1b'] = head['>b'].stack(body['>1b']).add_outline()
    sprs['>1'] = head['>c'].stack(body['>1']).add_outline()
    sprs['>2a'] = head['>a'].stack(body['>2a']).add_outline()
    sprs['>2b'] = head['>b'].stack(body['>2b']).add_outline()
    sprs['>2'] = head['>c'].stack(body['>2']).add_outline()

    sprs['<'] = sprs['>'].flip(True, False)
    sprs['<1'] = sprs['>1'].flip(True, False)
    sprs['<2'] = sprs['>2'].flip(True, False)
    sprs['<1a'] = sprs['>1a'].flip(True, False)
    sprs['<2a'] = sprs['>2a'].flip(True, False)
    sprs['<1b'] = sprs['>1b'].flip(True, False)
    sprs['<2b'] = sprs['>2b'].flip(True, False)

    sprs['v2'] = sprs['v1'].flip(True, False)
    sprs['v2a'] = sprs['v1a'].flip(True, False)
    sprs['v2b'] = sprs['v1b'].flip(True, False)
    sprs['^2'] = sprs['^1'].flip(True, False)
    sprs['^2a'] = sprs['^1a'].flip(True, False)
    sprs['^2b'] = sprs['^1b'].flip(True, False)

    return sprs

def sprite_loader():
    CHAR.update(get_sprites(head_n, head_col, body_n, body_col))
    CHAR_1.update(get_sprites((head_n+1) % len(HEADS), head_col, body_n, body_col))
    CHAR_2.update(get_sprites((head_n-1) % len(HEADS), head_col, body_n, body_col))
    CHAR_3.update(get_sprites(head_n, (head_col+1) % len(HEADS[head_n]), body_n, body_col))
    CHAR_4.update(get_sprites(head_n, (head_col-1) % len(HEADS[head_n]), body_n, body_col))

    CHAR_5.update(get_sprites(head_n, head_col, (body_n+1) % len(BODYS), body_col))
    CHAR_6.update(get_sprites(head_n, head_col, (body_n-1) % len(BODYS), body_col))
    CHAR_7.update(get_sprites(head_n, head_col, body_n, (body_col+1) % len(BODYS[body_n])))
    CHAR_8.update(get_sprites(head_n, head_col, body_n, (body_col-1) % len(BODYS[body_n])))

sprite_loader()


class AppControlls(simplified_pygame.EventReaderAsClass):
    def on_key_right():
        global head_col
        global head_n
        head_n = (head_n+1) % len(HEADS)
        head_col = head_col % len(HEADS[head_n])
        sprite_loader()
    def on_key_left():
        global head_col
        global head_n
        head_n = (head_n-1) % len(HEADS)
        head_col = head_col % len(HEADS[head_n])
        sprite_loader()
    def on_key_up():
        global head_col
        head_col = (head_col+1) % len(HEADS[head_n])
        sprite_loader()
    def on_key_down():
        global head_col
        head_col = (head_col-1) % len(HEADS[head_n])
        sprite_loader()
    def on_key_a():
        global body_n
        body_n = (body_n-1) % len(BODYS)
        sprite_loader()
    def on_key_d():
        global body_n
        body_n = (body_n+1) % len(BODYS)
        sprite_loader()
    def on_key_s():
        global body_col
        body_col = (body_col+1) % len(BODYS[body_n])
        sprite_loader()
    def on_key_w():
        global body_col
        body_col = (body_col-1) % len(BODYS[body_n])
        sprite_loader()
    def on_key_space():
        global time
        time = 0
    def on_key_escape():
        SCREEN.exit()


time = 0

for events, time_passed, pressed_keys in SCREEN.main_loop(framerate=600):
    AppControlls.read_events(events, time_passed, pressed_keys)

    SCREEN.sprite(40, 40, CHAR['v'])
    SCREEN.sprite(40, 5, CHAR_4['v'])
    SCREEN.sprite(40, 75, CHAR_3['v'])
    SCREEN.sprite(10, 40, CHAR_2['v'])
    SCREEN.sprite(70, 40, CHAR_1['v'])
    SCREEN.write(30, 46, '   <            >', size=10, col=(250, 250, 250), border=True)
    SCREEN.write(50, 30, '^', size=10, col=(250, 250, 250), border=True)
    SCREEN.write(50, 65, 'v', size=10, col=(250, 250, 250), border=True)


    SCREEN.sprite(240, 40, CHAR['v'])
    SCREEN.sprite(210, 40, CHAR_6['v'])
    SCREEN.sprite(270, 40, CHAR_5['v'])
    SCREEN.sprite(240, 5, CHAR_8['v'])
    SCREEN.sprite(240, 75, CHAR_7['v'])
    SCREEN.write(230, 46, '   a            d', size=10, col=(250, 250, 250), border=True)
    SCREEN.write(250, 30, 'w', size=10, col=(250, 250, 250), border=True)
    SCREEN.write(250, 65, 's', size=10, col=(250, 250, 250), border=True)


    if time < 500:
        SCREEN.sprite(100, 100, CHAR['v1'], scale=5)
        SCREEN.sprite(300, 100, CHAR['^1'], scale=5)
        SCREEN.sprite(100, 300, CHAR['<1'], scale=5)
        SCREEN.sprite(300, 300, CHAR['>2'], scale=5)
        time += time_passed
    elif time < 700:
        SCREEN.sprite(100, 100, CHAR['v1b'], scale=5)
        SCREEN.sprite(300, 100, CHAR['^1b'], scale=5)
        SCREEN.sprite(100, 300, CHAR['<1b'], scale=5)
        SCREEN.sprite(300, 300, CHAR['>2b'], scale=5)
        time += time_passed
    elif time < 900:
        SCREEN.sprite(100, 100, CHAR['v1a'], scale=5)
        SCREEN.sprite(300, 100, CHAR['^1a'], scale=5)
        SCREEN.sprite(100, 300, CHAR['<1a'], scale=5)
        SCREEN.sprite(300, 300, CHAR['>2a'], scale=5)
        time += time_passed
    else:
        SCREEN.sprite(100, 100, CHAR['v'], scale=5)
        SCREEN.sprite(300, 100, CHAR['^'], scale=5)
        SCREEN.sprite(100, 300, CHAR['<'], scale=5)
        SCREEN.sprite(300, 300, CHAR['>'], scale=5)

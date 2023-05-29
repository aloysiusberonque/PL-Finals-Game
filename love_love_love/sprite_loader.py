import random

import simplified_pygame
from simplified_pygame import SPRITES
import pygame



sprites = simplified_pygame.Canvas.load(simplified_pygame.assets_path('heart.png'), corner_alpha=True)
items = """ \
    heart1 heart2 heart3 heart4 skin_colors
    arrows wasd controller off on
    """
for k, line in enumerate(items.split('\n')):
    for i, U in enumerate(line.split()):
        X, Y = 5 + i*31, 5 + k*31
        SPRITES[U] = sprites.crop(X, Y, 30, 30)


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
_skin_color_map = recolor_map(SPRITES['skin_colors'])


sprites = simplified_pygame.Canvas.load(simplified_pygame.assets_path('heads.png'), corner_alpha=True)
k = 0
while sprites.surface.get_at((5, 5 + k*31))[:3] != (0, 0, 0):
    head = {}
    for i, U in enumerate('v va vb ^ ^a ^b > >a >b >c _'.split()):
        X, Y = 5 + i*31, 5 + k*31
        head[U] = sprites.crop(X, Y, 30, 30)
    HEADS.append(head)
    mappings = recolor_map(head[U])
    for m in mappings:
        HEADS.append({k: v.replace_colors(m) for k, v in head.items()})
    k += 1


sprites = simplified_pygame.Canvas.load(simplified_pygame.assets_path('body.png'), corner_alpha=True)
k = 0
while sprites.surface.get_at((5, 5 + k*31))[:3] != (0, 0, 0):
    bodys = {}
    for i, U in enumerate('v v1a v1b v1 ^ ^1a ^1b ^1 > >1a >1b >1 >2a >2b >2 <'.split()):
        X, Y = 5 + i*31, 5 + k*31
        bodys[U] = sprites.crop(X, Y, 30, 30)
    BODYS.append(bodys)
    mappings = recolor_map(bodys[U])
    for m in mappings:
        BODYS.append({k: v.replace_colors(m) for k, v in bodys.items()})
    k += 1

def random_character():
    head = random.choice(HEADS)
    body = random.choice(BODYS)
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

    # recolor skin
    skin_color = random.choice(_skin_color_map)
    for k in sprs:
        sprs[k] = sprs[k].replace_colors(skin_color)

    # add other directions
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

sprites = simplified_pygame.Canvas.load(simplified_pygame.assets_path('floor.png'), corner_alpha=True)
for k in range(3):
    for i, U in enumerate('v ^ < >  v<>  ^<>  v^< v^> v^ <>  v<  ^<  ^>  v>  v^<>'.split()):
        X, Y = 5 + i*41, 5 + k*56
        SPRITES['f'+str(k)+U] = sprites.crop(X, Y, 40, 55)


sprites = simplified_pygame.Canvas.load(simplified_pygame.assets_path('walls.png'), corner_alpha=True)
for k in range(3):
    for i, U in enumerate('w w> w< w<> w^< w^>  w^<> w^'.split()):
        X, Y = 5 + i*41, 5 + k*56
        SPRITES[U+str(k)] = sprites.crop(X, Y, 40, 55).surface
k = 3
for i, U in enumerate('mw mw> mw< mw<> mw^< mw^>  mw^<> mw^'.split()):
    X, Y = 5 + i*41, 5 + k*56
    SPRITES[U] = sprites.crop(X, Y, 40, 55).surface

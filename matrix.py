from random import randint

from microbit import Image, display, sleep

PAUSE_TIME_MS = 100
FULL_PIXEL = 9
FADEOUT_RATIO = 2

screen = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]


def screen2image(screen):
    return Image(":".join("".join(str(line[i]) for i in range(5))
                          for line in screen))


def fadeout_screen(screen):
    for x in range(5):
        for y in range(5):
            new_color = screen[y][x] - FADEOUT_RATIO
            screen[y][x] = new_color if new_color >= 0 else 0
    return screen


def put_random_pixel_top_row(screen):
    x = randint(0, 4)
    screen[0][x] = FULL_PIXEL
    return screen


def scroll_down_and_fade(screen):
    full_coords = []

    # find and keep 'leading' pixels
    for x in range(5):
        for y in range(5):
            if screen[y][x] == FULL_PIXEL:
                full_coords.append((x, y))

    screen = fadeout_screen(screen)

    # put 'leading' pixels one row below
    for x, y in full_coords:
        if y < 4:
            screen[y + 1][x] = FULL_PIXEL
    return screen


while True:
    im = screen2image(screen)
    display.show(im)
    screen = put_random_pixel_top_row(screen)
    screen = scroll_down_and_fade(screen)
    sleep(PAUSE_TIME_MS)

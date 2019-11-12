
from random import randint

from microbit import Image, display, sleep, button_a, button_b

PAUSE_TIME_MS = 50
FULL_PIXEL = 9
FADEOUT_RATIO = 2
wait_for_button = False


screen = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

buffer_screen = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]


def copy_screen(screen_to_copy):
    result_scr = [[], [], [], [], []]
    for x in range(5):
        for y in range(5):
            result_scr[x].append(screen_to_copy[x][y])
    return result_scr


def screen2image(screen):
    return Image(":".join("".join(str(line[i]) for i in range(5))
                          for line in screen))


def fadeout_screen(screen):
    for x in range(5):
        for y in range(5):
            new_color = screen[y][x] - FADEOUT_RATIO
            screen[y][x] = new_color if new_color >= 0 else 0
    return screen


def put_random_pixel(screen, count=1):
    for i in range(count):
        x = randint(0, 4)
        y = randint(0, 4)
        screen[y][x] = FULL_PIXEL
    return screen


def clear_screen(screen_to_clear):
    for x in range(5):
        for y in range(5):
            screen_to_clear[y][x] = 0
    return screen_to_clear


def splash(screen, buffer_screen):
    buffer_screen = clear_screen(buffer_screen)
    for x in range(5):
        for y in range(5):
            color = screen[y][x]
            if color > 0:
                new_lesser_x = x - 1 if x > 0 else 0
                new_lesser_y = y - 1 if y > 0 else 0
                new_greater_x = x + 1 if x < 4 else 4
                new_greater_y = y + 1 if y < 4 else 4
                buffer_screen[y][x] = color
                buffer_screen[y][new_lesser_x] = color
                buffer_screen[y][new_greater_x] = color
                buffer_screen[new_lesser_y][x] = color
                buffer_screen[new_greater_y][x] = color
    return copy_screen(buffer_screen)


def fade_out(screen, buffer_screen):
    screen = splash(screen, buffer_screen)
    return fadeout_screen(screen)


while True:
    if button_a.is_pressed():
        wait_for_button = True
        screen = put_random_pixel(screen)
    if button_b.is_pressed():
        wait_for_button = False
    if not wait_for_button:
        screen = put_random_pixel(screen)
        
    screen = fade_out(screen, buffer_screen)
    im = screen2image(screen)
    display.show(im)
    sleep(PAUSE_TIME_MS)

import pygame.display
import pygame.draw
import thread
import time

LINES = [(i, 1 + int(i % 3 == 0)) for i in range(12)]
lines2 = [(i * 0.75, j) for i, j in LINES]

transforms = {
    0:  0,
    1:  1,
    2:  2,
    3:  3,
    4:  (3, 0),
    5:  4,
    6:  (5, 1),
    7:  (6, 0),
    8:  (6, 2),
    9:  (7, 1),
    10: (8, 0),
    11: 8,
}
new_transforms = dict(
    [
        (
            j,
            (i, 2) if not i % 3 else (i, k)
        )
        for j, (i, k)
        in [
            (
                j,
                (i, 1) if k < 0.4 else (i, 0)
            )
            for j, i, k
            in [
                (
                    j,
                    int(round(k)),
                    abs(int(round(k)) - k)
                )
                for j, i, k
                in [
                    (j, i, i * 0.75)
                    for j, i
                    in enumerate(range(12))
                ]
            ]
        ]
    ]
)
transforms = new_transforms


def between(from_, to, grade):
    return from_ + (to - from_) * grade


def transform_lines(g):
    def trans_pair(index):
        rule = transforms[index]
        if not isinstance(rule, tuple):
            # original volume
            rule = rule, LINES[index][1]
        target_index, target_j = rule
        target_i = LINES[target_index][0]
        orig_i, orig_j = LINES[index]
        return between(orig_i, target_i, g), between(orig_j, target_j, g)

    temp = [trans_pair(index) for index, pair in enumerate(LINES)]
    return (
        [
            #((1 + 0.33333 * g) * i, j)
            (i, j)
            for i, j
            in temp
        ],
        between(12, 9, g)
    )


def concat_lines(num):
    position = 0
    result = []
    for i in range(0, num):
        g = i / float(num)
        line, length = transform_lines(g)
        for a, b in line:
            result.append((position + a, b))
        position += length
    return result, position

size = width, height = 800, 600
step = 30
screen = pygame.display.set_mode(size)
white = 255, 255, 255
black = 0, 0, 0


def draw_lines(offset, lines):
    for i, j in lines:
        pygame.draw.line(
            screen,
            white,
            (step * offset, height / 12 * i),
            (step * offset + 10 * j, height / 12 * i)
        )


def draw_all(num=10):
    for i in range(0, num):
        g = i / float(num)
        line, length = transform_lines(g)
        draw_lines(i, line)


forever = True


def flip_forever():
    while forever:
        pygame.display.flip()
        time.sleep(1)

if __name__ == '__main__':
    num = 10
    draw_all(num)
    th = thread.start_new(flip_forever, ())
    beats, whole_length = concat_lines(num)
    from pyo64 import Server
    server = Server().boot().start()
    from table import play_the_beats
    beat = play_the_beats(server, beats, whole_length)

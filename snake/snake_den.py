# -*- coding: utf-8 -*-
import curses

from collections import defaultdict

UP = 259
DOWN = 258
LEFT = 260
RIGHT = 261


class Segment():
    """
    Each segment of the snake is represented by an instance of this class
    """
    y = 0
    x = 0
    coordinates = property(lambda self: (self.y, self.x))

    def __repr__(self):
        return self.representation

    def __init__(self, cord, char='#'):
        self.representation = char
        self.y = cord[0]
        self.x = cord[1]

    def move(self, direction):
        if direction == UP:
            self.y -= 1
            self.representation = '^'
        elif direction == DOWN:
            self.y += 1
            self.representation = 'v'
        elif direction == LEFT:
            self.x -= 1
            self.representation = '<'
        else:  # RIGHT
            self.x += 1
            self.representation = '>'


class Snake():
    body = []

    def add_segment(self):
        seg = Segment(self.body[-1].coordinates)
        self.body.append(seg)

    def render(self):
        for segment in self.body:
            self.screen.addstr(
                segment.coordinates[0],
                segment.coordinates[1],
                segment.representation
            )

    def move(self):
        for i, seg in reversed(list(enumerate(self.body))):
            if not i:
                seg.move(self.direction)
            else:
                seg.x = self.body[i - 1].x
                seg.y = self.body[i - 1].y
                if i > 1:
                    seg.representation = self.body[i - 1].representation

    def check_loss(self):
        cords = defaultdict(int)
        for seg in self.body:
            if seg.y in (-1, curses.LINES + 1) or seg.x in (-1, curses.COLS + 1):
                raise KeyboardInterrupt
            cords[seg.coordinates] += 1
        if max(cords.values()) > 1:
            raise KeyboardInterrupt

    def __init__(self, screen, length, start_cord):
        self.body = []
        self.screen = screen
        self.length = length
        self.direction = UP
        self.head_cord = start_cord

        for offset in range(self.length):
            cord = (start_cord[0] + offset, start_cord[1])
            seg = Segment(cord)
            self.body.append(seg)


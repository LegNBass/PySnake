#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import curses
import random
import time

from curses import wrapper

from snake import Snake


class Game():
    star_cords = (0, 0)

    def __init__(self, screen):
        self.screen = screen
        self.RUNNING = True
        self.speed = 1.0
        self.place_star()

    def speed_up(self):
        self.speed /= 2.0

    def speed_down(self):
        self.speed *= 2.0

    def calc_start_loc(self):
        y = curses.LINES // 2
        x = curses.COLS // 2

        return (y, x)

    def start(self):
        self.snek = Snake(
            self.screen,
            6,
            self.calc_start_loc()
        )
        self.snek.render()
        while self.RUNNING:
            try:
                time.sleep(self.speed)
                self.tick()
            except KeyboardInterrupt:
                self.RUNNING = False

    def place_star(self):
        y = random.randint(0, curses.LINES - 1)
        x = random.randint(0, curses.COLS - 1)

        self.star_cords = (y, x)

    def check_star_get(self):
        if self.star_cords in [
            seg.coordinates
            for seg in self.snek.body
        ]:
            self.snek.add_segment()
            self.place_star()

    def tick(self):
        self.screen.clear()
        direction = self.screen.getch()
        if 258 <= direction <= 261:
            if direction == self.snek.direction:
                self.speed_up()
            elif (direction <= 259 and self.snek.direction <= 259
                  or direction >= 260 and self.snek.direction >= 260):
                self.speed_down()
            elif direction < 260:
                self.speed_down()
                self.snek.direction = direction
            else:
                self.speed_up()
                self.snek.direction = direction
        self.snek.move()
        self.snek.check_loss()
        self.check_star_get()
        self.screen.addstr(
            self.star_cords[0],
            self.star_cords[1],
            '*'
        )
        self.snek.render()
        self.screen.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()

    # Begin the game
    game = Game(stdscr)
    game.start()

wrapper(main)


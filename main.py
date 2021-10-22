#!/usr/bin/env python3

import pygame as pg
from constants import WIDTH, HEIGHT
from game import Game

win = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("Jeu d'échecs")

g = Game()

def draw():
    g.draw(win)
    pg.display.update()


def main():
    while True:
        draw()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return 0

        clock.tick(60)


if __name__ == '__main__':
    main()

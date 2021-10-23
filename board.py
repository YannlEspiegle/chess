#!/usr/bin/env python3

import pygame as pg
from constants import TAILLE_CASE, BLACK, WHITE
from pictures import PIECES


class Board:
    def __init__(self):
        self.plateau = [
            [14, 15, 16, 12, 13, 16, 15, 14],
            [11, 11, 11, 11, 11, 11, 11, 11],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [4, 5, 6, 2, 3, 6, 5, 4],
        ]

    def draw(self, win):
        taille = TAILLE_CASE
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    color = WHITE
                else:
                    color = BLACK

                case = (x * taille, y * taille, taille, taille)
                pg.draw.rect(win, color, case)

                if self.plateau[y][x]:
                    piece_image = PIECES[self.plateau[y][x]]
                    piece_image = pg.transform.scale(piece_image, (taille, taille))
                    win.blit(piece_image, (x * taille, y * taille))

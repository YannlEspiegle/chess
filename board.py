#!/usr/bin/env python3

import pygame as pg
from constants import TAILLE_CASE, BLACK, WHITE, CODE_PIECES
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
        self.piece_est_touchee = False
        self.piece_touchee = None
        self.update_pieces()

    def update_pieces(self):
        self.pieces = []
        for y in range(8):
            for x in range(8):
                if self.plateau[y][x]:
                    if self.plateau[y][x] > 10:
                        color = 2
                    else:
                        color = 1
                    piece = CODE_PIECES[self.plateau[y][x] % 10]
                    self.pieces.append(piece(self.plateau, x, y, color))

    def deplacer(self, x, y):
        print(x, y)
        if (x, y) in self.piece_touchee.coups_possibles():
            self.piece_touchee.deplacer(x, y)
            self.update_pieces()
            self.deselect()
            return True
        return False

    def select(self, x, y):
        if self.plateau[y][x]:
            self.piece_touchee = self.get_piece(x, y)
            self.piece_est_touchee = True
        else:
            self.deselect()
        print(self.piece_touchee.coups_possibles())

    def deselect(self):
        self.piece_touchee = None
        self.piece_est_touchee = False

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

    def get_piece(self, x, y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None

    def get_color(self, x, y):
        if self.plateau[y][x] > 10:
            return 2
        return 1

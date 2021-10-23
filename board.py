#!/usr/bin/env python3

import pygame as pg

from constants import BLACK, CODE_PIECES, TAILLE_CASE, WHITE, YELLOW
from pictures import PIECES, COUP_POSSIBLE, PRISE_POSSIBLE
from pieces import Roi


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
        old_plateau = [[case for case in ligne] for ligne in self.plateau]
        if (x, y) in self.piece_touchee.coups_possibles():
            self.piece_touchee.deplacer(x, y)
            self.update_pieces()

            # si le roi est en échec
            for piece in self.pieces:
                if isinstance(piece, Roi) and piece.color == self.piece_touchee.color:
                    if self.case_attaquee(piece.x, piece.y, piece.get_adverse()):
                        self.plateau = old_plateau
                        self.update_pieces()
                        return False

            self.deselect()
            return True
        return False

    def case_attaquee(self, x, y, color):
        for attaquant in self.pieces:
            if attaquant.color == color and (x, y) in attaquant.coups_possibles():
                return True
        return False

    def select(self, x, y):
        if self.plateau[y][x]:
            self.piece_touchee = self.get_piece(x, y)
            self.piece_est_touchee = True
        else:
            self.deselect()

    def deselect(self):
        self.piece_touchee = None
        self.piece_est_touchee = False

    def draw(self, win):
        taille = TAILLE_CASE
        if self.piece_est_touchee:
            cp = self.piece_touchee.coups_possibles()
        else:
            cp = []

        for y in range(8):
            for x in range(8):
                if self.piece_touchee and (x, y) == (self.piece_touchee.x, self.piece_touchee.y):
                    color = (201, 195, 44)
                elif (x + y) % 2 == 0:
                    color = WHITE
                else:
                    color = BLACK

                case = (x * taille, y * taille, taille, taille)
                pg.draw.rect(win, color, case)

                # desinner les pièces
                if self.plateau[y][x]:
                    piece_image = PIECES[self.plateau[y][x]]
                    piece_image = pg.transform.scale(piece_image, (taille, taille))
                    win.blit(piece_image, (x * taille, y * taille))

                # dessiner les coups/prises possibles
                if (x, y) in cp:
                    if self.plateau[y][x]:
                        image = PRISE_POSSIBLE
                    else:
                        image = COUP_POSSIBLE
                    image = pg.transform.scale(image, (taille, taille))
                    win.blit(image, (x * taille, y * taille))

    def get_piece(self, x, y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None

    def get_color(self, x, y):
        if self.plateau[y][x] > 10:
            return 2
        return 1

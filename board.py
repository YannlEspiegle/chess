#!/usr/bin/env python3

import pygame as pg

from constants import BLACK, CODE_PIECES, SPECIAL, TAILLE_CASE, WHITE
from pictures import COUP_POSSIBLE, PIECES, PRISE_POSSIBLE
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

    def deplacer(self, x, y, deplacer=True):
        old_plateau = [[case for case in ligne] for ligne in self.plateau]
        old_piece_touchee = self.piece_touchee.clone()
        if (x, y) in self.piece_touchee.coups_possibles():
            self.plateau = self.piece_touchee.deplacer(x, y)
            self.update_pieces()

            # si le roi est en échec
            for piece in self.pieces:
                if isinstance(piece, Roi) and piece.color == self.piece_touchee.color:
                    if self.case_attaquee(piece.x, piece.y, piece.get_adverse()):
                        self.plateau = old_plateau
                        self.piece_touchee = old_piece_touchee
                        self.update_pieces()
                        return False

            if not deplacer:
                self.plateau = old_plateau
                self.piece_touchee = old_piece_touchee
                self.update_pieces()
            else:
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
            cp = [(x,y) for x,y in self.piece_touchee.coups_possibles() if self.deplacer(x, y, False)]
        else:
            cp = []

        for y in range(8):
            for x in range(8):
                if self.piece_touchee and (x, y) == (self.piece_touchee.x, self.piece_touchee.y):
                    color = SPECIAL
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

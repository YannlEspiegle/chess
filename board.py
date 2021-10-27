#!/usr/bin/env python3

import pygame as pg

from constants import BLACK, CODE_PIECES, SPECIAL, TAILLE_CASE, WHITE
from pictures import COUP_POSSIBLE, PIECES, PRISE_POSSIBLE
from pieces import Roi, Tour


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

    def deplacer_si_possible(self, x, y):
        if self.coup_legal(self.piece_touchee, x, y):

            if isinstance(self.piece_touchee, Roi) and abs(x - self.piece_touchee.x) == 2:
                if x > self.piece_touchee.x:
                    self.check_roque(self.piece_touchee, 0, deplacer=True)
                self.check_roque(self.piece_touchee, 1, deplacer=True)

            self.piece_touchee.deplacer(x, y)
            self.update_pieces()
            self.deselect()

    def coup_legal(self, piece, x, y):
        if (x, y) in piece.coups_possibles():
            est_legal = True
            old_plateau = [[case for case in ligne] for ligne in self.plateau]
            if self.piece_touchee != None:
                old_piece_touchee = self.piece_touchee.clone()
            else:
                old_piece_touchee = None

            # on vérifie si on peut roquer
            if isinstance(piece, Roi) and abs(x - piece.x) == 2:
                if x > piece.x:
                    return self.check_roque(piece, 0, deplacer=False)
                return self.check_roque(piece, 1, deplacer=False)

            # ensuite, on anticipe le coup, on vérifie si le roi est en échec puis en replace la pièce et le plateau
            piece.deplacer(x, y)
            self.update_pieces()

            # si le roi est en échec
            roi = self.get_king(piece.color)
            if self.case_attaquee(roi.x, roi.y, roi.get_adverse()):
                est_legal = False

            for y in range(8):
                for x in range(8):
                    self.plateau[y][x] = old_plateau[y][x]
            self.piece_touchee = old_piece_touchee
            self.update_pieces()

            return est_legal
        return False

    def case_attaquee(self, x, y, color):
        for attaquant in self.pieces:
            if attaquant.color == color and (x, y) in attaquant.coups_possibles():
                return True
        return False

    def check_roque(self, roi: Roi, direction, deplacer):
        # on vérifie que le cases du roi ne sont pas attaquées
        for i in range(0, 3):
            x, y = roi.horizontale(direction, i)
            if self.case_attaquee(x, y, roi.get_adverse()):
                return False

        # on vérifie qu'il y a bien une tour au bout de la rangée
        if direction == 0:
            x_tour = 7
        elif direction == 1:
            x_tour = 0
        tour = self.get_piece(x_tour, roi.y)

        if isinstance(tour, Tour) and tour.color == roi.color:
            if deplacer:
                tour.deplacer(*roi.horizontale(direction, 1))
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
            cp = [(x,y) for x,y in self.piece_touchee.coups_possibles() if self.coup_legal(self.piece_touchee, x, y)]
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

    def peut_jouer(self, color):
        for piece in self.pieces:
            if piece.color == color:
                self.select(piece.x, piece.y)
                if [(x, y) for x, y in self.piece_touchee.coups_possibles() if self.coup_legal(self.piece_touchee, x, y)]:
                    self.deselect()
                    return True
        self.deselect()
        return False

    def get_king(self, color):
        for piece in self.pieces:
            if isinstance(piece, Roi) and piece.color == color:
                return piece

    def get_color(self, x, y):
        if self.plateau[y][x] > 10:
            return 2
        return 1

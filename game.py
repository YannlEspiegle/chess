#!/usr/bin/env python3

from board import Board
from constants import TAILLE_CASE

class Game:
    def __init__(self):
        self.board = Board()
        self.partie_finie = False
        self.trait = 1

    def on_click(self, pos):
        x, y = pos[0] // TAILLE_CASE, pos[1] // TAILLE_CASE

        if self.board.piece_est_touchee:
            coup_legal = self.board.deplacer(x, y)
            if coup_legal:
                self.tour_suivant()
            else:
                self.board.deselect()
        else:
            if self.board.get_color(x, y) == self.trait:
                self.board.select(x, y)

    def tour_suivant(self):
        if self.trait == 1:
            self.trait = 2
        else:
            self.trait = 1


    def draw(self, win):
        self.board.draw(win)

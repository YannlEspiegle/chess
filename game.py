#!/usr/bin/env python3

import pygame as pg

from board import Board
from constants import BLACK, HEIGHT, TAILLE_CASE, WHITE, WIDTH, TRUE_BLACK, GREY
from pictures import (
    TEXTE_EGALITE,
    TEXTE_VICTOIRE_BLANCS,
    TEXTE_VICTOIRE_NOIRS,
    TITRE_COULEUR_BLANC,
    TITRE_COULEUR_NOIR,
)


class Game:
    def __init__(self):
        self.board = Board()
        self.partie_finie = False
        self.trait = 1
        self.winner = 0

    def on_click(self, pos):
        x, y = pos[0] // TAILLE_CASE, pos[1] // TAILLE_CASE

        if self.board.piece_est_touchee:
            if self.board.coup_legal(self.board.piece_touchee, x, y):
                self.board.deplacer_si_possible(x, y)
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
        if not self.partie_finie:
            self.board.draw(win)
        else:
            self.draw_endscreen(win)

    def draw_endscreen(self, win):
        # Le titre fait les 2/3 de l'écran
        longueur_titre = 2 * WIDTH // 3
        hauteur_titre = longueur_titre // 2

        if self.winner == 1:
            # blancs gagnent -> fond blanc, écriture noire
            titre = TITRE_COULEUR_NOIR
            texte = TEXTE_VICTOIRE_BLANCS
            win.fill(WHITE)

        elif self.winner == 2:
            # noirs gagnent -> fond noir, écriture blanche
            titre = TITRE_COULEUR_BLANC
            texte = TEXTE_VICTOIRE_NOIRS
            win.fill(TRUE_BLACK)

        elif self.winner == 0:
            # égalité -> fond gris, écriture blanche
            titre = TITRE_COULEUR_BLANC
            texte = TEXTE_EGALITE
            win.fill(GREY)

        # on redimensionne le titre et le texte
        titre = pg.transform.scale(titre, (longueur_titre, hauteur_titre))
        texte = pg.transform.scale(texte, (longueur_titre, hauteur_titre))

        # titre centré -> espacement de 1/6 d'écran
        win.blit(titre, (WIDTH // 6, 40))
        win.blit(texte, (WIDTH // 6, HEIGHT // 2))

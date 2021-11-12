#!/usr/bin/env python3

import pygame as pg

from board import Board
from constants import HEIGHT, TAILLE_CASE, WIDTH
from pictures import (
    TEXTE_EGALITE,
    TEXTE_VICTOIRE_BLANCS,
    TEXTE_VICTOIRE_NOIRS,
    TITRE_COULEUR_BLANC,
    TITRE_COULEUR_NOIR,
)
from pieces import Cavalier, Dame, Fou, Tour
from themes import BLACK_BACKGROUND, DRAW_BACKGROUND, WHITE_BACKGROUND


class Game:
    def __init__(self):
        self.board = Board()
        self.partie_finie = False
        self.trait = 1
        self.winner = 0

    def on_click(self, pos):
        if not self.partie_finie:
            x, y = pos[0] // TAILLE_CASE, pos[1] // TAILLE_CASE

            if self.board.piece_est_touchee:
                if self.board.coup_legal(self.board.piece_touchee, x, y):
                    self.board.deplacer_si_possible(x, y)
                    self.tour_suivant()
                    self.check_partie_finie()
                else:
                    self.board.deselect()
            else:
                if self.board.get_color(x, y) == self.trait:
                    self.board.select(x, y)

    def check_partie_finie(self):
        roi = self.board.get_king(self.trait)
        # mat
        if not self.board.peut_jouer(self.trait):
            if self.board.case_attaquee(roi.x, roi.y, roi.get_adverse()):
                # échec et mat
                self.winner = roi.get_adverse()
            else:
                # pat
                self.winner = 0
            self.partie_finie = True

    def check_abandon_draw(self, key):
        if pg.key.get_mods() & pg.KMOD_CTRL:
            if key == pg.K_a:  # ABANDON
                if self.trait == 1:
                    self.winner = 2
                else:
                    self.winner = 1
                self.partie_finie = True
            elif key == pg.K_e:  # ÉGALITÉ
                self.winner = 0
                self.partie_finie = True

    def change_promotion_piece(self, key):
        key_piece = {
            pg.K_d: Dame,
            pg.K_t: Tour,
            pg.K_c: Cavalier,
            pg.K_f: Fou,
        }
        if key in key_piece:
            self.board.piece_promotion = key_piece[key]
            print(f"Promotions en {key_piece[key].nom}")

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
            win.fill(WHITE_BACKGROUND)

        elif self.winner == 2:
            # noirs gagnent -> fond noir, écriture blanche
            titre = TITRE_COULEUR_BLANC
            texte = TEXTE_VICTOIRE_NOIRS
            win.fill(BLACK_BACKGROUND)

        elif self.winner == 0:
            # égalité -> fond gris, écriture blanche
            titre = TITRE_COULEUR_BLANC
            texte = TEXTE_EGALITE
            win.fill(DRAW_BACKGROUND)

        # on redimensionne le titre et le texte
        titre = pg.transform.scale(titre, (longueur_titre, hauteur_titre))
        texte = pg.transform.scale(texte, (longueur_titre, hauteur_titre))

        # titre centré -> espacement de 1/6 d'écran
        win.blit(titre, (WIDTH // 6, 40))
        win.blit(texte, (WIDTH // 6, HEIGHT // 2))

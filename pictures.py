#!/usr/bin/env python3

import pygame as pg

PIECES = {
    1: pg.image.load("assets/pieces/pion_blanc.png"),
    2: pg.image.load("assets/pieces/roi_blanc.png"),
    3: pg.image.load("assets/pieces/dame_blanche.png"),
    4: pg.image.load("assets/pieces/tour_blanche.png"),
    5: pg.image.load("assets/pieces/cavalier_blanc.png"),
    6: pg.image.load("assets/pieces/fou_blanc.png"),
    11: pg.image.load("assets/pieces/pion_noir.png"),
    12: pg.image.load("assets/pieces/roi_noir.png"),
    13: pg.image.load("assets/pieces/dame_noire.png"),
    14: pg.image.load("assets/pieces/tour_noire.png"),
    15: pg.image.load("assets/pieces/cavalier_noir.png"),
    16: pg.image.load("assets/pieces/fou_noir.png"),
}

COUP_POSSIBLE = pg.image.load("assets/icones/mouvement_possible.png")
PRISE_POSSIBLE = pg.image.load("assets/icones/prise_possible.png")

TITRE_COULEUR_BLANC = pg.image.load("assets/textes/titre.png")
TITRE_COULEUR_NOIR = pg.image.load("assets/textes/titre_noir.png")

TEXTE_EGALITE = pg.image.load("assets/textes/egalite.png")
TEXTE_VICTOIRE_BLANCS = pg.image.load("assets/textes/victoire_blanc.png")
TEXTE_VICTOIRE_NOIRS = pg.image.load("assets/textes/victoire_noir.png")

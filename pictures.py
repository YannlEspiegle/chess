#!/usr/bin/env python3

import pygame as pg

PIECES = {
    1: pg.image.load("assets/pion_blanc.png"),
    2: pg.image.load("assets/roi_blanc.png"),
    3: pg.image.load("assets/dame_blanche.png"),
    4: pg.image.load("assets/tour_blanche.png"),
    5: pg.image.load("assets/cavalier_blanc.png"),
    6: pg.image.load("assets/fou_blanc.png"),
    11: pg.image.load("assets/pion_noir.png"),
    12: pg.image.load("assets/roi_noir.png"),
    13: pg.image.load("assets/dame_noire.png"),
    14: pg.image.load("assets/tour_noire.png"),
    15: pg.image.load("assets/cavalier_noir.png"),
    16: pg.image.load("assets/fou_noir.png"),
}

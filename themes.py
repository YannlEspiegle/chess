#!/usr/bin/env python3
import pygame as pg


THEME_NAME = "yann"


def hex_to_rgb(hex_color):
    assert isinstance(hex_color, str) and len(hex_color) == 7 and hex_color[0] == "#"
    rbg = [0] * 3
    triad = hex_color[1:]
    for i in range(3):
        hex_number = triad[i * 2 : i * 2 + 2]
        rbg[i] = int(hex_number, 16)
    return tuple(rbg)


def get_colors_from_files(colors_file):
    color_variables = {}
    with open(colors_file, "r", encoding="utf-8") as f:
        for ligne in f.readlines():
            if ligne[0] == "#":
                pass
            nom, hex_color = ligne.rstrip().split(":")
            nom = nom.upper().replace("-", "_")
            color_variables[nom] = hex_to_rgb(hex_color)
    return color_variables


def get_theme(name):
    pieces = {
        1: pg.image.load(f"themes/{name}/pieces/pion_blanc.png"),
        2: pg.image.load(f"themes/{name}/pieces/roi_blanc.png"),
        3: pg.image.load(f"themes/{name}/pieces/dame_blanche.png"),
        4: pg.image.load(f"themes/{name}/pieces/tour_blanche.png"),
        5: pg.image.load(f"themes/{name}/pieces/cavalier_blanc.png"),
        6: pg.image.load(f"themes/{name}/pieces/fou_blanc.png"),
        11: pg.image.load(f"themes/{name}/pieces/pion_noir.png"),
        12: pg.image.load(f"themes/{name}/pieces/roi_noir.png"),
        13: pg.image.load(f"themes/{name}/pieces/dame_noire.png"),
        14: pg.image.load(f"themes/{name}/pieces/tour_noire.png"),
        15: pg.image.load(f"themes/{name}/pieces/cavalier_noir.png"),
        16: pg.image.load(f"themes/{name}/pieces/fou_noir.png"),
    }

    color_variables = get_colors_from_files(f"themes/{name}/colors.txt")
    return pieces, color_variables


PIECES, color_variables = get_theme(THEME_NAME)

BLACK_CASE = color_variables["BLACK_CASE"]
WHITE_CASE = color_variables["WHITE_CASE"]
SELECTED_CASE = color_variables["SELECTED_CASE"]
BLACK_BACKGROUND = color_variables["BLACK_BACKGROUND"]
WHITE_BACKGROUND = color_variables["WHITE_BACKGROUND"]
DRAW_BACKGROUND = color_variables["DRAW_BACKGROUND"]

#!/usr/bin/env python3

from pieces import Cavalier, Dame, Fou, Pion, Roi, Tour

WIDTH = 600
HEIGHT = 600

TAILLE_CASE = WIDTH // 8

TRUE_BLACK = (30, 30, 30)
GREY = (90, 90, 90)
BLACK = (80, 80, 80)
WHITE = (230, 230, 230)
SPECIAL = (201, 195, 44)

CODE_PIECES = {1: Pion, 2: Roi, 3: Dame, 4: Tour, 5: Cavalier, 6: Fou}

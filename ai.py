#!/usr/bin/env python3
from board import Board
from pieces import Roi
import random as rd

class AI:
    def __init__(self):
        pass

    def evalue_position(self, board: Board, couleur):
        """Évalue la position pour le joueur de couleur `couleur` en renvoyant un nombre"""
        score = 0
        for piece in board.pieces:
            if piece.color == couleur:
                if not isinstance(piece, Roi):
                    score += piece.valeur
        return score

    def meilleur_coup(self, board, trait):
        """La méthode `prochain_coup` part d'un tableau 2D board et renvoie une liste
        de coordonnées (depart, arrivee) correspondant au meilleur coup trouvé par l'IA"""


        # cherche une pièce pouvant jouer (càd liste_coups != [])
        piece = rd.choice([piece for piece in board.pieces if piece.color == trait])
        while not piece.coups_possibles():
            piece = rd.choice([piece for piece in board.pieces if piece.color == trait])

        deplacement = rd.choice(piece.coups_possibles())

        return (piece.x, piece.y), deplacement

#!/usr/bin/env python3

from board import Board

class Game:
    def __init__(self):
        self.board = Board()

    def draw(self, win):
        self.board.draw(win)

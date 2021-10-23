#!/usr/bin/env python3


class Piece:
    def __init__(self, plateau, x, y, color):
        self.x = x
        self.y = y
        self.color = color  # 1 -> blanc, 2 -> noir
        self.plateau = plateau

    def deplacer(self, x, y):
        """Déplace la pièce sans se soucier du fait que le coup soit légal ou non"""
        self.plateau[y][x] = self.plateau[self.y][self.x]
        self.plateau[self.y][self.x] = 0
        self.x = x
        self.y = y

    def est_adverse(self, x, y):
        """Indique si la case (x, y) est occupée par une pièce adverse"""
        if 0 <= x < 8 and 0 <= y < 8:
            if self.color == 1:
                return self.plateau[y][x] > 10
            return self.plateau[y][x] < 10 and self.plateau[y][x] != 0
        return False

    def est_vide(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8 and self.plateau[y][x] == 0

    def diagonale(self, direction, l):
        """Renvoie la case en diagonale de direction {0, 1, 2, 3} et de longueur l par rapport à la pièce"""
        directions = {
            0: (self.x + l, self.y - l),
            1: (self.x - l, self.y - l),
            2: (self.x + l, self.y + l),
            3: (self.x - l, self.y + l),
        }
        return directions[direction]

    def horizontale(self, direction, l):
        """Voir `diagonale()`"""
        directions = {
            0: (self.x + l, self.y),
            1: (self.x - l, self.y),
            2: (self.x, self.y + l),
            3: (self.x, self.y - l),
        }
        return directions[direction]


class Pion(Piece):
    def __init__(self, plateau, x, y, color):
        super().__init__(plateau, x, y, color)

    def coups_possibles(self):
        res = []

        # en fonction de la couleur du pion, il se déplace vers le haut ou vers le bas
        if self.color == 1:
            horiz = [self.horizontale(3, l=1)]
            if self.y == 6:  # premier coup du pion
                horiz.append(self.horizontale(3, l=2))
            diagos = [self.diagonale(0, l=1), self.diagonale(1, l=1)]

        elif self.color == 2:
            horiz = [self.horizontale(2, l=1)]
            if self.y == 1:  # premier coup du pion
                horiz.append(self.horizontale(2, l=2))
            diagos = [self.diagonale(2, l=1), self.diagonale(3, l=1)]

        for x, y in horiz:
            if self.est_vide(x, y):
                res.append((x, y))

        for x, y in diagos:
            if self.est_adverse(x, y):
                res.append((x, y))

        return res


class Fou(Piece):
    def __init__(self, plateau, x, y, color):
        super().__init__(plateau, x, y, color)

    def coups_possibles(self):
        res = []
        for direction in range(4):
            longueur = 1
            x, y = self.diagonale(direction, longueur)

            while self.est_vide(x, y):
                res.append((x, y))
                longueur += 1
                x, y = self.diagonale(direction, longueur)

            if self.est_adverse(x, y):
                res.append((x, y))

        return res


class Cavalier(Piece):
    def __init__(self, plateau, x, y, color):
        super().__init__(plateau, x, y, color)

    def coups_possibles(self):
        res = []

        ajout_x = [2, 1, -1, -2, -2, -1, 1, 2]
        ajout_y = [1, 2, 2, 1, -1, -2, -2, -1]

        for i in range(8):
            x = self.x + ajout_x[i]
            y = self.y + ajout_y[i]

            if self.est_vide(x, y) or self.est_adverse(x, y):
                res.append((x, y))

        return res


class Tour(Piece):
    def __init__(self, plateau, x, y, color):
        super().__init__(plateau, x, y, color)

    def coups_possibles(self):
        res = []
        for direction in range(4):
            longueur = 1
            x, y = self.horizontale(direction, longueur)

            while self.est_vide(x, y):
                res.append((x, y))
                longueur += 1
                x, y = self.horizontale(direction, longueur)

            if self.est_adverse(x, y):
                res.append((x, y))

        return res


class Roi(Piece):
    def __init__(self, plateau, x, y, color):
        super().__init__(plateau, x, y, color)

    def coups_possibles(self):
        res = []
        for direction in range(4):
            x, y = self.horizontale(direction, l=1)
            if self.est_vide(x, y) or self.est_adverse(x, y):
                res.append((x, y))
            x, y = self.diagonale(direction, l=1)
            if self.est_vide(x, y) or self.est_adverse(x, y):
                res.append((x, y))

        return res


class Dame(Piece):
    def __init__(self, plateau, x, y, color):
        super().__init__(plateau, x, y, color)

    def coups_possibles(self):
        res = []
        for direction in range(4):
            for i in range(2):
                if i == 1:  # on regarde les déplacements diagonaux puis horizontaux/verticaux
                    deplacement = self.diagonale
                else:
                    deplacement = self.horizontale

                longueur = 1
                x, y = deplacement(direction, longueur)

                while self.est_vide(x, y):
                    res.append((x, y))
                    longueur += 1
                    x, y = deplacement(direction, longueur)

                if self.est_adverse(x, y):
                    res.append((x, y))

        return res

#!/usr/bin/env python3


class Piece:
    code = 0
    nom = "piece"

    def __init__(self, plateau, x, y, color):
        self.x = x
        self.y = y
        self.color = color  # 1 -> blanc, 2 -> noir
        self.plateau = plateau

    def clone(self):
        return self.__class__(self.plateau, self.x, self.y, self.color)

    def __repr__(self):
        return f"{self.nom}({self.x};{self.y})"

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

    def get_adverse(self):
        if self.color == 1:
            return 2
        return 1

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
    code = 1
    nom = "pion"

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
    code = 6
    nom = "fou"

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
    code = 5
    nom = "cavalier"

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
    code = 4
    nom = "tour"

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
    code = 2
    nom = "roi"

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

        # roque
        if (self.color == 1 and self.y == 7) or (self.color == 2 and self.y == 0):
            grand_roque = True
            petit_roque = True
            for i in range(1, 4):
                # le grand roque est possible si les trois case de droite sont vide
                grand_roque = grand_roque and self.est_vide(*self.horizontale(0, l=i))
            for i in range(1, 3):
                petit_roque = petit_roque and self.est_vide(*self.horizontale(1, l=i))

            if grand_roque:
                res.append(self.horizontale(0, l=2))
            if petit_roque:
                res.append(self.horizontale(1, l=2))

        return res


class Dame(Piece):
    code = 3
    nom = "dame"

    def __init__(self, plateau, x, y, color):
        super().__init__(plateau, x, y, color)

    def coups_possibles(self):
        res = []
        for direction in range(4):
            for i in range(2):
                # on regarde les déplacements diagonaux puis horizontaux/verticaux
                if i == 1:
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

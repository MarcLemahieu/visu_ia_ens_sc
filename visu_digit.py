from __future__ import annotations

from typing import *
from seven_segments import *

# Ce fichier a pour propos de créer une classe Digit qui permet 
# de créer des chiffres à 7 segments dans un canvas, de changer leur 
# couleur selon l'état "testé et approuvé" ou pas
# il permettra de disposer ces chiffres avec la taille et l'emplacement 
# désigné
# avant elle on créera une classe Segment qui serat utilisée pour 
# la classe Digit, un segment sera construit selon taille couleur et orientation 

import tkinter as tk

# On donne les coordonnées des sommets d'un polygone qui servira de
# modèle pour les segments horizontaux et verticaux pour tracer les
# chiffres par translation 
# Les dimmensions finale d'un tel chiffre sont inscrites dans un rectangle de 
# 178 par 249

v_seg = ((10, -50), (25, -30), (13, 30), (-10, 50), (-25, 30), (-13, -30))
h_seg = ((35, -20), (50, 0), (27, 20), (-35, 20), (-50, 0), (-27, -20))
# On donne les vecteurs de translation pour chacun des 7 segments 
vec_a = (21, -105)
vec_b = (65, -52)
vec_c = (43, 52)
vec_d = (-21, 105)
vec_e = (-65, 52)
vec_f = (-43, -52)
vec_g = (0, 0)
v = {'a':(vec_a, h_seg), 'b':(vec_b, v_seg), 
        'c':(vec_c, v_seg), 'd':(vec_d, h_seg), 
        'e':(vec_e, v_seg), 'f':(vec_f, v_seg), 
        'g':(vec_g, h_seg)}

dark = "gray48"
checked = "lawn green"
unchecked = "orange red"

class Digit(tk.Canvas):
    @staticmethod
    def homothetie(ratio: float, center: tuple[int], point: tuple[int])->tuple[int]:
        """renvoie les coordonnées entières d'un point pour une homothétie
        de rapport ratio, autour du centre center

        @arguments:
          ratio rapport de l'homothétie (positif)
          center coord du centre d'homothétie
          point coord du point dont on veut les coords de l'image

        @return
          coords du point image
        """
        x0, y0 = center
        x, y = point
        return int(x0 + (x - x0)*ratio), int(y0 + (y - y0)*ratio)

    @staticmethod
    def translation(vec: tuple[int], point: tuple[int])->tuple[int]:
        """renvoie les coordonnées entières de l'image d'un point point
        pour une translation de vecteur vec

        @arguments: 
          vec coord du vecteur de translation
          point coord du point dont on construit l'image

        @return 
          coords du point image
        """
        xt, yt = vec
        x, y = point
        return (x+xt, y+yt)

    @staticmethod
    def coord_poly_seg(nb_center: tuple[int], coeff: float, position: str,)->list[int]:
        """renvoie la liste des coordonnées du segment(polygone) 
        pour le chiffre à 7 segments centré en nb_center
        avec un coeff d'homothétie coeff correspondant au segment position du nb

        @arguments:
          nb_centre coords entières du centre du nombre construit
          coeff rapport d'homothétie du chiffre de hauteur initiale 100 (largeur:37) 
          position c'est la place "abcdefg" du segment dans le chiffre

        @return:
          liste de 12 entiers qui serviront à tracer le polygone
        """
        coeff = coeff/2.5
        points = v[position][1]
        points = [Digit.translation(Digit.homothetie(coeff, (0,0),v[position][0]),Digit.homothetie(coeff, (0,0), point)) for point in points]
        lst_polygone = []
        for point in points:
            lst_polygone += list(Digit.translation(nb_center, point))
        return lst_polygone

    def trace_nombre(self, nb_center: tuple[int], coeff: float, value: int, tag:str="")->None:
        """
        permet de dessiner les 7 polygones du chiffre à 7 segments
        en le centrant sur nb_centre avec un coeff d'homothétie de
        coeff par rapport à la taille de base de 37x100

        @arguments:
            - nb_centre : coordonnées du centre du chiffre
            - coeff : rapport d'homothétie 
            - value : le chiffre qui sera représenté
            - tag : str qui permettra de retrouver le polygone 
              de manière unique ou groupée
        """
        segments_actifs = seven_seg(value)
        coords = [self.coord_poly_seg(nb_center, coeff, s) for s in "abcdefg"]
        colors = [ unchecked if b else dark for b in segments_actifs]
        for coord, color, seg in zip(coords, colors, "abcdefg"):
            self.create_polygon(coord, fill= color, tag = tag+seg)
        


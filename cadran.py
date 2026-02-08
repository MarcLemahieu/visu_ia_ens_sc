from __future__ import annotations

from typing import *

from visu_digit import Digit, v
from seven_segments import seven_seg
from math import sin, cos, pi

# Ce fichier reprend Digit déjà crée pour finaliser les 
# positionnements des éléments graphiques dans le canvas:
#     - le cadran de chiffres qui changeront successivement
#       de couleurs à chaque validation ou reviendront à la $
#       couleur de non validation tous ensemble
#     - le chiffre central qui variera en fonction de celui  
#       qui est testé avec les pondérations
#     - les poids placés sur les 7 segments du chiffre central
#       qui seront amenés à varier.
#     - les trois boutons : 
#         - tester le nombre et éventuellement
#           passer au suivant
#         - augmenter les valeurs de coeff actifs
#         - diminuer les valeurs de coeff actifs

dark = "gray48"
checked = "lawn green"
unchecked = "orange red"
weights = [1, 2, 2, 1, 0, 0, -1]

class Cadran(Digit):
    def trace_cadran(self)->None:
        """
        construit dix chiffres autour d'un disque, proportionné
        à la taille du Canvas

        @return None, les polygones créés à cet effet sont nommés:
            cadr_0a, cadr_0b .... cadr_9f, cadr_9g
        """
        l, h = int(self.cget('width')),int(self.cget('height'))
        # pour le momment on considère qu'on a le rayon du cadran
        # il faudra changer la ligne suivante:
        r = 0.375*h
        rapport = h/600
        for i in range(10):
            angle = (-2.5+i)*pi/5
            centre = (l//2+int(r*cos(angle)), h//2+int(r*sin(angle)))
            self.trace_nombre(centre, rapport, i, f"cadr_{i}")

    def chge_color_nb(self, nb:int, color:str)->None:
        """
        permet de changer la couleur du nbre nb du cadran 
        a savoir tout les polygones tagués de la forme"cadr_{nb}*" 
        ATTENTION, il doit être tracé au préalable.

        @arguments :
           nb est le nombre du cadran dont on change la couleur.
           color est la couleur qui sera appliquée
        """
        assert isinstance(nb, int)and  nb<10 and nb > -1
        etat_seg = seven_seg(nb)
        for nom, etat in zip("abcdefg", etat_seg):
            for poly in self.find_withtag(f"cadr_{nb}{nom}"):
                if etat:
                    self.itemconfigure(poly, fill=color)

    def bon_test(self, nb:int)->None:
        """
        passe le chiffre nb du cadran (déjà tracé)
        de la couleur checked (variable globale
        """
        self.chge_color_nb(nb, checked)

    def reset_cadran(self)->None:
        """
        passe tous les chiffres du cadran en couleur unchecked
        """
        for i in range(10):
            self.chge_color_nb(i, unchecked)

    def create_central_digit(self)->None:
        """
        construit les 7 polygones du chiffre central 
        tous de la couleur globale dark
        ils sont tagués "centr_{s}" avec s dans "abcdefg"
        """
        l, h = int(self.cget('width')),int(self.cget('height'))
        pos = l//2, h//2
        coords = [self.coord_poly_seg(pos, 2.5*h/600, s) for s in "abcdefg"]
        for coord, seg in zip(coords,"abcdefg"):
            self.create_polygon(coord, fill=dark, tag=f"centr_{seg}")

    def change_central_digit(self, nb: int, color_on:str, color_off:str)->None:
        """
        actualise le chiffre central avec 
          - les polygones des segments actifs en color_on
          - les polygones des segments inactifs en color_off
        """
        seg_on = seven_seg(nb)
        for on, s in zip(seg_on,"abcdefg"):
            if on:
                for poly in self.find_withtag(f"centr_{s}"):
                    self.itemconfig(poly, fill=color_on)
            else:
                for poly in self.find_withtag(f"centr_{s}"):
                    self.itemconfig(poly, fill=color_off)


    def create_central_weights(self, weights:list[int])->None:
        """
        crée les pondérations placées sur les segments du 
        chiffre central 
        chaque pondération est tagué "weight_{s}" avec s dans"abcdefg"
        """
        l, h = int(self.cget('width')),int(self.cget('height'))
        pos = l//2, h//2
        coeff =  1.1 * h / 600
        coords = [(int(x*coeff)+pos[0], int(y*coeff)+pos[1])for x,y in [v[s][0] for s in "abcdefg"]]
        for coord, weight, s in zip(coords, weights,"abcdefg"):
            self.create_text(coord, text=f"{weight}", font=('Arial', int(17*h/300), "bold"), justify="center", fill="black", tag=f"weight_{s}")

    def change_central_weights(self, weights: list[int])->None:
        """
        modifie l'ensemble des poids attachés aux 7 segments du 
        chiffre central
        """
        for weight, s in zip(weights, "abcdefg"):
            for txt in self.find_withtag(f"weight_{s}"):
                self.itemconfigure(txt, text=str(weight))

    def create_button(self, role:str)->None:
        l, h = int(self.cget('width')),int(self.cget('height'))
        r = l//16
        ovals={"up": (r,r, 3*r,3*r), "test": (13*r,9*r,15*r,11*r), "down": (r,9*r,3*r,11*r)}
        triangles={"up":(2*r+int(r*cos(-pi/2)),2*r+int(r*sin(-pi/2)),2*r+int(r*cos(pi/3)),2*r+int(r*sin(pi/3)),2*r+int(r*cos(2*pi/3)),2*r+int(r*sin(2*pi/3))), "test":(14*r+int(r*cos(0)),10*r+int(r*sin(0)),14*r+int(r*cos(-2*pi/3)),10*r+int(r*sin(-2*pi/3)),14*r+int(r*cos(2*pi/3)),10*r+int(r*sin(2*pi/3))), "down":(2*r+int(r*cos(pi/2)),10*r+int(r*sin(pi/2)),2*r+int(r*cos(-pi/3)),10*r+int(r*sin(-pi/3)),2*r+int(r*cos(-2*pi/3)),10*r+int(r*sin(-2*pi/3)))}
        self.create_oval(ovals[role], fill=dark, width=int(4*l/800), outline=checked, activefill=unchecked, tag="bouton_"+role)
        self.create_polygon(triangles[role], fill=checked, tag="bouton_"+role)

    def create_auto(self, auto: bool):
        l= int(self.cget('width'))
        r = l//16
        etat = "normal" if auto else "hidden"
        self.create_text(14*r, 2*r, text="Auto", fill="black", font=("Arial", int(18*l/400), "bold"), state=etat, tag = "auto")

    def change_auto(self):
        for txt in self.find_withtag("auto"):
            etat = self.itemcget(txt,"state")
            if etat == "normal":
                etat = "hidden"
            else:
                etat = "normal"
            self.itemconfigure(txt, state = etat)

    def remise_a_plat(self):
        self.trace_cadran()
        self.create_central_digit()
        for role in ("up", "down", "test"):
            self.create_button(role)


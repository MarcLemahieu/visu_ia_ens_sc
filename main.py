from __future__ import annotations
from typing import *

import tkinter as tk
from cadran import Cadran
from seven_segments import seven_seg
from time import sleep

# pondérations initiales
weights = [1, 2, 2, 1, 0, 0, -1]

# couleurs globales
background = "gray40"
dark = "gray48"
checked = "lawn green"
unchecked = "orange red"

# mode de l'appli
auto = False

class GestionIA:
    """
    implémente la recherche d'une pondération qui 
    permette de reconnaitre sans faute la parité des 
    10 chiffres à 7 segments.
    """
    def __init__(self):
        """
        @attributes :
            - digit_to_test donne le chiffre en cours de test
            - weights donne les pondération en cours de validation
            - validated indique combien de chiffres sont déjà 
               validés avec weight inchangé.
        """
        self.digit_to_test = 0
        self.weights = weights
        self.validated = 0

    def test(self):
        """
        vérifie la validation du chiffre en cours pour 
        les pondérations en cours
        """
        compute = sum([w for w, on in zip(self.weights, seven_seg(self.digit_to_test)) if on]) >= 1
        return (self.digit_to_test % 2 ==1) == compute

    def weight_up(self):
        """
        augmente les pondérations de 1 pour les segments 
        actifs du chiffre en cours
        """
        seg_to_increase = seven_seg(self.digit_to_test)
        self.weights = [w+1 if s else w for w, s in zip(self.weights, seg_to_increase)]

    def weight_down(self):
        """
        diminue les pondérations de 1 pour les segments 
        actifs du chiffre en cours.
        """
        seg_to_decrease = seven_seg(self.digit_to_test)
        self.weights = [w-1 if s else w for w, s in zip(self.weights, seg_to_decrease)]

    def cycle(self)->bool:
        """
        réalise un cycle de test et met à jour le nombre de 
        chiffres validé et potentiellement le chiffre à tester
        
        @return self.test()
        """
        t = self.test()
        if t:
            self.digit_to_test = (self.digit_to_test + 1)%10
            self.validated += 1
            self.validated = min(10, self.validated)
        else:
            self.validated = 0
        return t

    def __repr__(self):
        return f'en cours : {self.digit_to_test}\tvalidés: {self.validated}\npondérations : {self.weights}\n'


def w_resize(root:tk.Tk, cnv:Cadran, dim:tuple[int])->None:
    """change les dimensions de root avec dim= l, h
    on place la fenêtre en taille bloquée

    @arguments:
      - root fenêtre principale
      - dim dimensions voulue
    """
    l, h = str(dim[0]), str(dim[1])
    root.configure(width=l, height=h)
    root.wm_resizable(False, False)
    root.update_idletasks()
    cnv.configure(width=l, height=h)
    cnv.update_idletasks()
    for item in cnv.find_all():
        cnv.delete(item)
    cnv.remise_a_plat()

def update_cadran(cnv: Cadran, gestion: GestionIA)->None:
    """met à jour le cadran, le chiffre central et les pondérations
    à partir de gestion
    
    @arguments:
      - cnv: Cadran
      - gestion avec le valeurs auquelles aligner cnv
    """
    cnv.change_central_digit(gestion.digit_to_test, unchecked, dark)
    cnv.reset_cadran()
    for i in range(gestion.validated):
        nb = gestion.digit_to_test-1-i
        nb = nb+10 if nb<0 else nb
        cnv.bon_test(nb)
    cnv.change_central_weights(gestion.weights)

def resize(root: tk.Tk, cnv: Cadran, gestion: GestionIA, dim: tuple[int], auto: bool):
    """
    change la taille de la fenêtre et laisse à jour avec les valeurs 
    de gestion et de auto
    
    @arguments :
      - root fenêtre principale
      - cnv Cadran dans root mis au même dimension
      - gestion qui contient l'état d'avancement
      - dim pour la nouvelle taille de fenêtre
      - auto pour préciser le type de recherche : automatique ou manuelle
    """
    w_resize(root, cnv, dim)
    cnv.create_central_weights(gestion.weights)
    update_cadran(cnv, gestion)
    cnv.create_auto(auto)

def test_manuel(cnv: Cadran, gestion: GestionIA)->None:
    """
    test attaché au clic des item tagués "bouton_test"
    en cas de mode manuel
    """
    if gestion.cycle():
        update_cadran(cnv, gestion)

def test_auto(cnv: Cadran, gestion: GestionIA)->None:
    """
    test attaché au clic des item tagués "bouton_test"
    en cas de mode auto
    """
    while not gestion.validated == 10:
        if gestion.cycle():
            update_cadran(cnv, gestion)
        elif gestion.digit_to_test % 2:
            gestion.weight_up()
            update_cadran(cnv, gestion)
        else:
            gestion.weight_down()
            update_cadran(cnv, gestion)
        cnv.update_idletasks()
        sleep(0.2)

def test(cnv, gestion):
    """
    test attaché au clic des item tagués "bouton_test"
    pour les deux modes
    """
    global auto
    if auto:
        test_auto(cnv, gestion)
    else:
        test_manuel(cnv, gestion)


def increase(cnv: Cadran, gestion: GestionIA)->None:
    """
    fonction de commande attachée aux item tagués "bouton_up"
    """
    global auto
    if not auto:
        gestion.weight_up()
        cnv.change_central_weights(gestion.weights)

def decrease(cnv: Cadran, gestion: GestionIA)->None:
    """
    fonction de commande attachée aux item tagués "bouton_down"
    """
    global auto
    if not auto:
        gestion.weight_down()
        cnv.change_central_weights(gestion.weights)


def mode_auto(cnv):
    """
    commande attachée au menu auto
    """
    global auto
    if not auto:
        auto = True
        cnv.change_auto()

def mode_manuel(cnv):
    """
    commande attachée au menu manuel
    """
    global auto
    if auto:
        auto = False
        cnv.change_auto()

gestion = GestionIA()


root = tk.Tk()
root.wm_title("Enseignement Scientifique initiation IA")
icon = tk.PhotoImage(file="brain.png")
root.iconphoto(True, icon)
menubar = tk.Menu(root)
sizemenu = tk.Menu(menubar, tearoff=0)
sizemenu.add_command(label="400x300", command=lambda:resize(root, cnv, gestion, (400,300),auto))
sizemenu.add_command(label="800x600", command=lambda:resize(root, cnv, gestion, (800,600), auto))
sizemenu.add_separator()
menubar.add_cascade(label='Taille', menu=sizemenu)

modemenu = tk.Menu(menubar, tearoff=0)
modemenu.add_command(label="Auto", command=lambda:mode_auto(cnv))
modemenu.add_command(label="Manuel", command=lambda:mode_manuel(cnv))
modemenu.add_separator()
menubar.add_cascade(label="Mode", menu=modemenu)

root.config(menu=menubar)

cnv = Cadran(root)
cnv.configure(bg='gray40', height="600", width='800')
cnv.pack(fill='both', expand = True)
cnv.trace_cadran()
cnv.create_central_digit()
cnv.change_central_digit(0, unchecked, dark)
cnv.create_central_weights([1,2,2,1,0,0,-1])
for role in ("up", "down", "test"):
    cnv.create_button(role)
cnv.create_auto(auto)

cnv.tag_bind("bouton_test","<Button-1>", lambda e: test(cnv, gestion))
cnv.tag_bind("bouton_up","<Button-1>", lambda e: increase(cnv, gestion))
cnv.tag_bind("bouton_down","<Button-1>", lambda e: decrease(cnv, gestion))

root.mainloop()

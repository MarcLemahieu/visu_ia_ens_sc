from __future__ import annotations

# premier fichier du code qui permet de coder 
# l'état des 7 segments selon la notation binaire sur 4 bits 
# des chiffres (on se servira des chiffres de 0 à 9 uniquement)
# les septs segments sont représentés comme illustré plus bas
# 
#    ____
#   | a  |
#  f|___ |b
#   | g  |
#  e|___ |c
#     d
#
# Pour la documentation à la base de cette section voir :
# https://fr.wikipedia.org/wiki/Affichage_à_sept_segments


from typing import List

def construit_entree(chiffre: int)->List[bool]:
    """renvoie les valeurs des quatres bits little endian
    de chiffre si chiffre est un int entre 0 et 9
    
    @argument: 
      chiffre: int compris entre 0 et 9
    
    @return:
      liste de quatre bool qui forment la valeur binaire du chiffre
      le premier bit est le bit de poids fort
    """
    if (not isinstance(chiffre, int)) or (not (chiffre>=0 and chiffre<= 9)):
        raise ValueError("l'argument n'est pas valable")
    b = [bool(int(car)) for car in bin(chiffre)[2:].rjust(4,'0')]
    return b

def etat_a(chiffre:int)->bool:
    """renvoie l'état du segment A pour le int chiffre si 
    celui-ci est int entre 0 et 9 False sinon

    @argument:
      chiffre; int compris entre 0 et9

    @return :
      bool True si le segment est allumé False sinon
    """
    try:
        i1, i2, i3, i4 = construit_entree(chiffre)
        final = (not i1)and i3
        final = final or (i1 and (not i4))
        final = final or (i2 and i3)
        final = final or not(i2 or i4)
        final = final or (i1 and (not i2) and (not i3))
        final = final or ((not i1) and i2 and i4)
    except ValueError:
        final = False
    finally:
        return final

def etat_b(chiffre:int)->bool:
    """renvoie l'état du segment B pour le int chiffre si 
    celui-ci est int entre 0 et 9 False sinon

    @argument:
      chiffre; int compris entre 0 et9

    @return :
      bool True si le segment est allumé False sinon
    """
    try:
        i1, i2, i3, i4 = construit_entree(chiffre)
        final = not (i1 or i2)
        final = final or not(i2 or i3)
        final = final or not(i2 or i4)
        final = final or ((not i1) and (i3 == i4))
        final = final or (i1 and (not i3) and i4)
    except ValueError:
        final = False
    finally:
        return final

def etat_c(chiffre:int)->bool:
    """renvoie l'état du segment B pour le int chiffre si 
    celui-ci est int entre 0 et 9 False sinon

    @argument:
      chiffre; int compris entre 0 et9

    @return :
      bool True si le segment est allumé False sinon
    """
    try:
        i1, i2, i3, i4 = construit_entree(chiffre)
        final = (i1 != i2)
        final = final or ((not i3)and i4)
        final = final or ((i3 == i4) and(not i2))
    except ValueError:
        final = False
    finally:
        return final

def etat_d(chiffre:int)->bool:
    """renvoie l'état du segment B pour le int chiffre si 
    celui-ci est int entre 0 et 9 False sinon

    @argument:
      chiffre; int compris entre 0 et9

    @return :
      bool True si le segment est allumé False sinon
    """
    try:
        i1, i2, i3, i4 = construit_entree(chiffre)
        final = i1 and (not i3) 
        final = final or (not(i1 or i2 or i4))
        final = final or (i2 and(i3 != i4))
        final = final or ((not i2)and i3 and i4)
    except ValueError:
        final = False
    finally:
        return final

def etat_e(chiffre:int)->bool:
    """renvoie l'état du segment B pour le int chiffre si 
    celui-ci est int entre 0 et 9 False sinon

    @argument:
      chiffre; int compris entre 0 et9

    @return :
      bool True si le segment est allumé False sinon
    """
    try:
        i1, i2, i3, i4 = construit_entree(chiffre)
        final = not(i2 or i4)
        final = final or (i3 and (not i4))
        final = final or (i1 and i2)
        final = final or (i1 and i3)
    except ValueError:
        final = False
    finally:
        return final

def etat_f(chiffre:int)->bool:
    """renvoie l'état du segment B pour le int chiffre si 
    celui-ci est int entre 0 et 9 False sinon

    @argument:
      chiffre; int compris entre 0 et9

    @return :
      bool True si le segment est allumé False sinon
    """
    try:
        i1, i2, i3, i4 = construit_entree(chiffre)
        final = i1 and (not i2) 
        final = final or (not(i3 or i4))
        final = final or ((not i3)and(i1 != i2))
        final = final or (i1 and i3)
        final = final or (i2 and (not i4))
    except ValueError:
        final = False
    finally:
        return final

def etat_g(chiffre:int)->bool:
    """renvoie l'état du segment B pour le int chiffre si 
    celui-ci est int entre 0 et 9 False sinon

    @argument:
      chiffre; int compris entre 0 et9

    @return :
      bool True si le segment est allumé False sinon
    """
    try:
        i1, i2, i3, i4 = construit_entree(chiffre)
        final = i3 and(i1 or (not i2) or (not i4))
        final = final or (i1 and i4)
        final = final or ((not i3) and (i1 != i2))
    except ValueError:
        final = False
    finally:
        return final

def seven_seg(chiffre : int)->list[bool]:
    """renvoie la liste des valeurs bool des 7 segments 
    du chiffre a compris entre 0 et 9 (inclus)
    @argument :
      chiffre: int compris entre 0 et 9

    @return :
      list[bool] allumage de chacun des sept segments pour
      le chiffre passé en argument
    """
    try:
        assert isinstance(chiffre,int) and chiffre >= 0 and chiffre < 10
        fcts = (etat_a, etat_b, etat_c, etat_d, etat_e, etat_f, etat_g)
        return [fct(chiffre) for fct in fcts]
    except AssertionError as e:
        if not isinstance(chiffre, int):
            print("l'argument doit être un int")
        else:
            print("l'argument doit être compris entre 0 et 9")

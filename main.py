
# ------------------------------------------ #
# IMPORT DES FONCTIONS EXTERNES              #
# ------------------------------------------ #

from train import train, estime
from UI import start as predict

print("\n\033[4;37mDoctissia - Intelligence artificielle par Sacha Herman, Mattéo Menou, Léo Jason Coulais\033[0m")

def menu():

    # ------------------------------------------ #
    # MENU PRINCIPAL                             #
    # ------------------------------------------ #

    menu = ""
    while menu!="train" and menu!="use" and menu!="time": menu = input("\n\033[1;32mQue voulez vous faire ?\n - Entrainer l'IA ? (train)\n - Utiliser l'IA ? (use)\n - Predire le temps d'entrainement de l'IA ? (time)\033[0m\n:")
    return menu

def train_s():

    # ------------------------------------------ #
    # ENTRAINER LE MODELE                        #
    # ------------------------------------------ #

    while True:
        epoques = input("\n\033[1;32mCombien d'epoques voulaient vous effectuer ?\033[0m\n:")
        if not epoques.isdigit(): continue
        if int(epoques) <= 0: continue
        break
    warning = ""
    while warning!="yes" and warning!="no": warning = input("\n\033[1;31mAttention ! Ce processus peut prendre beaucoup de temps ! Voulez vous continuer ? (yes/no)\n(Afin d'utiliser ce programme en arrière-plan, vous pouvez l'executer dans un docker)\n(Vous pouvez estimer ce temps via l'option \"time\" dans le menu, ce dernier depend du nombre d'époques specifié)\033[0m\n:")
    if warning=="no": return False
    train(epoques=int(epoques))

def time_s():

    # ------------------------------------------ #
    # ESTIMER LE TEMPS D'ENTRAINEMENT DU MODELE  #
    # ------------------------------------------ #

    while True:
        epoques = input("\n\033[1;32mSur combien d'epoques voulait vous estimer le temps ?\033[0m\n:")
        if not epoques.isdigit(): continue
        if int(epoques) <= 0: continue
        break
    estime(int(epoques))

def predict_s():

    # ------------------------------------------- #
    # UTILISER L'IA POUR PREDIRE L'ETAT DU POUMON #
    # ------------------------------------------- #

    warning = ""
    while warning!="yes" and warning!="no": warning = input("\n\033[1;31mAttention ! Cette option ouvre une interface graphique ! Voulez vous continuer ? (yes/no)\033[0m\n:")
    if warning=="no": return False
    predict()

while True:

    # ------------------------------------------ #
    # BOUCLE PRINCIPALE DU PROGRAMME             #
    # ------------------------------------------ #

    value = menu()
    if value == "train":
        if train_s() == False: continue
    elif value == "use":
        if predict_s() == False: continue
    elif value == "time":
        if time_s() == False: continue

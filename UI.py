#Importé la bibliothèque pour la GUI (pour plus d'informations, voir https://matto.glitch.me/mlib/ ou https://matto.glitch.me/mlib si le premier lien ne marche pas)
from math import floor
from mlib import *
from PIL import Image
from predict import predict
import concurrent.futures

def start():

    #Definir la taille de la fenêtre
    SIZE=(800, 450)

    #Fenêtre pygame
    window=display.set_mode(SIZE)
    #Fenêtre MLib
    app = MFenetre(window, "Doctissia", arrierePlanImage="src/background.png", arrierePlanImageAlignement="JC")
    #Widget principal pour l'analyse
    analyzer = MBordure((100, 130), (600, 260), app, arrierePlanCouleur=(255, 255, 255), bordureLargeur=3, bordureCouleur=(0, 0, 0, 255), bordureRayon=10)
    #Bouton pour analyser l'image
    analyzeImage = MBouton("Analyser l'image", (390, 60), (200, 40), analyzer, arrierePlanCouleur=(178,190,181), bordureLargeur=1, curseurSurvol=pygame.SYSTEM_CURSOR_NO, policeTaille=20, texteAlignement="CC")
    #Bouton pour changer l'image
    changeImage = MBouton("Changer d'image", (390, 10), (200, 40), analyzer, arrierePlanCouleur=(178,190,181), bordureLargeur=1, policeTaille=20, texteAlignement="CC")
    #Crédits
    credits = MTexte("UI et mlib par Mattéo Menou, IA par Léo Jason Coulais et Sacha Herman", (10, 420), (800, 30), app, texteAlignement="CC")
    #Image
    image = MImage("", (70, 10), (240, 240), analyzer, bordureLargeur=2, bordureCouleur=(0, 0, 0, 255), imageAlignement="FC")
    #Titre principal
    mainTitle = MTexte("Doctissia", (200, 15), (400, 100), app, arrierePlanCouleur=(255, 255, 255, 100), bordureCouleur=(0, 0, 0, 255), bordureLargeur=3, bordureRayon=15, policeTaille=50, policeType="Assets/bobacups.ttf", texteAlignement="CC")
    #Texte à afficher si aucune image apportée
    noImage = MTexte("Choisissez une image", (10, 95), (230, 50), image, policeTaille=20, texteAlignement="CC")
    #Résultat de prédiction widget + titre
    result = MTexte("Résultat", (390, 110), (200, 140), analyzer, bordureLargeur=2, bordureCouleur=(0, 0, 0, 255), policeTaille=22, texteAlignement="CH")
    #Texte du résultat de prédiction
    resultText = MTexte("Analysez une image", (5, 40), (190, 90), result, policeTaille=16, texteAlignement="GH")

    #Chemin d'accés de l'image
    imageLink = ""

    while True:
        #Faire les évènements nécessaires pour la GUI
        app.frame()

        #Quand le bouton d'analyse est cliqué
        if analyzeImage.get_click():
            #ISi l'image existe
            if imageLink != "" and fichierInfo(imageLink, "Image")["Existe"]:
                #Predire si l'image est saine ou non
                resultText.set_texte("Analyse en cours...")
                app.frame()
                display.flip()
                pygame.event.clear()
                thread = concurrent.futures.ThreadPoolExecutor().submit(predict, Image.open(imageLink))
                chance = thread.result()
                resultText.set_texte("Chance d'être malade: " + str(int(round(chance))) + "%.")

        #Quand le bouton pour changer d'image est cliqué
        if changeImage.get_click():
            imageLink = openDialogFile("Image")

        #Changer certains éléments de la GUI selon l'image sélectionné
        if imageLink == "":
            noImage.set_visible(True)
            analyzeImage.set_curseurSurvol(pygame.SYSTEM_CURSOR_NO)
        else:
            noImage.set_visible(False)
            analyzeImage.set_curseurSurvol(pygame.SYSTEM_CURSOR_HAND)

        image.set_imageLien(imageLink)

        #Afficher la fenêtre
        display.flip()


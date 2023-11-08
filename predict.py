
# ------------------------------------------ #
# IMPORTATION DES LIBRAIRIES                 #
# ------------------------------------------ #

from keras import models
import numpy as np
from PIL import Image

def cropImage(image=Image):

    # ------------------------------------------ #
    # ROGNER L'IMAGE POUR NE PAS LA DEFORMER     #
    # ------------------------------------------ #

    width, height = image.size

    # Si l'image est plus large que haute, rogner sur les côtés
    # Si l'image est plus haute que large, rogner sur les pôles

    if width > height:
        X = int((width - height)/2)
        Y = int((width + height)/2)
        image = image.crop(( X , 0 , Y , height ))

    elif height > width:
        X = int((width - height)/2)
        Y = int((width + height)/2)
        image = image.crop(( 0 ,  X , width , Y ))

    # Retourner la nouvelle image

    return image

def convertImage(image=Image):

    # ------------------------------------------ #
    # ENLEVER LES CANAUX SUPERFLUS DE L'IMAGE    #
    # ------------------------------------------ #

    # Si l'image a un canal alpha, le supprimer
    # Si l'image a trois canaux (RGB), faire la moyenne des canaux pour n'en laisser qu'un un seul

    if image.mode == "RGBA":
        image.load() 

        newImage = Image.new("RGB", image.size, (255, 255, 255))
        newImage.paste(image, mask=image.split()[3])
        image = newImage

    if image.mode == "RGB":
        newImage = Image.new("L", image.size, 255)

        for i in range(image.width):
            for j in range(image.height):
                moyenne = sum(image.getpixel((i,j)))/3
                newImage.putpixel((i,j), int(moyenne))

        image = newImage

    # Retourner la nouvelle image

    return image

def predict(image=Image):

    # ------------------------------------------ #
    # PREDIRE L'ETAT DU POUMON                   #
    # ------------------------------------------ #

    print("\nChargement du modèle et de l'image...")

    # Charge le modèle, puis modifie l'image avant le traitement

    model = models.load_model("pneumonia.h5")

    image = cropImage(image)
    image = convertImage(image)
    image = np.array(image.resize((256,)*2))
    image = image.reshape((1,256,256,1))

    # Predit l'etat du poumon, et renvoie True si il est atteint d'une pneumonie. Sinon, retourne False

    print("Prediction de l'etat du poumon...")

    data = model.predict(image,verbose=0)[0][0]

    print("Prediction terminée !")

    return data*100

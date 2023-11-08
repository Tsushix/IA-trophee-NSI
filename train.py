
print("\nImportation des librairies...\n")

# ------------------------------------------ #
# IMPORTATION DES LIBRAIRIES                 #
# ------------------------------------------ #

from gc import collect
from tqdm import tqdm
from keras import models,layers,optimizers
import numpy as np
from os import listdir
from PIL import Image
from random import randint
from time import time

def selectImage(Healthy_I=0,Pneumonia_I=0):

    # ----------------------------------------------- #
    # SELECTIONNER LA PROCHAINE IMAGE POUR LE DATASET #
    # ----------------------------------------------- #

    # Mise en place des variables

    etat = ("NORMAL","PNEUMONIA")
    choice = randint(0,1)

    path = "src/train/"

    numberOfHealty = len(listdir(path+"NORMAL")) - (1 if ".DS_Store" in listdir(path+"NORMAL") else 0)
    numberOfPneumonia = len(listdir(path+"PNEUMONIA")) - (1 if ".DS_Store" in listdir(path+"PNEUMONIA") else 0)

    # Si toutes les images de poumons sains sont déjà utilisées, prendre une image de poumons malades
    # Si toutes les images de poumons malades sont déjà utilisées, prendre une image de poumons sains

    if Healthy_I==numberOfHealty-1: choice = 1
    elif Pneumonia_I==numberOfPneumonia-1: choice = 0

    # Selectionner une image dans la bonne catégorie

    images = listdir(path+etat[choice])
    if ".DS_Store" in images: images.remove(".DS_Store")
    image = Image.open(path+etat[choice]+"/"+images[(Pneumonia_I if choice == 1 else Healthy_I)])

    # Si l'image tirée est un poumon sain, incrementer le compteur d'images de poumons sains utilisées
    # Sinon, incrementer le compteur d'images de poumons malades utilisées

    if choice == 0: Healthy_I+=1
    else: Pneumonia_I+=1

    # Retourner l'image, la classe et les compteurs

    return image, choice, Healthy_I, Pneumonia_I

def cropImage(image=Image):

    # ------------------------------------------ #
    # ROGNER LES IMAGES POUR NE PAS LES DEFORMER #
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
    # ENLEVER LES CANAUX SUPERFLUS DES IMAGES    #
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

def importImage(Healthy_I=0,Pneumonia_I=0):

    # --------------------------------------------- #
    # EFFECTUER LES DERNIERS TRAITEMENTS DE L'IMAGE #
    # --------------------------------------------- #

    # Tirer une image, la rogner, supprimer les canaux en trop et la transformer en matrice

    image, classe,Healthy_I,Pneumonia_I = selectImage(Healthy_I,Pneumonia_I)
    image = cropImage(image)
    image = convertImage(image)
    image = np.array(image.resize((256,)*2))

    # Retourner l'image, la classe et les compteurs

    return image, classe,Healthy_I, Pneumonia_I

def generateDataset(number=0):

    # --------------------------------------------- #
    # GENERER LE DATASET D'ENTRAINEMENT             #
    # --------------------------------------------- #

    # Initialise les variables

    numberOfHealty = len(listdir("src/train/NORMAL")) - (1 if ".DS_Store" in listdir("src/train/NORMAL") else 0)
    numberOfPneumonia = len(listdir("src/train/PNEUMONIA")) - (1 if ".DS_Store" in listdir("src/train/PNEUMONIA") else 0)

    Healthy_I,Pneumonia_I=0,0

    # Ajoute une dimension aux images et aux classes, puis les ajoute aux matrices finales

    for i in tqdm(range(numberOfHealty+numberOfPneumonia-1 if number==0 else number)):
        image,classe,Healthy_I,Pneumonia_I=importImage(Healthy_I,Pneumonia_I)
        image = image.reshape((1,256,256))

        if i==0:
            images = np.array(image)
            classes = np.array(classe).reshape((1,1))
        else:
            images = np.concatenate((images,image))
            classes = np.concatenate(( np.array(classes), np.array(classe).reshape((1,1)) ))
        del image
        del classe

    # Supprime toutes les images et classes de la RAM, ces dernières étant sauvegardées dans d'autres matrices
    
    collect()

    # Retourne les images et les classes, en ajoutant une dimension pour le canal

    return images.reshape(images.shape+(1,)), classes.reshape(classes.shape+(1,))

def train(datas=0,epoques=500):

    # --------------------------------------------- #
    # ENTRAINER LE MODEL                            #
    # --------------------------------------------- #

    first = time()

    print("\nGénération du dataset...")

    images,classes = generateDataset(datas)

    second = time()

    print("\nConstruction du modèle...")

    # Construction du model et de ses différentes couches

    modal = models.Sequential()

    modal.add(layers.Conv2D(128, (3,3),padding="same",input_shape=(256,256,1),data_format="channels_last",activation="relu"))
    modal.add(layers.MaxPooling2D((2,2)))
    modal.add(layers.Conv2D(128, (3,3),padding="same", activation="relu"))
    modal.add(layers.MaxPooling2D((2,2)))
    modal.add(layers.Conv2D(256, (3,3),padding="same", activation="relu"))
    modal.add(layers.MaxPooling2D((2,2)))

    modal.add(layers.Dense(64, activation="relu"))
    modal.add(layers.Flatten())
    modal.add(layers.Dense(1, activation="sigmoid"))

    print("Entrainement du modèle...")

    # Compile et entraine le model

    modal.compile(loss="binary_crossentropy", optimizer=optimizers.SGD(learning_rate=0.0001, momentum=0.9), metrics=["accuracy"])
    modal.fit(x=images,y=classes,epochs=epoques,verbose=1)

    print("\nEnregistrement du modèle...")

    # Enregistre les paramètres du model

    modal.save("pneumonia.h5")

    print("\nSession d'entrainement terminée !")

    return second-first,time()-second

def estime(epoques):
    generate_time,train_time=train(100,1)
    print("\n\033[1;34mTemps de generation:",generate_time*52,"\nTemps d'entrainement:",train_time*41*epoques,"\033[0m")
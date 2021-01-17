# -*- coding: UTF-8 -*-

# On import la librairie random permettant de mélanger la liste de prénoms, 
# et de piocher au hasard le nombre de personnes par groupes
# La librairie JSON permet de reporter les groupes formés dans un fichier JSON
# La librairie logging permet la mise en place de log pour le script.

from json import encoder
from random import *
import json
import logging

# logging.basicConfig(filename='Log.txt', level=logging.DEBUG)

# créer un logger
logger = logging.getLogger('RandomGroup')
logger.setLevel(logging.DEBUG)

# créer un gestionnaire de console et niveau de réglage pour le débogage
ch = logging.StreamHandler()
ch = logging.FileHandler('Log.txt', encoding='utf-8')
ch.setLevel(logging.DEBUG)

# créer un format d'affichage
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

# ajoute le format au ch
ch.setFormatter(formatter)

# ajoute le ch au logger
logger.addHandler(ch)

# 'application' code
logger.info('************************************** Début du script *****************************************************************')

# Ce bloc de code permet avec l'input "fichier", de choisir le fichier contenant les noms,
# ouvrir le fichier, le lire, le mélanger, et retirer les \n présents à chaque ligne

fichier = input("Veuillez entre le nom (ou chemin d'accès) du fichier : ")
logger.info('Le fichier %s va être utilisé pour constituer des groupes au hasard', fichier)
lecture = open(fichier, 'r', encoding='utf-8')
lecture = lecture.readlines()
# shuffle(lecture)
nbpers = len(lecture)
lectures = []
for prenom in lecture:
    prenom_strip = prenom.strip()
    lectures.append(prenom_strip)

# Avec le input "nbpersmax" on définit le nombre max de personne par groupe,
# ensuite on défini le nombre de groupes et le nombre de personnes par groupe

nbpersmax = int(input("nb de personnes max par groupe: "))
logger.info('Il y aura maximum %s personnes dans chaque groupe', nbpersmax)
nbgroupe = nbpers//nbpersmax+1
nbpersgroupe = nbpers//nbgroupe

# On initialise une liste vide qui nous permettra de déterminer le nombre de membre par groupe,
# et de déterminer le nombre de personnes restantes.

nbmembresgroupe = []
persrestantes = nbpers%nbgroupe

# Dans cette boucle, s'il y a des personnes restantes, il créer un nouveau groupe et dispatche 
# les personnes restantes dans chaque groupe sans dépasser la taille max.
# extend permet de rajouter un element dans une liste

for i in range(nbgroupe):
    if persrestantes>0:
        nbmembresgroupe.extend([nbpersgroupe+1])
        persrestantes -= 1
    else:
        nbmembresgroupe.extend([nbpersgroupe])

logger.info(f'La consitution des groupes sera comme suit : {nbmembresgroupe}')

# print("Nombre de personnes par groupe: ", nbmembresgroupe)

# On créer une liste vide "groupe_final" qui accueillera chaque groupe en forme de liste
# Grâce à la répartition du nombre de membre par groupe, on va pouvoir piocher aléatoirement dans le fichier de prénoms 
# le nombre de personne correspondant aux nombres de membre par groupe. Ensuite on les ajoutes dans la liste groupe_final 
# qui sera reporté dans le fichier JSON. On pense a supprimer les noms piochés pour ensuite recommencer la manipulation 
# jusqu'à ce que tout les groupes soit remplis.
# Le i permet d'incrémenter un compteur pour afficher le numéro du groupe.

logger.info('VOici donc la constitution des groupes après tirage au sort des personnes dans la liste de noms')

groupe_final = []
i = 0
while 0 < nbpers:
    try:
        for e in nbmembresgroupe:
            groupe = sample(lectures, e)
            affgroupe = f"Groupe {i+1} : {groupe}"
            groupe_final.append(affgroupe)
            print(affgroupe)
            logger.info(affgroupe)
            i +=1
            for nom in groupe:
                lectures.remove(nom)
    except:
        break
    
    nbpers -= nbgroupe-1

# print(groupe_final)

# On écrit le résultat final "groupe_final" dans un fichier JSON (Groupes.json)

with open("Groupes.json", 'w', encoding='utf-8') as result:
    json.dump(groupe_final, result)

logger.info('************************************** Fin du script *****************************************************************')
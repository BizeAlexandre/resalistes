# resalistes
resalistes-0.1.py est un script écrit en Python 3 qui transforme un fichier csv contenant une liste de réservations issues d'un SIGB en plusieurs fichiers pdf. Ceux-ci permettent de préparer des commandes dans le cas d'une bibliothèque fonctionnant en mode "drive". Il est actuellement utilisé quotidiennement en production à la BM de Reims.

(c) Denis Paris - Bibliothèque municipale de Reims - 2020


Ce programme est destiné à convertir des exports csv de listes de documents réservés à la bibliothèque de Reims en provenance du SIGB Syracuse, pour produire des pdf contenant des listes de commandes. Il doit pouvoir être adapté à d'autres SIGB. Les fichiers pdf en exemple sont produits avec le script resalistes-0.1.py et le fichier minimum d'exemple a.csv. (Données anonymisées)
Pour le faire fonctionner dans une autre bibliothèque :

1ere étape : construire un profil d'export dans Syracuse qui reproduise exactement les colonnes du fichier a.csv. Il faut le configurer comme dans le fichier profil.png, et chosir le type csv.

2e étape : installer les librairies Python nécessaires : "idna","csv","time","operator","os","datetime","reportlab", avec pip, en console.
Ex : pip install operator 

3e étape : adapter le code
- ligne 18 : renseigner le nom du fichier csv source. Ici : a.csv. A enregistrer dans le même répertoire que le script resalistes-0.1.py

- lignes 32 à 36 : renseigner les paramètres de durée

  expiration=5 # temps de mise à disposition des documents une fois prêtés, en jours

  expirationtransit=8 # temps de mise à disposition des documents une fois prêtés, en jours, en cas de transit

  retour=21 # durée du prêt, en jours

  retourtransit=24 # durée du prêt, en jours, s'il y a eu transit

- lignes 55 à 66 : modifier le nom des bibliothèques du réseau

- lignes 205-206 : choisir l'encodage du fichier source en commentant/décommantant la ligne adéquate (pour un fichier issu de l'export Syracuse et passé par Excel, choisir ISO8859-1)

4e étape : ouvrir une console et lancer les commandes suivantes :
- cd c:\python38-32 (dossier où est installé Python)
- python.exe resalistes-0.1.py

Les fichiers pdf sont créés dans un sous dossier à la date du jour. Ex : C:\python38-32\2020-06-06, et sont nommés d'après les bibliothèques et le jour d'édition. Ex ici : falala-2020-06-06.pdf

Le script se prête assez facilement à la création d'un exécutable pour Windows avec la librairie Cx_Freeze pour une génération de pdf en un clic :
https://python.jpvweb.com/python/mesrecettespython/doku.php?id=cx_freeze : En console, on exécute le script setup.py fourni :
- installer cx_freeze : pip install cx_freeze
- construire l'exécutable : python.exe setup.py build

On récupère l'exécutable (un dossier, pas seulement un .exe) dans un sous-dossier du dossier "build" (ex : c:\python38-32\build). Attention : un exécutable produit sur une machine Windows 64 bits (typiquement les Windows 10 pro) ne fonctionnera pas nativement sous Windows 32 bits (versions plus anciennes de Windows).

NB : concernant la production du csv : il sera bientôt possible de récupérer les données directement sur le serveur solr, à condition d'avoir login/mdp, et d'automatiser l'ensemble du processus. Actuellement, il manque l'indexation de la bibliothèque de mise à disposition dans Solr pour les réservations "en rayon".

La bibliothèque municipale de Reims n'assurera pas de support sur l'utilisation de ce script, mais nous serions heureux d'avoir des retours de ceux à qui il aura pu être utile.

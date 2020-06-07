# resalistes
resalistes-0.1.py est un script écrit en Python 3 qui transforme un fichier csv contenant une liste de réservations issues d'un SIGB en plusieurs fichiers pdf : un par bibliothèque, une page par réservateire. Ceux-ci permettent de préparer des commandes dans le cas d'une bibliothèque fonctionnant en mode "drive". Il est actuellement utilisé quotidiennement en production à la BM de Reims.

(c) Denis Paris - Bibliothèque municipale de Reims - 2020


Ce programme est destiné à convertir des exports csv de listes de documents réservés à la bibliothèque de Reims en provenance du SIGB Syracuse, pour produire des pdf contenant des listes de commandes. Il doit pouvoir être adapté à d'autres SIGB. Les fichiers pdf en exemple sont produits avec le script resalistes-0.1.py et le fichier minimum d'exemple a.csv. (Données anonymisées)
Pour le faire fonctionner dans une autre bibliothèque :

1ere étape : construire un profil d'export dans Syracuse qui reproduise exactement les colonnes du fichier a.csv. Il faut le configurer comme dans le fichier profil.png, et chosir le type csv.

Attention : Syracuse produit un fichier csv (en fait un txt) avec le caractère "|" comme séparateur, pas reconnu par défaut par Windows. Pour produire un .csv exploitable, il faut donc : ouvrir Excel,ouvrir le fichier sorti de Syracuse, sélectionner la première colonne, puis faire données>convertir>délimité, et mettre "|" comme séparateur. L'enregistrer sous a.csv (format csv, séparateur ;). A faire à chaque édition de liste.

2e étape : installer les librairies Python nécessaires : "idna","csv","time","operator","os","datetime","reportlab", avec pip. En console, exécuter la commande :
<br><code>pip install idna csv time operator os datetime reportlab</code>

3e étape : adapter le code :  Enregistrer le fichier resalistes-0.1.py dans le dossier où Python est installé, puis l'ouvrir avec un éditeur de texte et :
- ligne 18 : renseigner le nom du fichier csv source. Ici : a.csv. A enregistrer dans le même répertoire que le script resalistes-0.1.py

- lignes 29 à 33 : renseigner les paramètres de durée

  <code> expiration=5 </code> # temps de mise à disposition des documents une fois prêtés, en jours

 <code> expirationtransit=8 </code> # temps de mise à disposition des documents une fois prêtés, en jours, en cas de transit

  <code> retour=21 </code> # durée du prêt, en jours

  <code> retourtransit=24 </code> # durée du prêt, en jours, s'il y a eu transit

- lignes 51 à 60 : modifier le nom des bibliothèques du réseau : bien mettre les libellés exacts et leur attribuer un code (sans espace)

- lignes 68-69 : choisir l'encodage du fichier source en commentant/décommantant la ligne adéquate (pour un fichier issu de l'export Syracuse et passé par Excel, choisir ISO8859-1)

4e étape : ouvrir une console et lancer les commandes suivantes :
<code> cd c:\python38-32 </code> (dossier où est installé Python)
<code> python.exe resalistes-0.1.py </code>

Les fichiers pdf sont créés dans un sous dossier à la date du jour. Ex : C:\python38-32\2020-06-06, et sont nommés d'après les bibliothèques et le jour d'édition. Ex ici : falala-2020-06-06.pdf

Le script se prête assez facilement à la création d'un exécutable pour Windows avec la librairie Cx_Freeze pour une génération de pdf en un clic :
https://python.jpvweb.com/python/mesrecettespython/doku.php?id=cx_freeze : En console, on exécute le script setup.py fourni :
- installer cx_freeze : <code> pip install cx_freeze </code>
- construire l'exécutable : <code> python.exe setup.py build </code>

On récupère l'exécutable (un dossier, pas seulement un .exe) dans un sous-dossier du dossier "build" (ex : c:\python38-32\build). Attention : un exécutable produit sur une machine Windows 64 bits (typiquement les Windows 10 pro) ne fonctionnera pas nativement sous Windows 32 bits (versions plus anciennes de Windows).

NB : concernant la production du csv : il sera bientôt possible de récupérer les données directement sur le serveur solr, à condition d'avoir login/mdp et d'automatiser l'ensemble du processus. Actuellement, il manque l'indexation de la bibliothèque de mise à disposition dans Solr pour les réservations "en rayon". Ce cas est traité dans : https://github.com/olivierhirsch/resalistes/tree/gh-pages-solr (avec du code commenté davantage).

La bibliothèque municipale de Reims n'assurera pas de support sur l'utilisation de ce script, mais nous serions heureux d'avoir des retours de ceux à qui il aura pu être utile.

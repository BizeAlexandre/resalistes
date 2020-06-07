# resalistes
resalistes-0.1.py est un script écrit en Python 3.8 qui transforme un fichier csv contenant une liste de réservations issues d'un SIGB en plusieurs fichiers pdf : un par bibliothèque, une page par réservataire. Ceux-ci permettent de préparer des commandes dans le cas d'une bibliothèque fonctionnant en mode "drive". Il est actuellement utilisé quotidiennement en production à la BM de Reims, avec le SIGB Syracuse.

Les fichiers pdf en exemple sont produits avec le script resalistes-0.1.py et le fichier minimum d'exemple a.csv. (Données anonymisées). Voici comment l'adapter pour une autre bibliothèque.

©2020 Denis Paris, Olivier Hirsch - Bibliothèque municipale de Reims

<h2>mode d'emploi (Windows)</h2>

<h4>configurer Syracuse et Excel</h4>
Construire un profil d'export dans Syracuse qui reproduise exactement les colonnes du fichier a.csv fourni sur cette page. Il faut le configurer comme dans le fichier profil.png (idem). Chosir le type csv et pour les variables soumises à référentiel, choisir "libellé" plutôt que "code".
<br><br>
Attention : Syracuse produit un fichier csv (en fait un txt) avec le caractère "|" comme séparateur, pas reconnu par défaut par Windows. Pour produire un .csv exploitable, il faut donc : ouvrir Excel,ouvrir le fichier sorti de Syracuse, sélectionner la première colonne, puis faire données>convertir>délimité, et mettre "|" comme séparateur. L'enregistrer sous "a.csv" (format csv, séparateur point-virgule) dans le dossier Python. A faire à chaque édition de liste ; une méthode alternative est indiquée plus bas.
<br><br>
Désactiver aussi la notation scientifique dans Excel, pour les colonnes contenant des codes-barres : sélectionner la colonne>format de cellule>personnalisé>standard

<h4>installer et préparer Python</h4>

- Télécharger Python 3.8 ici : https://www.python.org/downloads/

- L'installer dans un dossier accessible. Ex: C:\python38-32. Cela nécessite d'avoir les droits administrateur du poste.

- Installer les librairies nécessaires : "idna","csv","time","operator","os","datetime","reportlab", avec pip. En console (lancer cmd.exe), exécuter la commande :
<br><br><code>pip install idna csv time operator os datetime reportlab</code><br><br>

<h4>adapter le code</h4>Enregistrer le fichier resalistes-0.1.py dans le dossier où Python est installé, puis l'ouvrir avec un éditeur de texte et :

- ligne 18 : renseigner le nom du fichier csv source. Ici : a.csv. A enregistrer dans le même répertoire que le script resalistes-0.1.py

- lignes 29 à 33 : renseigner les paramètres de durée

  <code> expiration=5 </code> # temps de mise à disposition des documents une fois prêtés, en jours

 <code> expirationtransit=8 </code> # temps de mise à disposition des documents une fois prêtés, en jours, en cas de transit

  <code> retour=21 </code> # durée du prêt, en jours

  <code> retourtransit=24 </code> # durée du prêt, en jours, s'il y a eu transit

- lignes 51 à 60 : modifier le nom des bibliothèques du réseau : bien mettre les libellés exacts et leur attribuer un code (sans espace)

- lignes 68-69 : Pas de modification à faire en principe. Elles permettent de choisir l'encodage du fichier source en commentant/décommantant la ligne adéquate. Pour un fichier issu de l'export Syracuse et passé par Excel, choisir ISO8859-1.
Choisir UTF8 si on ne passe pas par Excel, et à condition d'avoir modifié dans Windows le paramètre séparateur de liste pour mettre | :
https://support.office.com/fr-fr/article/changer-le-caract%c3%a8re-utilis%c3%a9-pour-s%c3%a9parer-des-milliers-ou-des-d%c3%a9cimales-c093b545-71cb-4903-b205-aebb9837bd1e?ui=fr-FR&rs=fr-FR&ad=FR

<h4> exécuter le code</h4>Ouvrir une console et lancer les commandes suivantes :<br><br>
<code> cd c:\python38-32 </code> (dossier où est installé Python)<br>
<code> python.exe resalistes-0.1.py </code><br><br>

Les fichiers pdf sont créés dans un sous dossier à la date du jour. Ex : C:\python38-32\2020-06-06, et sont nommés d'après les bibliothèques et le jour d'édition. Ici : falala-2020-06-06.pdf. Les codes-barres sont en code128, penser à reconfigurer les douchettes si elles ne lisent que le code39.

<h4>optionnel : créer un exécutable pour Windows</h4>
Le script se prête assez facilement à la création d'un exécutable pour Windows avec la librairie Cx_Freeze pour générer les pdf en un clic :
https://python.jpvweb.com/python/mesrecettespython/doku.php?id=cx_freeze : En console, on exécute le script setup.py fourni :<br>

- installer cx_freeze : <br><code> pip install cx_freeze sys </code>

- construire l'exécutable : <br><code> python.exe setup.py build </code><br><br>

On récupère l'exécutable (un dossier, pas seulement un .exe) dans un sous-dossier du dossier "build" (ex : c:\python38-32\build). Cet exécutable et son dossier peuvent être copiés sur un serveur commun et mis à la disposition de tous pour déléguer l'édition de listes.

<h4>Note sur la production du fichier csv source</h4>Pour automatiser l'ensemble du processus et se passer de l'export manuel depuis Syracuse, il est possible de récupérer les données directement sur le serveur solr. Il faut disposer pour cela d'un compte (login/mdp) sur ce serveur. Le script permettant de faire cela est disponible ici, avec un code davantage commenté :<br>
https://github.com/olivierhirsch/resalistes/tree/gh-pages-solr
<br><br>
Actuellement, pour que cela fonctionne en production, il manque une donnée dans Solr : la bibliothèque de mise à disposition pour les réservations "en rayon" n'est pas indéxée. L'indexation de la donnée manquante devrait intervenir dans les jours à venir, au moins à la BM de Reims.

<h4>avertissement</h4>
La bibliothèque municipale de Reims n'assurera pas de support sur l'utilisation de ce script. Mais nous serions heureux d'avoir des retours de ceux à qui il aura pu être utile.

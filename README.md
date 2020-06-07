# resalistes-solr
resalistes-0.1-solr.py est un script écrit en Python 3 qui transforme un fichier csv contenant une liste de réservations issues d'un SIGB en plusieurs fichiers pdf : un par bibliothèque, une page par réservataire. Ceux-ci permettent de préparer des commandes dans le cas d'une bibliothèque fonctionnant en mode "drive". Cette version constitue une version un peu plus ambitieuse du projet décrit ici : https://github.com/olivierhirsch/resalistes/tree/gh-pages

Le fichier csv source est ici produit non plus depuis un export manuel depuis le SIGB, mais en allant chercher directement les données sur le serveur solr de Syracuse. Il nécessite d'avoir un accès (login/mdp) à ce serveur. La requête recherche l'ensemble des exemplaires réservés dont la date de réservation est postérieure à J-5 et à l'état d'exemplaire "en rayon".

Les fichiers produits pdf ont le même aspect que dans la version "de base" disponible ici : https://github.com/olivierhirsch/resalistes/tree/gh-pages. Le code est mieux commenté ici que dans la version précédente.

(c) Denis Paris - Bibliothèque municipale de Reims - 2020

 Pour le faire fonctionner ailleurs qu'à la BM de Reims, il faut :

<h4>préparer Python</h4> Installer les librairies Python nécessaires : "idna","csv","time","operator","os","datetime","reportlab", "requests", "re" avec pip. "Requests" et "re" sont rajoutés par rapport à la version "de base". En console, exécuter la commande :
<br><code>pip install idna csv time operator os datetime reportlab requests re</code>

<h4>adapter le code</h4> Enregistrer le fichier solar_025.py dans le dossier où Python est installé, puis l'ouvrir avec un éditeur de texte et :
- ligne 16 : dans l'url, remplacer 
<br><code> url='http://srvpw-medindx:8985 </code><br> par l'adresse et le port du serveur solr de votre installation Syracuse. Dans l'URL, laisser la fin : il s'agit de la requête qui va chercher les données.

- ligne 17 : remplacer xxxx et yyyy respectivement par les login et mot de passe pour l'accès au serveur solr

3e étape : adapter le code de resalistes-0.1-solr.py. Enregistrer le fichier dans le dossier où Python est installé puis l'éditer, et :
- ligne 16 : renseigner le nom du fichier csv source. Ici : solar_025.csv

- lignes 29 à 33 : renseigner les paramètres de durée

 <code> expiration=5 </code> # temps de mise à disposition des documents une fois prêtés, en jours

  <code> expirationtransit=8 </code># temps de mise à disposition des documents une fois prêtés, en jours, en cas de transit

  <code> retour=21 </code> # durée du prêt, en jours

  <code> retourtransit=24 </code> # durée du prêt, en jours, s'il y a eu transit

- lignes 51 à 60 : modifier le nom des bibliothèques du réseau : bien mettre les libellés exacts et leur attribuer un code (sans espace)

<h4>exécuter le code</h4> Ouvrir une console et lancer les commandes suivantes :

<code> cd c:\python38-32 </code> (dossier où est installé Python)

<code> python.exe solr_025.py </code>

<code> python.exe resalistes-0.1-solr.py </code>

Les fichiers pdf sont créés dans un sous dossier à la date du jour. Ex : C:\python38-32\2020-06-06, et sont nommés d'après les bibliothèques et le jour d'édition. Ex ici : falala-2020-06-06.pdf

<h4>optionnel : automatiser complètement la production des listes</h4> Si on dispose d'une machine pouvant faire office de serveur Windows (une machine de bureau jamais éteinte et loggée sur une session disposant des accès serveur nécéssaires suffit), il est possible d'écrire le fichier batch suivant, nommé auto.bat, pour automatiser la production de listes :
<br>
<code>
<div> cd c:\python38-32 </div>
<div> set $madate=%date:~-4%-%date:~3,2%-%date:~0,2%  </div>
<div> python.exe solr_025.py </div>
<div> python.exe resalistes-0.1-solr.py </div>
<div> xcopy C:\Python38-32\%$madate% T:\deconfinement\drive\listes\%$madate% /E /C /R /H /I /K </div>
</code>

Où T:\deconfinement\drive\listes est le serveur commun où les fichiers seront lus et imprimés par les bibliothécaires. On peut programmer l'exécution quotidienne de ce batch avec le planificateur des tâches Windows. Configuré ainsi, les fichiers apparaissent tous les jours sans intervention humaine au bon endroit.

On peut aussi en faire un exécutable pour une utilisation à la demande en un clic. Voir la méthode à la fin de la page :
https://github.com/olivierhirsch/resalistes/blob/gh-pages/README.md

<h4>Note importante du 06/06/2020</h4> Cette version solr ne peut pas encore être mise en production. En effet, la donnée de bibliothèque de mise à disposition n'est pas indexée dans solr quand la réservation est "en rayon". Cela rend cette version pour le moment inutilisable en pratique. Mais l'éditeur de Syracuse a promis une correction très rapide de ce point, au moins à la BM de Reims.

<h4>avertissement</h4>
La bibliothèque municipale de Reims n'assurera pas de support sur l'utilisation de ce script, mais nous serions heureux d'avoir des retours de ceux à qui il aura pu être utile.

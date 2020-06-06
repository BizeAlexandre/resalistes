# resalistes
resalistes-0.1-solr.py est un script écrit en Python 3 qui transforme un fichier csv contenant une liste de réservations issues d'un SIGB en plusieurs fichiers pdf. Ceux-ci permettent de préparer des commandes dans le cas d'une bibliothèque fonctionnant en mode "drive". Cette version constitue une version un peu plus ambitieuse du projet décrit ici : https://github.com/olivierhirsch/resalistes/tree/gh-pages

Le fichier csv source est ici produit en allant chercher directement les données sur le serveur solr de Syracuse. Il nécessite d'avoir un accès (login/mdp) à ce serveur.

(c) Denis Paris - Bibliothèque municipale de Reims - 2020


Ce programme est destiné à convertir des exports csv de listes de documents réservés à la bibliothèque de Reims en provenance du SIGB Syracuse, pour produire des pdf contenant des listes de commandes. Il doit pouvoir être adapté à d'autres SIGB. Les fichiers pdf en exemple sont produits avec le script resalistes-0.1-solr.py et le fichier minimum d'exemple solr502.csv. (Données anonymisées)
Pour le faire fonctionner dans une autre bibliothèque :

1ère étape : installer les librairies Python nécessaires : "idna","csv","time","operator","os","datetime","reportlab", "requests", "re" avec pip, en console.
Ex : <code> pip install operator </code>

2e étape : adapter le code de solar_025.py :
- ligne 16 : dans l'url, remplacer 
<code> url='http://srvpw-medindx:8985 </code> par l'adresse et le port du serveur solr
- ligne 17 : remplacer xxxx et yyyy respectivement par les login et mot de passe du serveur

3e étape : adapter le code de resalistes-0.1-solr.py
- ligne 16 : renseigner le nom du fichier csv source. Ici : solar_025.csv. A enregistrer dans le même répertoire que le script resalistes-0.1-solr.py

- lignes 29 à 33 : renseigner les paramètres de durée

 <code> expiration=5 </code> # temps de mise à disposition des documents une fois prêtés, en jours

  <code> expirationtransit=8 </code># temps de mise à disposition des documents une fois prêtés, en jours, en cas de transit

  <code> retour=21 </code> # durée du prêt, en jours

  <code> retourtransit=24 </code> # durée du prêt, en jours, s'il y a eu transit

- lignes 51 à 60 : modifier le nom des bibliothèques du réseau : bien mettre les libellés exacts et leur attribuer un code (sans espace)

- lignes 176-177 : choisir l'encodage du fichier source en commentant/décommantant la ligne adéquate (pour un fichier issu de directement de Solr, choisir UTF8)

4e étape : ouvrir une console et lancer les commandes suivantes :
<code> cd c:\python38-32 </code> (dossier où est installé Python)
<code> python.exe solr_025.py </code>
<code> python.exe resalistes-0.1-solr.py </code>

Les fichiers pdf sont créés dans un sous dossier à la date du jour. Ex : C:\python38-32\2020-06-06, et sont nommés d'après les bibliothèques et le jour d'édition. Ex ici : falala-2020-06-06.pdf

Pour automatiser complètement la production des listes, et si on dispose d'une machine pouvant faire office de serveur Windows, il est possible d'écrire le fichier batch suivant :

<code>
<div> cd c:\python38-32 </div>
<div>set $madate=%date:~-4%-%date:~3,2%-%date:~0,2%  </div>
<div>python.exe solr_025.py </div>
<div>python.exe resalistes-0.1-solr.py </div>
<div>xcopy C:\Python38-32\%$madate% T:\deconfinement\drive\listes\%$madate% /E /C /R /H /I /K </div>
</code>

Où T:\deconfinement... est le serveur commun où les fichiers seront lus et imprimés par les bibliothécaires. On peut programmer l'exécution quotidienne de ce batch avec le planificateur des tâches Windows. COnfiguré ainsi, es fichiers apparaissent tous les jours sans intervention.

Note importante du 06/06/2020 : cette version solr ne peut pas encore être mise en production. En effet, la donnée de bibliothèque de mise à disposition n'est pas indexée dans Solr quand la réservation est "en rayon". Cela rend le produit pour le moment inutilisable en pratique. Mais l'éditeur de Syracuse a promis une correction très rapide de ce point, au moins à la BM de Reims.

La bibliothèque municipale de Reims n'assurera pas de support sur l'utilisation de ce script, mais nous serions heureux d'avoir des retours de ceux à qui il aura pu être utile.

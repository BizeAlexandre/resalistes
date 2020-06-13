# resalistes-solr
resalistes-0.1-solr.py est un script écrit en Python 3.8 qui transforme un fichier csv contenant une liste de réservations issues du SIGB Syracuse en plusieurs fichiers pdf : un par bibliothèque, une page par réservataire. Ceux-ci permettent de préparer des commandes dans le cas d'une bibliothèque fonctionnant en mode "drive". Cette version constitue une version un peu plus ambitieuse du projet décrit ici : https://github.com/olivierhirsch/resalistes/tree/gh-pages

Le fichier csv source n'est désormais plus produit par un export manuel depuis le SIGB. Il est généré automatiquement en allant chercher directement les données sur le serveur solr de Syracuse. C'est le fichier solr_025.py qui fait cela. Il faut donc disposer d'un accès (login/mdp) à ce serveur. La requête est stockée dans une URL : dans notre cas, on recherche l'ensemble des exemplaires réservés dont l'état d'exemplaire "en rayon".

Les fichiers pdf produits ont le même aspect que dans la version "de base" disponible ici : https://github.com/olivierhirsch/resalistes/tree/gh-pages. Le code est mieux commenté ici que dans la version précédente. Voici comment l'adapter pour une autre bibliothèque.

©2020 Denis Paris, Olivier Hirsch - Bibliothèque municipale de Reims 

<h2>mode d'emploi (Windows)</h2>

<h4>installer et préparer Python</h4>

- Télécharger Python 3.8 ici : https://www.python.org/downloads/

- L'installer dans un dossier accessible, par exemple à la racine de C. Ex: C:\python38-32. Cela nécessite d'avoir les droits administrateur du poste.

- Installer les librairies nécessaires : "idna","csv","time","operator","os","datetime","reportlab", "requests", "re" avec pip.  En console (lancer cmd.exe), exécuter la commande :
<br><br><code>pip install idna csv time operator os datetime reportlab requests re</code>

"requests" et "re" s'ajoutent par rapport à la version "de base".

<h4>adapter le code</h4><h5>adapter solar_025.py</h5> Enregistrer le fichier solar_025.py dans le dossier où Python est installé, puis l'ouvrir avec un éditeur de texte et :

- ligne 16 : dans l'url, remplacer 
<br><code> url='http://srvapw-medindx:8985 </code><br> par l'adresse et le port du serveur solr de votre installation Syracuse. Dans l'URL, laisser la fin : il s'agit de la requête qui va chercher les données.

- ligne 17 : remplacer xxxx et yyyy respectivement par les login et mot de passe pour l'accès au serveur solr.

<h5>adapter resalistes-0.1-solr.py</h5> Enregistrer le fichier resalistes-0.1-solr.py dans le dossier où Python est installé puis l'éditer et :

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

Les fichiers pdf sont créés dans un sous dossier à la date du jour. Ex : C:\python38-32\2020-06-06, et sont nommés d'après les bibliothèques et le jour d'édition. Ex ici : falala-2020-06-06.pdf. Les codes-barres sont en code128, penser à reconfigurer les douchettes si elles ne lisent que le code39.

<h4>optionnel : automatiser complètement la production des listes</h4> Il faut disposer d'une machine pouvant faire office de serveur Windows. Une machine de bureau suffit : il faut qu'elle soit allumée en permanence et loggée sur une session disposant des accès aux serveurs nécéssaires ; il faut aussi y installer Python et les librairies. Il est possible alors d'écrire le fichier batch suivant, nommé auto.bat (fourni), pour automatiser la production de listes :
<br>
<code>
<div> cd c:\python38-32 </div>
<div> set $madate=%date:~-4%-%date:~3,2%-%date:~0,2%  </div>
<div> if exist solr502.csv ren solr502.csv solr502-%$madate%.csv</div>
<div> python.exe solr_025.py </div>
<div> python.exe resalistes-0.1-solr.py </div>
<div> xcopy C:\Python38-32\%$madate% T:\deconfinement\drive\listes\%$madate% /E /C /R /H /I /K </div>
<div>del solr502.csv /f /q</div>
</code>

Où T:\deconfinement\drive\listes est le serveur commun où les fichiers seront lus et imprimés par les bibliothécaires. On programme l'exécution quotidienne de ce batch avec le planificateur des tâches de Windows.(Pour planifier une tâche : https://www.supinfo.com/articles/single/4998-utiliser-planificateur-taches-windows-10). Configuré ainsi, les fichiers apparaissent tous les jours sans intervention humaine au bon endroit.

On peut aussi en faire un exécutable pour une utilisation à la demande en un clic. Voir la méthode ici :
https://github.com/olivierhirsch/resalistes/blob/gh-pages/README.md#optionnel--cr%C3%A9er-un-ex%C3%A9cutable-pour-windows

Editer setup.py et remplacer resalistes-0.1.py par resalistes-0.1-solr.py, puis par solar_025.py (deux exécutables ; il existe des méthodes pour n'en faire qu'un seul).

<h4>automatiser l'impression pour une bibliothèque</h4> Bien entendu, une fois la production des fichiers pdf entièrement automatisée, il est tentant d'envisager celle de l'impression. Le script print.bat (fourni) fait cela : il nécessite la préseance d'Adobe Reader sur le "serveur". Il envoie l'impression du fichier du jour de la médiathèque Falala sur l'imprimante par défaut, du mardi au samedi. Il faut le programmer pour une exécution tous les jours, la détermination du jour de la semaine est faite dans le code.

<h4>note du 12/06/2020</h4> Après le passage du patch de Syracuse le 11/06 indexant la donnée manquante, cette version est mise en production à la BM de Reims.

<h4>avertissement</h4>La bibliothèque municipale de Reims n'assurera pas de support sur l'utilisation de ces scripts. Mais nous serions heureux d'avoir des retours de ceux à qui il aura pu être utile.

Précision de la société Archimed : aucun support ne sera donné là dessus, en particulier aucun accès au serveur solr de la part du service client. Ne pas les appeler pour cela.

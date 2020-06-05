# resalistes
Transforme un fichier csv contenant une liste de réservations issues d'un SIGB en plusieurs fichiers pdf permettant de préparer des commandes dans le cas d'un fonctionnement d'une bibliothèque en drive. (c) Denis Paris - Bibliothèque municipale de Reims


Ce programme est destiné à convertir des exports csv de listes de documents réservés à la bibliothèque de Reims en provenance du SIGB Syracuse, pour produire des pdf contenant des listes de commandes. Il doit pouvoir être adapté à d'autres SIGB. Les fichiers pdf en exemple sont produits avec le script resalistes-0.1.py et le fichier minimum d'exemple a.csv. (Données anonymisées)

1ere étape : construire un filtre d'export dans Syracuse qui reproduise exactement les colonnes du fichier a.csv. Ils sont notés dans profil.png

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import time
from operator import itemgetter, attrgetter
import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak
from reportlab.graphics.barcode import code128
from reportlab.graphics.barcode import eanbc, qr, usps
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


# Lecture du fichier CSV d'entrée (extrait de la base SolR, via le fichier python solr05.py)
fichier =  'solr502.csv'

# détermination de la date du jour qui servira à déterminer les dates d'expiration et de retour
aujourdhui=datetime.date.today()
now=str(aujourdhui) # date du jour en notation anglaise ex:
won=now[8:10]+"/"+now[5:7]+"/"+now[0:4] # réécriture de la date en format à la francaise

# Création du dossier de sauvegarde s'il n'existe pas encore
if os.path.isdir(now)==0 :
    os.mkdir(now)
#duplique le fichier CSV dans C: ou T:
#os.system('copy '+fichier+' T:\deconfinement\drive\listes\\'+now+"\\"+fichier)
#os.system('copy '+fichier+' C:\deconfinement\drive\listes\\'+now+"\\"+fichier)

# nb de jours avant expiration + retour selon transit ou non...
expiration=5
expirationtransit=8
retour=21
retourtransit=24

# ... et détermination des dates d'expiration et retour selon transit (chaine de caractères qui sera affichée)
delai=datetime.timedelta(days=expiration)
dateexpiration=str(aujourdhui+delai)
dateexp=dateexpiration[8:10]+"/"+dateexpiration[5:7]+"/"+dateexpiration[0:4] # expiration sans transit

delai=datetime.timedelta(days=expirationtransit)
dateexpirationtransit=str(aujourdhui+delai)
dateexptransit=dateexpirationtransit[8:10]+"/"+dateexpirationtransit[5:7]+"/"+dateexpirationtransit[0:4] # expiration avec transit

delai=datetime.timedelta(days=retour)
dateretour=str(aujourdhui+delai)
dateretourlect=dateretour[8:10]+"/"+dateretour[5:7]+"/"+dateretour[0:4] # retour sans transit

delai=datetime.timedelta(days=retourtransit)
dateretourtransit=str(aujourdhui+delai)
dateretourlecttransit=dateretourtransit[8:10]+"/"+dateretourtransit[5:7]+"/"+dateretourtransit[0:4] # retour avec transit

# texte de substitution servant au nom de fichier généré et l'entete des feuilles des commandes imprimées
entete=""
succ={"Bibliothèque Carnegie":"carnegie",
    "Bibliothèque du Chemin-Vert":"cheminvert",
    "Médiathèque Croix-Rouge":"croixrouge",
    "Bibliothèque Holden":"holden",
    "Médiathèque Jean Falala":"falala",
    "Médiathèque Laon-Zola":"laonzola",
    "Bibliothèque Saint-Remi":"saintremi",
    "Bibliobus urbain":"bibliobus",
    "Centre de documentation de l'ESAD":"esad",
    "Conservatoire (CRR)":"conservatoire"}

# lecture du fichier
nbchamp=17 #nombre de champs dans le fichier
tableau=[]
id=0

# ================= définition numéros de champs de colonne ========================
#pour eviter les confusions de noms de vartiables, les variables de champs sont définies avec un C majuscules (CHAMP) en début de nom de variable

Csucc=0     #succursale d'appartenance de l'exemplaire
Csecteur=1  #secteur de l'exemplaire
Ccote=2     #cote du document
Cdate_res=3 #Date à laquelle le lecteur a réservé le/les documents
            # exemple : 2020-05-28T10:37:50Z  // a toiletter
Ctitre=4    #Titre du ducument
            # exemple : Max et Lili - 72 : Simon a deux maisons - : / Dominique de Saint-Mars . - Calligram; 2005
            # ce champ integre plusieurs informations dont titre, complément de titre, tomaison, editeur, année d'edition...
            # => a nettoyer et recrééer champ titreseul et titresup (voir plus loin)
Csupport=5  # type de support Livre cd, dvd...
Ccbex=6     #CB exemplaire => à dédoublonner éventuellement
CBIMD=7     #?
Cdest= 7    # ======== => numéro à définir  =================
            #Bibliothèque dans laquelle le document est demandé
Cetat=8     # Etat du doument. / NOTE : on pourrait s'assurer que le document est "En rayon", ce qui n'est pas vérifié ici, on s'appuie sur le filtre effectué en amont
CTRDE=9     #?
Clect=10    #Civilité/Nom/Prénom du lecteur
Ccblect=11  #Codebare du compte lecteur
Ccotesup=12     #Cote supplémentaire ? pas exploité ici ? voir la requete qui genere le CSV
CDISP=13    #?
CDRES=14    #?
Ctitreseul=15   #variable définie à partir de CTitre, pour isoler le titre seul de l'ensemble des informations contenues dans Ctitre
Ctitresup=16    #variable définie à partir de CTitre, pour le complément de titre de l'ensemble des informations contenues dans Ctitre
# ================= FIN DE définition numéros de champs de colonne ========================


# les chaines de caratères sont à nettyer, notamment les compléments de titres 
def nettoyage(txt):
    #Nettoie le corps de la chaine de caracteres
    txt=txt.replace(". -"," ")    
    txt=txt.replace("\\\'","\'")
    txt=txt.replace("\\\"","\"")
    txt=txt.replace("\""," ")
    txt=txt.replace(" ,",",")
    txt=txt.replace("/"," ")
    txt=txt.replace(": :",":")
    txt=txt.replace(", :",",")
    txt=txt.replace(", .",",")
    txt=txt.replace("', '",",")
    txt=txt.replace(".,",",")
    txt=txt.replace(",.",",")
    txt=txt.replace("    "," ")
    txt=txt.replace("   "," ")
    txt=txt.replace("  "," ")
    #liste des caracteres interdits en debut ou fin de chaine de caracteres
    interdit="\"': -,"

    i=1 #répète cette opération tant qu'il y a encore du nettoyage à effectuer sur la chaine de caractère
    while i==1:
        i=0
        #nettoie spécifiquement les premiers caractères de la chaine de caracteres
        if len(txt)>0:
            if txt[0] in interdit: # est ce que le caractere en position zéro est dans la liste des caracteres interdits
                txt=txt[1:]
                i=1
        #nettoie spécifiquement les derniers caractères de la chaine de caracteres        
        if len(txt)>0:
            if txt[-1] in interdit: # est ce que le caractere en derniere position est dans la liste des caracteres interdits
                txt=txt[0:-1]
                i=1
    return txt


# -------------------
# Les CB de l'exemplaires peuvent apparaitre sous 2 formes:
# 1ere forme : 1234565100
# 2eme forme : 01234565100, (') 1234565100
# on veut que ca ressorte de façon unique, on choisit la premiere forme comme format de sortie    
def dedoublonne(txt):
    p=txt.find(",")
    if p!=-1:
        txt=txt[p:]
    txt=nettoyage(txt)
    return txt    

#-------------------
# Titre du document
# exemple : Max et Lili - 72 : Simon a deux maisons - : / Dominique de Saint-Mars . - Calligram; 2005
# ce champ integre plusieurs informations dont titre, complément de titre, tomaison, editeur, année d'edition...
# => on renvoie titreseul et complément de titre
def complementtitre(txt):
    p=txt.find("/ ")    # On recherche le séparateur "/" pour supprimer ce qui est relatif à l'éditeur/edition
    if p==-1:           # si pas d'éditeur, c'est tout le Ctitre, et pas de complément de titre
        complement=""
        p=len(txt)
        titre=txt
    else:
        txt=txt[0:p]    #sinon, suppression mention éditeur/édition
        p=txt.find("- ")#on recherche le séparateur "- " qui sépare le titre du complément de titre
        titre=txt[0:p]
        complement=txt[p+2:]
    # on nettoie les chaines de caractères    
    titre=nettoyage(titre)
    complement=nettoyage(complement)
    
    return [titre, complement]

# ==============================================================================================================
# ================================= LECTURE DU FICHIER CSV =====================================================
# ==============================================================================================================

# Code à utiliser si le fichier lu est encodé en ISO-8859-1
# with open(fichier,encoding='ISO-8859-1', newline='') as csvfile:
with open(fichier,encoding='utf8', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='|', quotechar='"')

    # remplissage du tableau cell
    for row in spamreader:
        cell=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        for i in range(15):
            cell[i]=str(row[i])


        # --------------------------------------------------------------------------
        # on repasse sur les valeurs lues afin qu'elles soient directement exploitables dans la suite du programme
        #---------------------------------------------------------------------------
        
        # dédoublonne le Code barre exemplaire si necessaire
        # exemple: 04068695100, 4068695100  => 4068695100
        cell[Ccbex]=dedoublonne(cell[Ccbex])

        # on construit titreseul et titresup à partir de la variable Ctitre
        cell[Ctitreseul] , cell[Ctitresup] = complementtitre(cell[Ctitre])

        # remplace "Disque Compact" en "CD"
        if cell[Csupport]=="Disque compact":
            cell[Csupport]="CD"

        # nettoie la date au moment de la réservation par l'usager
        # on passe de "2020-05-28T16:03:07Z" à "2020-05-28 16:03"
        cell[Cdate_res]=cell[Cdate_res][0:10]+" "+cell[Cdate_res][11:16]

        #on ajoute la ligne cell[0] à cell[17] dans le tableau avant de passer à lecture de la ligne suivante (boucle)
        tableau.append(cell)



# ==============================================================================================================
# ================================= FIN DE LECTURE DU FICHIER CSV ==============================================
# ==============================================================================================================

     
# On elimine la premiere ligne du tableau qui contient uniquement le nom des champs
del tableau[0]


# ==============================================================================================================
# ================================= Constitution des fichiers de commandes par biblithèque ======================
# ==============================================================================================================

# On trie d'abord le tableau par succursale d'appartenance du document
# en effet les collègues ne recevront leur feuille de leur succursale dans la quelle se trouvent les documents "en rayon" à chercher
tabdoc=list(sorted(tableau, key=itemgetter(0)))




# --------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ ENVOIPDF ----------------------------------------------------
# On est dans la bibliothèque d'appartenance des doc, et on remplit au fur et a mesur les fichier de commande en PDF
# Les autres bibliothèque appelleront tour à tour cette procédure
# --------------------------------------------------------------------------------------------------------------

def envoipdf(cell): 
    donnee=""

    #le sous tableau "cell" contient toutes les données du tableau global d'une seule succursale
    # on le trie dans un premier temps d'abord selon le nom du lecteur, ensuite selon le secteur, et dasn le secteur, selon la cote du document
    # Ca permet de faire un fiche par lecteur (voire plus si la commande est longue), et d'optimiser la recherche des documents dans la succursale
    tab=list(sorted(cell, key=itemgetter(Clect,Csecteur,Ccote)))
    succursale=tab[0][0]
    dest=succ[succursale]

    # ------ gestion d'une exception : la bibliothèque Carnegie ---------------------
    # la bibliothèque Carnegie place un fantome à la place des documents prétés
    # nous imprimons ce fantome en bas de chaque page pdf générée pour cette bibliothèque uniquement
    # cette partie de feuille sera découpée lors de la préparation de commandes
    if succursale=="Bibliothèque Carnegie":
        carnegie=1  # si c'est carnegie, alors la variable carnegie vaut 1, sinon 0
    else:
        carnegie=0
    # ------ fin : gestion d'une exception : la bibliothèque Carnegie ---------------------
    # cette variable "carnegie" sera exploitée plus loin dans le programme

    
    # on prépare l'enregistrement du pdfdans le dossier "date du jour' suivi du nom de fichier correspondant à la "succursale+date.pdf"
    destination = canvas.Canvas(now+"/"+dest+"-"+now+".pdf") 

    # On affiche le nombre de réservations de documents dans la succursale courante
    nbligne=len(tab)
    print (succursale+" => "+str(nbligne)+" commandes")

    
    #Paramètres de mise en page du fichier PDF
    # A4 largeur Xmax= 595.28  et hauteur Ymax=841.89

# définition des valeurs de mises en page:
    hautdepage=810  # on commence à écrire à cette hauteur sur la page
    basdepage=10    # limite inférieure d'écriture de la page
    partiebasse=basdepage   # partie basse de la page qui monte graduellement en fonction des fantomes générés
                            # c'est une variable utilisée pour l'exception "Carnegie"
    y=hautdepage    # ordonnée mobile en fonction de la création courante du PDF
    x=20            # abscisse de la marge de gauche
    xmid=300        # abscisse des la marge gauche colonne de droite
    deltay=15       # écart entre chaque ligne d'écriture pour la commande (interligne)
    deltacarn=20    # interligne du fantome (voir exception "carnegie")

    #pour que la boucle tourne, il faut prendre en considération la premiere page, et le nom du  premier lecteur "lect"
    premierepage=1
    lect=""
    for ligne in tab:
        transit=0   # initialisation de la variable "transit" = 1 si le document doit etre mis à disposition dans une autre succursale

        # Regle de mise en page:
        # si le réservataire de la commande est le meme que celui de la commande précédente,
        # alors on continue à écrire la page courante (sauf éventuellement si la page est pleine)
        # sinon, on crée une nouvelle page et on commence à écrire en haut de page
        
        if lect!=ligne[Clect]: # si lecteur différent du lecteur précédent
            partiebasse=basdepage   # on place le curseur du fantome en bas de page (voir exception Carnegie

            if premierepage==1: # condition sur la première page pour éviter une premiere page blanche
                premierepage=0
            else:
                # voir syntaxe sur
                # https://stackoverflow.com/questions/3593193/add-page-break-to-reportlab-canvas-object
                # PageBreak.drawOn(destination, 0, 1000, 0) ne semble pas fonctionner
                destination.pageNumer=2
                destination.showPage() # On crée une nouvelle page car nouveau lecteur
                y=hautdepage    # on positionne le curseur courant "y" en haut de page
                
            # Sur le haut de page on indique le nom de la bibliothèque d'appartenance du document, suivi du code barre du compte lecteur
            txt=dest+" "+ligne[Ccblect]
            destination.setFont("Helvetica", 10)    # police (attention : offre limitée de polices) + taille de police        
            destination.drawString(x,y,txt)         # coordonnées x,y du texte "txt" à écrire
            
            lect=ligne[Clect]   # lecteur courant : la variable "lect" reste inchangée
            lecteur=lect        # tandis qu'on va retoucher à la variable "lecteur" pour affichage (suppression civilité, et raccourci si trop long)
            
            if lecteur[0:3]=="M. ":
                lecteur=lecteur[3:]
            elif lecteur[0:4]=="Mme ":
                lecteur=lecteur[4:]
            if len(lecteur)>33:     # Nom de lecteur trop long (rique d'empieter sur le code barres)
                lecteur=lecteur[0:29]+"..."

            y -= int(1.5*deltay)    # on repositionne le curseur 1.5 fois d'interligne plus bas
            destination.setFont("Helvetica", 18)
            destination.drawString(x,y,lecteur) # on affice le nom simplifié du lecteur
            y-=deltay

            # on affiche le code barres du lecteur en code barre128 (syntaxe différente de celle du texte)
            y+=10       # le positionnement du CB se gène différemment du texte, je le reposition un peu polus haut(+10) et rétablit la situation par un (-10)
            txt=ligne[Ccblect] #CB lecteur
            barcode128Std = code128.Code128(txt, barWidth=0.3*mm, barHeight=8*mm, checksum=0)
            barcode128Std.drawOn(destination,x+400,y)
            y-=10
				
        # On vérifie s'il y a suffisamment de place pour écrire la suite de la commande sur la page courante
        # sinon, il faut créer une nouvelle page
        # Dans ce cas il faut recréer l'entête de la commande avant de poursuivre le remplissage courant de la fiche commande  
        if (y-6*deltay)< partiebasse+4*deltacarn*carnegie :
            # comment lire ce IF?
            # * on compare d'un coté jusqu'où ira le "y" courant si on ajoute une commande
            # ca vaudra (y - 6 lignes de commandes environ), soit y-6*deltay
            # * pour l'autre coté, on vérifie y arrive en dessus du bas de page
            # habituellement, le second membre sera simplement la variable "basdepage" (=10)
            # dans le cas général qui traite du fantome, il faut le comparer à "partiebasse" auquel il faut ajouter suffisamment d'espace pour le fantome (environ 4*deltacarn)
            # or, on a choisi (carnegie=0) si la bibliothèque courante N'EST PAS Carnegie, sinon (carnegie==1) si c'est Carnegie
            # on peut multiplier par "carnegie" pour tester la condition


            # IL N'Y A PAS SUFFISAMMENT DE PLACE, on poursuit la commande du lecteur sur une autre page
            destination.setFont("Helvetica", 12)            
            destination.drawString(350,5,"Suite page suivante.../...")
            # on en profite pour indiquer au préparateur de la commande qu'il y a une suite à la commande avant de passer à la page suivante
          
            # création de la page suivante (on reprend les différents éléments vu précedemment pour reconstruire l'entete de cette nouvelle page
            destination.pageNumer=2
            destination.showPage()
            y=hautdepage        # On repositionne le curseur courant en haut de page
            
            txt=dest+" "+ligne[Ccblect]     # on écrit en heut de page la bibliothèque, suivi du cb du lecteur
            destination.setFont("Helvetica", 10)            
            destination.drawString(x,y,txt)

            destination.setFont("Helvetica", 12)    # sur la meme ligne, à gauche on indique au préparateur de la commande que c'est la suite d'une meme commande       
            destination.drawString(450,y,"... suite")
            
            y -= int(1.5*deltay)    # on saute une ligne
            
            #lect=ligne[Clect]   #lecteur
            destination.setFont("Helvetica", 12)
            destination.drawString(x,y,lecteur)  #  ATTENTION la valeur "lecteur" a été calculée lors de la boucle précédente et n'a a priori pas été modifiée

            y-=deltay
            #cb lecteur en code barre128
            y+=10            
            txt=ligne[Ccblect] #CB lecteur
            barcode128Std = code128.Code128(txt, barWidth=0.3*mm, barHeight=8*mm, checksum=0)
            barcode128Std.drawOn(destination,x+400,y)
            y-=10

        # ---------------- Fin d'entête de commande qui deborde sur la page suivante ----------------------
        # On peut poursuivre une activité normale : ajouter les infos du doc courant commandé à la commande

            
        
        # On affiche le titre seul
        y-=deltay

        txt=ligne[Ctitreseul]
        if len(txt)>50:
            txt=txt[0:47]+"..." # titre trop long => troncature
            
        destination.setFont("Helvetica", 15)
        destination.drawString(x,y,txt)

        # date réservation + date prise en charge 
        txt=ligne[Cdate_res]+" / Traité le : "+won # "WON = NOW en notation française
        destination.setFont("Helvetica", 7)
        destination.drawString(430,y,txt)
        

        # ------------- ajoute une ligne si (Ccotesup + Ctitresup) existe 
        y-=deltay 
        cotesup=str(ligne[Ccotesup]) #cote sup
        if cotesup=="vide":
            cotesup=""
            txt= ligne[Ctitresup] # titre sup
        else :
            txt = cotesup+", "+ligne[Ctitresup]# titre sup

        txt=nettoyage(txt)
        if len(txt)>60:
            txt=txt[0:60]


        #cote - type doc - secteur
        txt2=ligne[Ccote]+" - "+ligne[Csupport]+" - "+ligne[Csecteur]

        txt2=nettoyage(txt2)        

        if txt=="":
            txt3=txt2
        else:
            txt3=txt+" > "+txt2

        destination.setFont("Helvetica", 10)
        destination.drawString(x,y,txt3)
        # ------------- Fin de : ajoute une ligne si (Ccotesup + Ctitresup) existe




# ------------Ligne suivante -----------------        

        y -= int(1.5*deltay)
        # Si la bibliothèque de sdestination est différente de la bibliothèque d'appartenance du document, on indique la destination du document
        if ligne[Cdest]!=succursale:    #destination ====================== A PRECISER, CETTE VARIABLE N'EST PAS ENCORE DEFINI PAR SYRACUSE ================
            
            txt="=> "+ligne[Cdest]      #destination
            destination.setFont("Helvetica", 15)
            destination.drawString(x,y,txt)
            transit=1

         #cb exemplaire en code barre128 suivi de la valeur de ce CB
        txt=ligne[Ccbex]
        barcode128Std = code128.Code128(txt, barWidth=0.3*mm, barHeight=5*mm, checksum=0)
        barcode128Std.drawOn(destination,xmid-15,y)

        txt=txt[0:-4]+" 5100" # j'ajoute une espace pour faciliter la lecture du CB (5100 est le radical commun à la bibliothèque de Reims)
        destination.setFont("Helvetica", 10)
        destination.drawString(xmid+120,y,txt)

        # la mention de réservation est indiqué, on l'indique au préparateur de la commande (le document n'est en effet pas en rayon)
        if "Réservé" in ligne[Cetat] :
            txt=" Retour-reservé"
            destination.setFont("Helvetica", 13)
            destination.drawString(xmid+200,y,txt)  




        y-=deltay

        # date d'expiration (depend de si il y a déplacement du document vers bibliothèque de destination)
        if transit==1:
            date=dateexptransit
        else:
            date=dateexp
        txt="Expire le : "+date
        destination.setFont("Helvetica", 12)
        destination.drawString(x,y,txt)
        
     






# ------------Ligne suivante -----------------



	# date de retour (depend de si il y a déplacement du document vers bibliothèque de destination)

        if transit==1:
            date=dateretourlecttransit
        else:
            date=dateretourlect
        dateretour="A rendre avant le : "+date
        destination.setFont("Helvetica", 14)
        destination.drawString(xmid,y,dateretour)

        y -= int(1.5*deltay)
        
        # ------------- Si la bibliothèque courante est Carnegie, il faut imprimer un fantome en bas de page
        # 
        # ici, on commence à écrire par le bas et on remonte

        if carnegie==1:            
            destination.setFont("Helvetica", 14)
            destination.drawString(x,partiebasse,ligne[Ccote])
            partiebasse+=deltacarn
            destination.setFont("Helvetica", 14)
            destination.drawString(x,partiebasse,ligne[Ctitreseul])
            partiebasse+=deltacarn
            destination.setFont("Helvetica", 14)
            destination.drawString(x,partiebasse,dateretour)
            partiebasse+=deltacarn
            partiebasse+=deltacarn
        # ------------- FIN DE : Si la bibliothèque courante est Carnegie, il faut imprimer un fantome en bas de page
    
       
    destination.save()

# --------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ FIN DE ENVOIPDF ---------------------------------------------
# --------------------------------------------------------------------------------------------------------------



# -------------- Initialisation de la lecture du tableau entier -----------------------------------------------
# ----- c'est le CSV qui a été converti en tableau Python, avec des données nettoyées -------------------------
nbligne=len(tabdoc)
print("Nombre total de commandes aujourd'hui : "+str(nbligne))

sucdoc=tabdoc[0][0]
cell=[]
for line in tabdoc:
    if line[0]==sucdoc:     #tant que la succursale reste la même on continue d'accumuler les données dasn un sous-tableau "cell"
        cell.append(line)
    else :
        envoipdf(cell)      # la succursale est différente, on envoie donc le sous-tableau constitué vers la génération du PDF
        cell=[]             # on réinitialise le sous tableau suivant et on commence à le remplir avec la donnée courante
        cell.append(line)
        sucdoc=line[0]
envoipdf(cell) # on envoie le dernier sous tableau parcouru à traiter en pdf

# -------------- Initialisation de la lecture du tableau entier -----------------------------------------------
# ----- c'est le CSV qui a été converti en tableau Python, avec des données nettoyées -------------------------




"""
##OH : ouvrir le pdf de Falala du jour dans Adobe Reader 
def imprfal():
    contenu=open("impr_fal.bat", "w")
    comm="\"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe\" /P "
    chemin="T:\deconfinement\drive\listes\\"+now+"\\falala"+"-"+now+".pdf"
    comm+=chemin 
    print(comm)
    contenu.write(comm)
    contenu.close()
    os.system('impr_fal.bat')
	
reponse=input('Voulez-vous imprimer pour Falala ?(y/n)')
if reponse=="y":
    imprfal()
else:
    print('ok')
"""



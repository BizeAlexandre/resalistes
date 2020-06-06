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

fichier =  'solr502.csv'

aujourdhui=datetime.date.today()
now=str(aujourdhui)
won=now[8:10]+"/"+now[5:7]+"/"+now[0:4]
#print("aujourd'hui : "+won)
if os.path.isdir(now)==0 :
    os.mkdir(now)
#duplique le fichier CSV dans T
#os.system('copy '+fichier+' T:\deconfinement\drive\listes\\'+now+"\\"+fichier)
#os.system('copy '+fichier+' C:\deconfinement\drive\listes\\'+now+"\\"+fichier)

# nb de jours avant expiration + retour
expiration=5
expirationtransit=8
retour=21
retourtransit=24
delai=datetime.timedelta(days=expiration)
dateexpiration=str(aujourdhui+delai)
dateexp=dateexpiration[8:10]+"/"+dateexpiration[5:7]+"/"+dateexpiration[0:4]

delai=datetime.timedelta(days=expirationtransit)
dateexpirationtransit=str(aujourdhui+delai)
dateexptransit=dateexpirationtransit[8:10]+"/"+dateexpirationtransit[5:7]+"/"+dateexpirationtransit[0:4]

delai=datetime.timedelta(days=retour)
dateretour=str(aujourdhui+delai)
dateretourlect=dateretour[8:10]+"/"+dateretour[5:7]+"/"+dateretour[0:4]

delai=datetime.timedelta(days=retourtransit)
dateretourtransit=str(aujourdhui+delai)
dateretourlecttransit=dateretourtransit[8:10]+"/"+dateretourtransit[5:7]+"/"+dateretourtransit[0:4]
#print("date expiration : "+dateexp)

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
nbchamp=17
tableau=[]
id=0

# ================= définition numéros de champs de colonne ========================
Csucc=0
Csecteur=1
Ccote=2
Cdate_res=3
Ctitre=4 # integre titre complément de titre tomaison editeur année dedition...
           # => a nettoyer et recrééer champ titreseul et titresup
Csupport=5
Ccbex=6#CB exemplaire => a dédoublonner
CBIMD=7
Cdest= 7 # ======== => numéro à définir  =================
Cetat=8
CTRDE=9
Clect=10
Ccblect=11
Ccotesup=12
CDISP=13
CDRES=14
Ctitreseul=15
Ctitresup=16
# ================= FIN DE définition numéros de champs de colonne ========================

def nettoyage(txt):
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

    i=1
    while i==1:
        i=0
        if len(txt)>0:
            if txt[0]==",":
                txt=txt[1:]
                i=1
        if len(txt)>0:
            if txt[0]=="'":
                txt=txt[1:]
                i=1
        if len(txt)>0:
            if txt[0]==":":
                txt=txt[1:]
                i=1                
        if len(txt)>0:
            if txt[0]==" ":
                txt=txt[1:]
                i=1
        if len(txt)>0:
            if txt[0]=="-":
                txt=txt[1:]
                i=1
                
        if len(txt)>0:
            if txt[-1]==",":
                txt=txt[0:-1]
                i=1
        if len(txt)>0:
            if txt[-1]==":":
                txt=txt[0:-1]
                i=1
        if len(txt)>0:
            if txt[-1]==" ":
                txt=txt[0:-1]
                i=1
        if len(txt)>0:
            if txt[-1]=="-":
                txt=txt[0:-1]
                i=1

    return txt
    
def dedoublonne(txt):
    p=txt.find(",")
    if p!=-1:
        txt=txt[p:]
    txt=nettoyage(txt)
    return txt    

def complementtitre(txt):
    p=txt.find("/ ")
    if p==-1:
        complement=""
        p=len(txt)
        titre=txt
    else:
        txt=txt[0:p]#suppression mention éditeur/édition
        p=txt.find("- ")
        titre=txt[0:p]
        complement=txt[p+2:]
        
    titre=nettoyage(titre)
    complement=nettoyage(complement)
    
    return [titre, complement]
       
#with open(fichier,encoding='ISO-8859-1', newline='') as csvfile:
with open(fichier,encoding='utf8', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        texte=str(row)
        #print(texte)
        id+=1

        #print(str(id)+" "+texte+"\n")
        texte=texte.replace("&amp;","&")
        #texte=texte.replace("; ",",")
        #print("row = "+texte)
        txt=""
        cell=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        numchamp=0
        for car in texte:
            #print (car)
            if car=="|":
                if numchamp==0:
                    txt=txt[2:]
                #print(numchamp)
                cell[numchamp]=txt
                #print("champ = "+txt)
                numchamp+=1
                txt=""

            else:
                txt+=car
        
        cell[numchamp]=txt[0:-2]
        
        # dédoublonne le Code barre exemplaire si necessaire
        # exemple: 04068695100, 4068695100  => 4068695100
        cell[Ccbex]=dedoublonne(cell[Ccbex])

        # créé titreseul et titresup
        cell[Ctitreseul] , cell[Ctitresup] = complementtitre(cell[Ctitre])

        # remplace Disque Compact en CD
        if cell[Csupport]=="Disque compact":
            cell[Csupport]="CD"

        # nettoie la date au moment de la réservation par l'usager
        cell[Cdate_res]=cell[Cdate_res][0:10]+" "+cell[Cdate_res][11:16]



        
        tableau.append(cell)
        
#print (tableau[10])
del tableau[0]
# tableau trié par succursale du document
tabdoc=list(sorted(tableau, key=itemgetter(0)))
#création du répertoire de destination


def envoipdf(cell): 
    donnee=""
    tab=list(sorted(cell, key=itemgetter(Clect,Csecteur,Ccote)))
    succursale=tab[0][0]
    dest=succ[succursale]
    print(succursale+"=>"+dest)
    destination = canvas.Canvas(now+"/"+dest+"-"+now+".pdf") #OH
    lect=""
    nbligne=len(tab)
    print (nbligne)
    premierepage=1
    hautdepage=810
    y=hautdepage
    x=20
    xmid=300
    deltay=15

    for ligne in tab:
        transit=0

        if lect!=ligne[Clect]:

            if premierepage==1:
                premierepage=0
            else:
                #https://stackoverflow.com/questions/3593193/add-page-break-to-reportlab-canvas-object
                destination.pageNumer=2
                destination.showPage()
                #PageBreak.drawOn(destination, 0, 1000, 0)                
                y=hautdepage
                
            lect=ligne[Clect]# lecteur
            lecteur=lect
            
            if lecteur[0:3]=="M. ":
                lecteur=lecteur[3:]
            elif lecteur[0:4]=="Mme ":
                lecteur=lecteur[4:]
            if len(lecteur)>33:
                lecteur=lecteur[0:29]+"..."
            txt=dest+" "+ligne[Ccblect]
            destination.setFont("Helvetica", 10)            
            destination.drawString(x,y,txt)
            y -= int(1.5*deltay)
            destination.setFont("Helvetica", 18)
            destination.drawString(x,y,lecteur)
            y-=deltay
            destination.setFont("Helvetica", 10) 
 ###OH   
            #cb lecteur en code barre128
            y+=10            
            txt=ligne[Ccblect] #CB lecteur
            
            barcode128Std = code128.Code128(txt, barWidth=0.3*mm, barHeight=8*mm, checksum=0)
            barcode128Std.drawOn(destination,x+400,y)
            y-=10
### OH
				
        # si la commande fait plus d'une page    
        if (y-6*deltay)<10 :
            destination.setFont("Helvetica", 12)            
            destination.drawString(350,5,"Suite page suivante.../...")
          
            destination.pageNumer=2
            destination.showPage()
            y=hautdepage
            lect=ligne[Clect] #lecteur
            txt=dest+" "+ligne[Ccblect]
            destination.setFont("Helvetica", 10)            
            destination.drawString(x,y,txt)

            destination.setFont("Helvetica", 12)            
            destination.drawString(450,y,"... suite")
            
            y -= int(1.5*deltay)
            destination.setFont("Helvetica", 12)
            destination.drawString(x,y,lecteur)
            y-=deltay
            destination.setFont("Helvetica", 10)
            #cb lecteur en code barre128
            y+=10            
            txt=ligne[Ccblect][1:-1] #CB lecteur
            barcode128Std = code128.Code128(txt, barWidth=0.3*mm, barHeight=8*mm, checksum=0)
            barcode128Std.drawOn(destination,x+400,y)
            y-=10
            
        #titre
        y-=deltay        
        txt=ligne[Ctitreseul]

        destination.setFont("Helvetica", 15)
        destination.drawString(x,y,txt)

        
        cotesup=str(ligne[Ccotesup]) #cote sup
        if cotesup=="vide":
            cotesup=""
            txt= ligne[Ctitresup] # titre sup
        else :
            txt = cotesup+", "+ligne[Ctitresup]# titre sup

        txt=nettoyage(txt)    
        
        if len(txt)>0:
            y-=deltay    
            destination.setFont("Helvetica", 10)
            destination.drawString(x,y,txt)

        #envoyer à
        if ligne[Cdest]!=succursale:    #destination
            txt="=> "+ligne[Cdest]      #destination
            destination.setFont("Helvetica", 15)
            destination.drawString(xmid,y,txt)
            transit=1

# ------------Ligne suivante -----------------
        y-=deltay

        #cote - type doc - secteur
        txt=ligne[Ccote]+" - "+ligne[Csupport]+" - "+ligne[Csecteur]

        txt=nettoyage(txt)        
        destination.setFont("Helvetica", 12)
        destination.drawString(xmid,y,txt)

        # date prise en charge        
        txt="Traité le : "+won
        destination.setFont("Helvetica", 12)
        destination.drawString(x,y,txt)


# ------------Ligne suivante -----------------
        y-=deltay
        
        # date réservation - rappel succ
        txt=ligne[Cdate_res]+" - "+ligne[Clect]
        destination.setFont("Helvetica", 7)
        destination.drawString(xmid,y,txt)

        # date d'expiration
        if transit==1:
            date=dateexptransit
        else:
            date=dateexp
        txt="Expire le : "+date
        destination.setFont("Helvetica", 12)
        destination.drawString(x,y,txt)

# ------------Ligne suivante -----------------
        y-=int(1.5*deltay)

        #cb exemplaire en code barre128 + CB

        
        txt=ligne[Ccbex]
        p=txt.find(",")
        if p!=-1:
            txt=txt[1:p-1]

        
        barcode128Std = code128.Code128(txt, barWidth=0.3*mm, barHeight=5*mm, checksum=0)
        barcode128Std.drawOn(destination,xmid-15,y)

        txt=txt[0:-4]+" 5100"
        destination.setFont("Helvetica", 10)
        destination.drawString(xmid+120,y,txt)

        if "Réservé" in ligne[Cetat] :
            txt=" Retour-reservé"
            destination.setFont("Helvetica", 13)
            destination.drawString(xmid+200,y,txt)

	# date de retour
        if transit==1:
            date=dateretourlecttransit
        else:
            date=dateretourlect
        txt="A rendre avant le : "+date
        destination.setFont("Helvetica", 14)
        destination.drawString(x,y,txt)

        y -= int(1.5*deltay)
    
        """if ligne[Cdest]!=succursale:
            donnee+="Envoyer à  => <b>"+ligne[Cdest]+"</b><br>\n"
            """
                   
    destination.save()

# -------------- fin d'envoi de fichier ------------
nbligne=len(tabdoc)
print(nbligne)

sucdoc=tabdoc[0][0]
cell=[]
for line in tabdoc:
    if line[0]==sucdoc:
        cell.append(line)
    else :
        envoipdf(cell)
        cell=[]
        cell.append(line)
        sucdoc=line[0]
envoipdf(cell)  	 


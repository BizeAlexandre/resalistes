#!/usr/bin/env python
# -*- coding: utf-8 -*-


#rappatrie le csv des réservations en rayon émises depuis 5 jours et moins depuis le serveur solr

import requests
import re


def cleanhtml(content):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', content)
    return cleantext

url='http://srvpw-medindx:8985/solr/PRODUCTIONSILS/select?start=0&rows=5000&q=RESD_date:{NOW\-5DAYS%20TO%20*}&fl=BIBL_display_store,SECT_display_store,COTA_store,RESD_date,REFA_store,TYPS_store,CBEX_display_store,BIMD_store,ETAT_store,TRDE_store,RESA1NOMEMPR_store,RESA1CBEMPR_store,COTS_display_store,DSIP_store,DRES_date&fq=(AREA_normalized:EXE%20OR%20AREA_normalized:ACQ)%20AND%20ACTI_bool:true&fq={!tag=ETAT_Q}ETAT_normalized:En\%20rayon&wt=csv'
r = requests.get(url, auth=('xxxxx', 'yyyyy'))

# --------------- remplace le séparateur de champs "," par "|" -------------
def decoupechamp (content):
    guill=0
    txt=""
    for t in content:
        if t=="\"":
            if guill==0:
                guill=1
            else:
                guill=0
        if (t==",") & (guill==0):
            t="|"
        txt+=t
    return txt
        
content = r.text
content=cleanhtml(content)
content=decoupechamp(content)


destination=open(u"solr502.csv" , "w" , encoding="utf-8") 
destination.write(content)
destination.close()

"""
Copyright (C) <2020>  <Olivier Hirsch, Denis Paris> <Bibliothèque municipale de Reims>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
    """
	

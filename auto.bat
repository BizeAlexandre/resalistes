cd c:\python38-32
set $madate=%date:~-4%-%date:~3,2%-%date:~0,2%
if exist solr502.csv ren solr502.csv solr502-%$madate%.csv
python.exe solr_025.py
python.exe resalistes-0.1-solr.py
xcopy C:\Python38-32\%$madate% T:\deconfinement\drive\listes\%$madate% /E /C /R /H /I /K
del solr502.csv /f /q
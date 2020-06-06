cd c:\python38-32
set $madate=%date:~-4%-%date:~3,2%-%date:~0,2%
python.exe solr_025.py
python.exe resalistes-0.1-solr.py
xcopy C:\Python38-32\%$madate% T:\deconfinement\drive\listes\%$madate% /E /C /R /H /I /K
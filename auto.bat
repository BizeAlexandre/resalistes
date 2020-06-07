cd c:\python38-32
set $madate=%date:~-4%-%date:~3,2%-%date:~0,2%
python.exe solr_025.py
python.exe resalistes-0.1-solr.py
xcopy C:\Python38-32\%$madate% T:\deconfinement\drive\listes\%$madate% /E /C /R /H /I /K


::Copyright (C) <2020>  >Olivier Hirsch>

  ::  This program is free software: you can redistribute it and/or modify
  ::  it under the terms of the GNU General Public License as published by
  ::  the Free Software Foundation, either version 3 of the License, or
  ::  (at your option) any later version.

  ::  This program is distributed in the hope that it will be useful,
  ::  but WITHOUT ANY WARRANTY; without even the implied warranty of
  ::  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  :: GNU General Public License for more details.

  ::  You should have received a copy of the GNU General Public License
  ::  along with this program.  If not, see <https://www.gnu.org/licenses/>
   

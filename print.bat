@echo off
setlocal 
for /f "skip=8 tokens=2,3,4,5,6,7,8 delims=: " %%D in ('robocopy /l * \ \ /ns /nc /ndl /nfl /np /njh /XF * /XD *') do (
 set "dow=%%D"
 set "month=%%E"
 set "day=%%F"
 set "HH=%%G"
 set "MM=%%H"
 set "SS=%%I"
 set "year=%%J"
)

set $madate=%date:~-4%-%date:~3,2%-%date:~0,2%
if %dow%=="mardi" or if %dow%=="mercredi" or if %dow%=="jeudi" or if %dow%=="vendredi" or if %dow%=="samedi" DO (
taskkill /F /IM AcroRd32.exe
timeout 10
"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe" /t "C:\python38-32\%$madate%\falala-%$madate%.pdf"
timeout 180
taskkill /F /IM AcroRd32.exe)
endlocal
@echo off

FOR /F "tokens=*" %%i IN ('time /T') DO SET startTime=%%i 

echo Start time : %startTime%

rm frequency.db
python createDB.py
python convert.py -n %1

FOR /F "tokens=*" %%i IN ('time /T') DO SET endTime=%%i 

echo Start time : %startTime%
echo End time   : %endTime%


@echo off
set /p FILENAME=Input file name: 
cd "C:\Users\Radek Augustyn\AppData\Local\Programs\Python\Python39"
python.exe C:/KubaPrograms/KCode/KCode/__init__.py %FILENAME%
pause
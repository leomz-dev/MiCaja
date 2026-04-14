@echo off
echo Compilando MiCaja con PyInstaller...
pyinstaller --noconfirm --onedir --windowed --name "MiCaja" --add-data "data;data" "main.py"
echo Compilacion terminada. El ejecutable se encuentra en la carpeta "dist\MiCaja".
pause

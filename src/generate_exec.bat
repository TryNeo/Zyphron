@echo off

echo Limpiando build anterior...
rmdir /s /q build
rmdir /s /q dist
REM Nombre app
set APPNAME=Zyphron
REM Escritorio usuario
set DESKTOP=%USERPROFILE%\Desktop
REM Carpeta destino
set DESTINO=%DESKTOP%\Zyphron

echo Compilando ejecutable...
flet pack main.py --name "Zyphron" --add-data "assets;assets" --product-name "Zyphron" --product-version "1.0.0" --file-version "1.0.0.0" --copyright "© 2025 Josue Lopez. Todos los derechos reservados." --icon "C:\Users\tsjos\Documents\Zyphron\src\assets\icons\coding.ico"
echo.
echo Moviendo ejecutable a Zyphron...
move "dist\%APPNAME%.exe" "%DESTINO%\%APPNAME%.exe"
echo.
echo ==========================
echo Listo!
echo EXE en: %DESTINO%
echo ==========================
rmdir /s /q build
rmdir /s /q dist
del "%APPNAME%.spec"
pause
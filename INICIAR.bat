@echo off
echo.
echo  ================================
echo    MACROWATCH - Iniciando...
echo  ================================
echo.
echo  Buscando puerto disponible...
echo  El navegador se abrira solo.
echo  Para detener: cierra esta ventana
echo.
cd /d "%~dp0"
python server.py
pause

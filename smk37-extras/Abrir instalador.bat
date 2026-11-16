@echo off
rem Abre o instalador do Polly SMK-37 no navegador (servidor local em http://localhost:8740).
rem Use no Chrome ou no Edge. Feche esta janela depois que a instalacao terminar.
cd /d "%~dp0"
python servidor-emulador.py 8740 instalador --abrir
if errorlevel 1 pause

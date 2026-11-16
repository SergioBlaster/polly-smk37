@echo off
rem Abre o emulador do Polly SMK-37 no navegador (servidor local em http://localhost:8737).
rem Feche esta janela para desligar o servidor.
cd /d "%~dp0"
python servidor-emulador.py 8737 emulador --abrir
if errorlevel 1 pause

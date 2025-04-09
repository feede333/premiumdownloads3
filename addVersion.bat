@echo off
setlocal EnableDelayedExpansion

set "jsonFile=data\versions.json"

:input
cls
echo =================================
echo    Agregar Nueva Version Avast
echo =================================
echo.
set /p version="Numero de Version (ej. 25.3.8549): "
set /p date="Fecha (ej. Abril 2025): "
set /p size="Tamaño (ej. 4.2 GB): "
set /p torrent="Link Torrent: "
set /p magnet="Link Magnet: "
set /p seeds="Seeds iniciales: "
set /p peers="Peers iniciales: "

echo.
echo --- Confirmar datos ---
echo Version: %version%
echo Fecha: %date%
echo Tamaño: %size%
echo Torrent: %torrent%
echo Magnet: %magnet%
echo Seeds: %seeds%
echo Peers: %peers%
echo.
set /p confirm="¿Los datos son correctos? (S/N): "

if /i "%confirm%"=="S" (
    node updateVersions.js "%version%" "%date%" "%size%" "%torrent%" "%magnet%" "%seeds%" "%peers%"
    echo Version agregada correctamente!
) else (
    goto input
)

pause
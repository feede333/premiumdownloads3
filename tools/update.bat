@echo off
echo Actualizando repositorio...

REM Forzar actualización del índice de git
git update-index --refresh

echo Verificando cambios...
git status

echo.
echo Subiendo cambios...
git add -A
git commit -m "Update: %date% %time%"
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo Cambios subidos exitosamente!
    timeout /t 2 >nul
) else (
    echo.
    echo Hubo un error al subir los cambios.
    echo Presiona cualquier tecla para cerrar...
    pause >nul
)

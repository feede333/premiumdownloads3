@echo off
echo Verificando token de GitHub...
if "%GITHUB_TOKEN%" == "" (
    echo Error: Variable GITHUB_TOKEN no encontrada
    echo Configure la variable de entorno GITHUB_TOKEN con su token de acceso personal
    pause
    exit /b 1
)

echo Sincronizando con GitHub...

echo.
echo Generando páginas HTML...
python tools/page_generator.py

echo.
echo Obteniendo cambios remotos...
git pull origin main --rebase

if %errorlevel% neq 0 (
    echo.
    echo Hubo un conflicto al intentar sincronizar con el remoto.
    echo Resolviendo conflictos automáticamente...
    git add .
    git rebase --continue
)

echo.
echo Subiendo cambios locales...
git add .
git commit -m "Actualización de programas y contenido"
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo Cambios subidos exitosamente!
    echo Por favor espera unos minutos para que GitHub Pages se actualice.
    timeout /t 5 >nul
) else (
    echo.
    echo Hubo un error al subir los cambios.
    echo Revisa la consola para más detalles.
    pause
)
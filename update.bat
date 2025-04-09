REM filepath: c:\Users\Federico\Downloads\downloads site\premiumdownloads2\update.bat
@echo off
echo Verificando token de GitHub...

REM Asegurarse de estar en el directorio raíz
cd /d %~dp0

REM Verificar la variable de entorno GITHUB_TOKEN
if "%GITHUB_TOKEN%" == "" (
    echo [ERROR] Variable GITHUB_TOKEN no encontrada
    echo Configure la variable de entorno GITHUB_TOKEN con su token de acceso personal
    echo Para configurar: 
    echo setx GITHUB_TOKEN "tu_token_aqui"
    pause
    exit /b 1
)

echo [OK] Token encontrado

echo.
echo Verificando rutas y archivos...
python tools/verify_setup.py

if %errorlevel% neq 0 (
    echo [ERROR] Error en la verificación de la estructura
    pause
    exit /b 1
)

echo.
echo Actualizando repositorio...
git add ./data/programs.json
git add ./images/*
git add ./*.html
git status

echo.
echo Confirmando cambios...
git commit -m "Update: Actualización de programas %date% %time%"

echo.
echo Configurando remote con token...
git remote remove origin
git remote add origin https://%GITHUB_TOKEN%@github.com/feede333/premiumdownloads3.git

echo.
echo Sincronizando con remoto...
git pull origin main --rebase

if %errorlevel% neq 0 (
    echo.
    echo [AVISO] Hubo conflictos, intentando resolverlos...
    git add .
    git rebase --continue
)

echo.
echo Subiendo cambios...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo [OK] Cambios subidos exitosamente!
    echo Por favor espera unos minutos para que GitHub Pages se actualice.
    timeout /t 5 >nul
) else (
    echo.
    echo [ERROR] Hubo un error al subir los cambios.
    echo Revisa la consola para más detalles.
    pause
)
REM filepath: c:\Users\Federico\Downloads\downloads site\premiumdownloads2\update.bat
@echo off
echo Verificando rutas...

REM Cambiar al directorio del proyecto (donde está el .git)
cd /d "%~dp0"

REM Verificar que estamos en el directorio correcto
if not exist ".git" (
    echo [ERROR] No se encuentra el repositorio Git.
    echo Directorio actual: %CD%
    echo Este script debe ejecutarse desde la raíz del proyecto.
    pause
    exit /b 1
)

echo [OK] Directorio del proyecto encontrado: %CD%

REM Verificar token
if "%GITHUB_TOKEN%" == "" (
    echo [ERROR] Variable GITHUB_TOKEN no encontrada
    echo Configure la variable de entorno GITHUB_TOKEN con su token de acceso personal
    pause
    exit /b 1
)

echo [OK] Token encontrado

echo.
echo Verificando estructura...
python tools/verify_setup.py

if %errorlevel% neq 0 (
    echo [ERROR] Error en la verificación
    pause
    exit /b 1
)

echo.
echo Actualizando repositorio...
git add data/programs.json
git add images/*
git add *.html
git status

echo.
echo Estado del repositorio:
git status

echo.
echo Confirmando cambios...
git commit -m "Update: Actualización de programas %date% %time%"

echo.
echo Subiendo a GitHub...
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
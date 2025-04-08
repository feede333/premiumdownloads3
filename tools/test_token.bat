@echo off
echo Verificando configuración del token de GitHub...

if "%GITHUB_TOKEN%" == "" (
    echo [ERROR] Token no encontrado
    echo Configure la variable de entorno GITHUB_TOKEN
    exit /b 1
)

echo [OK] Token encontrado

echo.
echo Probando conexión con GitHub...
git ls-remote https://%GITHUB_TOKEN%@github.com/feede333/premiumdownloads3.git HEAD

if %errorlevel% equ 0 (
    echo [OK] Conexión exitosa con GitHub
    echo [OK] El token tiene los permisos correctos
) else (
    echo [ERROR] No se pudo conectar con GitHub
    echo [ERROR] Verifique el token y los permisos
)
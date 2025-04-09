@echo off
cd %~dp0

REM Verificar API key de DeepSeek
if "%DEEPSEEK_API_KEY%" == "" (
    echo [AVISO] Variable DEEPSEEK_API_KEY no encontrada
    echo La función de autocompletar con IA no estará disponible
    timeout /t 3 >nul
)

python program_manager.py
pause
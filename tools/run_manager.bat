@echo off
cd %~dp0

REM Configurar API key de DeepSeek
set DEEPSEEK_API_KEY=sk-84b4c6e1bd82482cb5c131a45acb7d8b

python program_manager.py
pause
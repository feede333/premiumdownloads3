@echo off
cd /d "%~dp0"
python -c "from version_manager import VersionManagerGUI; import tkinter as tk; root = tk.Tk(); app = VersionManagerGUI(root); root.mainloop()"
pause
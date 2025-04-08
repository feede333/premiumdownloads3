import os
import json

def verify_setup():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Verificar estructura de directorios
    paths_to_check = [
        'data',
        'images',
        'js',
        'css'
    ]
    
    for path in paths_to_check:
        full_path = os.path.join(base_dir, path)
        if not os.path.exists(full_path):
            print(f"⚠️ Creando directorio faltante: {path}")
            os.makedirs(full_path)
    
    # Verificar archivo JSON
    json_path = os.path.join(base_dir, 'data', 'programs.json')
    if not os.path.exists(json_path):
        print("⚠️ Creando archivo programs.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({"programs": []}, f, indent=2)
    else:
        # Verificar que el JSON sea válido
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ JSON válido con {len(data.get('programs', []))} programas")
        except json.JSONDecodeError:
            print("❌ Error: programs.json no es un JSON válido")
    
    print("\nVerificación completada.")

if __name__ == "__main__":
    verify_setup()

# filepath: c:\Users\Federico\Downloads\downloads site\premiumdownloads2\tools\update_site.bat
"""
@echo off
REM filepath: c:\Users\Federico\Downloads\downloads site\premiumdownloads2\tools\update_site.bat
echo Verificando estructura...
python verify_setup.py

echo.
echo Sincronizando con GitHub...
git add .
git commit -m "Actualización de contenido"
git push origin main

echo.
echo Proceso completado!
echo Por favor espera unos minutos para que GitHub Pages se actualice.
pause
"""
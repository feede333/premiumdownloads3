import os
import json

def verify_setup():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(base_dir, 'frontend', 'public')
    
    # Verificar que el index.html existe en frontend/public
    if not os.path.exists(os.path.join(frontend_dir, 'index.html')):
        print("❌ Error: index.html no encontrado en frontend/public")
        return False
        
    # Crear un enlace simbólico al index.html en la raíz si no existe
    root_index = os.path.join(base_dir, 'index.html')
    if not os.path.exists(root_index):
        try:
            os.symlink(
                os.path.join(frontend_dir, 'index.html'),
                root_index
            )
            print("✅ Enlace simbólico a index.html creado en la raíz")
        except Exception as e:
            print(f"❌ Error creando enlace simbólico: {str(e)}")
            return False
    
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
    return True

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
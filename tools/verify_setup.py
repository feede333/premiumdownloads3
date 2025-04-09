import os
import json

def verify_setup():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Verificar estructura de directorios en la raíz
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

if __name__ == "__main__":
    verify_setup()
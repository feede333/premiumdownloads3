import json
import os
from datetime import datetime

class VersionManager:
    def __init__(self):
        self.data_folder = "data"
        self.json_file = os.path.join(self.data_folder, "versions.json")
        
        # Crear carpeta data si no existe
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        
        # Crear archivo JSON si no existe
        if not os.path.exists(self.json_file):
            self.save_versions({"versions": []})

    def load_versions(self):
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"versions": []}

    def save_versions(self, versions_data):
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(versions_data, f, indent=2, ensure_ascii=False)

    def add_version(self):
        print("\n=== Agregar Nueva Versión de Avast 2025 ===")
        version = input("Número de Versión (ej. 25.3.8549): ")
        date = input("Fecha (ej. Abril 2025): ")
        size = input("Tamaño (ej. 4.2 GB): ")
        torrent_link = input("Link Torrent: ")
        magnet_link = input("Link Magnet: ")
        seeds = input("Seeds iniciales: ")
        peers = input("Peers iniciales: ")

        versions_data = self.load_versions()
        
        new_version = {
            "version": version,
            "date": date,
            "size": size,
            "torrentLink": torrent_link,
            "magnetLink": magnet_link,
            "seeds": seeds,
            "peers": peers
        }

        versions_data["versions"].insert(0, new_version)
        self.save_versions(versions_data)
        print("\n✅ Versión agregada correctamente!")

    def remove_version(self):
        versions_data = self.load_versions()
        
        if not versions_data["versions"]:
            print("\n❌ No hay versiones para eliminar")
            return

        print("\n=== Eliminar Versión ===")
        print("\nVersiones disponibles:")
        for i, version in enumerate(versions_data["versions"]):
            print(f"{i+1}. Versión {version['version']} ({version['date']})")

        try:
            choice = int(input("\nSelecciona el número de la versión a eliminar (0 para cancelar): "))
            if choice == 0:
                print("\nOperación cancelada")
                return
                
            if 1 <= choice <= len(versions_data["versions"]):
                removed = versions_data["versions"].pop(choice-1)
                self.save_versions(versions_data)
                print(f"\n✅ Versión {removed['version']} eliminada correctamente!")
            else:
                print("\n❌ Número de versión inválido")
        except ValueError:
            print("\n❌ Por favor ingresa un número válido")

    def list_versions(self):
        versions_data = self.load_versions()
        
        if not versions_data["versions"]:
            print("\n❌ No hay versiones disponibles")
            return

        print("\n=== Versiones Disponibles ===")
        for i, version in enumerate(versions_data["versions"]):
            print(f"\n{i+1}. Versión {version['version']}")
            print(f"   Fecha: {version['date']}")
            print(f"   Tamaño: {version['size']}")
            print(f"   Seeds: {version['seeds']}")
            print(f"   Peers: {version['peers']}")

    def add_version_to_html(self):
        html_file_path = r"c:\Users\Federico\Downloads\downloads site\premiumdownloads2\subpages\2025.html"
        print("\n=== Agregar Nueva Versión al Archivo HTML ===")
        version = input("Número de Versión (ej. 25.3.8549): ")
        date = input("Fecha (ej. Abril 2025): ")
        size = input("Tamaño (ej. 4.2 GB): ")
        torrent_link = input("Link Torrent: ")
        magnet_link = input("Link Magnet: ")
        seeds = input("Seeds iniciales: ")
        peers = input("Peers iniciales: ")

        new_version = {
            "version": version,
            "date": date,
            "size": size,
            "torrentLink": torrent_link,
            "magnetLink": magnet_link,
            "seeds": seeds,
            "peers": peers
        }

        try:
            with open(html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            start_marker = '"versions": ['
            end_marker = ']'

            start_index = html_content.find(start_marker) + len(start_marker)
            end_index = html_content.find(end_marker, start_index)

            existing_data = html_content[start_index:end_index].strip()
            if existing_data:
                versions = json.loads(f"[{existing_data}]")
            else:
                versions = []

            versions.append(new_version)

            new_data = json.dumps(versions, indent=4)[1:-1]

            updated_html_content = (
                html_content[:start_index] + "\n" + new_data + "\n" + html_content[end_index:]
            )

            with open(html_file_path, "w", encoding="utf-8") as file:
                file.write(updated_html_content)

            print("\n✅ Nueva versión agregada al archivo HTML correctamente!")
        except FileNotFoundError:
            print("\n❌ Archivo HTML no encontrado")
        except json.JSONDecodeError:
            print("\n❌ Error al procesar los datos JSON en el archivo HTML")

def main():
    manager = VersionManager()
    
    while True:
        print("\n=== Gestor de Versiones Avast 2025 ===")
        print("1. Agregar versión")
        print("2. Eliminar versión")
        print("3. Listar versiones")
        print("4. Agregar versión al archivo HTML")
        print("5. Salir")
        
        choice = input("\nSelecciona una opción: ")
        
        if choice == "1":
            manager.add_version()
        elif choice == "2":
            manager.remove_version()
        elif choice == "3":
            manager.list_versions()
        elif choice == "4":
            manager.add_version_to_html()
        elif choice == "5":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida")

if __name__ == "__main__":
    main()
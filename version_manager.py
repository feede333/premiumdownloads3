import json
import os

class VersionManager:
    def __init__(self):
        self.html_file_path = r"c:\Users\Federico\Downloads\downloads site\premiumdownloads2\subpages\2025.html"

    def list_versions(self):
        try:
            with open(self.html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            start_marker = '"versions": ['
            end_marker = ']'

            start_index = html_content.find(start_marker) + len(start_marker)
            end_index = html_content.find(end_marker, start_index)

            existing_data = html_content[start_index:end_index].strip()
            if not existing_data:
                print("\n❌ No hay versiones disponibles")
                return

            versions = json.loads(f"[{existing_data}]")
            print("\n=== Versiones Disponibles ===")
            for i, version in enumerate(versions):
                print(f"\n{i+1}. Versión {version['version']}")
                print(f"   Fecha: {version['date']}")
                print(f"   Tamaño: {version['size']}")
                print(f"   Seeds: {version['seeds']}")
                print(f"   Peers: {version['peers']}")
        except FileNotFoundError:
            print("\n❌ Archivo HTML no encontrado")
        except json.JSONDecodeError:
            print("\n❌ Error al procesar los datos JSON en el archivo HTML")

    def add_version_to_html(self):
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
            with open(self.html_file_path, "r", encoding="utf-8") as file:
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

            with open(self.html_file_path, "w", encoding="utf-8") as file:
                file.write(updated_html_content)

            print("\n✅ Nueva versión agregada al archivo HTML correctamente!")
        except FileNotFoundError:
            print("\n❌ Archivo HTML no encontrado")
        except json.JSONDecodeError:
            print("\n❌ Error al procesar los datos JSON en el archivo HTML")

    def remove_version_from_html(self):
        try:
            with open(self.html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            start_marker = '"versions": ['
            end_marker = ']'

            start_index = html_content.find(start_marker) + len(start_marker)
            end_index = html_content.find(end_marker, start_index)

            existing_data = html_content[start_index:end_index].strip()
            if not existing_data:
                print("\n❌ No hay versiones para eliminar")
                return

            versions = json.loads(f"[{existing_data}]")
            print("\n=== Eliminar Versión ===")
            print("\nVersiones disponibles:")
            for i, version in enumerate(versions):
                print(f"{i+1}. Versión {version['version']} ({version['date']})")

            try:
                choice = int(input("\nSelecciona el número de la versión a eliminar (0 para cancelar): "))
                if choice == 0:
                    print("\nOperación cancelada")
                    return

                if 1 <= choice <= len(versions):
                    removed = versions.pop(choice-1)
                    new_data = json.dumps(versions, indent=4)[1:-1]

                    updated_html_content = (
                        html_content[:start_index] + "\n" + new_data + "\n" + html_content[end_index:]
                    )

                    with open(self.html_file_path, "w", encoding="utf-8") as file:
                        file.write(updated_html_content)

                    print(f"\n✅ Versión {removed['version']} eliminada correctamente!")
                else:
                    print("\n❌ Número de versión inválido")
            except ValueError:
                print("\n❌ Por favor ingresa un número válido")
        except FileNotFoundError:
            print("\n❌ Archivo HTML no encontrado")
        except json.JSONDecodeError:
            print("\n❌ Error al procesar los datos JSON en el archivo HTML")

def main():
    manager = VersionManager()

    while True:
        print("\n=== Gestor de Versiones Avast 2025 ===")
        print("1. Agregar versión al archivo HTML")
        print("2. Eliminar versión del archivo HTML")
        print("3. Listar versiones")
        print("4. Salir")

        choice = input("\nSelecciona una opción: ")

        if choice == "1":
            manager.add_version_to_html()
        elif choice == "2":
            manager.remove_version_from_html()
        elif choice == "3":
            manager.list_versions()
        elif choice == "4":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida")

if __name__ == "__main__":
    main()
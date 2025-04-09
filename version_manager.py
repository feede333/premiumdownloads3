import json
import os

class VersionManager:
    def __init__(self):
        self.subpages_path = r"c:\Users\Federico\Downloads\downloads site\premiumdownloads2\subpages"
        self.html_file_path = None

    def create_html_file(self):
        print("\n=== Crear Nuevo Archivo HTML ===")
        year = input("Ingresa el año para el nuevo archivo (ej. 2026): ")
        file_name = f"{year}.html"
        file_path = os.path.join(self.subpages_path, file_name)

        if os.path.exists(file_path):
            print(f"\n❌ El archivo {file_name} ya existe.")
            return

        # Crear el contenido base del archivo HTML
        base_html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Avast Premium Security {year} - Versiones</title>
    <link rel="stylesheet" href="../css/csscomun.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
    <header>
        <div class="container header-content">
            <a href="../index.html" class="logo">
                <span>⬇️</span>
                <span>PremiumDownloads</span>
            </a>
            <nav>
                <ul>
                    <li><a href="../index.html">Inicio</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <div class="container">
        <a href="../detail.html" class="back-link">
            <i class="fa fa-arrow-left"></i> Volver a detalles
        </a>

        <div class="download-detail">
            <h2>Versiones de {year}</h2>
            
            <div class="version-list">
                <!-- Las versiones se cargarán dinámicamente -->
            </div>

            <div class="torrent-note">
                <p><i class="fas fa-info-circle"></i> Para usar estos enlaces necesitas:</p>
                <ul>
                    <li>• qBittorrent (Recomendado)</li>
                    <li>• uTorrent</li>
                    <li>• BitTorrent</li>
                </ul>
            </div>
        </div>
    </div>

    <footer>
        <div class="container">
            <div class="footer-links">
                <a href="#">Términos de uso</a>
                <a href="#">Política de privacidad</a>
                <a href="#">DMCA</a>
                <a href="#">Contacto</a>
            </div>
            <p>© {year} PremiumDownloads. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>
"""
        # Crear el archivo HTML
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(base_html_content)

        print(f"\n✅ Archivo {file_name} creado correctamente.")

    def select_html_file(self):
        print("\n=== Seleccionar Archivo HTML ===")
        files = [f for f in os.listdir(self.subpages_path) if f.endswith(".html")]
        if not files:
            print("\n❌ No se encontraron archivos HTML en la carpeta subpages.")
            return False

        print("\nArchivos disponibles:")
        for i, file in enumerate(files):
            print(f"{i+1}. {file}")

        try:
            choice = int(input("\nSelecciona el número del archivo (0 para cancelar): "))
            if choice == 0:
                print("\nOperación cancelada.")
                return False

            if 1 <= choice <= len(files):
                self.html_file_path = os.path.join(self.subpages_path, files[choice - 1])
                print(f"\n✅ Archivo seleccionado: {files[choice - 1]}")
                return True
            else:
                print("\n❌ Número inválido.")
                return False
        except ValueError:
            print("\n❌ Por favor ingresa un número válido.")
            return False

    def list_versions(self):
        if not self.html_file_path:
            print("\n❌ No se ha seleccionado un archivo HTML.")
            return

        try:
            with open(self.html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            start_marker = '"versions": ['
            end_marker = ']'

            start_index = html_content.find(start_marker) + len(start_marker)
            end_index = html_content.find(end_marker, start_index)

            existing_data = html_content[start_index:end_index].strip()
            if not existing_data:
                print("\n❌ No hay versiones disponibles.")
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
            print("\n❌ Archivo HTML no encontrado.")
        except json.JSONDecodeError:
            print("\n❌ Error al procesar los datos JSON en el archivo HTML.")

    def add_version_to_html(self):
        if not self.html_file_path:
            print("\n❌ No se ha seleccionado un archivo HTML.")
            return

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
            print("\n❌ Archivo HTML no encontrado.")
        except json.JSONDecodeError:
            print("\n❌ Error al procesar los datos JSON en el archivo HTML.")

    def remove_version_from_html(self):
        if not self.html_file_path:
            print("\n❌ No se ha seleccionado un archivo HTML.")
            return

        try:
            with open(self.html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            start_marker = '"versions": ['
            end_marker = ']'

            start_index = html_content.find(start_marker) + len(start_marker)
            end_index = html_content.find(end_marker, start_index)

            existing_data = html_content[start_index:end_index].strip()
            if not existing_data:
                print("\n❌ No hay versiones para eliminar.")
                return

            versions = json.loads(f"[{existing_data}]")
            print("\n=== Eliminar Versión ===")
            print("\nVersiones disponibles:")
            for i, version in enumerate(versions):
                print(f"{i+1}. Versión {version['version']} ({version['date']})")

            try:
                choice = int(input("\nSelecciona el número de la versión a eliminar (0 para cancelar): "))
                if choice == 0:
                    print("\nOperación cancelada.")
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
                    print("\n❌ Número de versión inválido.")
            except ValueError:
                print("\n❌ Por favor ingresa un número válido.")
        except FileNotFoundError:
            print("\n❌ Archivo HTML no encontrado.")
        except json.JSONDecodeError:
            print("\n❌ Error al procesar los datos JSON en el archivo HTML.")

    def ensure_common_css(self):
        if not self.html_file_path:
            print("\n❌ No se ha seleccionado un archivo HTML.")
            return

        try:
            with open(self.html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            if '<link rel="stylesheet" href="../css/csscomun.css">' not in html_content:
                print("\n🔧 Agregando enlace a csscomun.css...")
                head_end_index = html_content.find("</head>")
                if head_end_index != -1:
                    html_content = (
                        html_content[:head_end_index]
                        + '    <link rel="stylesheet" href="../css/csscomun.css">\n'
                        + html_content[head_end_index:]
                    )

                    with open(self.html_file_path, "w", encoding="utf-8") as file:
                        file.write(html_content)

                    print("✅ Enlace a csscomun.css agregado correctamente.")
                else:
                    print("\n❌ No se pudo encontrar la etiqueta </head> en el archivo HTML.")
        except FileNotFoundError:
            print("\n❌ Archivo HTML no encontrado.")

def main():
    manager = VersionManager()

    while True:
        print("\n=== Gestor de Versiones ===")
        print("1. Crear nuevo archivo HTML")
        print("2. Seleccionar archivo HTML existente")
        print("3. Agregar versión al archivo HTML")
        print("4. Eliminar versión del archivo HTML")
        print("5. Listar versiones")
        print("6. Asegurar enlace a csscomun.css")
        print("7. Salir")

        choice = input("\nSelecciona una opción: ")

        if choice == "1":
            manager.create_html_file()
        elif choice == "2":
            manager.select_html_file()
        elif choice == "3":
            manager.add_version_to_html()
        elif choice == "4":
            manager.remove_version_from_html()
        elif choice == "5":
            manager.list_versions()
        elif choice == "6":
            manager.ensure_common_css()
        elif choice == "7":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida.")

if __name__ == "__main__":
    main()
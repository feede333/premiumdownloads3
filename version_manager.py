import json
import os

class VersionManager:
    def __init__(self):
        self.subpages_path = r"c:\Users\Federico\Downloads\downloads site\premiumdownloads2\subpages"
        self.html_file_path = None
        self.current_file = None

    def create_html_file(self):
        print("\n=== Crear Nuevo Archivo HTML ===")
        year = input("Ingresa el año para el nuevo archivo (ej. 2026): ")
        file_name = f"{year}.html"
        file_path = os.path.join(self.subpages_path, file_name)

        if os.path.exists(file_path):
            print(f"\n❌ El archivo {file_name} ya existe.")
            return False

        # Crear el contenido base del archivo HTML con csscomun.css
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

    <script>
    document.addEventListener('DOMContentLoaded', () => {{
        const data = {{
            "versions": []
        }};
        const versionList = document.querySelector('.version-list');
        versionList.innerHTML = data.versions.map(version => `
            <div class="version-item">
                <div class="version-info">
                    <h3 class="version-name">${{version.version}}</h3>
                    <span class="version-date">${{version.date}}</span>
                    <span class="file-size">${{version.size}}</span>
                </div>
                <div class="download-container">
                    <div class="download-options">
                        <a href="${{version.magnetLink}}" class="magnet-button">
                            <i class="fas fa-magnet"></i>
                            <span>Magnet</span>
                        </a>
                        <a href="${{version.torrentLink}}" class="torrent-button" target="_blank">
                            <i class="fas fa-download"></i>
                            <span>Torrent</span>
                        </a>
                    </div>
                    <div class="torrent-stats">
                        <div class="peer-info">
                            <span class="seeds-indicator"></span>
                            <span>Seeds: ${{version.seeds}}</span>
                        </div>
                        <div class="peer-info">
                            <span class="peers-indicator"></span>
                            <span>Peers: ${{version.peers}}</span>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }});
    </script>
</body>
</html>"""
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(base_html_content)

        print(f"\n✅ Archivo {file_name} creado correctamente.")
        self.html_file_path = file_path
        self.current_file = file_name
        return True

    def list_html_files(self):
        print("\n=== Listar Archivos HTML Existentes ===")
        files = [f for f in os.listdir(self.subpages_path) if f.endswith(".html")]
        if not files:
            print("\n❌ No se encontraron archivos HTML en la carpeta subpages.")
            return []

        print("\nArchivos disponibles:")
        for i, file in enumerate(files):
            print(f"{i+1}. {file}")
        return files

    def list_and_select_html(self):
        files = self.list_html_files()
        if not files:
            return False

        try:
            choice = int(input("\nSelecciona el número del archivo (0 para volver): "))
            if choice == 0:
                return False

            if 1 <= choice <= len(files):
                self.html_file_path = os.path.join(self.subpages_path, files[choice - 1])
                self.current_file = files[choice - 1]
                print(f"\n✅ Archivo seleccionado: {files[choice - 1]}")
                return True
            else:
                print("\n❌ Número inválido.")
                return False
        except ValueError:
            print("\n❌ Por favor ingresa un número válido.")
            return False

    def manage_versions_menu(self):
        while True:
            print(f"\n=== Gestión de Versiones ({self.current_file}) ===")
            print("1. Agregar versión")
            print("2. Eliminar versión")
            print("3. Listar versiones")
            print("4. Volver al menú principal")

            choice = input("\nSelecciona una opción: ")

            if choice == "1":
                self.add_version_to_html()
            elif choice == "2":
                self.remove_version_from_html()
            elif choice == "3":
                self.list_versions()
            elif choice == "4":
                return
            else:
                print("\n❌ Opción inválida.")

    def add_version_to_html(self):
        if not self.html_file_path:
            print("\n❌ No se ha seleccionado un archivo HTML.")
            return

        print("\n=== Agregar Nueva Versión ===")
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

            # Encontrar el array de versiones en el contenido HTML
            versions_start = html_content.find('"versions": [') + len('"versions": [')
            versions_end = html_content.find(']', versions_start)
            
            # Obtener las versiones existentes
            versions_content = html_content[versions_start:versions_end].strip()
            versions = []
            if versions_content:
                versions = json.loads(f"[{versions_content}]")
            
            # Agregar la nueva versión
            versions.append(new_version)
            
            # Convertir las versiones actualizadas a JSON
            new_versions_json = json.dumps(versions, indent=4)[1:-1]  # Removing outer brackets
            
            # Actualizar el contenido HTML
            updated_html = (
                html_content[:versions_start] + 
                "\n" + new_versions_json + "\n" +
                html_content[versions_end:]
            )

            # Guardar los cambios
            with open(self.html_file_path, "w", encoding="utf-8") as file:
                file.write(updated_html)

            print("\n✅ Versión agregada correctamente!")
            
        except Exception as e:
            print(f"\n❌ Error al agregar la versión: {str(e)}")

    def remove_version_from_html(self):
        if not self.html_file_path:
            print("\n❌ No se ha seleccionado un archivo HTML.")
            return

        try:
            with open(self.html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            # Encontrar el array de versiones en el contenido HTML
            versions_start = html_content.find('"versions": [') + len('"versions": [')
            versions_end = html_content.find(']', versions_start)
            
            # Obtener las versiones existentes
            versions_content = html_content[versions_start:versions_end].strip()
            if not versions_content:
                print("\n❌ No hay versiones para eliminar.")
                return

            versions = json.loads(f"[{versions_content}]")
            
            print("\n=== Versiones Disponibles ===")
            for i, version in enumerate(versions):
                print(f"{i+1}. Versión {version['version']} ({version['date']})")

            try:
                choice = int(input("\nSelecciona el número de la versión a eliminar (0 para cancelar): "))
                if choice == 0:
                    print("\nOperación cancelada.")
                    return

                if 1 <= choice <= len(versions):
                    removed = versions.pop(choice - 1)
                    new_versions_json = json.dumps(versions, indent=4)[1:-1]
                    
                    updated_html = (
                        html_content[:versions_start] + 
                        "\n" + new_versions_json + "\n" +
                        html_content[versions_end:]
                    )

                    with open(self.html_file_path, "w", encoding="utf-8") as file:
                        file.write(updated_html)

                    print(f"\n✅ Versión {removed['version']} eliminada correctamente!")
                else:
                    print("\n❌ Número inválido.")
            except ValueError:
                print("\n❌ Por favor ingresa un número válido.")
                
        except Exception as e:
            print(f"\n❌ Error al eliminar la versión: {str(e)}")

    def list_versions(self):
        if not self.html_file_path:
            print("\n❌ No se ha seleccionado un archivo HTML.")
            return

        try:
            with open(self.html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            # Encontrar el array de versiones en el contenido HTML
            versions_start = html_content.find('"versions": [') + len('"versions": [')
            versions_end = html_content.find(']', versions_start)
            
            # Obtener las versiones existentes
            versions_content = html_content[versions_start:versions_end].strip()
            if not versions_content:
                print("\n❌ No hay versiones disponibles.")
                return

            versions = json.loads(f"[{versions_content}]")
            
            print("\n=== Versiones Disponibles ===")
            for i, version in enumerate(versions):
                print(f"\n{i+1}. Versión {version['version']}")
                print(f"   Fecha: {version['date']}")
                print(f"   Tamaño: {version['size']}")
                print(f"   Seeds: {version['seeds']}")
                print(f"   Peers: {version['peers']}")
                print(f"   Magnet: {version['magnetLink']}")
                print(f"   Torrent: {version['torrentLink']}")
                
        except Exception as e:
            print(f"\n❌ Error al listar las versiones: {str(e)}")

def main():
    manager = VersionManager()

    while True:
        print("\n=== Gestor de Versiones ===")
        print("1. Crear nuevo archivo HTML")
        print("2. Seleccionar archivo HTML existente")
        print("3. Volver al menú principal")

        choice = input("\nSelecciona una opción: ")

        if choice == "1":
            if manager.create_html_file():
                manager.manage_versions_menu()
        elif choice == "2":
            if manager.list_and_select_html():
                manager.manage_versions_menu()
        elif choice == "3":
            print("\nVolviendo al menú principal...")
            continue
        else:
            print("\n❌ Opción inválida.")

if __name__ == "__main__":
    main()
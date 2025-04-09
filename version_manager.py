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

    def list_html_files(self):
        print("\n=== Listar Archivos HTML Existentes ===")
        files = [f for f in os.listdir(self.subpages_path) if f.endswith(".html")]
        if not files:
            print("\n❌ No se encontraron archivos HTML en la carpeta subpages.")
            return

        print("\nArchivos disponibles:")
        for file in files:
            print(f"• {file}")

def main():
    manager = VersionManager()

    while True:
        print("\n=== Gestor de Versiones ===")
        print("1. Crear nuevo archivo HTML")
        print("2. Listar archivos HTML existentes")
        print("3. Salir")

        choice = input("\nSelecciona una opción: ")

        if choice == "1":
            manager.create_html_file()
        elif choice == "2":
            manager.list_html_files()
        elif choice == "3":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida.")

if __name__ == "__main__":
    main()
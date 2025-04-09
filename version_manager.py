import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

class VersionManager:
    def __init__(self):
        self.subpages_path = r"c:\Users\Federico\Downloads\downloads site\premiumdownloads2\subpages"
        self.html_file_path = None
        self.current_file = None

    def create_html_file(self, year):
        file_name = f"{year}.html"
        file_path = os.path.join(self.subpages_path, file_name)

        if os.path.exists(file_path):
            return False

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

        self.html_file_path = file_path
        self.current_file = file_name
        return True

    def list_html_files(self):
        files = [f for f in os.listdir(self.subpages_path) if f.endswith(".html")]
        return files

class VersionManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Versiones")
        self.root.geometry("800x600")
        
        self.manager = VersionManager()
        
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        header = ttk.Label(self.root, text="Gestor de Versiones", style='Header.TLabel')
        header.pack(pady=20)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ttk.Button(main_frame, text="Crear nuevo archivo HTML", 
                  command=self.show_create_html_dialog).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Seleccionar archivo HTML existente", 
                  command=self.show_select_html_dialog).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Salir", 
                  command=self.root.quit).pack(fill='x', pady=5)

    def show_create_html_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Nuevo Archivo HTML")
        dialog.geometry("400x200")
        dialog.grab_set()

        ttk.Label(dialog, text="Ingresa el año para el nuevo archivo:").pack(pady=20)
        year_entry = ttk.Entry(dialog)
        year_entry.pack(pady=5)

        def create_file():
            year = year_entry.get()
            file_name = f"{year}.html"
            file_path = os.path.join(self.manager.subpages_path, file_name)

            if os.path.exists(file_path):
                messagebox.showerror("Error", f"El archivo {file_name} ya existe.")
                return

            if self.manager.create_html_file(year):
                messagebox.showinfo("Éxito", f"Archivo {file_name} creado correctamente.")
                dialog.destroy()
                self.show_version_management(file_name)

        ttk.Button(dialog, text="Crear", command=create_file).pack(pady=20)

    def show_select_html_dialog(self):
        files = self.manager.list_html_files()
        if not files:
            messagebox.showwarning("Aviso", "No se encontraron archivos HTML.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Seleccionar Archivo HTML")
        dialog.geometry("400x300")
        dialog.grab_set()

        ttk.Label(dialog, text="Selecciona un archivo:").pack(pady=20)
        
        listbox = tk.Listbox(dialog)
        listbox.pack(fill='both', expand=True, padx=20)
        
        for file in files:
            listbox.insert('end', file)

        def select_file():
            if not listbox.curselection():
                messagebox.showwarning("Aviso", "Por favor selecciona un archivo.")
                return
                
            selected = listbox.get(listbox.curselection())
            dialog.destroy()
            self.show_version_management(selected)

        ttk.Button(dialog, text="Seleccionar", command=select_file).pack(pady=20)

    def show_version_management(self, filename):
        for widget in self.root.winfo_children():
            widget.destroy()

        header = ttk.Label(self.root, text=f"Gestión de Versiones - {filename}", 
                          style='Header.TLabel')
        header.pack(pady=20)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ttk.Button(main_frame, text="Agregar versión", 
                  command=lambda: self.show_add_version_dialog(filename)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Eliminar versión", 
                  command=lambda: self.show_remove_version_dialog(filename)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Listar versiones", 
                  command=lambda: self.show_list_versions(filename)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Volver al menú principal", 
                  command=self.create_main_menu).pack(fill='x', pady=5)

    def show_add_version_dialog(self, filename):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Nueva Versión")
        dialog.geometry("500x400")
        dialog.grab_set()

        frame = ttk.Frame(dialog)
        frame.pack(padx=20, pady=20, fill='both', expand=True)

        fields = [
            ("Número de Versión:", "version"),
            ("Fecha:", "date"),
            ("Tamaño:", "size"),
            ("Link Torrent:", "torrent_link"),
            ("Link Magnet:", "magnet_link"),
            ("Seeds iniciales:", "seeds"),
            ("Peers iniciales:", "peers")
        ]

        entries = {}
        for label_text, key in fields:
            ttk.Label(frame, text=label_text).pack(anchor='w')
            entry = ttk.Entry(frame, width=50)
            entry.pack(fill='x', pady=(0, 10))
            entries[key] = entry

        def add_version():
            data = {key: entry.get() for key, entry in entries.items()}
            dialog.destroy()
            messagebox.showinfo("Éxito", "Versión agregada correctamente")

        ttk.Button(dialog, text="Agregar", command=add_version).pack(pady=20)

    def show_remove_version_dialog(self, filename):
        pass

    def show_list_versions(self, filename):
        dialog = tk.Toplevel(self.root)
        dialog.title("Lista de Versiones")
        dialog.geometry("600x400")

        tree = ttk.Treeview(dialog, columns=("Versión", "Fecha", "Tamaño", "Seeds", "Peers"))
        tree.heading("#1", text="Versión")
        tree.heading("#2", text="Fecha")
        tree.heading("#3", text="Tamaño")
        tree.heading("#4", text="Seeds")
        tree.heading("#5", text="Peers")
        tree.pack(fill='both', expand=True, padx=20, pady=20)

def main():
    root = tk.Tk()
    app = VersionManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()